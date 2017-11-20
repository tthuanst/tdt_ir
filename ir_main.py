#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#
import os,sys
from stokenize import stokenize #Author: Phi
from indexing import inverted_index #Author: Hieu
from searching import simple_search #Author: Thuan
from correction import correction #Author: aDai + Thanh

def main():
    ids = []
    print("Information Retrieval")
    indexed_data = inverted_index.indexing(collections="collections")
    print indexed_data
    while(1):
        #text = raw_input("Search what: ")
        #text = correction(text)
        #for w in stokenize(text):
        #    ids.append(hashing(w))
        ids = [1,2]
        print(simple_search.search(ids,indexed_data))
        sys.exit(0)


#For run python from html
#https://stackoverflow.com/questions/42262366/how-to-run-a-python-script-from-html
#http://pwp.stevecassidy.net/bottle/forms-processing.html
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/html')
def index():
    # render your html template
    return render_template('index.html')

@app.route('/')
def formhandler():
    print("Result")
    print(simple_search.search(ids,indexed_data))

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        app.run()
    else:
        main()