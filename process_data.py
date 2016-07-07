from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('new') if isfile(join('new', f))]
onlyfiles.sort()
