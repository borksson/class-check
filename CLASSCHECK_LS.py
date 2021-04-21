import pprint
pp = pprint.PrettyPrinter(indent=4)

fp = open("lsREL250.txt", "r")
page_lines = fp.readlines()
assignments = [i for i in page_lines if i.find("var assignments")!=-1]
assignments = assignments[0].split("{")[1:]
classcheck = []
i = assignments[0]
pp.pprint(i[i.find("name")+7:i.find("shortName")-3])
pp.pprint(i[i.find("fullDueTime")+14:i.find("}")-1])
for i in assignments:
	classcheck.append([i[i.find("name")+7:i.find("shortName")-3],i[i.find("fullDueTime")+14:i.find("}")-1]])

pp.pprint(classcheck)