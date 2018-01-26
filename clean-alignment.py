#!/usr/bin/env python

'''
================================================================================
clean-alignment: a simple tool to reduce the number of outliers and artifacts
in multiple sequence alignments
--------------------------------------------------------------------------------
Authors: Frederico Schmitt Kremer & Luciano da Silva Pinto   
Contact: fred.s.kremer@gmail.com                              
Version: 0.1                                               
================================================================================

'''

from Bio import AlignIO
import subprocess
import argparse
import random
import string
import os
import sys

# globals

working_dir = os.getcwd()
program_file_name = sys.argv[0]
program_abs_path = os.path.abspath(program_file_name)
program_abs_dir_path = os.path.dirname(program_abs_path)
bin_dir_path = "{0}/bin".format(program_abs_dir_path)

# useful functions

def randomFileName():
	'''
	randomFileName(): returns a random name 
	'''
	randomFileNameList = []
	
	while True:

		while True:

			fileName = ''.join([random.choice(string.lowercase) for i in range(20)])
			
			if fileName not in randomFileNameList:

				randomFileNameList.append(fileName)
				break
				
		yield randomFileNameList

def analyze(alignment, outputdir):

	global bin_dir_path
        _tempAlignmentFile = "{0}/{1}.fasta".format(outputdir, randomFileName())
	AlignIO.write([alignment], open(_tempAlignmentFile,'w'),'fasta')

	evalmsa_cmd = "{0}/EvalMSA/bin/./EvalMSA {1} {0}/EvalMSA/res/Matrix/blosum62".format(bin_dir_path, outputdir)
	subprocess.call(evalmsa_cmd, stdout=open(os.devnull,'w'), 
                        stderr=open(os.devnull,'w'), shell=True)

	return evalMsaReport
	
def main():

	## parse arguments

	argumentParser = argparse.ArgumentParser()
	argumentParser.add_argument('-i','--input', type=str, required=True)
	argumentParser.add_argument('-o','--output', type=str, required=True)
	argumentParser.add_argument('-if','--informat', type=str, default='fasta', choices=['fasta', 'phylip'])
	argumentParser.add_argument('-of','--outformat', type=str, default='fasta', choices=['fasta', 'phylip'])
	arguments = argumentParser.parse_args()

	# define I/O formats
      
	inputFileFormat = arguments.informat
	outputFileFormat = arguments.outformat

	# define I/O handlers (parsers and writers)

	inputFilePath = arguments.input
	inputFileHandle = open(inputFilePath)
	inputFileParser = AlignIO.parse(inputFileHandle, inputFileFormat)

	outputFilePath = arguments.output
	outputFileHandle = open(outputFilePath, 'w')
	outputFileWriter = None

	# load alignments

	alignments = [record for record in inputFileParser]
	cleanedAlignments = []
	
	# define settings

	## do processing

	outputdir = os.path.dirname(arguments.output)

	for alignment in alignments:

                evalMsaReport = analyze(alignment, outputdir)
                cleanedAlignment = clean(alignment,
                                         evalMsaReport,
                                         trimAll=True)
                cleanedAlignments.append(cleanedAlignment)

	# finish

	outputFileWriter = AlignIO.write(cleanedAlignments, outputFileHandle, outputFileFormat)

	return True

if __name__ == '__main__':

	main()
