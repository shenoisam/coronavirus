# Author: Sam Shenoi
# Assignment: Assignment 6
# Date Created: 2/24/2020
# Date Due: 2/26/2020
# Date Last Modified: 2/25/2020

# Imports
import re

class MSAGap:
    def __init__(self, filename):
        self.f = FAFSAChecker()
        self.msa_dict = self.f.multiple_fafsa_format(filename)

    #def gen_sequence(self):


# This class checks FAFSA sequences
class FAFSAChecker:
    # check_fafsa
    #
    # precondition: the seq
    # postcondition: the object is created
    # return: none
    def check_fafsa(self,seq):
        clean = False

        # Search for the nucleotides
        res = re.search("^[AGTC-gact]*$",seq)
        # If there are nucleotides, this is a good sequence
        if res is not None:
            clean = True
        # Return results
        return clean

    # open_fafsa
    #
    # precondition: the filename is passed in
    # postcondition: the sequence is retrieved
    # return: the sequence
    def open_fafsa(self, filename):
        # Open the file
        f = open(filename)
        # The first line of a Fasfa file is the title, so get the title
        name = f.readline()
        # Init the seq variable
        seq = ""
        # For each line in the file
        for s in f:
            # Replace the new lines with empty strings
            s = re.sub("\n","",s)
            # Add to the sequence
            seq = seq + s
        # Return the sequence
        f.close()
        return seq

    def multiple_fafsa_format(self,filename):
        f = open(filename)
        line = ""
        for l in f:
            line = line + l
        line = line.split(">")[1:]

        seq_obj = dict()
        for l in line:
            s = re.sub("\n", "", l[l.index("\n"):])
            #if self.check_fafsa(s):
            seq_obj[l[0:l.index("\n")]] = s
            #else:
            #    print("Not correct fasta")
            #    exit(1)

        return seq_obj





