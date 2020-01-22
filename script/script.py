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
    result = g.query("""SELECT * WHERE { ?s ?p ?o }""")

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
        if entry['name'] == "index.ttl":
            g.parse(loc + entry['name'], format="turtle")

    # get the 2 location files
    g.query("""SELECT * WHERE { ?s ?p ?o }""")

    # do something with the result

# get files from input argument url location
arg = sys.argv[1]
print("will retrieve files from %s" % arg)
loc = parseAllStuff(arg)
print(parseStuffLocation(loc))