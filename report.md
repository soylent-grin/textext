# Goal

Create a classifier, which predicts the company location from the given DBPedia abstract about the company.

# Main algorithm

- Use DBPedia SPARQL endpoint to fetch list of companies, their locations and abstract from article about the company. Location type may be `location city`, `location country`, `foundation place` and `headquarted location` according to DBPedia labels.
- Replace all coreferences, found in abstract, with the main meaning.
- For each location, found in abstract, perform feature extraction based on NER: all nowns, verbs and (separately) location-related verbs (e.g. `based`, `founded`) between company name entry and this location in each sentence of abstract.
- Train ML classifier on the resulting feature set, assuming that each location from step 3 is treated as one of 8 classes: `true` \ `false` for each location type from step 1.
- Evaluating the classifier: convert given abstract to features with described pipeline (coreference and NER annotation) and for each location, found in abstract, predict probability of whether it one of location type from step 1.

# Notes on algorithm

- For 4 types of locations we can crawl ~50k abstracts from DBPedia, and only ~24k of them would contain exact location label, returned by DBPedia.
- Currently, we also filter abstracts to only those written in English.
- The classifier may work in 2 different modes: binary (predict whether given location is or isn't company location) and non-binary (predict probability of whether given location is one of location types from step 1).
- For coreference replacement step we use the [small english model](https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_sm-3.0.0/en_coref_sm-3.0.0.tar.gz).
- Sometimes the prepare script fails with segfault on coreference step - most likely because of https://github.com/huggingface/neuralcoref/issues/47

# Results

With ~24k crawled entries we get around 120k featuresets to train with. Train\test split ratio is 0.8.


| Accuracy Binary Classifier| With CoRef | Without CoRef |
| --------------------------|-----------:| -------------:|
|                           |  78%       |          74%  |

| ?? Accuracy MultiClass Classifier| With CoRef | Without CoRef |
| ------------------------------|-----------:| -------------:|
|                               |  1.3%      |          1.2% |

Accuracy for non-binary classification is much lower for the current feature extraction model: with coreference step - 1.3%, without - 1.2%. 
This may be caused by indistinguishable features for different location types; however, the probability estimation of such classifier still may be useful. 

| Accuracy MultiClass Classifier| With CoRef | Without CoRef |
| ------------------------------|-----------:| -------------:|
| location city                 |  X.X%      |          X.X% |
| location country              |  X.X%      |          X.X% |
| foundation place              |  X.X%      |          X.X% |
| headquarted location          |  X.X%      |          X.X% |


# Used tools

- Python 3.6.5
- [NLTK](http://www.nltk.org/) for NER annotation and classifier
- [neuralcoref](https://github.com/huggingface/neuralcoref) for coreference replacement
- [sparqlwrapper](https://rdflib.github.io/sparqlwrapper/)
