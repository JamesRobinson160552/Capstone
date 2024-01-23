#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
homeLink = 'https://old.reddit.com/r/AmItheAsshole/top/?sort=top&t=all'
driver.get(homeLink)

for i in range(5):
    nextPageButton = driver.find_element(By.CLASS_NAME, 'next-button')
    divs = driver.find_elements(By.CLASS_NAME, 'thing')
    for div in divs:
        print (div.get_attribute('data-permalink'))
    nextPageButton.click()

time.sleep(1)

driver.quit()
