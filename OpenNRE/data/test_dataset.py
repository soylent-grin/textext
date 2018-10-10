## script for testing the dataset

import json
from pprint import pprint

j = json.load(open('train.json'))
#j = json.load(open('test.json'))
print(len(j))


for i, o in enumerate(j): 
    #if i>=570 and i<=575:
    if o['relation'] not in ['locatedIn', 'Unrelated']:
        print(o)
