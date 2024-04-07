Quandary
Created by James Robinson 100160552
For COMP 4983 WI2024
Supervisor Dr. Greg Lee

Quandary is a web scraper, text classifier, API and ubiquitous app based on Reddit's r/AmITheAsshole.

Technologies used are:
* Python
* Selenium
* BeautifulSoup
* NumPy
* Pandas
* NLTK
* SciKit-Learn
* Pytorch
* Flask
* Flutter

With cloud hosting provided by pythonanywhere.com

## Setup
To run the web scraper:
* Navigate to the Webscraper directory
* Install dependencies manually or with 
```sh 
pip install -r requirements.txt
```
* Run aholefinder.py

To build a text classifier model:
* Navigate to the Classifier directory
* Install dependencies manually or with 
```sh 
pip install -r requirements.txt
```
* Open aholeClassifier.ipynb
* Run cells in order, or select "Run All"

The Front End can be run by installing the appropriate version or
```sh 
flutter pub get
flutter run 
```
to run in debug mode

For more information, contact 160552r@acadiau.ca
