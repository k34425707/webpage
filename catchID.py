# 使用網友統計的番組計畫活躍帖子標題統計，從中提煉出活躍用戶的ID

import csv
import collections
import json

IDs = collections.Counter()

with open("topic_id.csv", "r", encoding="utf-8") as fp:
    raws = csv.reader(fp)
    for row in raws:
        IDs[row[2]] += 1

with open("IDs.json", "w", encoding="utf-8") as fp:
    json.dump(IDs, fp)