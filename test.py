import json, os
import nltk

from extract_features import extract_features

raw = json.load(open('./data/raw.json'))

print((extract_features(raw[0])))