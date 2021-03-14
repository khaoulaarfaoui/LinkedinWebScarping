from time import sleep

from selenium import webdriver
import csv
from parsel import Selector

# defining new variable passing two parameters
import parameters


driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys('medicochurirgical123@gmail.com')
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys('khaoula1997')
sleep(0.5)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)
driver.get('https://www.google.com')
sleep(3)
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "python developer" AND "London"')
from selenium.webdriver.common.keys import Keys

sleep(0.5)
search_query.send_keys(Keys.RETURN)
linkedin_urls = driver.find_elements_by_class_name('iUh30')
linkedin_urls = [url.text for url in linkedin_urls]
sleep(3)

