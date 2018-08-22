import nltk
from nltk import Tree
from constants import *
import spacy

import networkx as nx
nlp = spacy.load('en_coref_sm')

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

LOCATION_RELATED_VERBS = ["locate", "headquart", "found", "base", "establish", "operate"]

# spacy helpers

def extract_locations_from_sent_spacy(doc):
    locations = []

    for ent in doc.ents:
        if (ent.label_ == "GPE"):
            locations.append(ent.text)

    return locations

def extract_dependency_distance_spacy(company, location, doc):
    # TODO
    return -1

def extract_location_related_verbs_spacy(doc):
    verbs = []

    for token in doc:
        if token.pos_ == "VERB":
            for index, v in enumerate(LOCATION_RELATED_VERBS):
                if v in token.text:
                    verbs.append(token.text)

    return verbs;

def extract_verbs_spacy(doc):
    verbs = []

    for token in doc:
        if (token.pos_ == "VERB"):
            verbs.append(token.text)

    return verbs;

def extract_nouns_spacy(doc):
    nouns = []

    for token in doc:
        if (token.pos_ == "NOUN"):
            nouns.append(token.text)

    return nouns;

# nltk helpers

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

def extract_nouns(sent):
    nouns = []
    for (word, label) in sent:
        if label == 'NN':
            nouns.append(word)
    return nouns;

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

def extract_dependency_distance(company, location, raw_sent):
    try:
        company_replacement = "nokia"
        location_replacement = "america"
        # print("replacing {0} to {1}, {2} to {3}".format(company, company_replacement, location, location_replacement))
        prepared_sent = raw_sent.replace(company, company_replacement).replace(location, location_replacement)
        # print(prepared_sent)
        document = nlp(prepared_sent)

        edges = []
        for token in document:
            # FYI https://spacy.io/docs/api/token
            for child in token.children:
                edges.append((token.lower_, child.lower_))

        graph = nx.Graph(edges)

        path = nx.shortest_path_length(graph, source=company_replacement, target=location_replacement);
        # print(path)
        return path
    except:
        # print("Error occured while getting dependency distance on company {0} and location {1}".format(company, location))
        return -1

def get_words_between(company, location, raw_sent):
    words = []
    company_index = raw_sent.find(company)
    if company_index > -1:
        location_index = raw_sent.find(location)
        if location_index > -1:
            substr = raw_sent[company_index + len(company) + 1:location_index - 1]
            words = nltk.pos_tag(nltk.word_tokenize(substr))
    return words

def get_words_between_spacy(company, location, raw_sent):
    words = []
    company_index = raw_sent.find(company)
    if company_index > -1:
        location_index = raw_sent.find(location)
        if location_index > -1:
            substr = raw_sent[company_index + len(company) + 1:location_index - 1]
            words = nlp(substr)
    return words

def extract_features_by_location(company, location, raw_sent):
    features = {}
    words_between = get_words_between(company, location, raw_sent)

    if (len(words_between) > 0):
        features["dependency_distance"] = extract_dependency_distance(company, location, raw_sent)
    else:
        features["dependency_distance"] = -1

    features["distance"] = len(words_between)
    for vb in extract_verbs(words_between):
        features["VB({0})".format(vb)] = True
    for nown in extract_nouns(words_between):
        features["NN({0})".format(nown)] = True
    for vb in extract_location_related_verbs(words_between):
        features["LOCATION_VERB({0})".format(vb)] = True

    return features

def extract_features_by_location_spacy(company, location, sent, doc):
    features = {}

    words_between = get_words_between_spacy(company, location, sent)

    features["distance"] = len(words_between)

    if (len(words_between) > 0):
        features["dependency_distance"] = extract_dependency_distance(company, location, sent)
        features["distance"] = len(words_between)
        for vb in extract_verbs_spacy(words_between):
            features["VB({0})".format(vb)] = True
        for nown in extract_nouns_spacy(words_between):
            features["NN({0})".format(nown)] = True
        for vb in extract_location_related_verbs_spacy(words_between):
            features["LOCATION_VERB({0})".format(vb)] = True
    else:
        features["dependency_distance"] = -1

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
    #     for nown in extract_nouns(sent):
    #         features["NN({0})".format(nown)] = True
    #     for vb in extract_location_related_verbs(sent):
    #         features["LOCATION_VERB({0})".format(vb)] = True

    # features["words_count"] = words_count

    return featuresets

