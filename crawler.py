from SPARQLWrapper import SPARQLWrapper, JSON
import json, os, sys

limit = 10000
if len(sys.argv) > 1:
    limit = sys.argv[1]

print("hello; querying DBPedia endpoint for first {0} companies...".format(limit))

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    prefix dbo: <http://dbpedia.org/ontology/>
    prefix dbp: <http://dbpedia.org/property/>

    select distinct 
    (str(?companyName) as ?companyName_en), (MIN(str(?locationName)) as ?locationName_en), (str(?abstract) as ?abstract_en)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbp:hqLocation ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter langMatches(lang(?abstract),'en')
    }
    order by ?company
    limit 
""" + str(limit))

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

targetPath = "./data"
targetFile = "raw.json"
print("done; serializing to {0}/{1} file...".format(targetPath, targetFile))

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

targetJSON = []

for result in results["results"]["bindings"]:
    targetJSON.append({
        "company": result["companyName_en"]["value"],
        "location": result["locationName_en"]["value"],
        "abstract": result["abstract_en"]["value"]
    })

json.dump(targetJSON, open("{0}/{1}".format(targetPath, targetFile), "w+"))

print("done; ready to annotate")
