## Description

Here, we create the datasets needed to train a relation extraction model with [OpenNRE](https://github.com/thunlp/OpenNRE).

There is one script, `create_openNRE_dataset.py` to create the data.
The data will be put into the `data` subdirectory, and contains 
```
    train.json 
    test.json 
    rel2id.json # relation-type to id mappings
    word_vec.json # word embedding vectors
```
(see [OpenNRE](https://github.com/thunlp/OpenNRE) for details about the dataset formats).
    


#### Basic steps to use this

1. First run the dataset and feature creation from DBpedia in the parent directory.
2. Check that `../data/raw-with-replaced-coreferences.json` has been created.
3. `python create_openNRE_dataset.py`
4. Copy the created dataset directory to OpenNRE and run the training there.

### Configuration of `create_openNRE_dataset.py`

`create_openNRE_dataset.py` has many config options, at the beginning of the script

Some of those are (including the default value):
* `REPLACE_COMPANY_NAME = True`: If set to true, replace the company name with 'IBM'. We did this, because company name should have much influence on the relation extraction,
 and we know that the default company name is always found in the word embeddings.
* `BINARY_LOCATION = True`: In the original dataset collection with SPARQL, we collect different properties which correspond to location information, eg. `headquarterLocation`, etc.
If this is set to true, we only use the generic 'locatedIn' as location relation (instead of fine-grained relations).
* `SENTENCE_MUST_CONTAIN_COMPANY = True`: If set, then include only sentences in the resulting datasets that contain the `company_name`
* `FIRST_SENTENCE_ONLY = True`: If set, only take the first sentence from the abstract (instead of all sentences in the Wikipedia abstract)
* `SKIP_IF_NOT_FOUND_IN_EMBEDDINGS = True`: If set, skip all sentences where not both `company_name` AND `location_name` are in the word embedding vocabulary.


