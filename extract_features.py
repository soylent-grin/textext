import nltk
from nltk import Tree

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

def annotate(raw_entry):
    sentences = nltk.sent_tokenize(raw_entry["abstract"])
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
 
    annotated_text = []
    for tree in chunked_sentences:
        annotated_text.append(tree2dict(tree))
    raw_entry["abstract_annotated"] = annotated_text

    return raw_entry

def extract_features(raw_entry):
    annotated_entry = annotate(raw_entry)

    features = {}

    features["company"] = annotated_entry["company"]

    // TBD according to https://github.com/soylent-grin/textext/issues/1

    return features