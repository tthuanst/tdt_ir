#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

def search(ids,indexed_data):
    result = set(indexed_data[ids[0]])
    for i in ids[1:]:
        result = result & set(indexed_data[i])
    return result