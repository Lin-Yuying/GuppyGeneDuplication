'''
This scripts multi-processes raw fastq files with fastqc.
Author: Y.Lin
Usage: python3 qc_multi.py [-h] [-t THREADS] [-fq FASTQ_PATH] [-o OUTPUT] [-trim] [-qc]
'''

import os
import argparse
import sys
from multiprocessing import Process, Pool

######### 00.get command lines arguments ######
parse = argparse.ArgumentParser(description="This script is used for multiple processing quality control for raw fastq files")
parse.add_argument('-t','--threads',help="threads,the number of samples you run for one time")
parse.add_argument('-fq','--fastq_path',help="path of fq files")
parse.add_argument('-o','--output', help = "output path")
parse.add_argument('-trim','--trimmomatic', action='store_true')
parse.add_argument('-fastqc','--qc', action='store_true')
args = parse.parse_args()

# get arguments 
# thread
t = int(args.threads) if args.threads else 1
# fastq path
fq_path = args.fastq_path + '/' if args.fastq_path[-1] != '/' else args.fastq_path
# out path
out = args.output if args.output else os.getcwd()

###### 01. get fq files list ########
fq_files = os.listdir(fq_path)
fqs = []
for f in fq_files:
    if f.split(".")[-1] == "gz":
        fqs.append(f)


####### 02. fastqc ########
def run_fastqc(fq):
    if args.qc:
        cmd = "fastqc -t 4 -o {} {}".format(out,fq_path+fq)
        os.system(cmd)

###### 03. trimmomatic ########
def trimming(fq):
    '''
    java -jar trimmomatic-0.39.jar PE input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 MINLEN:36
    '''
    if fq.split(".")[-3][-1] == '1':
        extension = ".fastq.gz"
        prefix = fq.split(".fastq.gz")[-2][:-1]
        new_name = fq.split(".")[-3][:-1]
        cmd = "java -jar /Linux/Trimmomatic-0.36/trimmomatic-0.36.jar PE {} {} {} {} {} {} ILLUMINACLIP:/Linux/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:10 LEADING:3 TRAILING:3 MINLEN:50".format(fq_path+prefix+"1.fastq.gz", fq_path+prefix+"2.fastq.gz",new_name+"1.paired.fq.gz", new_name+"1.unpaired.fq.gz",new_name+"2.paired.fq.gz",new_name+"2.unpaired.fq.gz")
        os.system(cmd)


if args.trimmomatic:
    with Pool(t) as a:
        a.map(trimming,fqs)

if args.qc:
    with Pool(t) as p:
        p.map(run_fastqc,fqs)
