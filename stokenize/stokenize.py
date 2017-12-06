#!/usr/bin/env python

#
# Author: Thanh
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

def stokenize(sentence):
    #return sentence.split()
    return nltk.word_tokenize(sentence)

def stokenize_stop(sentence):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    list_of_words = [i.lower() for i in wordpunct_tokenize(sentence) if i.lower() not in stop_words]
    return list_of_words

if __name__ == '__main__':
    #For test: ./stokenize.py
    while(1):
        sentence = raw_input("Input a sentence: ")
        print("Stokenize normally: %s"%stokenize(sentence))
        print("Stokenize remove stopwords: %s"%stokenize_stop(sentence))