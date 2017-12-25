#!/usr/bin/env python

#
# Author: Thuan, Hieu, Thanh, Phi, Dai, Thuy
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#
import os,sys
import subprocess
import numpy as np
from collections import Counter
from datetime import datetime
from stokenize import stokenize #Author: Thanh
from indexing import inverted_index #Author: Hieu + Dai
from searching import searching #Author: Thuan
from correction import correction #Author: Phi + Thuy

data_path = ""
indexed_simple = {}
indexed_rank = {}
#For run python from html
#https://www.tutorialspoint.com/flask/flask_http_methods.htm
from flask import Flask, render_template, request, redirect, url_for
import webbrowser as wb

app = Flask(__name__)

def display_result(input,searchMode):
    global data_path,indexed_simple,indexed_rank
    #Pattern for egrep to show a part of document
    pattern = "\"("
    query = []
    for w in stokenize.stokenize_stop(input):
        w = correction.correction(w.lower())
        query.append(w)
        pattern = pattern+w+"|"
    pattern = pattern[:-1]+")\" "
    #Searching follow searchMode
    time_start = datetime.now()
    if searchMode == "simple":
        docs = searching.simple_search(query,indexed_simple)
    elif searchMode == "rank":
        docs = searching.rank_search(query,indexed_rank)
    #Show corrected sentences which is used to search
    result = "Result simple search for <b><i><font color=\"red\">"+" ".join(query)+"</font></i></b><br>"
    #Show time searching and number of document found
    if "Not found" not in docs:
        found = len(docs)
    else:
        found = 0
    result = result+"Found {0} documents in {1} <br>".format(found,datetime.now()-time_start)
    #Get top 10 highest score
    score = Counter(docs)
    for d in score.most_common(10): #Only show top 10 document
        #For each document, show hyperlink to it and show a part of document
        #TODO: hyperlink to local file cannot click to open
        #Copy link and paste to address bar of browswer to open
        if type(d) is tuple:
            d = d[0]
        if os.path.exists(os.path.join(data_path,d)):
            result = result + "<br><a href=\"file:///{0}/{1}\" target=\"_blank\">{1}</a><br>".format(data_path,d)
            cmd = "/bin/egrep -m 3 -i "+str(pattern)+"\""+str(os.path.join(data_path,d))+"\""
            out = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
            out = out.replace('\n','<br>')
            for w in query:
                out = out.replace(w,"<b>"+w+"</b>")
            result = result+out+"<br>"
        else:
            result = result+"<br>"+"<b>"+d+"</b><br>"
    return result

@app.route('/search_simple/<input>')
def search_simple(input):
    return display_result(input,"simple")

@app.route('/search_rank/<input>')
def search_rank(input):
    return display_result(input,"rank")

@app.route('/search',methods = ['POST'])
def search():
    if request.form['submit'] == "Simple search":
        #Handle simple search button
        text = request.form['input']
        print("Simple search: %s"%text)
        return redirect(url_for('search_simple',input = text))
    if request.form['submit'] == "Rank search":
        #Handle rank search button
        text = request.form['input']
        print("Rank search: %s"%text)
        return redirect(url_for('search_rank',input = text))

@app.route('/')
def index():
    #The first page of searching for query input
    return render_template('index.html')

#################################################
def console():
    #Console mode (to debug) can load 10 result per time
    global indexed_simple,indexed_rank
    while(1):
        query = []
        text = raw_input("Search what: ")
        for w in stokenize.stokenize_stop(text):
            #Correct each word in query
            w = correction.correction(w.lower())
            query.append(w)
        if len(query) == 0:
            #All words in query are stop words
            print("No meaning word to search")
        else:
            #Print corrected sentence then search result
            print("Searching \"%s\" ..."%(" ".join(query)))
            time_start = datetime.now()
            docs = searching.simple_search(query,indexed_simple)
            #Show time searching and number of document found
            if "Not found" not in docs:
                found = len(docs)
            else:
                found = 0
            print(">>> Result simple:")
            print(">>> Found {0} documents in {1}".format(found,datetime.now()-time_start))
            print(docs)
            time_start = datetime.now()
            docs = searching.rank_search(query,indexed_rank)
            #Show time searching and number of document found
            if "Not found" not in docs:
                found = len(docs)
            else:
                found = 0
            print(">>> Result rank:")
            print(">>> Found {0} documents in {1}".format(found,datetime.now()-time_start))
            result = Counter(docs)
            count = 0
            for d in result.most_common(100): #Get top 100 document highest rank
                print(d)
                count = count + 1
                if count%10 == 0:
                    #To show only 10 result per time
                    raw_input("Enter to load more")

#Print usage of this program
def usage():
    print("Usage: %s search [console](optional)"%sys.argv[0])
    print("Usage: %s index"%sys.argv[0])
    print("Note: indexing new files in collections to update if database exists")
    print("Note: indexing all files in collections to update if database not exists")
    sys.exit(0)

#For print error message then program's usage
def error(message):
    print(message)
    usage()

if __name__ == '__main__':
    try:
        #Get current directory path which have this script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(dir_path,"collections/ohsumed-all-docs")
        if sys.argv[1] == "search":
            #No index database, return error. If exist, load it to global vars
            if not (os.path.exists('simple_index.npy') and os.path.exists('rank_index.npy')):
                error("No indexing database")
            else:
                indexed_simple = np.load('simple_index.npy').item()
                indexed_rank = np.load('rank_index.npy').item()
            if len(sys.argv) == 3 and sys.argv[2] == "console":
                #For test with console: ./ir_main.py search console
                console()
            else:
                #For test with browser (default): ./ir_main.py search
                #CTRL + click to link to open it in default web browser
                app.run(debug = True)
        elif sys.argv[1] == "index":
            #Index as new or updating index database (only new files will be indexed)
            print("Collections: %s"%data_path)
            try:
                indexed_simple = np.load('simple_index.npy').item()
                print("   ==> Simple indexing ... updating {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            except:
                indexed_simple = {}
                print("   ==> Simple indexing ... start {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            indexed_simple = searching.indexing(data_path,indexed_simple)
            #indexed_simple = inverted_index.indexing_basic(data_path)
            np.save('simple_index.npy',indexed_simple)
            print("   ==> Simple indexing ... DONE {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            try:
                indexed_rank = np.load('rank_index.npy').item()
                print("   ==> Rank indexing ... updating {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            except:
                indexed_rank = {}
                print("   ==> Rank indexing ... start {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            #indexed_rank = inverted_index.indexing_TF_IDF(data_path)
            indexed_rank = searching.indexing_2(data_path,indexed_rank)
            np.save('rank_index.npy',indexed_rank)
            print("   ==> Rank indexing ... DONE {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            raise IndexError
    except IndexError:
        #Print usage if user input wrongly
        usage()
