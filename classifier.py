import json, os
import nltk

from extract_features import extract_features

featureset = json.load(open('./data/feature-set.json'))
raw = json.load(open('./data/raw.json'))

train_to_test_ratio = 0.6

divide_index = int(len(featureset) * train_to_test_ratio)

train_set, test_set = featureset[:divide_index], featureset[divide_index:]

print("training classifier with {0} items...".format(len(train_set)))
classifier = nltk.NaiveBayesClassifier.train(train_set)

target_index = 1001
print("done; classifying entry {0} from raw dataset:".format(target_index))
print(raw[target_index])


print("predicted location is: " + classifier.classify(extract_features(raw[target_index])))

print("calculating model accuracy:")
print(nltk.classify.accuracy(classifier, test_set))