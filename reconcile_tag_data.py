from os import listdir
import shutil
from os.path import isfile, join
from collections import Counter
import json
import csv


#read total jobs count
jobs_count = {}
with open(join('result', "jobs_count.csv")) as counts_f:
    jobs_reader = csv.reader(counts_f, delimiter=',')
    for row in jobs_reader:
        count = row[1]
        date = row[0][4:14]
        jobs_count[date] = int(count)

#read tags counts
onlyfiles = [f for f in listdir(join('result','tags')) if isfile(join('result','tags', f))]
onlyfiles.sort()
reconciled_tags = {}  # <tag, [date,count]>
processed_data = []

for fname in onlyfiles:
    with open(join('result','tags',fname)) as f:
        data = json.load(f)
        current_date = fname[9:19]
        #TODO make num_jobs read from another file
        current_tags = {"date": current_date, "num_jobs": jobs_count[current_date], "tags": []}
        rank = 1
        for k,v in data:
            #we don't want insignificant terms , typos , etc..
            if v > 1:
                current_tags["tags"].append({
                    "tag": k,
                    "perc": "{0:.2f}".format((v*1.0/current_tags["num_jobs"])*100),
                    "rank": rank
                })
                rank +=1

        processed_data.append(current_tags)

with open(join('result', 'data.json'), 'w+') as f:
    json.dump(processed_data, f)
