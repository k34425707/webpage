# 儲存作品對應相似度矩陣中的哪一列

import json
import csv
from collections import defaultdict
with open("ratings.json", "r") as fp:
    D = json.load(fp)

    W2 = set()
    for ratings in D.values():
        for work in ratings.keys():
            W2.add(work)
    W3 = sorted(list(W2))

    cnt = 1
    I2R = dict()
    for work in W3:
        I2R[work] = cnt
        cnt += 1
    
    with open("Id2Row.json", "w") as fp1:
        json.dump(I2R, fp1)