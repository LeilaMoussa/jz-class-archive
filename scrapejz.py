from credentials import USERNAME, PASSWORD  # personal portal credentials
from constants import PROF, OP_FILE, SITE_URL, WEBDRIVER_PATH, FIRST_RECORDED_SEMESTER
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime

def format_semester_name(current_semester: tuple) -> str:
	(semester, year1, year2) = current_semester
	if year1 >= 2014:
		return f'{year1}-{year2} Academic Year - {semester}'
	else:
		return f'{year1}-{year2} {semester}'

# Actually, i need to hang on to both the tuple and the string.
def get_current_semester() -> tuple:
	# Start semester I'm "counting down" from.
	now = datetime.now()
	year = now.year
	month = now.month
	if 9 <= month <= 12:
		semester = 'Fall Semester'  # should make these named constants
		year1 = year
		year2 = year + 1
	elif 1 <= month <= 5:
		semester = 'Spring Semester'
		year1 = year - 1  # double check this, i might be tweaking
		year2 = year
	else:
		semester = 'Summer Session'
		year1 = year - 1
		year2 = year
	# Intersessions?
	return (semester, year1, year2)

def get_previous_semester(current_semester: tuple) -> tuple:
	(semester, year1, year2) = current_semester
	if semester == 'Fall Semester':
		prev_semester = 'Summer Session'
		prev_year1 = year1 - 1
		prev_year2 = year1
	elif semester == 'Spring Semester':
		prev_semester = 'Fall Semester'
		prev_year1 = year1
		prev_year2 = year1 + 1
	elif semester == 'Summer Session':
		prev_semester = 'Spring Semester'
		prev_year1, prev_year2 = year1, year2
	return (prev_semester, prev_year1, prev_year2)

def login():
	driver.find_element_by_id('userName').send_keys(USERNAME)
	driver.find_element_by_id('password').send_keys(PASSWORD)
	driver.find_element_by_id('siteNavBar_btnLogin').click()

def navigate_to_search():
	driver.find_element_by_link_text('Students').click()
	driver.find_element_by_id('pg1_V_lblAdvancedSearch').click()
	driver.implicitly_wait(2)

def launch_search(semester_name: str):
	semester_menu = Select(driver.find_element_by_id('pg0_V_ddlTerm'))
	semester_menu.select_by_visible_text(semester_name)
	faculty_menu = Select(driver.find_element_by_id('pg0_V_ddlFaculty'))
	faculty_menu.select_by_visible_text(PROF)
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
			print("oopsie!")
			return semester_classes

def return_to_search():
	driver.find_element_by_link_text('Search Again').click()
	driver.implicitly_wait(2)

def write_to_output_file(semester: str, classes: list):
	print("pretend i'm writing")
	return
	with open(OP_FILE) as op:
		pass
		# create a new sheet named semester and populate first column with classes

def main():
	login()
	navigate_to_search()
	current_semester = get_current_semester()
	semester_name = format_semester_name(current_semester)
	classes = []
	while semester_name != FIRST_RECORDED_SEMESTER:
		launch_search(semester_name)
		semester_classes = scrape_classes()
		#print("semester classes", semester_classes)
		classes.append(semester_classes)  # think reference thingy
		return_to_search()
		current_semester = get_previous_semester(current_semester)
		semester_name = format_semester_name(current_semester)
	#print("in the end, classes are", classes)
	write_to_output_file(semester_name, classes)

if __name__ == '__main__':
	global driver
	driver = webdriver.Chrome(WEBDRIVER_PATH) # should i make the browser configurable?
	driver.get(SITE_URL)
	main()
	#driver.close()
	print("Done, check output file in this directory")
