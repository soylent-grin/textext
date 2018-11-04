
# Various sample datasets and the results with OpenNRE

Here you find a number of datasets created for the *company-location* relation,
and we did an evaluation of those with OpenNRE.


## Prelimiary: corpus creation settings used (and their defaults):

Corpus create setting default: (for more info see parent directory Readme.md)


Setting | Default value | quick explanation 
--------|---------------|-------------------
REPLACE_COMPANY_NAME            | True | replace company name with 'IBM' 
BINARY_LOCATION                 | True | only use generic 'locatedIn' as location relation (instead of fine-grained relations) 
SENTENCE_MUST_CONTAIN_COMPANY   | True | only include sentences in the result that contain the company_name 
FIRST_SENTENCE_ONLY             | True |  only take the first sentence from the abstract 
SKIP_IF_NOT_FOUND_IN_EMBEDDINGS | True | skip sentences where not both company_name and location_name are in the word embedding vocabulary 

## OpenNRE Settings used:

*Model settings:* PCNN, Att (both default)

*Custom settings:* 40 Epochs (instead of 60), and weights initialized with np.ones(), else I run into problems.
 
  
## Test datasets and their evaluation results with OpenNRE 

### train1/test1 



*Settings:* all defaults 
*Size of dataset:*  train1.json : 14536 ---  test1.json : 3635

Output of last epoch (default died because of out-of-memory):
```    
###### Epoch 14 ######
epoch 14 step 12 time 4.35 | loss: 0.411964, not NA accuracy: 0.848573, accuracy: 0.843269
Average iteration time: 5.065202
Testing...
Tensor("word_embedding_14/concat:0", shape=(400002, 50), dtype=float32)
Tensor("word_embedding_14/embedding_lookup:0", shape=(?, 120, 50), dtype=float32)
Calculating weights_table...
Finish calculating
[TEST] step 4 | not NA accuracy: 0.878947, accuracy: 0.835000
[TEST] auc: 0.911017871741
Finish testing
Best model, storing...
terminate called after throwing an instance of 'std::bad_alloc'
  what():  std::bad_alloc
```    

### train2/test2:



*Settings:* defaults, except `REPLACE_COMPANY_NAME=False`
*Size of dataset:*  train2.json : 464   ---  test2.json : 116

Output of last epoch (default died because of out-of-memory):
```    
    Killed by system after:
    ###### Epoch 18 ######
    epoch 18 step 2 time 0.73 | loss: 0.453322, not NA accuracy: 0.723898, accuracy: 0.752083
    Average iteration time: 0.731681
    Testing...
    Tensor("word_embedding_18/concat:0", shape=(400002, 50), dtype=float32)
    Tensor("word_embedding_18/embedding_lookup:0", shape=(?, 120, 50), dtype=float32)
    Calculating weights_table...
    Finish calculating
    [TEST] step 0 | not NA accuracy: 0.721739, accuracy: 0.800000
    [TEST] auc: 0.712972508559
```    


### train3/test3: 

*Settings:* defaults, except `BINARY_LOCATION=False`
*Size of dataset:*  train3.json : 14536 ---  test3.json : 3635



Output of last epoch (default died because of out-of-memory):
```    
    ###### Epoch 27 ######
    epoch 27 step 15 time 1.18 | loss: 0.088221, not NA accuracy: 0.887038, accuracy: 0.890625
    Average iteration time: 4.004085
    Testing...
    Tensor("word_embedding_27/concat:0", shape=(400002, 50), dtype=float32)
    Tensor("word_embedding_27/embedding_lookup:0", shape=(?, 120, 50), dtype=float32)
    Calculating weights_table...
    Finish calculating
    [TEST] step 4 | not NA accuracy: 0.651230, accuracy: 0.676250
    [TEST] auc: 0.612947643549
    Finish testing
    ######
    Finish training textext_pcnn_att
    Best epoch auc = 0.616813
```    

### train4/test4: 

*Settings:* defaults, `SKIP_IF_NOT_FOUND_IN_EMBEDDINGS=False, FIRST_SENTENCE_ONLY=False`
*Size of dataset:*  train4.json : 38145 ---  test4.json : 9537

Output of last epoch (default died because of out-of-memory)
```    
    ###### Epoch 19 ######
    epoch 19 step 44 time 3.95 | loss: 0.194087, not NA accuracy: 0.900917, accuracy: 0.900417
    Average iteration time: 3.753848
    Testing...
    Tensor("word_embedding_19/concat:0", shape=(400002, 50), dtype=float32)
    Tensor("word_embedding_19/embedding_lookup:0", shape=(?, 120, 50), dtype=float32)
    Calculating weights_table...
    Finish calculating
    [TEST] step 14 | not NA accuracy: 0.918182, accuracy: 0.883750
    [TEST] auc: 0.957753014051
    Finish testing
    Best model, storing...
    Killed
```    
