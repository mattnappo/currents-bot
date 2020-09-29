from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

# The currents url. This link is prompted with an email textbox
url = 'https://currents.google.com/u/1/communities/112231973545069490014?hl=en'

with open('creds.json') as f:
    creds = json.load(f)
    username = creds['username']
    password = creds['password']

driver = webdriver.Firefox()
driver.get(url)

email_box = driver.find_element_by_name('identifier')
email_box.send_keys(username)

next_button = driver.find_element_by_xpath("//*[@id='identifierNext']/div")
next_button.click()

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))

    password_box = driver.find_element_by_name('password')

    password_box.send_keys(password)
    password_box.send_keys(Keys.RETURN)

except TimeoutException as e:
    print(e)
