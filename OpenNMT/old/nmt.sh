
## use in openNMT folder
MYPATH=/home/wohlg/itmo/textext/OpenNMT

## step 1
python preprocess.py -train_src $MYPATH/src-train.txt -train_tgt $MYPATH/tgt-train.txt -valid_src $MYPATH/src-val.txt -valid_tgt $MYPATH/tgt-val.txt -save_data data/demo

## optional: if embeddings are used
python tools/embeddings_to_torch.py -emb_file_enc "glove/glove.6B.100d.txt" -emb_file_dec "glove/glove.6B.100d.txt" -dict_file "data/demo.vocab.pt" -output_file "data/embeddings" -type GloVe


## step 2
#python train.py -data data/demo -save_model demo-model

## optional: if embeddings are used
python train.py -save_model data/demo -batch_size 64 -layers 2 -rnn_size 200 -word_vec_size 100  -pre_word_vecs_enc "data/embeddings.enc.pt" -pre_word_vecs_dec "data/embeddings.dec.pt" -data data/demo
python train.py -data data/demo -save_model demo-model -word_vec_size 100 -pre_word_vecs_enc "data/embeddings.enc.pt" -pre_word_vecs_dec "data/embeddings.dec.pt"


## step 3
python translate.py -model demo-model_acc_45.04_ppl_28.38_e13.pt -src $MYPATH/src-val.txt -output $MYPATH/pred.txt -replace_unk -verbose


## to make openNMT work on my system I had to patch it a bit according to:
# https://github.com/OpenNMT/OpenNMT-py/issues/403
    # Step 1- in onmt/Models.py-
    # Change h.detach_() to h.detach() 

    # nikhilweee
