
## use in openNMT folder
MYPATH=/home/wohlg/itmo/textext

## step 1
python preprocess.py -train_src $MYPATH/data/src-train.txt -train_tgt $MYPATH/data/tgt-train.txt -valid_src $MYPATH/data/src-val.txt -valid_tgt $MYPATH/data/tgt-val.txt -save_data data/demo


## step 2
python train.py -data data/demo -save_model demo-model

## step 3
#python translate.py -model demo-model_acc_45.04_ppl_28.38_e13.pt -src $MYPATH/data/src-test.txt -output $MYPATH/data/pred.txt -replace_unk -verbose
python translate.py -model demo-model_acc_45.04_ppl_28.38_e13.pt -src $MYPATH/data/src-val.txt -output $MYPATH/data/pred.txt -replace_unk -verbose


## to make openNMT work on my system I had to patch it a bit according to:
# https://github.com/OpenNMT/OpenNMT-py/issues/403
    # Step 1- in onmt/Models.py-
    # Change h.detach_() to h.detach() 

    # nikhilweee
