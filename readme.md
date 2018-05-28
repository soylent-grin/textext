## Description
Main goal: train a ML classifier, that given a company name and an abstract as input produce a company location as an output.

#### Steps
1. Use DBPedia SPARQl Endpoint to form a training dataset of companies, locations and abstracts,
2. Extract meaningful features from abstract, that correlate with company location
3. Train some classifier on this features
4. Use the result model to get company location from abstract

Maybe we'll use pure NLP methods (based on NLTK named entity recognition and relation extraction) as a comparasion baseline.

## Prereq

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

## Extracting features

```bash
python ./raw-to-featureset.py
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
python ./classifier.py $INDEX # where $INDEX is index of item to predict in raw dataset
```

## Printing list of features per entry

```bash
python ./test.py $INDEX # where $INDEX is index of item to predict in raw dataset
```