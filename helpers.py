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
        if "locate" in word or "headquart" in word or "found" in word or "base" in word or "establish" in word:
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
    raw_entry["tokenized_sentences"] = tokenized_sentences
    raw_entry["tagged_sentences"] = tagged_sentences
    raw_entry["raw_sentences"] = sentences

    return raw_entry

def get_distance(company, location, sent):
    # TODO
    return 1;

def get_words_between(company, location, raw_sent):
    words = []
    company_index = raw_sent.find(company)
    if company_index > -1:
        location_index = raw_sent.find(location)
        if location_index > -1:
            substr = raw_sent[company_index + len(company) + 1:location_index - 1]
            words = nltk.pos_tag(nltk.word_tokenize(substr))
    return words

def extract_features_by_location(company, location, raw_sent):
    features = {}
    words_between = get_words_between(company, location, raw_sent)

    features["distance"] = len(words_between)
    for vb in extract_verbs(words_between):
        features["VB({0})".format(vb)] = True
    for nown in extract_nowns(words_between):
        features["NN({0})".format(nown)] = True
    for vb in extract_location_related_verbs(words_between):
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
            featureset = extract_features_by_location(raw_entry["company"], location, annotated_item["raw_sentences"][idx])
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
                featureset = extract_features_by_location(item["company"], l, annotated_item["raw_sentences"][idx])
                training_set.append((featureset, l == item["location"]))

    return training_set


def prepare_predict_item(item):
    predict_set = []
    target_locations = []

    annotated_item = annotate(item)
    for idx, sent in enumerate(annotated_item["abstract_annotated"]):
        locations = extract_locations_from_sent(sent)
        for l in locations:
            featureset = extract_features_by_location(item["company"], l, annotated_item["raw_sentences"][idx])
            predict_set.append(featureset)
            target_locations.append(l)

    return (predict_set, target_locations)

def predict(classifier, item):
    print("trying to predict location for item: ")
    print(item)
    predict_set, locations = prepare_predict_item(item)
    for idx, l in enumerate(locations):
        print("predicting for location '{0}': {1}".format(l, classifier.classify(predict_set[idx])))


