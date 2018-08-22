import json, os, sys
import nltk
import argparse

from helpers import predict, prepare_training_set, convert_to_binary

parser=argparse.ArgumentParser()

featuresets = json.load(open('./data/feature-set.json'))
raw = json.load(open('./data/raw.json'))

predict_index = len(raw) - 1

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser.add_argument('--predict-index', help='Index of predicting item', type=int, default=predict_index)
parser.add_argument('--is-binary', help='Whether or not to use binary location classification', type=str2bool, default=False)
parser.add_argument('--ne-detection-type', help='Named Entity recognition framework; options: nltk, spacy', type=str, default="nltk")

args=parser.parse_args()

print(args)

print("using: predict index = {0}, binary = {1}, NE detection type = {2}".format(args.predict_index, args.is_binary, args.ne_detection_type))

print("overall featureset size: {0}".format(len(featuresets)))

if args.is_binary:
    print("converting featuresets to binary")
    featuresets = convert_to_binary(featuresets)

train_to_test_ratio = 0.8

divide_index = int(len(featuresets) * train_to_test_ratio)

train_set, test_set = featuresets[:divide_index], featuresets[divide_index:]

def process_classifier(clf, name):
    print("training {0} with {1} items...".format(name, len(train_set)))
    classifier = clf.train(train_set)

    print("done; measuring classifier accuracy...")
    print("accuracy is {0}".format(str(nltk.classify.accuracy(classifier, test_set))))

    print("determining first 5 most valuable features...")
    print(classifier.show_most_informative_features(5))

    print("done; classifying entry #{0} from raw dataset:".format(args.predict_index))
    target_item = raw[args.predict_index]
    predict(classifier, target_item, args.is_binary, args.ne_detection_type)

process_classifier(nltk.NaiveBayesClassifier, "Naive Bayes classifier")
# process_classifier(nltk.DecisionTreeClassifier, "Decision tree classifier")