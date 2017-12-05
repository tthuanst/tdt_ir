#!/usr/bin/env python

#
# Author: Thuan, Hieu, Thanh, Phi, Dai, Thuy
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#
import os,sys
import numpy as np
from stokenize import stokenize #Author: Phi
from indexing import inverted_index #Author: Hieu
from searching import simple_search #Author: Thuan
from correction import correction #Author: aDai + Thanh

def main():
    ids = []
    print("Information Retrieval")
    if not os.path.exists('index.npy'):
        indexed_data = inverted_index.indexing_basic('/home/tdt/MaxEnt_POS/Trainset/')
        np.save('index.npy',indexed_data)
    else:
        indexed_data = np.load('index.npy').item()
    while(1):
        text = raw_input("Search what: ")
        #text = correction(text)
        #for w in stokenize.stokenize(text):
        #    ids.append(inverted_index.hashing(w))
        print(">>> Result: %s"%simple_search.search(text,indexed_data))


#For run python from html
#https://www.tutorialspoint.com/flask/flask_http_methods.htm
from flask import Flask, render_template, request, redirect, url_for
import webbrowser as wb

app = Flask(__name__)

@app.route('/search_result/<input>')
def search_result(input):
    global indexed_data
    ids = []
    for w in stokenize.stokenize(input):
        ids.append(inverted_index.hashing(w))
    result = "Result:"+"<br>"
    for i in simple_search.search(ids,indexed_data):
        print(i)
        result = result+str(i)+"<br>"
    return result

@app.route('/search',methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        text = request.form['input']
        return redirect(url_for('search_result',input = text))
    else:
        text = request.args.get('input')
        return redirect(url_for('search_result',input = text))

@app.route('/')
def index():
   return render_template('index.html')


if __name__ == '__main__':
    #For test with browser: ./ir_main.py server
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        if not os.path.exists('index.npy'):
            iindexed_data = indexing('/home/tdt/MaxEnt_POS/Trainset/')
            np.save('index.npy',indexed_data)
        else:
            indexed_data = np.load('index.npy').item()
        wb.open("http://127.0.0.1:5000/")
        app.run(debug = True)
    else:
        #For test with console: ./ir_main.py
        main()