## script for testing the dataset

import json, sys
from pprint import pprint

if len(sys.argv) > 1:
    j = json.load(open(sys.argv[1]))
    print('\nSize of dataset: ', sys.argv[1], ':', len(j), '\n')

else:
    datasets = [('train1.json', 'test1.json'),('train2.json', 'test2.json'),('train3.json', 'test3.json'),('train4.json', 'test4.json')]

    for no, (a,b) in enumerate(datasets):
        i, j = json.load(open(a)), json.load(open(b)) 

        print('\nSize of dataset: train', datasets[no][0], '.json:', len(i), '--- test', datasets[no][1], '.json:', len(j))


