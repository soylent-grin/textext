import json
from pprint import pprint

# ------------------------- CONFIG -----------------------

# input and output file names
IN_FN="../data/raw.json"

OUTFN = ["src-train.txt", "tgt-train.txt",
         "src-val.txt", "tgt-val.txt"]

# ------------------------- END OF CONFIG -----------------------



def load_data(distinct_abstracts=True, train_ratio=0.9):

    with open(IN_FN) as f:
        data = json.load(f)

    # for d in data:
    #     pprint(d)
    #     print()

    print("Number of items found in full  dataset at start", len(data))

    if distinct_abstracts:

        filt, seen = [], set()

        for d in data:
            if not d['abstract'] in seen:
                filt.append(d)
                seen.add(d['abstract'])

        #print(filt)
        #print(len(filt))

        data=filt



    split_border = int(train_ratio * len(data))

    train = data[:split_border]
    val   = data[ split_border:]

    print("Number of items found in full  dataset", len(data))
    print("Number of items found in train dataset", len(train))
    print("Number of items found in val   dataset", len(val))

    return train, val


def write_nmt_datafiles(src, tgt, our_data):

    src_fh = open(src, 'w')
    tgt_fh = open(tgt, 'w')
    
    for i in our_data: 
        
        # make sure we have only ONE line per abstract
        abstract = i['abstract'].replace('\n','. ') 
        src_fh.write(abstract + '\n')        
        tgt_fh.write(i['location'] + '\n')        


  
if __name__ == "__main__":

    train, val = load_data(distinct_abstracts=True, train_ratio=0.8)

    # write train and val data to files 
    write_nmt_datafiles(OUTFN[0], OUTFN[1], train)
    write_nmt_datafiles(OUTFN[2], OUTFN[3], val)



    print("TODO .. add optional FILTER to items -- to only have items which have the result in the abstract")
    print("TODO .. use embeddings")


