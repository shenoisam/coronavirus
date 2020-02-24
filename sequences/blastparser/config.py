# Author: Sam Shenoi
# Description: This file defines the database names and locations in order to be used
# only any machine. Since the path to the db changes with each machine. This config file
# is important in order to run this program.

# Imports
from collections import defaultdict


# Environment: Defines environment variables for this os
class Environment:

    # __init__
    #
    # precondition: the class needs to be created
    # postcondition: this class is created
    # return type: none
    def __init__(self):

        # Define a default dictionary to the paths for the databases; Default to ecoli database 
        self.dbnames =  defaultdict(lambda: "/home/csi/s/shenoi/blastdb/ecoli.fsa") 
        self.dbnames[9606] = "/home/csi/s/shenoi/blastdb/humans.fsa"
        self.dbnames[2697049] = "/home/csi/s/shenoi/blastdb/wuhan.fasta"
        self.dbnames[-1] = "/home/csi/s/shenoi/blastdb/dbFile.fsa" 

    # getDb
    #
    # precondition: the taxid of the db being queried against is passed in
    # postcondition: the path to the database is found
    # return: the path to the database
    def getDb(self, id):
        return self.dbnames[id]
