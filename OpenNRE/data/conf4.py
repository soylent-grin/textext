############################### configuration section ##################################
TRAIN_FN="data/train4.json"
TEST_FN="data/test4.json"
SENTENCE_MUST_CONTAIN_COMPANY=True  ## only include sentences in the result that contain the company_name
BINARY_LOCATION=True
SKIP_IF_NOT_FOUND_IN_EMBEDDINGS=False
EMB_FILE='data/word_vec.json'
##FULL_PARAGRAPH=False# instead of sentences, use the full paragraph as input data?
FIRST_SENTENCE_ONLY=False
TO_LOWER=False ## convert sentences to lowercase (needed for OpenNRE_old)
REPLACE_COMPANY_NAME=True ## convert sentences to lowercase (needed for OpenNRE)
COMPANY_NAME_REPLACEMENT="IBM" ## convert sentences to lowercase (needed for OpenNRE)
