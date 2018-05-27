import json, os
import nltk

from helpers import prepare_predict_item

raw = json.load(open('./data/raw.json'))

print((prepare_predict_item(raw[0])))