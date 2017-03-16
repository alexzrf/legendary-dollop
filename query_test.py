from SPARQLWrapper import SPARQLWrapper2, JSON
import requests
import rdflib

from rdflib import Graph

var1= raw_input('Entity ->')
var2= raw_input('Predicate ->')
print var1, var2

sparql = SPARQLWrapper2("http://localhost:50053/sparql")
sparql.setQuery("""
SELECT DISTINCT ?entity ?article ?title ?predicate ?actor2
WHERE
{
?entity gaf:denotedBy ?mention .
?mention ks:mentionOf ?article .
?article ks:hasMention ?mention2 ;dct:title ?title.
?mention2 nif:anchorOf ?predicate .
OPTIONAL { ?action gaf:denotedBy ?mention2 ; sem:hasActor* ?actor .
?actor2 sem:hasActor* ?action .  }
FILTER ((regex(str(?entity), """+str(var1)+""", "i")) && (regex(str(?predicate), """+str(var2)+""", "i")))
}
GROUP BY ?actor2 ?predicate ?entity  ?article ?title
""") 
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print results.variables  # this is an array consisting of "subj" and "prop"
for binding in results.bindings :
        # each binding is a dictionary. Let us just print the results
        print "%s: %s (of type %s)" % ("entity",binding[u"entity"].value,binding[u"entity"].type)
        print "%s: %s (of type %s)" % ("article",binding[u"article"].value,binding[u"article"].type)
	print "%s: %s (of type %s)" % ("title",binding[u"title"].value,binding[u"title"].type)
	print "%s: %s (of type %s)" % ("predicate",binding[u"predicate"].value,binding[u"predicate"].type)
	print "%s: %s (of type %s)" % ("actor2",binding[u"actor2"].value,binding[u"actor2"].type)
	print 	
	print "#########################################################"
	print

#response = requests.get("http://localhost:50053/resources?id=http://www.bbc.co.uk/news/uk-politics-eu-referendum-36616747#England")
#print response.status_code
#print response.content


#import rdflib
#import rdflib_jsonld
# Use the parse functions to point directly at the URI
#uri = 'http://localhost:50053/ui?action=lookup&id=http%3A%2F%2Fdbpedia.org%2Fresource%2FMedrano_Tamen'
#graph = rdflib.Graph()
#graph.parse(uri)
#new_graph = graph.serialize(format='nt')
#print (new_graph)




