from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import itertools
import time
import json

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

op = webdriver.ChromeOptions()
#op.add_argument('headless')

driver = webdriver.Chrome("C://Users//craz0//Downloads//chromedriver_win32//chromedriver.exe", options=op)

URL = "https://cas.byu.edu/cas/login?service=https%3A%2F%2Flearningsuite.byu.edu%2F"
class LSAssignment:
	def __init__(self, title, dueDate, submit, score, gradePercent):
		self.title = title
		self.dueDate = dueDate
		self.submit = submit
		self.score = score
		self.gradePercent = gradePercent

	def PrintAssignment(self):
		return self.title + "(Due " + self.dueDate + ")"

class LSClass:
	def __init__(self, name, xpath):
		self.name = name
		self.xpath = xpath
		self.assignments = []

	def addAssignment(self, title, dueDate, submit, score, gradePercent):
		self.assignments.append(LSAssignment(title, dueDate, submit, score, gradePercent))

	def getAssignments(self):
		s = []
		for i in self.assignments:
			s.append([i.title, i.dueDate, i.submit, i.score, i.gradePercent])
		return s

def LS_login(username, password, passcode=None):
	print("Logging in...")
	driver.get (URL)
	driver.find_element_by_id("username").send_keys(username)
	driver.find_element_by_id ("password").send_keys(password)
	driver.find_element_by_name("submit").click()
	driver.switch_to.frame("duo_iframe")
	print("Pushing DUO...")
	if passcode!= None:
		driver.find_element_by_id("passcode").click()
		driver.find_element_by_name("passcode").send_keys(passcode)
		driver.find_element_by_id("passcode").click()
	else:
		driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button").click()
	element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "current")))
	driver.switch_to.default_content()
	print("Logged in.")

def getClasses():
	classList = []
	print("Getting classes...")
	content = driver.page_source
	soup = BeautifulSoup(content, features="html5lib")
	classes = soup.find_all("a", class_="course-title")
	for Class in classes:
		xpath = xpath_soup(Class)
		classList.append(LSClass(Class.contents[0].strip(), xpath))
	print("Classes got: ", [i.name for i in classList])
	return classList

def scrapeClass(LSClass):
	print("Scraping class: " + LSClass.name)
	driver.find_element_by_xpath(LSClass.xpath).click()
	try:
		element = WebDriverWait(driver, 5).until(
		EC.element_to_be_clickable((By.XPATH, "/html/body/nav[1]/a[5]")))
	except:
		if(driver.current_url.find("instructure")!=-1):
			print("CANVAS CLASS")
			driver.find_element_by_xpath("/html/body/div[2]/header[2]/div[1]/ul/li[1]/a").click()
			driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[4]/div/div/div/a").click()
			driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/nav/ul/li[5]/a").click()
			content = driver.page_source
			soup = BeautifulSoup(content, features="html5lib")
			for EachPart in soup.select('tr[class*="student_assignment"]'):
				if(EachPart.find('th', class_="title").find('a')!=None):
					title = EachPart.find('th', class_="title").find('a').text
				else:
					title = EachPart.find('th', class_="title").text
				if(EachPart.find('td', class_="due").text.strip()!=""):
					dueDate = datetime.strptime(EachPart.find('td', class_="due").text.strip() + ' ' + str(datetime.now().year), '%b %d by %I:%M%p %Y')
				else:
					dueDate = EachPart.find('td', class_="due").text.strip()
				#datetime.strptime("Apr 28 by 11:59pm" + ' ' + str(datetime.now().year), '%b %d by %I:%M%p %Y')
				if(EachPart.find('td', class_="center-align submission-col")!=None):
					if(EachPart.find('td', class_="center-align submission-col").find('p')!=None):
						submit = EachPart.find('td', class_="center-align submission-col").find('p').text
					else:
						submit = "No data"
				else:
					submit = "No data"
				if(EachPart.find('td', class_="score-col passing-true")!=None):
					score = EachPart.find('td', class_="score-col passing-true").get('title')
				else:
					score = "No data"
				if(EachPart.find('span', class_="hide-low-scores")!=None):
					gradePercent = EachPart.find('span', class_="hide-low-scores").text
				else:
					gradePercent = "No data"
				LSClass.addAssignment(title.strip(), dueDate, submit, score, gradePercent)
			driver.get("https://learningsuite.byu.edu")
			return
	element.click()
	content = driver.page_source
	soup = BeautifulSoup(content, features="html5lib")
	for EachPart in soup.select('tr[class*="assignment "]'):
		title = EachPart.find('a', class_="openAssignmentInfo").text
		dueDate = datetime.strptime(EachPart.find('input', class_="dateTimeString").get('value') + ' ' + str(datetime.now().year), '%A, %b %d at %I:%M%p %Y')
		#datetime.strptime("Thursday, May 8 at 2:50pm" + ' ' + str(datetime.now().year), '%A, %b %d at %I:%M%p %Y'))
		if(EachPart.find('td', class_="center-align submission-col").find('p')!=None):
			submit = EachPart.find('td', class_="center-align submission-col").find('p').text
		else:
			submit = "No data"
		if(EachPart.find('td', class_="score-col passing-true")!=None):
			score = EachPart.find('td', class_="score-col passing-true").get('title')
		else:
			score = "No data"
		if(EachPart.find('span', class_="hide-low-scores")!=None):
			gradePercent = EachPart.find('span', class_="hide-low-scores").text
		else:
			gradePercent = "No data"
		LSClass.addAssignment(title, dueDate, submit, score, gradePercent)
	driver.find_element_by_xpath("/html/body/header/nav[2]/ul/li[1]/div/a[1]").click()
	print("Class scraped.")
	return

def classesToJSON(classList):
	export = []
	for Class in classList:
		eqList = []
		for A in Class.assignments:
			eqList.append({"title": A.title, "dueDate": A.dueDate, "submit": A.submit, "score": A.score, "gradePercent": A.gradePercent})
		export.append({"className": Class.name, "assignments": eqList})
	export = [{"updated": datetime.today(), "classes": export}]
	return export


#Login
LS_login("ms973", "password")
#Get classes
classList = getClasses()
#Scrape for assignments
print("Scrapping classes...")
for Class in classList:
	scrapeClass(Class)
	print("Classes scraped.")
driver.quit()
#Convert to json
print("Writing to JSON...")
with open("dataFile.json", "w") as f:
	json.dump(classesToJSON(classList), f, default = myconverter)
f.close()
print("Datafile created.")