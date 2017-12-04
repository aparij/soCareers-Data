from os import listdir
import shutil
from os.path import isfile, join
from collections import Counter
import json

synonyms = {
    'html5': 'html',
    'golang': 'go',
    'node': 'node.js',
    'nodejs': 'node.js',
    'react': 'reactjs',
    'react.js': 'reactjs',
    'angular': 'angularjs',
    'angular.js': 'angularjs',
    'angular2': 'angularjs',
    'angular4': 'angularjs',
    'angular-2': 'angularjs',
    'angular-js': 'angularjs',
    'python-2.7': 'python',
    'python-3.x': 'python',
    'ruby-on-rails-4': 'ruby-on-rails',
    'ruby-on-rails-3': 'ruby-on-rails',
    'rails': 'ruby-on-rails',
    'php5': 'php',
    'php5+': 'php',
    'php5.6': 'php',
    'php-5.6': 'php',
    'asp.net-mvc-3': 'asp.net-mvc-3',
    'asp.net-mvc-4': 'asp.net-mvc-4',
    'asp.net-mvc-5': 'asp.net-mvc-5',
    '.net-4.0': '.net',
    '.net-4.5': '.net',
    '.net-3.5': '.net',
    'java-8': 'java',
    'java-7': 'java',
    'java8': 'java',
    'c++11': 'c++',
    'c++14': 'c++',
    'css3': 'css',
    'twitter-bootstrap-3': 'bootstrap',
    'twitter-bootstrap': 'bootstrap',
    'amazon-web-services': 'aws',
    'vue': 'vue.js',
    'vue2': 'vue.js',
    'vuejs': 'vue.js',
    'postgres': 'postgresql'
}
onlyfiles = [f for f in listdir('new') if isfile(join('new', f)) and f.endswith("json")]
onlyfiles.sort()
for fname in onlyfiles:
    with open(join('new',fname)) as f:
        data = json.load(f)
        c = Counter()
        total_rows = 0
        for row in data:
            total_rows += 1
            found_synonym = ''
            all_tags = set(row['tags'])
            for tag in row['tags']:
                if tag in synonyms and not synonyms[tag] in all_tags:
                    tag = synonyms[tag]
                elif tag in synonyms:
                    #don't double count synonyms
                    continue
                c[tag] += 1
    print(fname,c.most_common(10))
    with open(join('result','tags','tags-%s'%fname),'w+') as f:
        json.dump(c.most_common(), f)
    with open(join('result', 'jobs_count.csv'),'a+') as f:
        f.write(','.join([fname,str(total_rows),'\n']))

    shutil.move(join('new',fname), join('processed',fname))



