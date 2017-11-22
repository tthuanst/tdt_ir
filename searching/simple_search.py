#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

def search(ids,indexed_data):
    result = None
    for i in ids:
        if indexed_data.has_key(i):
            if result is None:
                result = set(indexed_data[i])
            else:
                result = result & set(indexed_data[i])
    if result is None or len(result) == 0:
        return set(["Not found"])
    else:
        return result


if __name__ == '__main__':
    print("Test done by ir_main.py")
