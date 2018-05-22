import json, os

def extract_features(entry):
    features = {}

    features["distance"] = len(entry["company"])
    features["company"] = entry["company"]

    return features

print("hello; extracting features from annotated text...")

annotated = json.load(open('./data/annotated.json'))

featuresets = []

for entry in annotated:
    featuresets.append((extract_features(entry), entry["location"]))

targetPath = "./data"
targetFile = "features.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(featuresets, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; extracted featureset of {0} items; ready to learn".format(len(featuresets)))