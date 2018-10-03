from SPARQLWrapper import SPARQLWrapper, JSON
from constants import indexToLocationType
import json, os, sys

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

endpointLimit = 10000
limit = 30000

prefixes = """
prefix dbo: <http://dbpedia.org/ontology/>
prefix dbp: <http://dbpedia.org/property/>

"""

queries = [
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbo:locationCity ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
""",
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbo:locationCountry ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
""",
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbo:foundationPlace ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
""",
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbp:hqLocation ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
""",
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbo:country ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
""",
"""
select distinct (str(?companyName) as ?companyNameStr) (str(?locationName) as ?locationNameStr) (str(?abstract) as ?abstractStr)
    where {
      ?company a dbo:Company ;
         rdfs:label ?companyName ;
         dbo:state ?location ;
         dbo:abstract ?abstract .
      ?location rdfs:label ?locationName .
      filter (langMatches(lang(?companyName),'en') && langMatches(lang(?locationName),'en') && langMatches(lang(?abstract),'en'))
    }
"""
]

def makeNextQuery(base, offset):
    return base + " LIMIT " + str(endpointLimit) +  " OFFSET " + str(offset)

def peformQuery(q):
    sparql.setQuery(prefixes + q)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def performIterateQuery(q, index):
    results = []
    currentOffset = 0
    while currentOffset < limit:
        print("> performing iterate query; current offset is " + str(currentOffset))
        results += sparqlResultsToList(peformQuery(makeNextQuery(q, currentOffset)), index)
        currentOffset += endpointLimit
    return results

def sparqlResultsToList(results, index):
    targetJSON = []
    for result in results["results"]["bindings"]:

        # gwohlgen: changed, as this gave me an error:
        # TypeError: Object of type 'bytes' is not JSON serializable

        # targetJSON.append({
        #     "company": result["companyNameStr"]["value"].encode('utf-8').strip(),
        #     "location": result["locationNameStr"]["value"].encode('utf-8').strip(),
        #     "abstract": result["abstractStr"]["value"].encode('utf-8').strip()
        # })
        targetJSON.append({
            "company": result["companyNameStr"]["value"].strip(),
            "location": result["locationNameStr"]["value"].strip(),
            "abstract": result["abstractStr"]["value"].strip(),
            "locationType": index
        })



    return targetJSON

def queryAndMerge():
    print("hello; querying DBPedia endpoint for companies...")
    targetJSON = []
    for idx, q in enumerate(queries):
        print("performing {0} query...".format(idx + 1))
        nthResult = performIterateQuery(q, idx + 1)
        targetJSON += nthResult
        print("got {0} items".format(len(nthResult)))
    print("total items count is {0}; fitering to find only abstracts with company name and location...".format(len(targetJSON)))
    filteredJSON = []
    for entry in targetJSON:
        if entry["company"] in entry["abstract"] and entry["location"] in entry["abstract"]:
            filteredJSON.append(entry)
    print("total item count after filtering is {0}".format(len(filteredJSON)))
    return filteredJSON

def writeToFile(res):
    targetPath = "./data"
    targetFile = "raw.json"
    print("serializing to {0}/{1} file...".format(targetPath, targetFile))
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    outfile = open("{0}/{1}".format(targetPath, targetFile), "w+")
    outfile.write(json.dumps(res, indent=4, sort_keys=True))
    outfile.close()

    print("done; ready to annotate")

writeToFile(queryAndMerge())
