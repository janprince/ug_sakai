from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



class Sakai:

    def __init__(self):
        self.authenticated = False
        # option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        self.driver = webdriver.Edge()

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
            course_elements = div_sem.find_elements(by=By.CLASS_NAME, value="fav-title")

            course_titles = [title.text for title in course_elements]
            return course_titles
        else:
            print("Please Authenticate by logging in.")

    def get_assignments(self, course_elements):
        """
        :param course_elements: a list of <div class="fav-title"> elements containing links to individual course pages
        :return:
        """

        # link to individual course pages
        course_link = course_elements[0].find_element(by=By.TAG_NAME, value='a')
        course_link.send_keys(Keys.RETURN)


    def sync_assignments(self):
        """
        syncs assignment deadlines with calendar
        :return:
        """
        pass


student_id = input("Student_Id: ")
student_pin = input("Password: ")
f = Sakai()
f.login(student_id, student_pin)

# # List of courses for this semester
courses = f.get_courses()
for i in courses: print(i)