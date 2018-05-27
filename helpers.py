import nltk
from nltk import Tree

import sys
reload(sys)
sys.setdefaultencoding('utf8')

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_locations_from_sent(sent):
    locations = []

    if hasattr(sent, 'label') and sent.label:
        if sent.label() == 'GPE':
            locations.append(' '.join([child[0] for child in sent]))
        else:
            for child in sent:
                locations.extend(extract_locations_from_sent(child))

    return locations

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

def annotate(raw_entry):
    sentences = nltk.sent_tokenize(raw_entry["abstract"])
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)

    annotated_text = []
    for tree in chunked_sentences:
        annotated_text.append(tree)

    raw_entry["abstract_annotated"] = annotated_text
    raw_entry["tagged_sentences"] = tagged_sentences

    return raw_entry

def get_distance(company, location, sent):
    # TODO
    return 1;

def extract_features_by_location(company, location, sent):
    features = {}

    features[location] = location
    features["distance"] = get_distance(company, location, sent)
    for vb in extract_verbs(sent):
        features["VB({0})".format(vb)] = True
    for nown in extract_nowns(sent):
        features["NN({0})".format(nown)] = True
    for vb in extract_location_related_verbs(sent):
        features["LOCATION_VERB({0})".format(vb)] = True

    return features

def extract_locations(annotated_entry):
    locations = []
    for idx, sent in enumerate(annotated_entry["abstract_annotated"]):
        locations += extract_locations_from_sent(sent)
    return locations

def extract_features(annotated_entry):
    featuresets = []

    for idx, sent in enumerate(annotated_entry["abstract_annotated"]):
        locations = extract_locations(sent)
        # print("found locations: {0}".format(locations))
        for location in locations:
            featureset = extract_features_by_location(raw_entry["company"], location, annotated_entry["tagged_sentences"][idx])
            featuresets.append(featureset)

    # print(featuresets)
    #     for ne in extract_named_entities(sent):
    #         features["NE({0})".format(ne)] = True

    # words_count = 0
    # for sent in annotated_entry["tagged_sentences"]:
    #     words_count += len(sent)
    #     for vb in extract_verbs(sent):
    #         features["VB({0})".format(vb)] = True
    #     for nown in extract_nowns(sent):
    #         features["NN({0})".format(nown)] = True
    #     for vb in extract_location_related_verbs(sent):
    #         features["LOCATION_VERB({0})".format(vb)] = True

    # features["words_count"] = words_count

    return featuresets

def prepare_training_set(raw_set):
    print("preparing train set...")
    training_set = []

    for index, item in enumerate(raw_set):
        sys.stdout.write("processing entry {0}... \r".format(str(index + 1)))
        sys.stdout.flush()
        annotated_item = annotate(item)
        for idx, sent in enumerate(annotated_item["abstract_annotated"]):
            locations = extract_locations_from_sent(sent)
            for l in locations:
                featureset = extract_features_by_location(item["company"], l, annotated_item["tagged_sentences"][idx])
                training_set.append((featureset, l == item["location"]))

    return training_set


def prepare_predict_item(item):
    predict_set = []
    target_locations = []

    annotated_item = annotate(item)
    for idx, sent in enumerate(annotated_item["abstract_annotated"]):
        locations = extract_locations_from_sent(sent)
        for l in locations:
            featureset = extract_features_by_location(item["company"], l, annotated_item["tagged_sentences"][idx])
            predict_set.append(featureset)
            target_locations.append(l)

    print(target_locations)
    return (predict_set, target_locations)

def predict(classifier, item):
    print("trying to predict location for item: ")
    print(item)
    predict_set, locations = prepare_predict_item(item)
    print(predict_set, locations)
    for idx, l in enumerate(locations):
        print("predicting for location '{0}': {1}".format(l, classifier.classify(predict_set[idx])))


