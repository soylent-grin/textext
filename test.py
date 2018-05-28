import json, os, sys
import nltk

from helpers import prepare_training_set

raw = json.load(open('./data/raw.json'))

index = int(sys.argv[1])

print(raw[index])
print((prepare_training_set(raw[index:index + 1])))