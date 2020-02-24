# Author: Shuting Chen
# Computational Biology Spring 2020
# main
from Ensembl import Ensembl
import requests, sys, os

if __name__ == "__main__":

    obj = Ensembl()
    file = open("FINAL_SEQUENCE_LIST.txt",'r')
    for i in file.readlines():
        query = obj.query_NCBI(i)
        filename = i + ".fsa"
        obj.write_sequence(query,{},filename)
