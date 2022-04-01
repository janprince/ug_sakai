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
stud_pin.send_keys("81364")
submit.send_keys(Keys.RETURN)

assert "Your credentials were incorrect." not in driver.page_source

# click the view_all_sites btn
all_sites_btn = driver.find_element(by=By.ID, value="viewAllSites")
all_sites_btn.send_keys(Keys.RETURN)

# get the div containing this semester's courses
div_sem = driver.find_element(by=By.CLASS_NAME, value="fav-sites-term")    # the first div with class= "fav-sites-term"
course_elements = div_sem.find_elements(by=By.CLASS_NAME, value="fav-title")   #

# link to individual course pages
course_link = course_elements[5].find_element(by=By.TAG_NAME, value='a')
course_link.send_keys(Keys.RETURN)



# get all the links of the options on the nav menu
nav_item_links = driver.find_elements(by=By.CLASS_NAME, value="Mrphs-toolsNav__menuitem--link ")

# filter for link containing the text: "Assignments"
assignment_link = [link for link in nav_item_links if link.text == "Assignments"]
assignment_link[0].send_keys(Keys.RETURN)

# get the assignments table
assignment_table = driver.find_element(by=By.CLASS_NAME, value="table")

# extract data from the table
assignment_table_rows = assignment_table.find_elements(by=By.TAG_NAME, value="tr")

data = [
    
]


for row in assignment_table_rows:
    if assignment_table_rows.index(row) == 0:
        # table header cells
        cells = row.find_elements(by=By.TAG_NAME, value="th")
    else:
        # table data cells
        cells = row.find_elements(by=By.TAG_NAME, value="td")

    row_data = []
    for cell_data in cells[1:]:
        row_data.append(cell_data.text)

    data.append(row_data)

print(data)

