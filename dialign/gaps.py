from FAFSAChecker import *


def find_insertion(filename):
    my_MSA = MSAGap(filename)
    corona = my_MSA.msa_dict["NC_045512.2"]
    insertions = []

    for x in my_MSA.msa_dict:
        i = 0
        count_deletes = 0
        individual = []
        if x != "NC_045512.2":
            while i < len(my_MSA.msa_dict[x]):
                if my_MSA.msa_dict[x][i] == '-':
                    frag, i = next_index_insert(my_MSA.msa_dict[x], i, corona)
                    individual.insert(0, frag)
                i += 1
            insertions.insert(0, individual)
    return insertions


def next_index_insert(seq, index, corona):
    insertion = []
    next_count = 0
    while seq[index + next_count] == "-":
        insertion.insert(next_count, corona[index + next_count])
        next_count += 1
    return insertion, index + next_count


# this function will return an array of gaps in corona
def find_deletion(filename):
    my_MSA = MSAGap(filename)
    corona = my_MSA.msa_dict["NC_045512.2"]
    i = 0
    deletions = []
    count_deletes = 0
    while i < len(corona):
        if corona[i] == '-':
            frag, i = next_index_delete(my_MSA.msa_dict, i, corona)
            deletions.insert(count_deletes, frag)
            count_deletes += 1
        i += 1
    return deletions


def next_index_delete(dics, index, corona):
    deletions = []
    for i in range(46):
        deletions.insert(0, [])

    next_seqs = 0
    while corona[index + next_seqs + 1] == "-":
        next_seqs += 1

    count = 0
    for x in dics:
        ini_index = 0
        if x != "NC_045512.2":
            while ini_index <= next_seqs:
                deletions[count].insert(index + ini_index, dics[x][index + ini_index])
                ini_index += 1
            count += 1
    return deletions, index + next_seqs
