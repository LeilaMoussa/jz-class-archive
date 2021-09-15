from credentials import USERNAME, PASSWORD  # personal portal credentials
#import constants  # named constants
from selenium import webdriver
from selenium.webdriver.support.ui import Select

WEBDRIVER_PATH = '../../Downloads/chromedriver.exe'
SITE_URL = 'https://my.aui.ma/ics'

PROF = 'NISAR SHEIKH, Naeem'  # as written in dropdown menu
SEMESTERS = 2  # arbitary tbh
OP_FILE = 'summary.xlsx'  # file format: as many sheets as semesters, on each sheet: row is class: roster (or something else)

def get_current_semester():
	global current_semester
	# get current month: fall if between sept & dec (or jan?) inclusively, spring if between jan (or feb?) and may, summer if between $$$ & $$$, winter interssion if between two
	pass

def login():
	driver.find_element_by_id('userName').send_keys(USERNAME)
	driver.find_element_by_id('password').send_keys(PASSWORD)
	driver.find_element_by_id('siteNavBar_btnLogin').click()
	# No, I will not handle edge cases or errors.

def navigate_to_search():
	driver.find_element_by_link_text('Students').click()
	driver.find_element_by_id('pg1_V_lblAdvancedSearch').click()
	driver.implicitly_wait(2)
	# select faculty in the same way

def get_semester_name() -> str:
	pass
	# if moving from spring to fall, decrement year
	# decide whether i want the result to exactly match the portal at this point. probably tbh

def launch_search(semester_name: str):
	menu = Select(driver.find_element_by_id('pg0_V_ddlTerm'))
	menu.select_by_visible_text('2008-2009 Spring Semester')  # need to construct this string
	menu = Select(driver.find_element_by_id('pg0_V_ddlFaculty'))
	menu.select_by_visible_text(PROF)
	driver.find_element_by_id('pg0_V_btnSearch').click()

def scrape_classes() -> list:
	semester_classes = []
	i = 1
	# for the following, i could also try to use find_elements_by_partial_link_text and search for CSC, MTH, and EGR (?) classes
	while True:
		try:
			semester_classes.append(driver.find_element_by_id(f'pg0$V$dgCourses$sec2$row{i}$lnkCourse').text)
			i += 2
		except:
			return semester_classes

def return_to_search():
	pass
	# click on "search again"

def write_to_output_file(semester: str, classes: list):
	with open(OP_FILE) as op:
		pass
		# create a new sheet named semester and populate first column with classes

def main():
	login()
	navigate_to_search()
	classes = []
	for semester in range(SEMESTERS):
		semester_name = get_semester_name()
		launch_search(semester_name)
		semester_classes = scrape_classes()
		print("semester classes", semester_classes)
		classes.append(semester_classes)  # think reference thingy
		return_to_search()
	write_to_output_file(semester_name, classes)
	# not thinking about roster yet

if __name__ == '__main__':
	global driver
	get_current_semester()
	driver = webdriver.Chrome(WEBDRIVER_PATH) # should i make the browser configurable?
	driver.get(SITE_URL)
	main()
	#driver.close()
	print("Done, check output file in this directory")
