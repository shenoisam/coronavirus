# Author: Sam Shenoi
# Description: This program looks at the gaps within the MSA sequences and then BLASTs them against the nt database


# Import the MSA checker 
from FAFSAChecker import MSAGap

def main():
   # Read the MSA into a dict object. Dict object contains { seq name: sequence}
   # for each of the sequences. 
    m = MSAGap("seq.fa")



if __name__ == "__main__":
    main()
