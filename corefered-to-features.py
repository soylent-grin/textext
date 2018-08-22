import json, os, sys, nltk, argparse

from helpers import prepare_training_set

parser=argparse.ArgumentParser()

featuresets = json.load(open('./data/feature-set.json'))
raw = json.load(open('./data/raw.json'))

parser.add_argument('--count', help='Size of training set', type=int, default=1000)
parser.add_argument('--ne-detection-type', help='Named Entity recognition framework; options: nltk, spacy', type=str, default="nltk")

args=parser.parse_args()

print("hello; reading raw data...")

raw = json.load(open('./data/raw-with-replaced-coreferences.json'))

print("done; extracting features...")

print("using: count = {0}, NE detection type = {1}".format(args.count, args.ne_detection_type))

feature_set = prepare_training_set(raw[:args.count], args.ne_detection_type)

targetPath = "./data"
targetFile = "feature-set.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(feature_set, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to train model")
