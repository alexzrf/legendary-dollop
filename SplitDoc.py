import os
import time 

os.chdir('NewsData/')
os.mkdir('Split')
with open ('NewsList.txt') as f:
	line = ''
	start = 0
	counter = 1
	for x in f.read().split("\n"):
		if (x=='###############'):
			if (start==1):
				with open('Split' + '/' + str(counter) + '.txt','w') as fo:
					fo.write(line)
					fo.close()
					line=''
					counter+=1
			else:
				start=1
		else:
			if (line==''):
				line = x
			else:
				line = line + '\n' + x
	f.close()
