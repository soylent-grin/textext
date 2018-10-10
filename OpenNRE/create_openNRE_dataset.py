# -*- coding: utf-8 -*-

# Author: Gerhard Wohlgenannt / ITMO Univ / 2018

import sys
sys.path.append('..')

import json, hashlib, sys, nltk
from pprint import pprint
from helpers import annotate, extract_features_by_location, extract_locations_from_sent, extract_locations_from_sent_spacy
from constants import indexToLocationType

import spacy
nlp = spacy.load('en')

############################### configuration section ##################################
TRAIN_FN="data/train1.json"
TEST_FN="data/test1.json"
SENTENCE_MUST_CONTAIN_COMPANY=True  ## only include sentences in the result that contain the company_name
BINARY_LOCATION=True
SKIP_IF_NOT_FOUND_IN_EMBEDDINGS=True
EMB_FILE='data/word_vec.json'
##FULL_PARAGRAPH=False# instead of sentences, use the full paragraph as input data?
FIRST_SENTENCE_ONLY=True
TO_LOWER=False ## convert sentences to lowercase (needed for OpenNRE_old)
REPLACE_COMPANY_NAME=True ## convert sentences to lowercase (needed for OpenNRE)
COMPANY_NAME_REPLACEMENT="IBM" ## convert sentences to lowercase (needed for OpenNRE)

#################### constants
NEGATIVE_TYPE='Unrelated'
BINARY_TYPE='locatedIn'

count = None 
if len(sys.argv) > 1:
    count = int(sys.argv[1])


class DSItem:
    def __init__(self, sentence, company_name, location_name, location_type):

        self.company_name = company_name
        self.location_name = location_name
        self.location_type = location_type

        if type(location_type) == type(1):
            self.location_type = indexToLocationType[location_type].replace(' ', '_')

        if type(sentence) == type([]):
            self.sentence = ' '.join(sentence)
        else:
            self.sentence = sentence

        if len(location_name.split(' ')) > 1:
            self.location_name = location_name.replace(' ', '_')

            ## also replace in sentence
            self.sentence = self.sentence.replace(location_name, self.location_name)

        ##  replace " " with "_" in company_name and sentence
        if len(company_name.split(' ')) > 1:
            self.company_name = company_name.replace(' ', '_')

            ## also replace in sentence
            self.sentence = self.sentence.replace(company_name, self.company_name)

        if TO_LOWER:
            self.sentence      = self.sentence.lower()
            self.company_name  = self.company_name.lower()
            self.location_name = self.location_name.lower()

        if REPLACE_COMPANY_NAME:
            self.sentence      = self.sentence.replace(self.company_name, COMPANY_NAME_REPLACEMENT)
            self.company_name  = COMPANY_NAME_REPLACEMENT

    
    def print_me(self):
        print("\n DSItem")
        print("Company: ", self.company_name)
        print("Location: ", self.location_name)
        print("LocationType: ", self.location_type)
        print("Sentence: ", self.sentence)

    def sentence_contains_company(self):
    
        if self.sentence.replace(' ', '').find(self.company_name.replace(' ','')) > -1:
            #print('contains:', self.company_name, '//', self.sentence)
            return True
        else:
            #print('NOT contains:', self.company_name, '//', self.sentence)
            return False
        


def create_basic_datastructure(data):
    """ create a datastructure which the following characteristics 
        type: dict
        key: company_name
        A company has these elements:
        * the basic data from the input JSON
        * but: we merge based on the company name, and add a 
          'gold_relations': [('locationCity', 'Vienna'), ('locationCountry', 'Austria'), ()] list
        """
    basic_data = {}
    print('create_basic_datastructure: len of data at start:', len(data))
    
    for d in data:
        #pprint (d)
        annotated_d = annotate(d)
        d = annotated_d    

        ## call annotation function

        if d['company'] in basic_data:
            #print(d['company'])
            basic_data[d['company']]['gold_relations'].append( (d['locationType'], d['location']) )
        else:
            basic_data[d['company']] = d
            basic_data[d['company']]['gold_relations'] = []
            basic_data[d['company']]['gold_relations'].append( (d['locationType'], d['location']) )

    print('create_basic_datastructure: len of basic_data on exit:', len(basic_data))
    return basic_data 


def create_dataset(data):
    """ now, for every company we iterate over it's sentences
        for any sentence:
            * check if we find our gold locations in there -- this will be the positive examples
            * check which other (location) NEs we find there -- this will be the negative examples
    """
    ds_items = []

    for company_name in data:
        company = data[company_name]
        gold_locs = [gold_loc for (gold_locType, gold_loc) in company['gold_relations']]

        ## extract all loctions per sentence!
        #for idx, sent in enumerate(company["abstract_annotated"]):

        sentences = nltk.sent_tokenize(company["abstract"])
        for idx, sent in enumerate(sentences):
            print(sent)
            #locations = set(extract_locations_from_sent(sent))
            #print("AAA: ",locations)
            doc = nlp(sent)
            locations = set(extract_locations_from_sent_spacy(doc))
            print("BBB: ", locations)

            ## check if the gold relation is in the list of locations
            for (gold_locType, gold_loc) in company['gold_relations']:
                if gold_loc in locations:
                    item = DSItem(company['tokenized_sentences'][idx], company_name, gold_loc, gold_locType) 
                    #item.print_me()
                    #print(sent)
                    #print('\n\n')
                    ds_items.append(item)
                else:
                    pass
                    #print('not found')

            ## ok, and now iterate over locations -- if they don't overlap with the gold_locations, add them as negative samples 

            for l in locations:
                if l in gold_locs:
                    #print("l in gold_locs", l, gold_locs)
                    pass
                else: 
                    ## create negative sample
                    
                    ## first some more checks?
                    item = DSItem(company['tokenized_sentences'][idx], company_name, l, NEGATIVE_TYPE) 
                    #item.print_me()
                    #print(sent)
                    #print('\n\n')
                    ds_items.append(item)
                    
                    #print("l NOT in gold_locs", l, gold_locs)

            if FIRST_SENTENCE_ONLY:
                # only use first sentence? 
                break
    
            #    training_set.append((featureset, constructDecision(item["locationType"], l == item["location"])))

        ## what to do now with locations / sentence pairs?!

    return data, ds_items

   
