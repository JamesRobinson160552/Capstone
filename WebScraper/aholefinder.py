#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File:          aholefinder.py                                                                   #
# Author:        James Robinson                                                                   #
# Purpose:       Collect data from the subreddit r/AmItheAsshole to train a classifier.           #
# Last Modified: 11/29/2023                                                                       #
# TODO: Get more than 25 posts at a time? Deal with edge cases :(                                 #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Error Jail                                                                                                              #
# Traceback (most recent call last):                                                                                      #
#  File "c:\Users\james\Downloads\Projects\Scraper\WebScraper\AITA\aholefinder.py", line 57, in analyze_post              #
#    filename = datetime.today().strftime('%Y-%m-%d') + '.json'                                                           #
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                  #
#  File "C:\Users\james\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1252.py", line 19, in encode              #
#    return codecs.charmap_encode(input,self.errors,encoding_table)[0]                                                    #
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                       #
# UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f480' in position 2422: character maps to <undefined> #
# -its a skull emoji
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#imports-------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup #To parse HTML
import requests #To get HTML
from datetime import datetime #To get date for file naming
import traceback #To debug better
from selenium import webdriver #To run chrome
from selenium.webdriver.common.by import By #To gather post URLs
import time #To wait
import random #To confuse the narcs

#Setup---------------------------------------------------------------------------------------------


#Ensures text pulled from posts is compatible with JSON
def clean_text(text):
    """Adds escape characters to double quotes.
    Removes leading and trailing whitespace."""
    clean_text = text.strip()
    clean_text = clean_text.replace('"', '\\"')
    return clean_text

#Analyze Post Function-----------------------------------------------------------------------------
def analyze_post(post_link):
    """Navigate to a specific post by link.
    Get the title, post body, and public decision.
    Store the above in a json file."""

    #Get post
    post = requests.get(post_link)
    postsoup = BeautifulSoup(post.text, 'lxml')

    #Parse for relevant data
    try:
        title = clean_text(postsoup.find('h1').text)
        paragraphs = postsoup.find_all('p')
        body = ""
        for paragraph in paragraphs[1:]:
            body += clean_text(paragraph.text)
        decision = clean_text(postsoup.find('shreddit-post-flair').text)
        if (decision == ''): #Skip posts with no decision
            return
    except:
        print ("Issue with post: " + post_link)

    #Store results in a JSON file
    #print (title)
    #print (body)
    print (decision)
    WriteToFile(title, body, decision)

#Write To File Function---------------------------------------------------------------------------
def WriteToFile(title, body, decision):
    """Writes a post's data as a json entry in today's file."""
    filename = datetime.today().strftime('%Y-%m-%d') + '.json'
    with open('./data/' + filename, 'a') as f:
        try:
            f.write("\n{\n\t\"title\" : \"" + title + "\",")
            f.write("\n\t\"body\" : \"" + body + "\",")
            if ('\U0001f4a9' in decision): #This handles decisions of 'Poo Mode' which include an unreadable character (poo emoji)
                decision = 'POO Mode'
            f.write("\n\t\"decision\" : \"" + decision + "\",")
            f.write("\n\t\"valid\" : \"true\" \n},")
        except: #This takes care of crash-causing edge cases, mostly unencodable chars atm
            f.write("\n\t\"valid\" : \"false\" \n},") #Since exceptions occur in the body typically, this maintains the JSON file format
            print("")
            traceback.print_exc()
            print("")

def GetPosts(driver, category, timeFrame):
    homeLink = 'https://old.reddit.com/r/AmItheAsshole/?sort='+category+'&t='+timeFrame
    driver.get(homeLink)
    nextPageButton = driver.find_element(By.CLASS_NAME, 'next-button')
    while (nextPageButton):
        nextPageButton = driver.find_element(By.CLASS_NAME, 'next-button')
        divs = driver.find_elements(By.CLASS_NAME, 'thing')
        for div in divs:
            isAnAdd = ('user' in div.get_attribute('data-permalink'))
            if (isAnAdd):
                print("Skipping add")
                break
            analyze_post('https://www.reddit.com' + (div.get_attribute('data-permalink')))
        nextPageButton.click()
        time.sleep(random.randrange(1, 50)/10)

#Main----------------------------------------------------------------------------------------------
filename = datetime.today().strftime('%Y-%m-%d') + '.json'
f = open('./data/' + filename, 'w')
with open('./data/' + filename, 'w') as f:
    f.write("[")

driver = webdriver.Chrome()
GetPosts(driver, 'top', 'all')
driver.quit()

with open('./data/' + filename, 'a') as f:
    f.write("\n]\n")
