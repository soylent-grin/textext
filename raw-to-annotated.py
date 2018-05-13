import json
import nltk
from nltk import Tree

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

import os

print("hello; reading raw data...")

raw = json.load(open('./data/raw.json'))

print("done; annotating abstracts...")

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

for entry in raw:
    sentences = nltk.sent_tokenize(entry["abstract"])
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
 
    annotated_text = []
    for tree in chunked_sentences:
        annotated_text.append(tree2dict(tree))
    entry["abstract"] = annotated_text

targetPath = "./data"
targetFile = "annotated.json"
print("done; writing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

json.dump(raw, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to extract features")
