import json, os, sys
import nltk

# from helpers import prepare_training_set

raw = json.load(open('./data/raw.json'))

index = int(sys.argv[1])

print(raw[index])
# print((prepare_training_set(raw[index:index + 1])))

# import spacy
# nlp = spacy.load('en_coref_sm')
# doc = nlp(raw[index]["abstract"])

# print(doc._.coref_clusters)
# print(doc._.coref_clusters[1].mentions)
# print(doc._.coref_clusters[1].mentions[-1])
# print(doc._.coref_clusters[1].mentions[-1]._.coref_cluster.main)

# token = doc[-1]
# print(token._.in_coref)
# print(token._.coref_clusters)

# span = doc[-1:]
# print(span._.is_coref)
# print(span._.coref_cluster.main)
# print(span._.coref_cluster.main._.coref_cluster)

# mentions = [{'start':    span.start_char,
#              'end':      span.end_char,
#              'text':     span.text,
#              'resolved': span._.coref_main_mention.text
#             } for span in doc._.coref_mentions]
# clusters = list(list(span.text for span in cluster)
#                 for cluster in doc._.coref_clusters)
# resolved = doc._.coref_resolved

# print(json.dumps({
#     "mentions": mentions,
#     "clusters": clusters,
#     "resolved": resolved
# }))