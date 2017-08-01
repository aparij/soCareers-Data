from os import listdir
import shutil
from os.path import isfile, join
from collections import Counter
import json
import csv
import arrow

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

#find the data from a year ago
utc_now = arrow.utcnow()
year_ago = utc_now.shift(years=-1)
print(year_ago)
year_ago_filename = None
for fname in onlyfiles:
    if arrow.get(fname[9:19])>year_ago :
        year_ago_filename = fname
        print(fname)
        break
year_ago_data = None
current_tags = None
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
        #keep a year ago data for calculating top movers and loosers
        if fname == year_ago_filename:
            year_ago_data = current_tags
with open(join('result', 'data.json'), 'w+') as f:
    json.dump(processed_data, f)

#calculate top movers and losers
changes = []
for tag in current_tags["tags"]:
    change = None
    rank = None
    for old_tag in year_ago_data["tags"]:
        if old_tag["tag"] == tag['tag'] and old_tag["perc"]!="0.0":
            change = ((float(tag["perc"]) - float(old_tag["perc"]))/float(old_tag["perc"]))*100.0
            rank = tag["rank"]
            break
    #if not found in last year data
    #TODO better for 100% calculation
    if change == None:
        change = 100
        rank = tag["rank"]
    changes.append({"tag": tag["tag"], "rank": int(rank), "change": int(change)})

topChanges = {}
sortedlist = sorted(changes, key=lambda k: k['rank'])
#take from the top 25 tech
sortedTop25 = sorted(sortedlist[0:24], key=lambda k: k['change'])
winners = sortedTop25[-5:]
winners.reverse()
topChanges["top25"]={'winners': winners, 'losers':sortedTop25[0:5]}

#take from the top 50 tech
sortedTop50 = sorted(sortedlist[0:49], key=lambda k: k['change'])
winners = sortedTop50[-5:]
winners.reverse()
topChanges["top50"]={'winners': winners, 'losers':sortedTop50[0:5]}



#take from the  ALL tech
sortedTopALL = sorted(sortedlist, key=lambda k: k['change'])
winners = sortedTopALL[-5:]
winners.reverse()
topChanges["topALL"]={'winners': winners, 'losers':sortedTopALL[0:5]}


with open(join('result', 'top_changes.json'), 'w+') as f:
    json.dump(topChanges, f)
