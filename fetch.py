# 切割檔案時忘了把分割點記錄下來，所以重新處理一次

import os, json
D = list()
files = os.listdir("dataBase")
for fn in files:
    D.append(int(fn.split(".")[0]))
print(sorted(D))
with open("hash.json", "w") as fp:
    json.dump(sorted(D), fp)