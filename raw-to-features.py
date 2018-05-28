import json, os, sys, nltk

from helpers import prepare_training_set

print("hello; reading raw data...")

raw = json.load(open('./data/raw.json'))

print("done; extracting features...")

count = 1000
if len(sys.argv) > 1:
    count = int(sys.argv[1])

feature_set = prepare_training_set(raw[:count])

targetPath = "./data"
targetFile = "feature-set.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(feature_set, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to train model")
