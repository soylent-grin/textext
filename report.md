# Goal

Prepare the classifier, that would predict company location from the given DBPedia abstract about the company

# Concept of algorithm

- Use DBPedia SPARQL endpoint to fetch list of companies, their locations and abstract from article about the company. Location type may be `location city`, `location country`, `foundation place` and `headquarted location` according to DBPedia labels.
- Replace all coreferences, found in abstract, with the main meaning.
- For each location, found in abstract, perform feature extraction based on NER: all nowns, verbs and (separately) location-related verbs (e.g. `based`, `founded`) between company name entry and this location in each sentence of abstract.
- Train ML classifier on result feature set, assuming that each location from step 3 is treated as one of 8 classes: `true` \ `false` fro each location type from step 1.
- Evaluating the classifier: convert given abstract to features with described pipeline (coreference and NER annotation) and for each location, found in abstract, predict probability of whether it one of location type from step 1.

# Notes on algorithm

- For 4 types of locations we can crawl ~50k abstracts from DBPedia, and only ~24k of them would contain exact location label, returned by DBPedia.
- We also filter abstract for only written in English.
- Classifier may works in 2 different modes: binary (predict whether given location is or isn't company location) and non-binary (predict probability of whether given location is one of location types from step 1).
- For coreference replacement step we use [small english model](https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_sm-3.0.0/en_coref_sm-3.0.0.tar.gz).
- Sometimes prepare script fails with segfault on coreference step - most likely because of https://github.com/huggingface/neuralcoref/issues/47

# Results

With ~24k crawled entries we get around 120k featuresets to train with. Train\test split ratio is 0.8.
Accuracy for binary classification: with coreference step - 78%, without - 74%.
Accuracy for non-binary classification is much more mess and not usable with current feature extraction model: with coreference step - 1.3%, without - 1.2%.

# Used tools

- Python 3.6.5
- [NLTK](http://www.nltk.org/) for NER annotation and classifier
- [neuralcoref](https://github.com/huggingface/neuralcoref) for coreference replacement
- [sparqlwrapper](https://rdflib.github.io/sparqlwrapper/)
