# 把分析出來的用戶ID一個一個爬收藏列表，只保留「有打分」的資料，捨棄「看完沒打分」的作品、捨棄「沒有打任何分數」的用戶

# 後日談:
# 日後在做其他專題時發現，GRequests效果非常糟，當時爬5132個用戶的收藏列表(31448個網頁)花了十個小時。
# 我當時看網路上的資料以為傳統的Requests會鎖CPU，但其實只要處理好資料共用問題，搭配threading的話相當快，別用GR了
# 理想做法是用threading去request網頁資料，回傳的資料一起序向處理(反正也不大耗CPU)，效率和安全兼顧
from bs4 import BeautifulSoup
import grequests
import requests
import json
import time
from collections import defaultdict
import os
import csv

#format of the request URL, put the userID between this two
head = "https://mirror.bgm.rin.cat/anime/list/"
tail = "/collect"

#my browser's header
myHeader = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

PLSIZE = os.cpu_count()     #pool size
users = []                  #users' id list
ratings = defaultdict(dict) #a user's rating
pool = {}                   #request pool
start_time = time.time()    #record the start time
crawl_count = 0             #count how many user is processed
counter = 0

#open the user list
with open("IDs.json", "r") as fp:
    users = list(json.load(fp).keys())

size = len(users) #record the goal to estimate ETA

#initialize
for _ in range(PLSIZE):
    if (len(users) > 0):
        pool[users.pop()] = 1 #id -> page

def exc(req, exc):
    print(exc)
    time.sleep(60)


#main loop
while len(pool) > 0:
    #Grequest pool
    GRpool = (grequests.get(str(head + usr + tail), params = {"orderby" : "rate", "page" : pool[usr]}, headers = myHeader, timeout = 10) for usr in list(pool.keys()))
    responses = grequests.imap(GRpool, grequests.Pool(PLSIZE), exception_handler=exc)

    counter += 1
    print("round {}({}): {}".format(counter, counter * 8, pool))
    for res in responses:
        #if the fetch failed
        

        #request a page and transform to a soup obj
        data =  BeautifulSoup(res.text, "html.parser")
        
        #detect rare case: the user changed their username recently
        usr = data.find("a", class_ = "avatar").get("href")[6:]
        if pool.get(usr) == None:
            UsrData = requests.get("https://mirror.api.bgm.rin.cat/user/" + usr, headers = myHeader).json()
            pool[usr] = pool.pop(str(UsrData["id"]))
            R = requests.get(head + usr + tail, params = {"orderby" : "rate", "page" : pool[usr]}, headers = myHeader)
            data = BeautifulSoup(R.text, "html.parser")
        
        #iter every animation works, record the subject id and rate
        works = data.find("ul", class_ = "browserFull").find_all("div", class_ = "inner")
        for work in works:
            #check if the user has vote
            rate = work.find("span", class_ = "starstop-s")
            if (rate != None):
                ratings[usr][work.find("a").get("href")[9:]] = int(rate.find("span").get("class")[1][5:])
            else:
                #end searching if the last vote is founded
                pool[usr] = -1
                break
        
        pgButton = data.find("strong", class_ = "p_cur")
        if pgButton == None:
            #only 1 page
            pool[usr] = -1
        elif data.find("strong", class_ = "p_cur").find_next_siblings("a") == None:
            #this is last page
            pool[usr] = -1
        elif pool[usr] != -1:
            #request next page
            pool[usr] += 1

    #clean the complete user and get a new one
    clear = []
    for usr, page in pool.items():
        if page == -1:
            clear.append(usr)
    for i in clear:
        pool.pop(i)
        crawl_count += 1
        if ratings.get(i) != None:
            with open("save.txt", "a") as fp:
                fp.write("\"" + i + "\": " + json.dumps(ratings.pop(i)) + ", ")
        if (len(users) > 0):
            pool[users.pop()] = 1
            
        #print progress
        passed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        ETA = time.strftime("%H:%M:%S", time.gmtime((time.time() - start_time) / crawl_count * (size - crawl_count)))
        print("{}: {}/ {} ({:02.3f}%), {} passed, ETA: {}".format(time.strftime("%H:%M:%S", time.localtime()), crawl_count, size, crawl_count / size * 100, passed, ETA))

        #save for safe
        
        if crawl_count % 2 == 0:
            with open("ratings.json", "r+") as fp:
                tmp = json.load(fp)
                print(tmp)
                json.dump(tmp.update(ratings), fp)
with open("ratings.json", "w") as fp:
    json.dump(ratings, fp)

print("Complete at ", time.strftime("%H:%M:%S", time.localtime()))