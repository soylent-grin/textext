
############################### configuration section ##################################
TRAIN_FN="data/train2.json"
TEST_FN="data/test2.json"
SENTENCE_MUST_CONTAIN_COMPANY=True  ## only include sentences in the result that contain the company_name
BINARY_LOCATION=True
SKIP_IF_NOT_FOUND_IN_EMBEDDINGS=True
EMB_FILE='data/word_vec.json'
##FULL_PARAGRAPH=False# instead of sentences, use the full paragraph as input data?
FIRST_SENTENCE_ONLY=True
TO_LOWER=False ## convert sentences to lowercase (needed for OpenNRE_old)
REPLACE_COMPANY_NAME=False ## convert sentences to lowercase (needed for OpenNRE)
COMPANY_NAME_REPLACEMENT="IBM" ## convert sentences to lowercase (needed for OpenNRE)