def prepare_training_set_nltk(raw_set):
    training_set = []

    for index, item in enumerate(raw_set):
        print("processing entry {0}... \r".format(str(index + 1)), end='', flush=True)
        annotated_item = annotate(item)
        for idx, sent in enumerate(annotated_item["abstract_annotated"]):
            locations = extract_locations_from_sent(sent)
            for l in locations:
                featureset = extract_features_by_location(item["company"], l, annotated_item["raw_sentences"][idx])
                training_set.append((featureset, constructDecision(item["locationType"], l == item["location"])))

    return training_set

def prepare_training_set_spacy(raw_set):
    training_set = []

    for index, item in enumerate(raw_set):
        print("processing entry {0}... \r".format(str(index + 1)), end='', flush=True)
        sentences = nltk.sent_tokenize(item["abstract"])
        for idx, sent in enumerate(sentences):
            doc = nlp(sent)
            locations = extract_locations_from_sent_spacy(doc)
            for l in locations:
                featureset = extract_features_by_location_spacy(item["company"], l, sent, doc)
                training_set.append((featureset, constructDecision(item["locationType"], l == item["location"])))

    return training_set

def prepare_training_set(raw_set, ne_detection_type):
    print("preparing train set (ne_detection_type is {0})...".format(ne_detection_type))
    if ne_detection_type == 'nltk':
        return prepare_training_set_nltk(raw_set)
    elif ne_detection_type == 'spacy':
        return prepare_training_set_spacy(raw_set)
    else:
        print("unknown ne_detection_type: {0}".format(ne_detection_type))
        return []

def prepare_predict_item_nltk(item):
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

def prepare_predict_item_spacy(item):
    predict_set = []
    target_locations = []

    sentences = nltk.sent_tokenize(item["abstract"])
    for idx, sent in enumerate(sentences):
        doc = nlp(sent)
        locations = extract_locations_from_sent_spacy(doc)
        for l in locations:
            featureset = extract_features_by_location_spacy(item["company"], l, sent, doc)
            predict_set.append(featureset)
            target_locations.append(l)

    return (predict_set, target_locations)

def prepare_predict_item(item, ne_detection_type):
    print("preparing prediction item (ne_detection_type is {0})...".format(ne_detection_type))
    nlp = spacy.load('en_coref_sm')
    doc = nlp(item["abstract"])
    item["abstract"] = doc._.coref_resolved
    if ne_detection_type == 'nltk':
        return prepare_predict_item_nltk(item)
    elif ne_detection_type == 'spacy':
        return prepare_predict_item_spacy(item)
    else:
        print("unknown ne_detection_type: {0}".format(ne_detection_type))
        return ([], [])

def predict(classifier, item, is_binary = False, ne_detection_type = "nltk"):
    print("trying to predict location for item: ")
    print(item)
    predict_set, locations = prepare_predict_item(item, ne_detection_type)
    for idx, l in enumerate(locations):
        result = ""
        if is_binary:
            print("predicting for location '{0}': {1}".format(l, classifier.classify(predict_set[idx])))
        else:
            dist = classifier.prob_classify(predict_set[idx])
            result = "predicting for location '{0}': ".format(l)
            predictions = []
            for label in dist.samples():
                if (parseDecisionResult(label)):
                    predictions.append("{0} ({1:.2f}%)".format(parseDecisionLabel(label), dist.prob(label) * 100))
            print("predicting for location '{0}': {1}".format(l, ", ".join(predictions)))

def prepare_correct_wrong_set(raw_set, train_set):
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(classifier.show_most_informative_features(5))
    correct = []
    wrong = []

    for index, item in enumerate(raw_set):
        print("classifying entry {0}... \r".format(str(index + 1)), end='', flush=True)
        predict_set, locations = prepare_predict_item(item)
        isCorrect = False
        for idx, l in enumerate(locations):
            prediction = classifier.classify(predict_set[idx])
            if (parseDecisionResult(prediction)):
                decisionIndex = parseDecisionLabelIndex(prediction)
                if decisionIndex == str(item["locationType"]):
                    isCorrect = True


        result_item = {
            "location": item["location"],
            "company": item["company"],
            "abstract": item["abstract"],
            "features": [{ 'location':location, 'features': predict_set[i]} for i, location in enumerate(locations)]
        }

        if (isCorrect):
            correct.append(result_item)
        else:
            wrong.append(result_item)

    print("{0} correct items, {1} wrong items".format(len(correct), len(wrong)))

    return correct, wrong

def replace_coreferences(raw):
    print("replacing coreferences...")
    nlp = spacy.load('en_coref_sm')

    for index, item in enumerate(raw):
        print("processing entry {0}... \r".format(str(index + 1)), end='', flush=True)
        doc = nlp(item["abstract"])
        item["abstract"] = doc._.coref_resolved

    return raw

def convert_to_binary(featuresets):
    for item in featuresets:
        item[1] = parseDecisionResult(item[1])

    return featuresets