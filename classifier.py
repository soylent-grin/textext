import json, os
import nltk

from extract_features import extract_features

raw = json.load(open('./data/raw.json'))

def get_featureset():
    featureset = []

    for entry in raw:
        featureset.append((extract_features(entry), entry["location"]))

    return featureset

featureset = get_featureset()

train_set, test_set = featureset[500:], featureset[:500]

print("training classifier with {0} items".format(len(train_set)))
classifier = nltk.NaiveBayesClassifier.train(train_set)

print("done; classifying first entry from raw dataset:")
print(raw[502])

print(classifier.classify(extract_features(raw[502])))