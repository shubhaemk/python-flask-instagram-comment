
import os
import sys
import time
import json
import requests
import argparse
import io
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize import word_tokenize

positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ]
neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]

def word_feats(words):
    return dict([(word, True) for word in words])

def main(comments):

        corpus = []
        # To clean Comments
        for dataComment in comments:

            # column : "comment", row ith
            comment = re.sub('[^a-zA-Z]', ' ', dataComment)

            # convert all cases to lower cases
            comment = comment.lower()

            # split to array(default delimiter is " ")
            comment = comment.split()

            # creating PorterStemmer object to
            # take main stem of each word
            ps = PorterStemmer()

            # loop for stemming each word
            # in string array at ith row
            comment = [ps.stem(word) for word in comment
                        if not word in set(stopwords.words('english'))]

            # rejoin all string array elements
            # to create back into a string
            comment = ' '.join(comment)

            # append each string to create
            # array of clean text
            corpus.append(comment)

        positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
        negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
        neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

        train_set = negative_features + positive_features + neutral_features

        classifier = NaiveBayesClassifier.train(train_set)

        neg = 0
        pos = 0
        neu = 0

        words = word_tokenize(str(corpus))
        for word in words:
            classResult = classifier.classify( word_feats(word))
            if classResult == 'neg':
                neg = neg + 1
            if classResult == 'pos':
                pos = pos + 1
            if classResult == 'neu':
                neu = neu + 1

        pos=float(pos)/len(words)
        neg=float(neg)/len(words)
        neu=float(neu)/len(words)
        print('Positive: ' + str(pos) + 'Negative: ' + str(neg) + 'Neutral: ' + str(neu))

if __name__ == "__main__":
    data=json.loads(sys.argv[1])
    comments=[]
    for comment in data['comments']:
        comments.append(comment['text'])
    main(comments)
