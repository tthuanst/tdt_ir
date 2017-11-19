#!/usr/bin/env python
import os,sys
import stokenize #Phi
import indexing #Hieu
import searching #Thuan
import correction #aDai + Thanh

def main():
    ids = []
    print("Information Retrieval")
    if os.path.exists("vob.npy") and os.path.exists("data.npy"):
        #Load indexed data
        while(1):
            text = raw_input("Search what: ")
            text = correction(text)
            for w in stokenize(text):
                ids.append(hashing(w))
            print(searching(ids))
    else:
        #Indexing data: vob.npy + data.npy
        indexing(collections="collections")


#For run python from html
#https://stackoverflow.com/questions/42262366/how-to-run-a-python-script-from-html
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/html')
def index():
    # render your html template
    return render_template('example.html')

@app.route('/')
def click():
    print("Do searching")
    #search()

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        app.run()
    else:
        main()