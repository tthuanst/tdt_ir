#!/usr/bin/env python

#
# Author: Thuan, Hieu, Thanh, Phi, Dai, Thuy
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#
import os,sys
import numpy as np
from stokenize import stokenize #Author: Thanh
from indexing import inverted_index #Author: Hieu + Dai
from searching import searching #Author: Thuan
from correction import correction #Author: Phi + Thuy

indexed_data = {}
#For run python from html
#https://www.tutorialspoint.com/flask/flask_http_methods.htm
from flask import Flask, render_template, request, redirect, url_for
import webbrowser as wb

app = Flask(__name__)

@app.route('/search_result/<input>')
def search_result(input):
    global indexed_data
    result = "Result:"+"<br>"
    for i in searching.simple_search(stokenize.stokenize_stop(input),indexed_data):
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


def console(mode):
    while(1):
        query = []
        text = raw_input("Search what: ")
        for w in stokenize.stokenize_stop(text):
            w = correction.correction(w.lower())
            query.append(w)
        if len(query) == 0:
            print("No meaning word to search")
        elif mode == "basic":
            print(">>> Result: %s"%searching.simple_search(query,indexed_data))
        elif mode == "rank":
            print(">>> Result: %s"%searching.rank_search(query,indexed_data))


if __name__ == '__main__':
    try:
        #First argument for mode selection
        mode = sys.argv[1]
    except:
        #Default mode is basic
        mode = "basic"
    try:
        #Second argument for GUI selection
        gui = sys.argv[2]
    except:
        #Default GUI is console
        gui = "console"

    print("Information Retrieval mode=%s, app=%s"%(mode,app))
    #Get current directory path which have this script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path,"collections/ohsumed-all-docs")
    print(data_path)
    if mode == "basic":
        if not os.path.exists('simple_index.npy'):
            indexed_data = inverted_index.indexing_basic(data_path)
            np.save('simple_index.npy',indexed_data)
        else:
            indexed_data = np.load('simple_index.npy').item()
    elif mode == "rank":
        if not os.path.exists('rank_index.npy'):
            indexed_data = inverted_index.indexing_TF_IDF(data_path)
            np.save('rank_index.npy',indexed_data)
        else:
            indexed_data = np.load('rank_index.npy').item()
    else:
        print("Incorrect mode!")

    if gui == "server":
        #For test with browser: ./ir_main.py <mode> server
        #wb.open("http://127.0.0.1:5000/")
        app.run(debug = True)
    elif gui == "console":
        #For test with console: ./ir_main.py <mode> console
        console(mode)
    else:
        print("Incorrect GUI!")
