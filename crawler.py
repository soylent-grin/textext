from SPARQLWrapper import SPARQLWrapper, JSON
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
"""
]

def makeNextQuery(base, offset):
    return base + " LIMIT " + str(endpointLimit) +  " OFFSET " + str(offset)

def peformQuery(q):
    sparql.setQuery(prefixes + q)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def performIterateQuery(q):
    results = []
    currentOffset = 0
    while currentOffset < limit:
        print("> performing iterate query; current offset is " + str(currentOffset))
        results += sparqlResultsToList(peformQuery(makeNextQuery(q, currentOffset)))
        currentOffset += endpointLimit
    return results

def sparqlResultsToList(results):
    targetJSON = []
    for result in results["results"]["bindings"]:
        targetJSON.append({
            "company": result["companyNameStr"]["value"].encode('utf-8').strip(),
            "location": result["locationNameStr"]["value"].encode('utf-8').strip(),
            "abstract": result["abstractStr"]["value"].encode('utf-8').strip()
        })
    return targetJSON

def queryAndMerge():
    print("hello; querying DBPedia endpoint for companies...")
    targetJSON = []
    for idx, q in enumerate(queries):
        print("performing {0} query...".format(idx + 1))
        nthResult = performIterateQuery(q)
        targetJSON += nthResult
        print("got {0} items".format(len(nthResult)))
    print("total items count is {0}".format(len(targetJSON)))
    return targetJSON

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
