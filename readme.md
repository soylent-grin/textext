## Description
Main goal: train a ML classifier, that given a company name and an abstract as input produce a company location as an output.

#### Steps
1. Use DBPedia SPARQl Endpoint to form a training dataset of companies, locations and abstracts,
2. Extract meaningful features from abstract, that correlate with company location
3. Train some classifier on this features
4. Use the result model to get company location from abstract

Maybe we'll use pure NLP methods (based on NLTK named entity recognition and relation extraction) as a comparasion baseline.

## Prereq

Due to neuralcoref issue with models pipeline only works with python 3 now. Try [pyenv](https://github.com/pyenv/pyenv) for python version management (and do not forget about `sudo apt-get install libsqlite3-dev`)


Install neuralcoref from repo:
```bash
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -e .
```

Install main requirements:
```bash
pip install -r requirements.txt
```

## Crawling training data

```bash
python ./crawler.py
```

Result is stored in `./data/raw.json` in intermediate format:

```json
[
  {
    "company": "2.13.61",
    "location": "Estados Unidos",
    "abstract": "2.13.61, Inc. is a publisher and record company founded by musician Henry Rollins and named after his date of birth (February 13, 1961). The company has released albums by the Rollins Band, all of Rollins's spoken-word work, and numerous books. It is based in Los Angeles, California. In his mass-market anthology The Portable Henry Rollins, Rollins stated that he had given 2.13.61 its name because someone had told him that his first self-released book, 20 (1984), had to have a company name on it, and since he felt at the time that he would only ever get to release one book, he simply used his birthdate. 2.13.61 branched out into releasing records not long after Rollins started a solo career following the breakup of Black Flag, initially just releasing Rollins' spoken-word albums. The first two 2.13.61 releases, Big Ugly Mouth and Sweatbox, were first co-released with the label Rollins was signed with at the time as a musician, Texas Hotel Records. Since then, the label has branched out into various rock and jazz releases and even spawned two specialist reissue sublabels, Infinite Zero Archive (a joint venture with Rick Rubin's American Recordings), and District Line, which specializes in reissuing the music of Rollins' hometown of Washington, D.C. It is also used as the name of Rollins' Blazin' (finishing move) in the video game Def Jam: Fight for NY. The literary company's authors include: Henry Rollins (Publisher, Black Flag), Iggy Pop (The Stooges), Exene Cervenka (X, Auntie Christ, The Knitters), Nick Cave (Birthday Party, Bad Seeds, Grinderman), Michael Gira (Swans), Joe Cole, Tricia Warden, Don Bajema, Bill Shields, Jeffery Lee Pierce (The Gun Club), and Ellyn Maybe."
  },
  ...
```

## Replacing coreferences
```bash
python ./raw-to-corefered.py $COUNT # $COUNT is number of first raw entries to parse. Default is 1000.
```
Result is stored in `./data/raw-with-replaced-coreferences.json`; it looks the same as raw entries, except coreferences are replaced by the main mention.

## Extracting features

```bash
# $COUNT is number of first raw entries to annotate. Default is 1000.
# $NE_TYPE is named entity detection framework ("spacy" or "nltk"). Default is "nltk"
python ./corefered-to-featureset.py --count=$COUNT --ne-detection-type=$NE_TYPE
```

Result is stored in `./data/feature-set.json` in intermediate format:

```json
  ...
  [
    {
      "LOCATION_VERB(based)": true,
      "NN(organization)": true,
      "NN(policy)": true,
      "NN(political-journalism)": true,
      "VB(based)": true,
      "VB(covers)": true,
      "VB(is)": true,
      "distance": 23
    },
    false
  ],
  ...
```

## Evaluating the model

```bash
# $INDEX is index of item to predict in raw dataset. Default is last in raw.json.
# $IS_BINARY defines whether we use 8 (y\n location country, y\n locatin city, etc) location classes or 2(y\n). Default is false (8 classes).
# $NE_TYPE is named entity detection framework ("spacy" or "nltk"). Default is "nltk"
python ./classifier.py --predict-index=$INDEX --is-binary=$IS_BINARY --ne-detection-type=$NE_TYPE
```

Sample output:

```
predicting for location 'Italian': location city (3.91%), location country (4.69%)
predicting for location 'Turin': location city (97.04%), location country (0.92%)
predicting for location 'Italy': location city (96.25%), location country (1.20%)
```

## Printing list of extracted features per entry

```bash
python ./test.py $INDEX # where $INDEX is index of item to predict in raw dataset
```

## Constructing wrong and correct datasets

```bash
python ./prepare-correct-and-wrong-classification-sets.py $COUNT # where $COUNT is number of items to classify
```
The result output would be presented in `data/correct.json` and `data/wrong.json` files
