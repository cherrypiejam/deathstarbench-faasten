import sys
from datetime import datetime

with open(sys.argv[1], 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    times = []
    for l in lines:
        if not l:
            continue
        try:
            t = datetime.strptime(l, '%Y-%m-%d %H:%M:%S.%f')
            times.append(t)
            #  print(l)
        except:
            continue
    #  print(len(times))
    diffs = []
    for i in range(0, len(times), 2):
        diff = times[i+1] - times[i]
        diff = diff.total_seconds() * 1000
        diffs.append(diff)
        print(diff)
    print("average:")
    print(sum(diffs)/len(diffs))
