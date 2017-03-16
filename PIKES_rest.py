import requests
import datetime
import sys
import tarfile
import subprocess
import os
import signal
#payload = {'text': 'Barack Obama was the president of the United States.'}
#r = requests.get('http://localhost:8011/text2rdf', params=payload)
#print r.url
#print r.text

def create_menu():
	print '\n RDF converter'
	print '\n ###################'
	print '\n Filename (1) or No. of documents (2)?'
loop = True
while loop: 
	create_menu()
	choice = input('--> ')
	if choice == 1:
		o = raw_input('--> ')
		url = 'http://localhost:8011/text2rdf'
		with open('NewsData/news_Filename/' + str(o), 'r') as m:
		    	uri = m.readline().strip()
			timestamp = m.readline().strip()
			title = m.readline().strip()
			article = m.readline()
			content = {'meta_uri' : uri, 'meta_date' : timestamp, 'meta_title' : title, 'text' : article }
			r = requests.post(url, data=content)
			f = open('NewsData/filename_Ready4KS/' + str(o) + '.trig', 'w')
			f.write(r.text.encode("utf-8"))
			f.close()
			print 'Done ' + str(o)
		print 'Creating Archive...'
		now = datetime.datetime.now()
		stamp = now.strftime("%Y-%m-%d-%H-%M")
		command1 = ("tar -czf NewsData/" + str(stamp) + ".tar.gz NewsData/filename_Ready4KS")
		proc1 = subprocess.Popen(command1, shell=True, executable='/bin/bash')
		proc1.communicate()
		print 'Done'
		print 'Aggregating .trig files...'
		command2 = "tar -O -xf NewsData/" + str(stamp) + ".tar.gz | pigz -9 - > knowledgestore-docker-master/data/additional_data/" + str(stamp) + "_PROC.trig.gz"
		proc2 = subprocess.Popen(command2, shell=True, executable='/bin/bash')
		proc2.communicate()
		print 'Done'
		loop = False
	elif choice == 2: 
		print '\n Input the number of documents:'
		p = input('--> ')
		for a in range (1, p+1):
			url = 'http://localhost:8011/text2rdf'
			with open('NewsData/news_Split/'+ str(a) + '.txt', 'r') as f:
		    		uri = f.readline().strip()
				timestamp = f.readline().strip()
				title = f.readline().strip()
				article = f.readline()
				#print uri
				#print timestamp
				#print title
				#print article
				#print '\n'
				content = {'meta_uri' : uri, 'meta_date' : timestamp, 'meta_title' : title, 'text' : article }
				r = requests.post(url, data=content)
				#print content
				#print r.url
				#print content
				#print r.text
				f = open('NewsData/split_Ready4KS/' + str(a) + '.trig', 'w')
				f.write(r.text.encode("utf-8"))
				f.close()
				print 'Done ' + str(a) + '/' + str(p)
		print 'Creating Archive...'
		now = datetime.datetime.now()
		stamp = now.strftime("%Y-%m-%d-%H-%M")
		command1 = ("tar -czf NewsData/" + str(stamp) + ".tar.gz NewsData/split_Ready4KS")
		proc1 = subprocess.Popen(command1, shell=True, executable='/bin/bash')
		proc1.communicate()
		print 'Done'
		print 'Aggregating .trig files...'
		command2 = "tar -O -xf NewsData/" + str(stamp) + ".tar.gz | pigz -9 - > knowledgestore-docker-master/data/additional_data/" + str(stamp) + "_PROC.trig.gz"
		proc2 = subprocess.Popen(command2, shell=True, executable='/bin/bash')
		proc2.communicate()
		print 'Done'
		loop = False
	else:
		raw_input("Incorrect selection. Press any key")
		


