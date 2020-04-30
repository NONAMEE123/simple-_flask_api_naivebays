from flask import Flask
from flask import request
from flask import Response
from flask import json
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import collections
from nltk.metrics.scores import f_measure
import simplejson as json
from flask import Flask,jsonify,request
from flask_restful import Resource,Api



app = Flask(__name__)
#initialize Restful_API
api = Api(app)
class classification_sentiment(Resource):
    def get(self,text:str):
        data = {
            'Text'  : text,
            'Sentiment' : find_sentiment(text),
            'Score': find_scores()
            }
        #serialisation data    
        js = json.dumps(data,ensure_ascii=False)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
	
def find_sentiment(text):
    #Text formatting to classify
    def format_text(text):
        return({word: True for word in nltk.word_tokenize(text)})
    #Load positive categorized text
    pos = []
    with open("./pos.txt", encoding='ISO-8859-1') as f:
        for i in f:
            pos.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'positive'])
    #Load negative categorized text
    neg = []
    with open("./neg.txt", encoding='ISO-8859-1') as f:
        for i in f:
            neg.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'negative'])

    neu = []
    with open("./neu.txt", encoding='ISO-8859-1') as f:
        for i in f:
            neu.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'neutre'])        
    #Training classifier
    training_set = pos + neg + neu
    classifier = NaiveBayesClassifier.train(training_set)
    return classifier.classify(format_text(text))

def find_scores():
    #Text formatting to classify 
    def format_text(text):
        return({word: True for word in nltk.word_tokenize(text)})
    #Load positive categorized text	
    pos = []
    with open("./pos.txt", encoding='ISO-8859-1') as f:
        for i in f: 
            pos.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'positive'])
    #Load negative categorized text
    neg = []
    with open("./neg.txt", encoding='ISO-8859-1') as f:
        for i in f: 
            neg.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'negative'])
    #Load negative categorized text        
    neu = []
    with open("./neu.txt", encoding='ISO-8859-1') as f:
        for i in f: 
            neu.append([format_text(i.encode("utf-8").decode("unicode-escape")), 'neutre'])
    #Split data into training(80%) and testing(20%) sets 
    training_set = pos[:int((.80)*len(pos))] + neg[:int((.80)*len(neg))] + neu[:int((.80)*len(neu))]
    test_set = pos[int((.80)*len(pos)):] + neg[int((.80)*len(neg)):] + neu[int((.80)*len(neu)):]
    #Training classifier    
    classifier = NaiveBayesClassifier.train(training_set)   
    #Calculate scores	
    trueset = collections.defaultdict(set)
    testset = collections.defaultdict(set)
    #Test all test-set items using defined classifier
    for i, (text, label) in enumerate(test_set):
        trueset[label].add(i)
        result = classifier.classify(text)
        testset[result].add(i)
        #accurays
    return accuracy(classifier, test_set), f_measure(trueset['positive'], testset['negative']), f_measure(testset['negative'], trueset['positive']), f_measure(testset['neutre'], trueset['positive']), f_measure(testset['positive'], trueset['neutre']), f_measure(testset['negative'], trueset['neutre']), f_measure(testset['neutre'], trueset['negative'])    
	
#api Resources adding
api.add_resource(classification_sentiment,'/sentiment_analysis/<string:text>')

if __name__ == "__main__":
    app.run(debug=True)

