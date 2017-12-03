#!/usr/bin/env python

#
# Author: Phi, Thuy
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import spell_correction

def correction(input):
    #Correct input
    corrected = spell_correction.correction(input)
    return corrected


if __name__ == '__main__':
    #For test: ./correction.py
    while(1):
        sentence = raw_input("Input a word: ")
        print(correction(sentence))