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
from Bio.Align import MultipleSeqAlignment
import subprocess
import argparse
import random
import string
import os
import sys
import csv

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
				
		yield fileName

def analyze(alignment, outputdir, weightTreshold):

	global bin_dir_path
	randomFilePrefix = randomFileName()
	_tempFilePrefix = next(randomFilePrefix)
	_tempAlignmentFile = "{0}/{1}.fasta".format(outputdir, _tempFilePrefix)
	_tempEvalMsaResult = "{0}/{1}_values.csv".format(outputdir, _tempFilePrefix)
	AlignIO.write([alignment], open(_tempAlignmentFile,'w'),'fasta')

	evalmsa_cmd = "{0}/EvalMSA/bin/./EvalMSA {1} {0}/EvalMSA/res/Matrix/blosum62".format(bin_dir_path, _tempAlignmentFile)
	subprocess.call(evalmsa_cmd, stdout=open(os.devnull,'w'), 
                        stderr=open(os.devnull,'w'), shell=True)
	
	evalMsaResult = csv.reader(open(_tempEvalMsaResult), delimiter=',')

	evalMsaReport = []

	for indexRow, row in enumerate(evalMsaResult):

		if indexRow == 0:

			continue

		if float(row[3]) < weightTreshold:

			evalMsaReport.append(row[0])

	os.system("rm -r {0}/{1}*".format(outputdir, _tempFilePrefix))

	return evalMsaReport

def clean(alignment, evalMsaReport, outputdir, trimAll=True):

	global bin_dir_path

	cleanedAlignment = MultipleSeqAlignment([record for record in alignment if record.id not in evalMsaReport])
	
	if trimAll:

		_tempTrimallInput = "{0}/temptrimall.in.fasta".format(outputdir)
		_tempTrimallOutput = "{0}/temptrimall.out.fasta".format(outputdir)

		AlignIO.write([cleanedAlignment], open(_tempTrimallInput,'w'), 'fasta')

		trimall_cmd = ("{0}/trimAl/source/./trimal "
		               "-in {1} -out {2} -fasta -noallgaps").format(bin_dir_path,
		                                                            _tempTrimallInput,
																	_tempTrimallOutput)
		
		subprocess.call(trimall_cmd, stdout=open(os.devnull,'w'),
		                             stderr=open(os.devnull,'w'),
									 shell=True)

		cleanedAlignment = next(AlignIO.parse(open(_tempTrimallOutput), 'fasta'))

		os.remove(_tempTrimallInput)
		os.remove(_tempTrimallOutput)

	return cleanedAlignment

def main():

	## parse arguments

	argumentParser = argparse.ArgumentParser()
	argumentParser.add_argument('-i','--input', type=str, required=True)
	argumentParser.add_argument('-o','--output', type=str, required=True)
	argumentParser.add_argument('-if','--informat', type=str, default='fasta', choices=['fasta', 'phylip'])
	argumentParser.add_argument('-of','--outformat', type=str, default='fasta', choices=['fasta', 'phylip'])
	argumentParser.add_argument('-wt','--weightthreshold', type=float, default='0.7')
	arguments = argumentParser.parse_args()

	# define I/O formats
      
	inputFileFormat = arguments.informat
	outputFileFormat = arguments.outformat

	# define I/O handlers (parsers and writers)

	inputFilePath = arguments.input

	if not os.path.isfile(inputFilePath):

		print "Error: File '{0}' not found!".format(inputFilePath)
		exit()

	inputFileHandle = open(inputFilePath)
	inputFileParser = AlignIO.parse(inputFileHandle, inputFileFormat)

	outputFilePath = arguments.output
	outputFileHandle = open(outputFilePath, 'w')
	outputFileWriter = None

	outputdir = os.path.dirname(os.path.abspath(arguments.output))

	if not os.path.isdir(os.path.dirname(os.path.abspath(outputFilePath))):

		print "Error: Output dir '{0}' not found!".format(outputdir)
		exit()

	# load alignments

	alignments = [record for record in inputFileParser]
	cleanedAlignments = []
	
	# define settings

	## do processing

	for alignment in alignments:

                evalMsaReport = analyze(alignment, outputdir, arguments.weightthreshold)
                cleanedAlignment = clean(alignment,
                                         evalMsaReport,
										 outputdir,
                                         trimAll=True)
                cleanedAlignments.append(cleanedAlignment)

	# finish

	outputFileWriter = AlignIO.write(cleanedAlignments, outputFileHandle, outputFileFormat)

	return True

if __name__ == '__main__':

	main()
