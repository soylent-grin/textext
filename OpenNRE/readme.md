## Description

Here, we create the dataset needed to train a relation extraction model with [OpenNRE](https://github.com/thunlp/OpenNRE).

There is one script, `create_openNRE_dataset.py` to create the data.
The data will be put into the `data` subdirectory, and contains 
```
    train.json 
    test.json 
    rel2id.json # relation-type to id mappings
    word_vec.json # word embedding vectors
```
(see [OpenNRE](https://github.com/thunlp/OpenNRE) for details about the dataset formats).
    


#### Steps to use this

1. First run the dataset and feature creation from DBpedia in the parent directory.
2. Check that `../data/raw-with-replaced-coreferences.json` has been created.
3. `python create_openNRE_dataset.py`
4. Copy the created dataset directory to OpenNRE and run the training there.

