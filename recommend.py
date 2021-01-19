# 根據相似度矩陣計算推薦作品的順序
# 用字典轉換的方式把list.txt特定行的資料轉回來計算
# 後來發現list太大了，所以在php實作時有小改做法

import math
import json
import time
import linecache

def Recommend(userData, data, W, K):
    rank = dict()
    siz = 12255
    for work, rate in userData.items():
        for j, wj in sorted(W[work].items(), key=lambda x:x[1], reverse=True)[0:K]:
            if j in userData.keys():
                continue
            rank.setdefault(j, 0)
            rank[j] += rate * wj
    
    return sorted(rank.items(), key=lambda x:x[1], reverse=True)

    
start = time.time()
with open("ratings.json", "r") as fp1:
    #raw data
    data = json.load(fp1)

    with open("Id2Row.json", "r") as fp2:
        I2R = json.load(fp2)
        with open("requests.txt", "r") as fp3:
            userData = dict()
            D = fp3.readlines()
            for i in D:
                tmp = i.rstrip().split(' ')
                if I2R.get(tmp[0]):
                    userData[tmp[0]] = float(tmp[1])
            print(userData.keys())

            W = dict()
            for work in userData.keys():
                W.update(json.loads(linecache.getline("list.txt", I2R[work])))

            print (time.time() - start, "sec")
            result = Recommend(userData, data, W, 15)[:25]
            
            for i in result:
                print(i)