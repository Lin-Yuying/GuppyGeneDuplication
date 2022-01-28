import sys,os
import pandas as pd
import numpy as np
from collections import *
'''
input a high fst bed [chr,start,end]
and a single SNP Fst file [chr,pos,Fst,M:F read depth ratio]
output a new file [chr,pos,Fst,M:F read depth ratio, is_highlight]
'''
#with open(sys.argv[1],'r') as inf:
def get_pos(vcf):
    tmp_dict = defaultdict(list)
    with open(vcf,'r') as inf:
        for line in inf:
            line.rstrip("\n")
            if line.startswith("#"):
                pass
            elif line.startswith("LG"):
                 chrom,pos,*_ = line.split("\t")
                 chrom = chrom.replace("LG","")
                 tmp_dict[chrom].append(pos)
    return tmp_dict

pos_dict = get_pos(sys.argv[1])

with open(sys.argv[2],'r') as infile, open(sys.argv[3],'w') as outfile:
    header = infile.readline()
    outfile.write(header)
    for lines in infile:
        lines = lines.rstrip("\n")
        chrom,snp,bp,fst,*info = lines.split()
        info = "\t".join([str(i) for i in info])
        if chrom in pos_dict:
            if bp in pos_dict[chrom]:
                outfile.write("\t".join([chrom,snp,bp,fst]))
                outfile.write(info)
                outfile.write("\n")
            else:
                pass
        else:
            pass
    
#print(get_pos(sys.argv[1]))
