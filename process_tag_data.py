from os import listdir
import shutil
from os.path import isfile, join
from collections import Counter
import json
onlyfiles = [f for f in listdir('new') if isfile(join('new', f))]
onlyfiles.sort()
for fname in onlyfiles:
    with open(join('new',fname)) as f:
        data = json.load(f)
        c = Counter()
        total_rows = 0
        for row in data:
            total_rows += 1
            for tag in row['tags']:
                c[tag] += 1
    print(fname,c.most_common(10))
    with open(join('result','tags','tags-%s'%fname),'w+') as f:
        json.dump(dict(c), f)
    with open(join('result', 'jobs_count.csv'),'a+') as f:
        f.write(','.join([fname,str(total_rows),'\n']))

    shutil.move(join('new',fname), join('processed',fname))



