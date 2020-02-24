# Author: Sam Shenoi
# This python script cleans data

import re
from collections import Counter
import csv
import sys
import copy 


def main():
    mainList = []
    with open(sys.argv[1]) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            mainList.append(row)
    removeIDs = []
    while len(mainList) > 0:
        # Convert all points to list
        finalList = []
        for l in mainList:
            finalList = finalList + l

        # Check to see which is the most common ID
        c = Counter(finalList)
        remove = c.most_common()[0][0]

        # Add the most common one to the removeIDs list
        removeIDs.append(remove)

        newList = []
        for i in mainList:
            if i[0] != remove and i[1] != remove:
                newList.append(i)
        mainList = newList
    
    for r in removeIDs:
        print(r)


if __name__ == '__main__':
    main()
