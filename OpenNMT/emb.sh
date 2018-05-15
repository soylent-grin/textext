glove_dir="./glove"

mkdir "$glove_dir"
wget http://nlp.stanford.edu/data/glove.6B.zip
unzip glove.6B.zip -d "$glove_dir"
