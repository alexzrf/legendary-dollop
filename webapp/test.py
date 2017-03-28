from flask import Flask
from flask import request
from flask import render_template
from SPARQLWrapper import SPARQLWrapper2, JSON
import requests
import rdflib
import re

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
   if request.form['btn'] == 'SendText':
	identify = 0
	identifyliteral = "Send news article"
	newsArticle = request.form['textInput']
    	url = 'http://35.187.76.238:8011/text2rdf'
        content = {'text' : newsArticle }
        r = requests.post(url, data=content)
        transformed = r.text.encode("utf-8")
	entityList = []
	extendedentityList = []
	eventList = []
	labelList = []
       # matched_lines = [line for line in transformed.split('\n') if ("sem:Event" in line) or ("owl:sameAs" in line)]
	for line in transformed.split('\n'):
		if "owl:sameAs" in line and "dbpedia" in line:
			line = re.sub(r'.*dbpedia:', 'dbpedia:', line)
			line = re.sub(r'.*resource/', 'dbpedia:', line)
			line = re.sub(r'>', '', line)
			line = line[:-2]
			entityList.append(line)
		if "foaf:name" in line:
			line = re.sub(r'foaf:name', '', line)
			line = re.sub(r'.*>', '', line)
			line = line[:-2]
			extendedentityList.append(line)
		if "sem:Event" in line:
			line = re.sub(r'.*#', '', line)
			line = line[:-15]
			eventList.append(line)	
		if "rdfs:label" in line:
			labelList.append(line)
	
	#matched_lines.reverse
        return render_template("my-form.html", entityList=entityList, extendedentityList=extendedentityList, eventList=eventList, labelList=labelList)

   if request.form['btn'] == 'Query':
	   if request.form.getlist('option'):
		value = request.form.getlist('option')
		if 1 < len(value) <= 2:
			finalentity=[]
			finalevent=[]
			for i in value:
				if "dbpedia" in i:
					finalentity.append(i)
				else:
					finalevent.append(i)
			if len(finalentity) == 2:
				identifier = "TwoEntities"
				varent1 = finalentity[0]
				varent2 = finalentity[1]

				sparql = SPARQLWrapper2("http://localhost:50053/sparql")
				sparql.setQuery("""
				SELECT DISTINCT ?actor1Name ?actor2Name ?article ?title ?date ?eventName 
				WHERE
				{
				?actor1 owl:sameAs """+str(varent1)+""" ; gaf:denotedBy ?mention ; foaf:name ?actor1Name.
				?mention ks:mentionOf ?article .
				?article dct:title ?title ; dct:created ?date .
				?actor2 owl:sameAs """+str(varent2)+""" ; gaf:denotedBy ?mention2 ; foaf:name ?actor2Name.
				?mention2 ks:mentionOf ?article .
				OPTIONAL {?event a sem:Event; sem:hasActor* ?actor1 ; sem:hasActor* ?actor2 ; rdfs:label ?eventName}
				}

				""") 
				sparql.setReturnFormat(JSON)
				results = sparql.query().convert()
				headers = ['actor1', 'actor2', 'article', 'title', 'date', 'event']
			    	
				return render_template("result.html", headers=headers, results=results, identifier=identifier)

			elif (len(finalentity) == 1) and (len(finalevent) == 1):
				identifier = "EntityAndEvent"
				varentity = finalentity[0]
				varevent = '"' + finalevent[0] + '"'
				print varevent
				print varentity

				sparql = SPARQLWrapper2("http://localhost:50053/sparql")
				sparql.setQuery("""
				SELECT DISTINCT  ?actorName ?title ?date ?article ?event2Name ?event3Name
				WHERE
				{
				?frame rdfs:isDefinedBy framenet: .
				?event a sem:Event ; rdfs:label ?eventlabel ; a ?frame .
				FILTER regex(str(?eventlabel),"""+str(varevent)+""", "i")
				?event2 a ?frame ; gaf:denotedBy ?mention2 ; rdfs:label ?event2Name.

				?actor  owl:sameAs """+str(varentity)+""" ; gaf:denotedBy ?mention ; foaf:name ?actorName .
				?mention ks:mentionOf ?article .
				?article dct:title ?title ; dct:created ?date .
				?mention2 ks:mentionOf ?article .
			    
				OPTIONAL {?event2 sem:hasActor* ?event3 .
				?event3 rdfs:label ?event3Name .
				FILTER (?event2!=?event3) }
				}
				""") 
				sparql.setReturnFormat(JSON)
				results = sparql.query().convert()
				headers = ['actor', 'title', 'date', 'article', 'event', 'event2']
			    	
				return render_template("result.html", headers=headers, results=results, identifier=identifier)
				
				#Sparql for 1 entity and 1 event
			else:
				message = "Incorrect selection!"
				return render_template("my-form.html", message=message)
			
			return render_template("result.html", results=value)
		else:
			message = "Incorrect selection!"
			return render_template("my-form.html", message=message)
	   else: 
		message = "Incorrect selection!"
		return render_template("my-form.html", message=message)

   if request.form['btn'] == 'SendForm1':
	identify = 1
	identifyliteral = "A named event for a named entity"
	var1 = request.form['entity']
	var2 = request.form['entity2']

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
	GROUP BY  ?entity ?actor2 ?predicate ?article ?title
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['entity', 'article', 'title', 'predicate', 'actor2']
    	
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'SendForm2':
	identify = 2
	identifyliteral = "A named event for a named dbpedia Person"
	var1 = request.form['person']
	var2 = request.form['event']

	sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT DISTINCT  ?actorName ?title ?date ?article ?event2Name ?event3Name
	WHERE
	{
        ?frame rdfs:isDefinedBy framenet: .
        ?event a sem:Event ; rdfs:label ?eventlabel ; a ?frame .
        FILTER regex(str(?eventlabel),"""+str(var2)+""", "i")
        ?event2 a ?frame ; gaf:denotedBy ?mention2 ; rdfs:label ?event2Name.

        ?actor  owl:sameAs """+str(var1)+""" ; gaf:denotedBy ?mention ; foaf:name ?actorName .
	?mention ks:mentionOf ?article .
	?article dct:title ?title ; dct:created ?date .
        ?mention2 ks:mentionOf ?article .
    
        OPTIONAL {?event2 sem:hasActor* ?event3 .
        ?event3 rdfs:label ?event3Name .
	FILTER (?event2!=?event3) }
	}
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['actor', 'title', 'date', 'article', 'event', 'event2']
    	
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'SendForm3': 
	identify = 3
	identifyliteral = "Events in the paths of two dbpedia Persons"
	var3 = request.form['person1']
	var4 = request.form['person2']

	sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT DISTINCT ?actor1Name ?actor2Name ?article ?title ?date ?eventName 
	WHERE
	{
	?actor1 owl:sameAs """+str(var3)+""" ; gaf:denotedBy ?mention ; foaf:name ?actor1Name.
	?mention ks:mentionOf ?article .
	?article dct:title ?title ; dct:created ?date .
	?actor2 owl:sameAs """+str(var4)+""" ; gaf:denotedBy ?mention2 ; foaf:name ?actor2Name.
	?mention2 ks:mentionOf ?article .
	OPTIONAL {?event a sem:Event; sem:hasActor* ?actor1 ; sem:hasActor* ?actor2 ; rdfs:label ?eventName}
	}

	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['actor1', 'actor2', 'article', 'title', 'date', 'event']
    	
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'DBpediaPersons': 
	identify = 5
	identifyliteral = "Reports&DBpediaPersons"
        sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT (COUNT (?people) AS ?mentionedPeople)
	WHERE
	{
	?DBpersons a dbo:Person .
	?people owl:sameAs ?DBpersons .
	FILTER EXISTS {?people gaf:denotedBy ?mention}
        }
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['mentionedPeople']
        
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'NewsArticles': 
	identify = 6
	identifyliteral = "Reports&Articles"
        sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT (COUNT (?article) AS ?articlescount)
	WHERE
	{
	?article a ks:Resource
        }
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['articleCount']
        
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'DetectedEvents': 
	identify = 7
	identifyliteral = "Reports&Events"
        sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT (COUNT (?event) AS ?eventCount)
	WHERE
	{
	?event a sem:Event
	}
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['eventCount']
        
        return render_template("result.html", headers=headers, results=results)

   if request.form['btn'] == 'EventsFrequency': 
	identify = 7
	identifyliteral = "Reports&Events"
        sparql = SPARQLWrapper2("http://localhost:50053/sparql")
	sparql.setQuery("""
	SELECT ?label (COUNT (DISTINCT ?event) AS ?eventsCount)
	WHERE
	{
	?event a sem:Event .
	?event rdfs:label ?label . 
	}
	GROUP BY ?label
	ORDER by desc(?eventsCount)
	LIMIT 100
	""") 
	sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        headers = ['eventName', 'eventFrequency']
        
        return render_template("result.html", headers=headers, results=results)

if __name__ == '__main__':
    app.run(debug = True)
