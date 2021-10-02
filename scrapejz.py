from credentials import USERNAME, PASSWORD  # personal portal credentials
#import constants  # named constants
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime

WEBDRIVER_PATH = '../../Downloads/chromedriver.exe'
SITE_URL = 'https://my.aui.ma/ics'

PROF = 'NISAR SHEIKH, Naeem'  # as written in dropdown menu
SEMESTERS = 2  # Number of semester I'm looking back, but most likely I'll have to go all the way back and ditch this.
OP_FILE = 'summary.xlsx'  # file format: as many sheets as semesters, on each sheet: row is class: roster (or something else)

def get_current_semester() -> tuple:
	# Start semester I'm "counting down" from.
	now = datetime.now()
	year = now.year
	month = now.month
	if 9 <= month <= 12:
		semester = 'Fall'
		year1 = year
		year2 = year + 1
	elif 1 <= month <= 5:
		semester = 'Spring'
		year1 = year - 1  # double check this, i might be tweaking
		year2 = year
	else:
		semester = 'Summer'
		year1 = year - 1
		year2 = year
	# Intersessions?
	return (semester, year1, year2)

def get_previous_semester(current_semester: tuple) -> tuple:
	(semester, year1, year2) = current_semester
	if semester == 'Fall':
		prev_semester = 'Summer'
		prev_year1 = year1 - 1
		prev_year2 = year1
	elif semester == 'Spring':
		prev_semester = 'Fall'
		prev_year1 = year1
		prev_year2 = year1 + 1
	elif semester == 'Summer':
		prev_semester = 'Spring'
		prev_year1, prev_year2 = year1, year2
	return (prev_semester, prev_year1, prev_year2)

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

def launch_search(semester_name: str):
	menu = Select(driver.find_element_by_id('pg0_V_ddlTerm'))
	menu.select_by_visible_text('2008-2009 Spring Semester')  # need to construct this string, the problem is that they're not all uniform
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
	driver.find_element_by_link_text('Search Again').click()

def write_to_output_file(semester: str, classes: list):
	with open(OP_FILE) as op:
		pass
		# create a new sheet named semester and populate first column with classes

def main():
	login()
	navigate_to_search()
	semester = get_current_semester()
	classes = []
	for i in range(SEMESTERS):  # again, might make this a while
		launch_search(semester)
		semester_classes = scrape_classes()
		#print("semester classes", semester_classes)
		classes.append(semester_classes)  # think reference thingy
		return_to_search()
		semester = get_previous_semester(current_semester)
	write_to_output_file(semester_name, classes)
	# not thinking about roster yet

if __name__ == '__main__':
	global driver
	set_current_semester()
	driver = webdriver.Chrome(WEBDRIVER_PATH) # should i make the browser configurable?
	driver.get(SITE_URL)
	main()
	#driver.close()
	print("Done, check output file in this directory")
