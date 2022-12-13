import json

files = [
    'concurrent_invoke_alice.txt',
    'concurrent_invoke_bob.txt',
    'concurrent_invoke_carol.txt',
    'concurrent_invoke_dave.txt',
    'concurrent_invoke_eve.txt',
]

i = 0
for file in files:
    with open(file) as f:
        lines = f.readlines()
        line = lines[-1]
        l = json.loads(line)['latencies']
        d = {}
        arr = []
        for ll in l:
            a = ll[0]
            b = ll[1]['nanos'] + ll[1]['secs']*1000000000
            if a not in d.keys():
                d[a] = []
            d[a].append(b)
            arr.append(b)
    print(file.split('.')[0].split('_')[-1], end=', ')
    print(', '.join([str(x) for x in arr]), end='\n')


