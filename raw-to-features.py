import json, os, sys, nltk

from extract_features import extract_features

print("hello; reading raw data...")

raw = json.load(open('./data/raw.json'))

print("done; extracting features...")

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

feature_set = []
for index, entry in enumerate(raw):
    if index < 1000:
        sys.stdout.write("processing entry {0}... \r".format(str(index + 1)))
        sys.stdout.flush()
        feature_set.append((extract_features(entry), entry["location"]))

targetPath = "./data"
targetFile = "feature-set.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(feature_set, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to train model")
