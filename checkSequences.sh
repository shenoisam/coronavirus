#!/bin/bash 

# Author: Sam Shenoi 
# Description: This BASH script pulls sequences from a csv file from NCBI, runs BLAST on them, cleans the BLAST output,
#   and then writes the sequences that need to be removed to a file. 
#   Sequences that need to be removed have > 85% similarity to other sequences. By removing these sequences we ensure that the 
#   tree that is created is a valid tree. 


# First change directory to the blastparser directory
cd sequences/blastparser 
useFiles=1 
# Run the program to get the sequences and parse the data
echo "Running BLAST"  
cat ../ALL_SEQUENCES.csv > faster.csv
for a
do 
   if [[ $a == '-f' ]]
   then
       sed 's/,/.fsa,/g' ../ALL_SEQUENCES.csv > faster.csv
       echo "Switching to filenames" 
       useFiles=0
   fi
done
python3 main.py -f `cat faster.csv` -g -1 -o out.tsv 
echo $(wc -l out.tsv)
# Blast Program returns only sequences have have greater than 84% similarity 
# Now run the tuple gnerator 
echo "To Sets"
mv out.tsv ../../
cd ../../
sed 's/,/\n/g' sequences/ALL_SEQUENCES.csv > ALL_SEQUENCES.txt
java gotoSETs out.tsv

# Sort the output file 
sort -u sets.tsv > uniqSETs.tsv 
grep 'N.*' uniqSETs.tsv > better.tsv

# Remove old artifacts
#Replace the commans with new lines in the original file 


# After turning to sets, run the program to find which sequences to keep 
echo "Removing less similar sequences" 
python3 rmSeq.py better.tsv | sort > res.txt 
sort sequences/ALL_SEQUENCES.txt > o.txt 

grep -v -f res.txt -F -x o.txt > resultFile.txt 

rm res.txt 
rm o.txt 
rm better.tsv 
rm out.tsv  
rm sets.tsv
rm uniqSETs.tsv
rm ALL_SEQUENCES.txt 
cd ../../
