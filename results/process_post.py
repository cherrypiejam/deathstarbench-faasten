#!/usr/bin/python3
import re
import statistics

from datetime import datetime

d = {}
times = []
with open("post_raw.txt") as f:
    for line in f:
        if not line:
            continue
        line = line.strip()
        try:
            t = datetime.strptime(line, '%Y-%m-%d %H:%M:%S.%f')
            times.append(t)
            #  print(line)
        except:
            l = line.split(' "')
            if 'func":' in l:
                index = l.index('func":')
                func = ''.join(list(l[index+1])[:-2])
                #  print(func)
                begin = ''.join(list(l[index+3])[:-2])
                begin = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S.%f')
                end = ''.join(list(l[index+5])[:-2])
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
                if func not in d:
                    d[func] = []
                d[func].append((begin, end))

diffs = []
for i in range(0, 10):
    s = times[i*2]
    begins = [v[i][0] for v in d.values()]
    ends = [v[i][1] for v in d.values()]
    n = min(begins)
    m = max(ends)
    diff = (m-n).total_seconds()*1000
    diffs.append(diff)
    print(diff)
print("average:")
print(sum(diffs)/len(diffs))


