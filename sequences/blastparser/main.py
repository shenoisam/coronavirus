# Author: Sam Shenoi
# Assignment: Assignment 3
# Date Created: 2/4/2020
# Date Due: 2/7/2020
# Date Last Modified: 2/4/2020

# Import classes
from Blast import Blast
import argparse


def main():

    # Define an argument parser to pull arguments from the command line
    parser = argparse.ArgumentParser(description='Run a local blast query on a variety of sequences.')

    # f1 argument
    parser.add_argument('-f', metavar='-f', nargs='+',required=True,
                        help='A list of filenames or Refseq ids ')

    # f2 argument
    parser.add_argument('-g', metavar='-g', nargs='+', required=True,type=int,
                        help='Genomes passed by taxid: 9606, 562, 2697049')

    # Output file
    parser.add_argument('-o', metavar='-o',nargs='+',required=True,
                        help='The name of the output file')

    # e value argument
    parser.add_argument('-e', nargs='?', default=10, type=int,
                        help='e-value threshold. Defaults to 10.')

    # Parse arguments
    args = parser.parse_args()

    # Generate the blast object with the arguments
    blast = Blast(args)

    # Get the filenames of the query sequences needed
    filenames = blast.pull_sequences()

    # Run the blast query
    blast.format_file()
    blast.run_blast(filenames)


if __name__ == "__main__":
    main()
