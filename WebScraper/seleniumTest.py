#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File:          aholefinder.py                                                                   #
# Author:        James Robinson                                                                   #
# Purpose:       Alternative data gathering technique using selenium to increase collection rate #
# Last Modified: 01/10/2024                                                                       #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Configure driver to run headless
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


homeLink = 'https://www.reddit.com/r/AmItheAsshole/'
divs = driver.find_elements(By.TAG_NAME, 'div')
print (divs)


def AnalyzePost(postlink):
    driver.get(postlink)
    ps = driver.find_elements(By.TAG_NAME, 'p')
    for p in ps:
        print(p.text)
#Main
AnalyzePost('https://www.reddit.com/r/AmItheAsshole/')

driver.quit()

#document.querySelector("#t3_19c7cei > div._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3._1Qs6zz6oqdrQbR7yE_ntfY > div.STit0dLageRsa2yR4te_b > a")
