from gaps import *
from FAFSAChecker import *

if __name__ == "__main__":

    deletions = find_deletion("seq.fa")
    print("There is ", len(deletions), "gaps in conona virus")
    for i in range(len(deletions)):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("#", i + 1, "gap(deletion) aligned with other 46's")
        con_seq = consensus_seq(deletions[i])
        f = open("insert_consensus_seq.txt", "a")
        f.write("".join(con_seq)+"\n")
        f.close()
        for j in range(len(deletions[i])):
            print("".join(deletions[i][j]))
