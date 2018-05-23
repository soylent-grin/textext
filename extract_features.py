import nltk
from nltk import Tree

import sys
reload(sys)
sys.setdefaultencoding('utf8')

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

def extract_location_related_verbs(sent):
    verbs = []
    for (word, label) in sent:
        if "located" in word or "headquatered" in word or "founded" in word or "based" in word:
            verbs.append(word)
    return verbs;

def extract_verbs(sent):
    verbs = []
    for (word, label) in sent:
        if label.startswith("VB"):
            verbs.append(word)
    return verbs;

def extract_nowns(sent):
    nowns = []
    for (word, label) in sent:
        if label == 'NN':
            nowns.append(word)
    return nowns;

def extract_named_entities(sent):
    entity_names = []

    if hasattr(sent, 'label') and sent.label:
        if sent.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in sent]))
        else:
            for child in sent:
                entity_names.extend(extract_named_entities(child))

    return entity_names

def traverse_tree(tree):
    print("tree:", tree)
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            traverse_tree(subtree)

def annotate(raw_entry):
    sentences = nltk.sent_tokenize(raw_entry["abstract"])
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    annotated_text = []
    for tree in chunked_sentences:
        annotated_text.append(tree)

    raw_entry["abstract_annotated"] = annotated_text
    raw_entry["tagged_sentences"] = tagged_sentences

    return raw_entry

def extract_features(raw_entry):

    annotated_entry = annotate(raw_entry)

    features = {}

    for sent in annotated_entry["abstract_annotated"]:
        for ne in extract_named_entities(sent):
            features["NE({0})".format(ne)] = True

    words_count = 0
    for sent in annotated_entry["tagged_sentences"]:
        words_count += len(sent)
        for vb in extract_verbs(sent):
            features["VB({0})".format(vb)] = True
        for nown in extract_nowns(sent):
            features["NN({0})".format(nown)] = True
        for vb in extract_location_related_verbs(sent):
            features["LOCATION_VERB({0})".format(vb)] = True

    features["words_count"] = words_count

    return features