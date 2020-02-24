# Author: Sam Shenoi
# File Description: This file defines a class object that can
#   be used to pull gene sequences from Ensembl


# Imports
import requests
import json
import re
import sys
import time

# This class accesses the Ensembl REST servers and returns sequences associated with identifiers
class Ensembl:
    # __init__
    #
    # precondition: none
    # postcondition: a Ensembl class object is created and initalized with the base urls and parameters needed
    # return: none
    def __init__(self):
        # Define url for the Ensembl REST website
        self.URI = "https://rest.ensembl.org"

        # Define the path for getting a sequence by id for ensembl
        self.ensemblId = "/sequence/id/"

        # Define the url for converting RefSeq ids to Ensembl ids
        self.convert = "https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json"

        # Define the url for getting the taxid information stuff
        self.tax = "/info/genomes/taxonomy/"

        # Define the ftp for pulling the genome
        self.ftp = "https://ftp.ncbi.nlm.nih.gov/genomes/all/"

        # Define the NCBI downloader link
        self.ncbi = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&rettype=fasta"

        # Parameters for RefSeq -> Ensembl id conversion
        self.parameters = {
            "method": "db2db",
            "input": "",
            "inputValues": "",
            "outputs": "Ensembl Gene ID"
        }

        # Dictionary containing the types of RefSeq accession numbers
        self.refseqId = {
            "gene": "RefSeq Genomic Accession",
            "protein": "RefSeq Protein Accession",
            "mrna": "RefSeq mRNA Accession"

        }

    # identify_sequence_type
    #
    # precondition: sequence id is passed in
    # postcondition: a constructed url containing all of the needed parameters is created
    # return: the constructed url
    def identify_sequence_type(self, seqId):
        # Figure out how to identify each sequence by their particular type

        # If the sequence is a refseq sequence it should have one of the following beinging two letters
        # AC, NC, NG, NT,NW,NZ,NM,NR,XM,XR,AP,NP,YP,XP,WP

        # Genomic Sequences: AC, NC, NG, NT, NW, NS, NZ
        gen = re.search("(^AC)|(^N[CGTWSZ])", seqId)

        # mRNA Sequence: NM, NR, XM, XR
        rna = re.search("(^[XN][MR])", seqId)

        # Protein: AP, NP. YP, XP, ZP
        pro = re.search("^[ANYXZ]P", seqId)

        # Taxid: sequence of numbers
        tax = re.search("[A-Z]", seqId)

        # Ensembl id: Starts with an E
        en = re.search("^E", seqId)

        # Check if a fsa file
        file = re.search(".fsa",seqId)

        type = ""

        # Check to see what type of accession number this is
        if gen is not None:
            # This is a refseq nucleotide sequence
            type = "gene"
        elif rna is not None:
            # This is a refseq mrna sequence
            type = "mrna"
        elif pro is not None:
            # This is a refseq protein sequence
            type = "protein"
        elif en is not None:
            type = "Ensembl"
        elif tax is None:
            # this is a taxid
            type = "tax"
        #else:
            # Otherwise this is not a valid input. Exit the program
        #    type = "filename"

        if file is not None:
            type = "filename"

        # Return the created query string
        return type

    def pull_by_taxid(self, taxId, file):
        # Pull the information associated with taxid
        url = self.URI + self.tax + taxId

        res = self.pull_sequence(url, {})

        if len(res) > 0:
            # Get the relevant information from the returned results
            assembly_name = res[0]["assembly_name"]
            assembly_accession = res[0]["assembly_accession"]

            # Construct the query based on the results
            query = self.ftp + assembly_accession[0:3] + "/"
            query = query + assembly_accession[4:7] + "/"
            query = query + assembly_accession[7:10] + "/"
            query = query + assembly_accession[10:13] + "/"
            query = query + assembly_accession + "_" + assembly_name + "/"
            query = query + assembly_accession + "_" + assembly_name
            query = query + "_genomic.fna.gz"
        else:
            print("Unable to retrieve sequence")
            sys.exit()

        # Pull just the compressed fasta file
        print("Downloading your sequence... Please be patient")
        r = requests.get(query)
        filename = file + ".gz"
        open(filename, "wb").write(r.content)
        return filename

    def build_refseq_from_Ensembl_Id(self, ensemblID):
        # Construct the query looking for the particular gene name
        gene_query = self.URI + self.ensemblId + ensemblID
        return gene_query

    # build_refseq_query
    #
    # precondition: the type of refseq sequence (nucleotide, protein, mRNA) is passed in
    # postcondition: the constructed query is created
    # return: the constructed url
    def build_refseq_query(self, type, seqId):
        # Construct the conversion query parameters
        self.parameters["input"] = self.refseqId[type]
        self.parameters["inputValues"] = seqId

        # Pull the ensembl ids
        ids = self.pull_sequence(self.convert, self.parameters)

        # We only care whether or not there are ensembl ids associated with this refseq accession number
        ids = ids["0"]["outputs"]
        ensemblID = ""

        # If there is an ensembl id associated with this sequence, save it
        if len(ids) > 0:
            ensemblID = ids["Ensembl Gene ID"]["0"]
            gene_query = self.build_refseq_from_Ensembl_Id(self, ensemblID)
        else:
            # Just download it from NCBI bc Ensembl is unreliable
            print("NCBI")
            gene_query = self.query_NCBI(seqId)

        # Return the constructed query
        return gene_query

    def query_NCBI(self, seqID):
        return self.ncbi + "&id=" + seqID

    # pull_sequence
    #
    # precondition: query url and parameters are passed in
    # postcondition: REST query is sent
    # return: results of the REST query
    def pull_sequence(self, query, parameters):
        print(query)
        # Send the request
        r = requests.get(query, headers={"Content-Type": "application/json"}, params=parameters)

        # Convert results to json
        ret = "404"
        if r.status_code != requests.codes.ok:
            print("Error")
            sys.exit(1)
        # Return results
        return r.json()

    # write_sequence
    #
    # precondition: the result string and file name are passed in
    # postcondition: file is written with sequence, and file size is printed (in MB)
    # return: none
    def write_sequence(self,query,parameters,file):
        # Call API
        r = requests.get(query, headers={"Content-Type": "application/json"}, params=parameters)

        # If the request was sucessful, write the results to a file
        if r.status_code == requests.codes.ok:
            open(file,'wb').write(r.content)
        else:
            # Otherwise exit the program
            print(r.content)
            print("Error retrieving sequences. Aborting")
            sys.exit(1)

        # Sleep for half a second to prevent from being banned
        time.sleep(.5)

    # write_file
    #
    # precondition: the result string and file name are passed in
    # postcondition: file is written with sequence, and file size is printed (in MB)
    # return: none
    def write_file(self, res, file):
        # Open the file for writing
        f = open(file, 'w')

        # If there is a sequence associated with this response, write it to the file
        if 'seq' in res:
            # Fasta format with a header lines
            f.write(">" + file + "\n")
            f.write(res["seq"])

        # Close the file
        f.close()


