import pickle
#import scipy
#import sklearn
import re
import torch
#import nltk
#nltk.download('stopwords')
#nltk.download('stem')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from flask import Flask
from flask import request

app = Flask(__name__)

vectorizer = pickle.load(open('vectorizer2.pkl', 'rb'))
ps = PorterStemmer()

@app.route('/')
def vectorize():
    input = request.args.get('input')
    input = re.sub('[^a-zA-Z]', ' ', input)
    input = input.lower()
    input = input.split()
    input = [ps.stem(word) for word in input if not word in set(stopwords.words('english'))]
    input = ' '.join(input)
    return torch.from_numpy(vectorizer.transform([input]).toarray()).float()
