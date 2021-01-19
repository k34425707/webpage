# 計算作品之間的相似度
# 算好的相似度矩陣，以列為單位儲存成一個JSON字串

import math
import json
import time

def ItemSim(data):
    # item - item rated count
    C = dict()
    # item - user rated count
    N = dict()
    cnt = 0
    siz = len(data)
    for usr, ratings in data.items():
        print("state 1: {}/{}".format(cnt,siz))
        cnt += 1
        for i in ratings.keys():
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in ratings.keys():
                if i == j:
                    continue
                C[i].setdefault(j, 0)
                C[i][j] += 1

    # find itemCF
    W = dict()
    cnt = 0
    siz = len(C)
    for i, related_items in C.items():
        W.setdefault(i, {})
        print("state 2: {}/{}".format(cnt,siz))
        cnt += 1
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return [(k, W[str(k)]) for k in sorted([int(i) for i in W.keys()])]

with open("ratings.json", "r") as fp:
    #raw data
    data = json.load(fp)

    start = time.time()

    W = ItemSim(data)

    print(time.time() - start)

    with open("list.txt", "w") as fp:
        for work, asso in W:
            fp.write("{{\"{}\": {}}}\n".format(work, json.dumps(asso)))
    print(time.time() - start)