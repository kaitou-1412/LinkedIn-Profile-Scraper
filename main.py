from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import parameters
import time


driver = webdriver.Chrome(parameters.chrome_path)
driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)

driver.get(parameters.linkedin_profile)
driver.implicitly_wait(1)
soup = BeautifulSoup(driver.page_source, 'lxml')

profile_link = (driver.current_url)
name_div = soup.find('div', {'class': 'display-flex justify-space-between pt2'})

try:
    name = name_div.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
except IndexError: # To ignore any kind of error
    name = 'NULL'
except AttributeError:
    name = 'NULL'

try:
    title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
except IndexError:
    title = 'NULL'
except AttributeError:
    title = 'NULL'

driver.execute_script(
    "(function(){try{for(i in document.getElementsByTagName('a')){let el = document.getElementsByTagName('a')[i]; "
    "if(el.innerHTML.includes('Contact info')){el.click();}}}catch(e){}})()")

# Wait 5 seconds for the page to load
time.sleep(5)

# Scrape the email address from the 'Contact info' popup
email = driver.execute_script(
    "return (function(){try{for (i in document.getElementsByClassName('pv-contact-info__contact-type')){ let el = "
    "document.getElementsByClassName('pv-contact-info__contact-type')[i]; if(el.className.includes('ci-email')){ "
    "return el.children[2].children[0].innerText; } }} catch(e){return '';}})()")

print(profile_link)
print(name)
print(title)
print(email)