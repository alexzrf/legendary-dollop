import requests
import sys
#payload = {'text': 'Barack Obama was the president of the United States.'}
#r = requests.get('http://localhost:8011/text2rdf', params=payload)
#print r.url
#print r.text

print '\n RDF converter'
print '\n ###################'
print '\n Input the number of documents:'
p = input('--> ')
for a in range (1, p+1):
	#url = 'http://localhost:8011/text2rdf'
	content = {'text' : open('NewsData/Split/'+str(a)+'.txt', 'rb'), 'meta_uri' : 'HERE RECURSIVELY INPUT'}
	#r = requests.post(url, data=content)
	#print content
	#print r.url
	print content
	#print r.text
	#f = open('NewsData/str(a).ttl', 'w')
	#f.write(r.text)
	#f.close()
	#print 'Done'

