from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
from parsel import Selector

# Function call extracting title and linkedin profile iteratively
def find_profiles():
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            print("aaaaaaaaaaaaaa")
            print(link['href'])

            # add a 5 second pause loading each URL
            sleep(5)
            driver.get(link['href'])
            print('oui')
            sleep(5)
            sel = Selector(text=driver.page_source)
            header = sel.xpath("//span[@class='text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view']/text()").extract()
            college = header[1].split('\n\n')[0]
            company_one = header[0]
            print(college)
            if college:
                college = college.strip()
            title = None
            title = r.find('h3')

            # returns True if a specified object is of a specified type; Tag in this instance
            if isinstance(title, Tag):
                title = title.get_text()

            description = None
            description = r.find('span', attrs={'class': 'st'})

            if isinstance(description, Tag):
                description = description.get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
                colleges.append(college)

                print(colleges)
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue


# This function iteratively clicks on the "Next" button at the bottom right of the search page.
def profiles_loop():
    find_profiles()

    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
    next_button.click()


def repeat_fun(times, f):
    for i in range(times): f()


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/usr/bin/chromedriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_id('session_key')

# send_keys() to simulate key strokes
username.send_keys('medicochurirgical123@gmail.com')
sleep(0.5)

# locate password form by_class_name
password = driver.find_element_by_id('session_password')

# send_keys() to simulate key strokes
password.send_keys('khaoula1997')
sleep(0.5)

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
log_in_button.click()
sleep(0.5)

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(3)

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys('site:linkedin.com/in/ AND "full stack developer" AND "Tunis"')

# .send_keys() to simulate the return key
search_query.send_keys(Keys.RETURN)

soup = BeautifulSoup(driver.page_source, 'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})
# initialize empty lists
links = []
titles = []
descriptions = []
colleges = []
# Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like.
repeat_fun(1, profiles_loop)

print(titles)
print(links)

# Separates out just the First/Last Names for the titles variable
name = []
job = []
company = []
for i in titles:
    slots = i.split(' - ')
    print(len(slots))
    if len(slots) == 3:
        name.append(i.split('-', 10)[0])
        job.append(i.split('-', 10)[1])
        company.append(i.split('-', 10)[2])
    elif len(slots) != 3:
        name.append(i.split('-', 10)[0])
        job.append(i.split('-', 10)[1])
        company.append(None)
# The function below stores scraped data into a .csv file
from itertools import zip_longest

# Load titles and links data into csv
d = [name, links, job, company, colleges]
export_data = zip_longest(*d, fillvalue='')
with open('results_file.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("Titles", "Links", "Current_Job", "Job", "college"))
    wr.writerows(export_data)
myfile.close()
