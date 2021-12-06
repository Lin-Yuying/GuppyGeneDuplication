'''
This script calculate p-value of fst permutation test. 
Usage: python3 cal_pvalues.py -h 
Author: Y.Lin
Date: Nov-16-2020
'''
import os,sys,argparse,pprint
import numpy as np
from collections import defaultdict

############## 00. cmd line arguments ###############
def parserargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-in_fst")
	parser.add_argument("-out")
	return parser.parse_args()

################ 01. read fst file #################
def read_fst_file(fst_fl):
	with open(fst_fl,'r') as inf:
		next(inf) # skip header, line 0 
		fst_list = []
		tmp_dict = {}
		for line in inf:
			line = line.rstrip("\n")
			chrom,pos,fst = line.split("\t") # the first fst is the original fst
			if chrom in tmp_dict:
				if pos in tmp_dict[chrom]:
					tmp_dict[chrom][pos].append(fst)
				else:
					yield tmp_dict
					tmp_dict = {}
					tmp_dict[chrom] = {pos:[fst]}
			else:
				tmp_dict[chrom] = {pos:[fst]}
		yield tmp_dict

# debug 
# pprint.pprint(read_fst_file(sys.argv[1]))

################ 02. cal pvalue #################
def cal_pvalues(fst_dict):
	for i in fst_dict:
		for x in fst_dict[i].keys():
			original = fst_dict[i][x][0] # the first fst is the original fst
			permutated = sorted(fst_dict[i][x][1:]) # permutated fst
			idx = np.searchsorted(permutated, original, side="left") # distributions
			l = float(len(permutated))
			pvalue = max((l - idx) / l, 1.0 / l)
			yield i, x, original, pvalue


################ 03. execute #################### 
if "__main__":
	args = parserargs()
	with open(args.out,'w') as outf:
		outf.write("\t".join(["CHROM","POS","FST", "PVALUE\n"])) # header
		for fst_dict in read_fst_file(args.in_fst):
			for chrom, pos, fst, pvalue in cal_pvalues(fst_dict):
				outf.write("\t".join([str(chrom),str(pos), str(fst), str(pvalue)]))
				outf.write("\n")
