'''
This script calculates gene-based Tajima's D 
Input: (1)gene boundary file (2) site-based Tajima'D 
Output: Mean gene-based Tajima's D
Usage: python3 gene_TajimaD gene_boundary.csv site.TajimaD prefix_output
Date: Jan 13, 2021
'''
import sys,os
import pandas as pd
import math

def get_gene_boundary(bed):
	with open(bed,'r') as inf:
		header = inf.readline()
		for line in inf:
			line = line.rstrip("\n")
			chrom, start, end, gene_IDs = line.split("\t") 
			yield chrom, start, end, gene_IDs


def get_mean_TajimaD(file,chrom,start,end,gene_IDs):
	# CHROM   BIN_START       N_SNPS  TajimaD
	#total = 0
	#length = 0
	df = pd.read_csv(file, sep = "\t")
	subset = df[(df["CHROM"]== str(chrom)) & (df["BIN_START"] <= int(end)) & (df["BIN_START"] > int(start))]
	if len(subset) == 0:
		pass 
	else:
		#sum(subset['TajimaD'])
		#length = len(subset['TajimaD'])
		return sum(subset['TajimaD']) / len(subset['TajimaD'])

with open(sys.argv[3], 'w') as outf:
	outf.write('\t'.join(["CHROM", "START","END", "gene_IDs","mean_TajimaD","\n"]))

	for chrom, start, end, gene_IDs in get_gene_boundary(sys.argv[1]):
		TajimaD = get_mean_TajimaD(sys.argv[2],chrom,start,end,gene_IDs)
		outf.write('\t'.join([chrom, str(start), str(end), str(TajimaD), gene_IDs,'\n']))



	
	

