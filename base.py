from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
from parsel import Selector

# List where we gonna store all our output
import parameters

companies = []
locations = []
names = []
jobs = []
colleges = []

# Function call extracting title and linkedin profile iteratively
def find_profiles():
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            # add a 5 second pause loading each URL
            sleep(5)
            driver.get(link['href'])
            sleep(15)
            sel = Selector(text=driver.page_source)
            header0 = sel.xpath("//div[@class='flex-1 mr5']/ul/li[1]/text()").extract()
            full_name = header0[0].strip()
            print(full_name)
            location = header0[1].strip()
            print(location)
            sleep(15)
            header1 = sel.xpath("//div[@class='flex-1 mr5']/h2/text()").extract()
            job_title = header1[0].strip()
            sleep(15)
            header = sel.xpath(
                "//span[@class='text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view']/text()").extract()
            college = header[1].split('\n\n')[0]
            print(college)
            if college:
                college = college.strip()
            company_one = header[0]
            print(company_one)
            if company_one:
                company_one = company_one.strip()
            sleep(15)
            title = None
            title = r.find('h3')

            # returns True if a specified object is of a specified type; Tag in this instance
            if isinstance(title, Tag):
                title = title.get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '':
                links.append(link['href'])
                titles.append(title)
                colleges.append(college)
                companies.append(company_one)
                names.append(full_name)
                locations.append(location)
                jobs.append(job_title)

        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue


# This function iteratively clicks on the "Next" button at the bottom right of the search page.
def profiles_loop():
    find_profiles()
    # next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
    # next_button.click()


def repeat_fun(times, f):
    for i in range(times): f()


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/usr/bin/chromedriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')
sleep(10)
# locate email form by_class_name
username = driver.find_element_by_id('session_key')

# send_keys() to simulate key strokes
username.send_keys(parameters.key)
sleep(5)

# locate password form by_class_name
password = driver.find_element_by_id('session_password')

# send_keys() to simulate key strokes
password.send_keys(parameters.password)
sleep(5)

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
log_in_button.click()
sleep(5)

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(5)

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys('site:linkedin.com/in/ AND "full stack developer" AND "Tunis"')
sleep(15)
# .send_keys() to simulate the return key
search_query.send_keys(Keys.RETURN)
sleep(5)
soup = BeautifulSoup(driver.page_source, 'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})
# initialize empty lists
links = []
titles = []

# Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like.
repeat_fun(1, profiles_loop)

from itertools import zip_longest

# Load titles and links data into csv
d = [names, links, jobs, companies, colleges, locations]
export_data = zip_longest(*d, fillvalue='')
with open('results_file.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("Names", "Links", "Title", "Company", "College", "Locations"))
    wr.writerows(export_data)
myfile.close()
