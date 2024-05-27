#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File:          aholefinder.py                                                                   #
# Author:        James Robinson                                                                   #
# Purpose:       Collect data from the subreddit r/AmItheAsshole to train a classifier.           #
# Last Modified: 01/25/2024                                                                       #
# TODO:          Make it cloud-based                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#imports-------------------------------------------------------------------------------------------
from selenium import webdriver #To run chrome
from selenium.webdriver.common.by import By #To gather post URLs

from bs4 import BeautifulSoup #To parse HTML
from datetime import datetime #To get date for file naming

import requests #To get HTML
import traceback #To debug better
import time #To wait
import random #To randomize wait times

import re #To remove emojis

def GetPosts(driver: webdriver, community: str, category: str, timeFrame: str) -> None:
    """Uses Selenium Werbdriver to gather post URLs and pass them to AnalyzePost"""
    jsonFile = OpenFile(community, category, timeFrame)
    homeLink = 'https://old.reddit.com/r/'+community+'/'+category+'/?sort='+category+'&t='+timeFrame
    driver.get(homeLink)
    numPosts, numPages = 0, 0

    nextPageButton = driver.find_element(By.CLASS_NAME, 'next-button')
    while (nextPageButton):
        #Get all posts on this page, go to the next page
        numPages += 1
        print ("\nPage " + str(numPages) + ":\n")
        posts = driver.find_elements(By.CLASS_NAME, 'thing')
        for post in posts:
            numPosts += 1
            print ("Post " + str(numPosts))
            postURL = 'https://www.reddit.com' + (post.get_attribute('data-permalink'))
            AnalyzePost(postURL, jsonFile)     
        nextPageButton = GetNextPage(driver, nextPageButton)
        

def GetNextPage(driver: webdriver, nextPageButton: webdriver) -> webdriver: #WebElement
    """Navigates the driver to the next page.
    Returns the new next page button.
    Waits a random amount of time between pages."""
    nextPageButton.click()
    time.sleep(random.randrange(1, 50)/10)
    try:
        nextPageButton = driver.find_element(By.CLASS_NAME, 'next-button')
    except:
        nextPageButton = None #End of pages, ~40
    return nextPageButton

def AnalyzePost(postLink: str, filename: str) -> None:
    """Navigate to a specific post by URL.
    Return the post's title, body, and decision."""
    post = requests.get(postLink)
    postSoup = BeautifulSoup(post.text, 'lxml')

    #Parse for relevant data
    try:
        title = cleanText(postSoup.find('h1').text)
        paragraphs = postSoup.find_all('p')
        body = ""
        for paragraph in paragraphs[1:]:
            body += cleanText(paragraph.text)
        decision = cleanText(postSoup.find('shreddit-post-flair').text)
        print (decision)
        if (decision == ''): #Skip posts with no decision
            return
    except:
        #Write error to error log file and continue
        with open ('./errors/' + filename + '.txt', 'a') as e:
            e.write(traceback.format_exc())
        return
    WriteToFile(title, body, decision, filename)

def cleanText(text: str) -> str:
    """Adds escape characters to double quotes.
    Removes leading and trailing whitespace.
    Removes emojis."""
    cleanText = text.strip()
    cleanText = cleanText.replace('"', '\\"')

    #Removes emojis based on their python encoding, will add more as they come up
    emojiPattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # Emoticons
            u"\U0001F300-\U0001F5FF"  # Symbols and Pictographs
            u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
            u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\u20A0-\u20CF"          # Currency Symbols
            u"\u2060"                 # Word Joiner
                            "]+", flags=re.UNICODE)
    cleanText = (emojiPattern.sub(r'', cleanText))

    return cleanText

def WriteToFile(title: str, body: str, decision: str, filename: str) -> None:
    """Writes a post's data as a json entry in the proper file."""
    with open('./data/' + filename, 'a') as f:
        try:
            #Write post data to file as a new json entry
            f.write("\n{\n\t\"title\" : \"" + title + "\",")
            f.write("\n\t\"body\" : \"" + body + "\",")
            f.write("\n\t\"decision\" : \"" + decision + "\",")
            f.write("\n\t\"valid\" : \"true\" \n},")
        except:
            #Write error to error log file and continue
            f.write("\n\t\"valid\" : \"false\" \n},")
            with open('./errors/' + filename + '.txt', 'a') as e:
                e.write(traceback.format_exc())

def OpenFile(community: str, category: str, timeFrame: str) -> str:
    """Opens a new json file for the given category, timeframe, and today's date."""
    filename = datetime.today().strftime('%Y-%m-%d') + '_' + community + '_' + category + '_' + timeFrame + '.json'
    f = open('./data/' + filename, 'w')
    with open('./data/' + filename, 'w') as f:
        f.write("[")
    return filename

#Main----------------------------------------------------------------------------------------------
driver = webdriver.Chrome()
#GetPosts(driver, 'amitheasshole', 'top', 'all')
#GetPosts(driver, 'amitheasshole', 'controversial', 'all')

#GetPosts(driver, 'amitheasshole', 'top', 'year')
#GetPosts(driver, 'amitheasshole', 'controversial', 'year')

GetPosts(driver, 'amitheasshole', 'top', 'month')
GetPosts(driver, 'amitheasshole', 'controversial', 'month')

GetPosts(driver, 'amitheasshole', 'top', 'week')
GetPosts(driver, 'amitheasshole', 'controversial', 'week')

driver.quit()
