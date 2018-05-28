import json, os, sys
import nltk

from helpers import predict, prepare_training_set

featuresets = json.load(open('./data/feature-set.json'))
raw = json.load(open('./data/raw.json'))

print("overall featureset size: {0}".format(len(featuresets)))

train_to_test_ratio = 0.8

divide_index = int(len(featuresets) * train_to_test_ratio)

train_set, test_set = featuresets[:divide_index], featuresets[divide_index:]

predict_index = len(raw) - 1
if len(sys.argv) > 1:
    predict_index = int(sys.argv[1])

def process_classifier(clf, name):
    print("training {0} with {1} items...".format(name, len(train_set)))
    classifier = clf.train(train_set)

    print("done; measuring classifier accuracy...")
    print("accuracy is {0}".format(str(nltk.classify.accuracy(classifier, test_set))))

    print("determining first 5 most valuable features...")
    print(classifier.show_most_informative_features(5))

    print("done; classifying entry #{0} from raw dataset:".format(predict_index))
    target_item = raw[predict_index]
    predict(classifier, target_item)

process_classifier(nltk.NaiveBayesClassifier, "Naive Bayes classifier")
process_classifier(nltk.DecisionTreeClassifier, "Decision tree classifier")