import urllib.request
import pprint
pp = pprint.PrettyPrinter(indent=4)
assignments = []
#bring in page

fp = open("canvas.txt", "r")

#page_lines = [i.decode("utf8") for i in mybytes]
page_lines = fp.readlines()
fp.close()
#sort page
for i in range(len(page_lines)):
	if page_lines[i].find('class="title"')!=-1:
		assignments.append([page_lines[i+1], page_lines[i+5]]) #until 
#sort assignment data
i = assignments[0][0]
#pp.pprint(i[i.find('>')+1:i.find("</a>")])
i = assignments[0][1]
#pp.pprint(i.strip())
classcheck = []
for i in assignments:
	classcheck.append([i[0][i[0].find('>')+1:i[0].find("</a>")], i[1].strip()])
classcheck = classcheck[:-6]
pp.pprint(classcheck)
#form new classcheck
f = open("classcheck.txt", "w")
for i in classcheck:
	f.write(i[0] + " (Due " + i[1] + "), ")
f.close()
#assignment_name (Due assignment_date),