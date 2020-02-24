# Author: Sam Shenoi
# File Description: This file runs the BLASTN program from python.


# Import modules
from subprocess import Popen, PIPE
from Ensembl import Ensembl
import re
from config import Environment

# This class runs the blast program and parses the data into a format that is human readable
class Blast:

    # __init__
    #
    # precondition: arguments are passed in
    # postcondition: object is initalized
    # return: none
    def __init__(self, args):

        # The query sequences
        self.ids = args.f

        # The output file
        self.output = args.o

        # The evalue
        self.eval = args.e

        # Create the Ensembl interface
        self.En = Ensembl()

        # Init environment variables (Mainly db paths)
        env = Environment()

        # Get the database path
        self.db = env.getDb(int(args.g[0]))

        actual = []
        # Split comma separated query values
        for i in self.ids:
            # Split on the comma
            r = i.split(",")

            # For each id, clean it and add to list
            for e in r:
                # Remove whitespaces
                e = re.sub(" ", "", e)

                # If this is not empty string, include it
                if e != "":
                    actual.append(e)

        # Init object with actual sequence ids
        self.ids = actual
    # pull_sequences
    #
    # precondition: ids are passed in
    # postcondition: fasta files are created with all of the sequences needed for this program
    # return: array of filenames
    def pull_sequences(self):
        # Check what type of file the first one is
        type = self.En.identify_sequence_type(self.ids[0])

        # Declare an array of filenames
        files = []

        # If we are given a type of id, pull the results from the databases
        if type != "filename":
            # Do this for each of the ids
            for e in self.ids:
                # Generate the proper query
                query = self.En.query_NCBI(e)
                # Create  the proper filename
                filename = e + ".fsa"

                # Write results to a file
                self.En.write_sequence(query, {}, filename)

                # Add the filename to the list of files
                files.append(filename)

                # Wait for a few milliseconds so that we dont do more than 3 per second

        else:
            # If we were already provided filenames, just use that
            files = self.ids

        # Return the filenames
        return files

    # format_file
    #
    # precondition: object was created with values
    # postcondition: the header line is written to the output file
    # return: none
    def format_file(self):
        # Open the file
        out = open(self.output[0], 'w')

        # Write the sequence
        out.write("Query ID\tHit ID\tE-value\tPercent Positive Matches\n")

        # Close the file
        out.close()

    # run_blast
    #
    # precondition: filenames of the fasta files are passed in
    # postcondition: results are written to output file
    # return: none
    def run_blast(self, filenames):
        # Open the files
        out = open(self.output[0], 'a')

        # For each filename run the blast query
        for f in filenames:
            # Run the process as a process: Removing the only get one query sequence parameter 
            p = Popen(["./blastn", "-db", self.db, "-query", f, "-evalue", str(self.eval)],#,"-max_target_seqs", "1"],
                                 stdout=PIPE)

            # Store the results from the query
            o, err = p.communicate()

            # Convert from bytes to string
            op = o.decode("utf-8")
             
            # split the results into segments 
            res = op.split(">")
             
            summary = res.pop(0) 
            # Get the query sequence name
            q = re.search("Query=.*", summary)

            # If there was an alignment, return it
            if q is not None:
                  q = q.group()
                  # Remove extra text
                   
            else:
                  q = "N/A"

            # remove extra text
            q = re.sub("Query= ", "", q)
            q = re.sub(" .*","",q) 
            for output in res: 
               output ="Query=" + output 
               # Check what the E value is
               expect = re.search("Expect.*", output)

               # If there is an evalue, return it
               if expect is not None:
                   expect = expect.group()
               else:
                   expect = "N/A"

               # Remove extra text so only value remains
               expect = re.sub("Expect = ", "", expect)

               # Get the percent matching
               identities = re.search("Identities .*,", output)

               # If there is a percent matching return it
               if identities is not None:
                  identities = identities.group()
               else:
                  identities = "N/A"

               # remove extra text
               identities = re.sub("Identities = ", "", identities)
               identities = re.sub(",", "", identities)
               identities = re.sub(".* \(","",identities)               
               identities = re.sub("%\)","",identities)  
               # Get the aligned query sequence
               query = re.search("Query=.*", output)

               # If there was an alignment, return it
               if query is not None:
                  query = query.group()
               else:
                  query = "N/A"

               # remove extra text
               query = re.sub("Query=", "", query)
               query = re.sub(" .*", "", query)

               # Get all lines of the sequence
               sequence = re.findall("Query .*", output)
               final_seq = ""
               # For each line remove extra text and add to long sequence
               for s in sequence:
                   s = re.sub("[0-9]", "", s)
                   s = re.sub("Query", "", s)
                   s = re.sub(" ", "", s)

                   final_seq += s

               # Write to file
               if q != query and int(identities) > 84: 
                  out.write(q + "\t" + query + "\t" + expect + "\t" + identities +  "\n")

