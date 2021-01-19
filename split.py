# 後來發現重達1.8GB的list.txt讀取速度太糟，而且Infiniry free可以放的檔案大小有上限10MB
# 所以我就以10MB為一單位把list.txt切開了

import json
from linecache import getline

buf = list()
siz = 0
for cnt in range(1, 12256):
    tmp = getline("list.txt", cnt)
    if siz + len(tmp) > 10 * 2**20:
        with open("dataBase/{}.txt".format(cnt-1), "w") as fp:
            fp.writelines(buf)
        buf.clear()
        siz = 0
    buf += tmp
    siz += len(tmp)

if len(buf):
    with open("dataBase/12255.txt", "w") as fp:
        fp.writelines(buf)