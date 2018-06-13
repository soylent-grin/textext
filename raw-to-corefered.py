import json, os, sys, nltk

from helpers import replace_coreferences

print("hello; reading raw data...")

raw = json.load(open('./data/raw.json'))

print("done; replacing coreferences...")

count = 1000
if len(sys.argv) > 1:
    count = int(sys.argv[1])
replaced = replace_coreferences(raw[:count])

targetPath = "./data"
targetFile = "raw-with-replaced-coreferences.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(replaced, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to annotate")
