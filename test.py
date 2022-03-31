from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# sakai url
url = "https://sakai.ug.edu.gh"

driver = webdriver.Edge()
driver.get(url)

# get input fields
stud_id = driver.find_element(by=By.NAME, value="eid")
stud_pin = driver.find_element(by=By.NAME, value="pw")
submit = driver.find_element(by=By.NAME, value='submit')

# login
stud_id.clear()
stud_id.send_keys("10839289")
stud_pin.send_keys("8136")
submit.send_keys(Keys.RETURN)

assert "Your credentials were incorrect." not in driver.page_source

# click the view_all_sites btn
all_sites_btn = driver.find_element(by=By.ID, value="viewAllSites")
all_sites_btn.send_keys(Keys.RETURN)

# get the div containing this semester's courses
div_sem = driver.find_element(by=By.CLASS_NAME, value="fav-sites-term")    # the first div with class= "fav-sites-term"
course_elements = div_sem.find_elements(by=By.CLASS_NAME, value="fav-title")   #

# link to individual course pages
course_link = course_elements[0].find_element(by=By.TAG_NAME, value='a')
course_link.send_keys(Keys.RETURN)
