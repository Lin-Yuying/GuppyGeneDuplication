'''
This script calculates Male to female read depth ratio 
Input: male.cds.ldepth female.cds.ldepth
Output: M_F.cds.coverage.ratio.csv
Usage: python gene_coverage.py gene_boundary.bed male.cds.ldepth female.cds.ldepth
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
			#chrom, start, end, gene_IDs = line.split("\t") 
			chrom, start, end = line.split("\t") 
			yield chrom, start, end #gene_IDs


def get_sex_depth(file,chrom,start,end):
	# CHROM   POS     SUM_DEPTH       SUMSQ_DEPTH
	df = pd.read_csv(file, sep = "\t")
	subset = df[(df["CHROM"]== str(chrom)) & (df["POS"] <= int(end)) & (df["POS"] > int(start))]
	if len(subset) == 0:
		return 0 
	else:
		return sum(subset["SUM_DEPTH"]) / len(subset["SUM_DEPTH"])

with open(sys.argv[4], 'w') as outf:
	outf.write('\t'.join(["CHROM", "START","END", "male_average", "female_average", "M_F_ratio","\n"]))

	for chrom, start, end in get_gene_boundary(sys.argv[1]):
		male_average = get_sex_depth(sys.argv[2],chrom,start,end)
		female_average = get_sex_depth(sys.argv[3],chrom,start,end)
		if male_average == 0 or female_average == 0:
			M_F_ratio = 0
		else:
			M_F_ratio = male_average/female_average
		outf.write('\t'.join([chrom, str(start), str(end), str(male_average), str(female_average), str(M_F_ratio)]))
		outf.write('\n')



	
	

