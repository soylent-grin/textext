import json, os
import nltk

from helpers import predict, prepare_training_set

raw = json.load(open('./data/raw.json'))

featuresets = prepare_training_set(raw[:100])

train_to_test_ratio = 0.6

divide_index = int(len(featuresets) * train_to_test_ratio)

train_set, test_set = featuresets[:divide_index], featuresets[divide_index:]

print("training classifier with {0} items...".format(len(train_set)))
classifier = nltk.NaiveBayesClassifier.train(train_set)

print("done; classifying last entry from raw dataset:")
print(len(raw))
target_item = raw[len(raw) - 2]
predict(classifier, target_item)