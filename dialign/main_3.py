from gaps import *
from FAFSAChecker import *

if __name__ == "__main__":

    inserts =find_insertion("seq.fa")
    print("There is ", len(inserts), "seqs aligned with corona")
    for i in range(len(inserts)):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("#", i+1, "sequence's insertions")
        for j in range(len(inserts[i])):
            print("no.", j+1," insertion:")
            print("".join(inserts[i][j]))