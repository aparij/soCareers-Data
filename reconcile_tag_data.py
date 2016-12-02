from os import listdir
import shutil
from os.path import isfile, join
from collections import Counter
import json


onlyfiles = [f for f in listdir(join('result','tags')) if isfile(join('result','tags', f))]
onlyfiles.sort()
reconciled_tags = {}  # <tag, [date,count]>
for fname in onlyfiles:
    with open(join('result','tags',fname)) as f:
        data = json.load(f)
        current_date = fname[9:19]
        print(data)