from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pprint
import getpass

class Sakai:

    def __init__(self):
        self.authenticated = False
        self.course_elements = []

        # Edge
        self.driver = webdriver.Edge("drivers/msedgedriver.exe")

        # Chrome
        # self.driver = webdriver.Edge("drivers/chromedriver.exe") #

        # open the portal
        self.driver.get("https://sakai.ug.edu.gh")

    def login(self, id, pin):
        """
        :param id: student id
        :param pin: student pin
        :return: logs into the student's sakai account
        """

        # get input fields
        stud_id_input = self.driver.find_element(by=By.NAME, value="eid")
        stud_pin_input = self.driver.find_element(by=By.NAME, value="pw")
        submit = self.driver.find_element(by=By.NAME, value='submit')

        # login
        stud_id_input.clear()
        stud_id_input.send_keys(str(id))

        stud_pin_input.clear()
        stud_pin_input.send_keys(str(pin))

        submit.send_keys(Keys.RETURN)

        # confirm successful login
        try:
            assert "Your credentials were incorrect." not in self.driver.page_source
            self.authenticated = True
        except AssertionError:
            print("Invalid credentials.")
            self.authenticated = False
            self.driver.close()

    def get_courses(self):
        """
        :return: a list of current courses if and only if authenticated
        """
        if self.authenticated:
            # click the view_all_sites btn
            all_sites_btn = self.driver.find_element(by=By.ID, value="viewAllSites")
            all_sites_btn.send_keys(Keys.RETURN)

            # get the div containing this semester's courses
            div_sem = self.driver.find_element(by=By.CLASS_NAME, value="fav-sites-term")
            self.course_elements = div_sem.find_elements(by=By.CLASS_NAME, value="fav-title")

            course_titles = [title.text for title in self.course_elements]
            return course_titles
        else:
            print("Please Authenticate by logging in.")

    def get_assignments(self):
        """
        :param course_elements: a list of <div class="fav-title"> elements containing links to individual course pages
        :return:
        """

        # get courses
        self.get_courses()

        assignments = {}

        for i in range(len(self.course_elements)):
            course = self.course_elements[i]

            # course_title
            course_title = course.text

            # link to individual course pages
            course_link = course.find_element(by=By.TAG_NAME, value='a')
            course_link.send_keys(Keys.RETURN)

            # get all the links of the options on the nav menu
            nav_item_links = self.driver.find_elements(by=By.CLASS_NAME, value="Mrphs-toolsNav__menuitem--link ")

            # filter for link containing the text: "Assignments"
            assignment_link = [link for link in nav_item_links if link.text == "Assignments"]
            assignment_link[0].send_keys(Keys.RETURN)

            # confirm existence of assignments
            try:
                assert "There are currently no assignments at this location." not in self.driver.page_source
            except AssertionError:
                assignments[course_title] = "There are currently no assignments."
                if i != len(self.course_elements) - 1:
                    self.get_courses()
                continue

            # get the assignments table
            assignment_table = self.driver.find_element(by=By.CLASS_NAME, value="table")

            # extract all rows from the table
            assignment_table_rows = assignment_table.find_elements(by=By.TAG_NAME, value="tr")

            data = []

            # extracting data from rows
            for row in assignment_table_rows:
                if assignment_table_rows.index(row) == 0:
                    # table header cells
                    cells = row.find_elements(by=By.TAG_NAME, value="th")
                else:
                    # table data cells
                    cells = row.find_elements(by=By.TAG_NAME, value="td")

                row_data = []
                # data from cells
                for cell_data in cells[1:]:
                    row_data.append(cell_data.text)

                data.append(row_data)


            assignments[course_title] = data

            if i != len(self.course_elements) - 1:
                self.get_courses()


        return assignments


    def sync_assignments(self):
        """
        syncs assignment deadlines with calendar
        :return:
        """
        pass


student_id = input("Student_Id: ")
# student_pin = getpass.getpass("Password: ", stream=None) # hides password when typing
student_pin = input("Password: ")
f = Sakai()
f.login(student_id, student_pin)

# # List of courses for this semester
assignments = f.get_assignments()
pprint.pprint(assignments)
