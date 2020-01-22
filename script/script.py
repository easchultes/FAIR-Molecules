import sys
import requests
import rdflib
import json

if len(sys.argv) == 1:
    print("FAILED: expected one argument")
    sys.exit(1)

def parseAllStuff(arg):
    g = rdflib.Graph()
    g.parse(arg, format="turtle")

    # parse all files
    result = g.query("""prefix fdo: <http://example.com/fdo#> 

SELECT DISTINCT ?location {

?fdoRecord a fdo:Record;
fdo:digitalObjectOfType fdo:MGFile;
fdo:locationOfDO ?location.
}""")

    location = None
    # find file location
    for row in result:
        location = str(row[0])

    return location

def parseStuffLocation(loc):
    # parse 'index' ttl file
    g = rdflib.Graph()
    r = requests.get(loc)

    for entry in r.json():
        if entry['name'] == "description.ttl":
            g.parse(loc + entry['name'], format="turtle")

    # get the 2 location files
    result = g.query("""prefix fdo: <http://example.com/fdo#> 

SELECT DISTINCT ?adjacencyFileUrl ?atomFileUrl {

?mgFile a  fdo:MGFile;
fdo:hasAdjacencyFile ?adjacencyFileUrl;
fdo:hasAtomsFile ?atomFileUrl.

}""")

    results = {}

    for row in result:
        results['adjecencyFileUrl'] = str(row[0])
        results['atomFileUrl'] = str(row[1])
    # do something with the result
    return json.dumps(results)

# get files from input argument url location
arg = sys.argv[1]
loc = parseAllStuff(arg)
print(parseStuffLocation(loc))