def filter_ds_items(ds_items, sentence_must_contain_company=False):

    filtered_ds_items = [] 
    print("filter_sentence_must_contain_company: Number of items at entry:", len(ds_items))

    for ds_item in ds_items:

        if sentence_must_contain_company and not ds_item.sentence_contains_company():
            continue

        ## sanity filter
        if ds_item.company_name == ds_item.location_name:
            print('company_name == location_name:', ds_item.company_name, ds_item.location_name, ' ---> skipping!')
            continue

        filtered_ds_items.append(ds_item)

    print("filter_sentence_must_contain_company: Number of items at exit:",  len(filtered_ds_items))
    
    return filtered_ds_items    

def create_OpenNRE_dict(data):

        res = []

        for item in data:

            ## convert all relation types (except the NEGATIVE_TYPE) to BINARY_TYPE
            ## so for example "headquarter" --> 'locatedIn' .. 
            if BINARY_LOCATION:
                if item.location_type != NEGATIVE_TYPE:
                    item.location_type = BINARY_TYPE


            idh = hashlib.md5(item.company_name.encode('utf8')).hexdigest()
            idt = hashlib.md5(item.location_name.encode('utf8')).hexdigest()
            new_entry = { 'head': {'type':'COMPANY',  'word':item.company_name,  'id': idh}, 
                          'tail': {'type':'LOCATION', 'word':item.location_name, 'id': idt}, 
                          'relation': item.location_type, 
                          'sentence': item.sentence}

            print(new_entry)
            res.append(new_entry)

        print('Number of items in dataset:', len(res))   
        return res



def write_dl_dataset(ds_items):
    """ finally, write everything to the target file
    """

    split = int( len(ds_items) * 0.8 )
    train_ds = ds_items[:split]
    test_ds  = ds_items[split:]

    #[ds_item.write(train_fh) for ds_item in train_ds]
    #[ds_item.write(test_fh)  for ds_item in test_ds]

    train_opennre = create_OpenNRE_dict(train_ds)
    test_opennre  = create_OpenNRE_dict(test_ds)

    #train_fh = open(TRAIN_FN, 'w')
    #test_fh  = open(TEST_FN, 'w')

    with open(TRAIN_FN, 'w') as outfile:
        json.dump(train_opennre, outfile)

    with open(TEST_FN, 'w') as outfile:
        json.dump(test_opennre, outfile)



def check_if_NEs_in_embeddings(ds_items, emb_fn):

    data = json.load(open(EMB_FILE)) 
    words = [d['word'] for d in data]

    print('\nNumber of words in the embeddings:', len(words))
    #print(words[:20])
    company_found, company_not_found, location_found, location_not_found = 0, 0, 0, 0

    filtered_ds_items = []

    for d in ds_items:
        if d.company_name.lower() in words:
            company_found = company_found + 1 
        else:
            company_not_found = company_not_found + 1 

        if d.location_name.lower() in words:
            location_found = location_found + 1 
        else:
            location_not_found = location_not_found + 1 

        if SKIP_IF_NOT_FOUND_IN_EMBEDDINGS: 
            if (d.company_name.lower() in words and d.location_name.lower() in words):
                filtered_ds_items.append(d)
        else:
            filtered_ds_items.append(d)

    print("check_if_NEs_in_embeddings: Number company_found", company_found)
    print("check_if_NEs_in_embeddings: Number company_not_found", company_not_found)
    print("check_if_NEs_in_embeddings: Number location_found", location_found)
    print("check_if_NEs_in_embeddings: Number location_not_found", location_not_found)

    return filtered_ds_items

if __name__ == '__main__':
    check_if_NEs_in_embeddings([], EMB_FILE) 
    data = json.load(open('../data/raw-with-replaced-coreferences.json'))
   
    if count: 
        data = create_basic_datastructure(data[:count]) 
    else:
        data = create_basic_datastructure(data) ## all

    data, ds_items = create_dataset(data)

    ds_items = filter_ds_items(ds_items, sentence_must_contain_company=SENTENCE_MUST_CONTAIN_COMPANY)  

    ds_items = check_if_NEs_in_embeddings(ds_items, EMB_FILE)
    ds_items = check_if_NEs_in_embeddings(ds_items, EMB_FILE)

    write_dl_dataset(ds_items)

    next_steps = """ \n\n

NEXT STEPS:

Try variations like 
    first sentence only
    all paragraph


NEXT:
    Fix Encoding Issues: could not solve this yet, see wohlg_test/1.py
    Other embeddings -- TODO, download some more: FastText (2.5M tokens): 42 instead of 9 found for first 100 items.
    Extraction: if some locations are seperated by "," or "and", and one of them is relevant (for binary task), others are also!
    """

    print(next_steps)
