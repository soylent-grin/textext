import json, os, sys, nltk

from helpers import prepare_training_set, prepare_correct_wrong_set

print("hello; reading raw data...")

raw = json.load(open('./data/raw.json'))
featuresets = json.load(open('./data/feature-set.json'))

count = 1000
if len(sys.argv) > 1:
    count = int(sys.argv[1])

(correct, wrong) = prepare_correct_wrong_set(raw[:count], featuresets)

targetPath = "./data"

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(correct, open("{0}/correct.json".format(targetPath), "w+"))
json.dump(wrong, open("{0}/wrong.json".format(targetPath), "w+"))