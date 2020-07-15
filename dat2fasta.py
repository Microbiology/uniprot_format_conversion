#!/usr/bin/env python
# dat2fasta.py
# Geoffrey Hannigan
# Merck ESC, Computational Biology

# Use this script to convert uniprot dat files to fasta format

import sys
import re
import optparse

# Parse that command line
parser = optparse.OptionParser()

parser.add_option("-i", "--input", dest="input",
	help="Input uniprot dat file name.", metavar="FILE")
parser.add_option("-o", "--output", dest="output",
	help="Output fasta file name.", metavar="FILE")
(options, args) = parser.parse_args()

# Bring in the dat file
fastafile = open(options.output, "w")

with open(options.input, "r") as a_file:
	for line in a_file:
		if re.match("^ID", line):
			# This variable allows us to ignore repeated
			# accession variables. We only want the first.
			repeat_accession = 0
			stripped_line = line.strip()
			stripped_line = re.sub(r"ID +", r"", stripped_line)
			stripped_ID = re.sub(r" .+", r"", stripped_line)
		if re.match("^AC", line) and repeat_accession == 0:
			stripped_line = line.strip()
			stripped_line = re.sub(r"AC +", r"", stripped_line)
			stripped_line = re.sub(r";", r"", stripped_line)
			stripped_AC = re.sub(r" .+", r"", stripped_line)
			fastafile.write(">sp|" + stripped_AC + "|" + stripped_ID + "\n")
			stripped_ID = None
			stripped_AC = None
			repeat_accession = 1
		elif re.match("^ ", line):
			stripped_line = line.strip()
			# Remove those pesky white spaces
			stripped_line = re.sub(r" ", r"", stripped_line)
			fastafile.write(stripped_line + "\n")

fastafile.close()
