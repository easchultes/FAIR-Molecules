import sys
import requests
import rdflib

if len(sys.argv) == 1:
    print("FAILED: expected one argument")
    sys.exit(1)

def parseAllStuff(arg):
    g = rdflib.Graph()
    r = requests.get(arg)

    for entry in r.json():
        if entry['type'] == "file":
            url = arg + entry['name']
            print("adding %s to graph" % url)
            g.parse(url, format="turtle")

    # parse all files
    result = g.query("""prefix fdo: <http://example.com/fdo#> 

SELECT DISTINCT ?location {

?fdoRecord a fdo:Record;
fdo:digitalObjectOfType fdo:MGFile;
fdo:locationOfDO ?location.
}""")

    location = None
    # find file location
    for stmt in result:
        print(stmt)

    return location

def parseStuffLocation(loc):
    # parse 'index' ttl file
    g = rdflib.Graph()
    r = requests.get(loc)

    for entry in r.json():
        if entry['name'] == "description.ttl":
            g.parse(loc + entry['name'], format="turtle")

    # get the 2 location files
    g.query("""prefix fdo: <http://example.com/fdo#> 

SELECT DISTINCT ?adjacencyFileUrl ?atomFileUrl {

?mgFile a  fdo:MGFile;
fdo:hasAdjacencyFile ?adjacencyFileUrl;
fdo:hasAtomsFile ?atomFileUrl.

}""")

    # do something with the result

# get files from input argument url location
arg = sys.argv[1]
print("will retrieve files from %s" % arg)
loc = parseAllStuff(arg)
print(parseStuffLocation(loc))
