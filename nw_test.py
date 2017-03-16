#from rdflib import Graph
import requests

#g = Graph()
#g.parse("http://localhost:50053/resources?id=http://www.w3.org/2000/01/rdf-schema#Resource")
#print len(g)

response = requests.get("http://localhost:50053/resources/ksdemo?id=http://www.bbc.co.uk/news/uk-politics-eu-referendum-36616747#England")
print response.status_code
print response.content


#import rdflib
#import rdflib_jsonld
# Use the parse functions to point directly at the URI
#uri = 'http://localhost:50053/ui?action=lookup&id=http%3A%2F%2Fdbpedia.org%2Fresource%2FMedrano_Tamen'
#graph = rdflib.Graph()
#graph.parse(uri)
#new_graph = graph.serialize(format='nt')
#print (new_graph)




