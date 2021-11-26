from credentials import USERNAME, PASSWORD
from constants import PROF, OP_FILE, SITE_URL, WEBDRIVER_PATH, FIRST_RECORDED_SEMESTER
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import xlsxwriter

def format_semester_name(current_semester: tuple) -> str:
	(semester, year1, year2) = current_semester
	if year1 >= 2014:
		return f'{year1}-{year2} Academic Year - {semester}'
	else:
		return f'{year1}-{year2} {semester}'

def get_current_semester() -> tuple:
	now = datetime.now()
	year = now.year
	month = now.month
	if 9 <= month <= 12:
		semester = 'Fall Semester'
		year1 = year
		year2 = year + 1
	elif 1 <= month <= 5:
		semester = 'Spring Semester'
		year1 = year - 1
		year2 = year
	elif 6 <= month <= 7:
		semester = 'Summer Session'
		year1 = year - 1
		year2 = year
	# Intersessions need to be accounted for.
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

def launch_search(semester_name: str) -> bool:
	semester_menu = Select(driver.find_element_by_id('pg0_V_ddlTerm'))
	semester_menu.select_by_visible_text(semester_name)
	try:
		faculty_menu = Select(driver.find_element_by_id('pg0_V_ddlFaculty'))
		faculty_menu.select_by_visible_text(PROF)
	except:
		print("Couldn't find professor -- moving on.")
		return False
	driver.find_element_by_id('pg0_V_btnSearch').click()
	return True

def scrape_classes() -> list:
	semester_classes = []
	i = 1
	while True:
		try:
			semester_classes.append(driver.find_element_by_id(f'pg0_V_dgCourses_sec2_row{i}_lnkCourse').text)
			i += 2
		except:
			print("Couldn't find section.")  # this is printed way too many times
			return semester_classes

def return_to_search():
	driver.find_element_by_link_text('Search Again').click()
	driver.implicitly_wait(2)

def get_sheet_name(semester: str) -> str:
	elts = semester.split(' ')
	return elts[0] + elts[-2]

def write_to_output_file(semester: str, classes: list):
	opf = xlsxwriter.Workbook(OP_FILE)
	for (semester, sections) in classes:
		row = 0
		sheet = opf.add_worksheet(get_sheet_name(semester))
		for sec in (sections):
			sheet.write(row, 0, sec)
			row += 1
	opf.close()
			
def main():
	login()
	navigate_to_search()
	current_semester = get_current_semester()
	semester_name = format_semester_name(current_semester)
	classes = []
	while semester_name != FIRST_RECORDED_SEMESTER:
		carryon = launch_search(semester_name)
		if carryon:
			semester_classes = scrape_classes()
			classes.append((semester_name, semester_classes))
			return_to_search()
		current_semester = get_previous_semester(current_semester)
		semester_name = format_semester_name(current_semester)
	write_to_output_file(semester_name, classes)

if __name__ == '__main__':
	global driver
	driver = webdriver.Chrome(WEBDRIVER_PATH)
	driver.get(SITE_URL)
	main()
	driver.close()
	print("Done, check output file in this directory")
