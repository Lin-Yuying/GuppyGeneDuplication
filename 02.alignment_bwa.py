'''
This script is used for multiprocessing alignment for paired end Illumina data using bwa-mem
Author: Y.Lin
Date: Jul 13, 2020 
Usage: python [script.py] -h
'''

import os,re
import argparse
import sys
from multiprocessing import Process, Pool

####### 00. get command line arguments #####
parse = argparse.ArgumentParser(description="This script is used for multiple processing alignment and genotyping")
parse.add_argument('-r','--reference',help="reference genome",required=True)
parse.add_argument('-t','--threads',help="threads,the number of samples you run for one time")
parse.add_argument('-fq','--fastq_path',help="path of fq files")
parse.add_argument('-bwa','--BWA',help="path of BWA")
parse.add_argument('-a','--align',help='using bwa for alignment',action='store_true')
args = parse.parse_args()

######### 00. set up command line arguments #####
# genome path
if args.reference:
    ref = args.reference
else:
    print("please specify reference genome")
# fastq files
if args.fastq_path:
    fq_path = args.fastq_path + '/' if args.fastq_path[-1] != '/' else args.fastq_path
# software
bwa = args.BWA if args.BWA else 'bwa'
#threads
t = int(args.threads) if args.threads else 1


###### 1.2 get fq files list #########

fq_files = os.listdir(fq_path)
fqs = []
for f in fq_files:
    if f.split(".")[-1] == 'gz':
        tmp,extension = f.split(".",1)
        #  P452_R1.paired.fq.gz
        prefix = tmp.split("_")[0]
        #prefix = re.findall(r'\w\d+',tmp)[0]  # change when use
        fqs.append(prefix)
fqs = list(set(fqs))

########### 2. alignment pipelines ###############
###### 2.1 check if reference genome indexed #######
def check_ref_idx(ref):
    ref_path = os.path.split(ref)[0] if os.path.split(ref)[0] else os.getwd() + '/' 
    ref_name = os.path.splitext(ref)[0]
    if str(ref_name)+'idx' not in os.listdir(ref_path):
        cmd = '{} index {}'.format(bwa,ref)
    else:
        print("reference genome has been indexed")

###### 2.2 alignmenti, illumina pair-end reads #####        
def alignment(fq):
    """
    bwa-0.7.15 mem -M -R "@RG\tPL:Illumina\tID:$prefix\tSM:$prefix" ref.fa read1.fq.gz read2.fq.gz 
    """
    read1,read2 = fq+'_R1.paired.fq.gz',fq+'_R2.paired.fq.gz'
    cmd = "{} mem -t 6 -M -R '@RG\tPL:Illumina\tID:{}\tSM:{}' {} {} {} 1> {} 2> {}".format(bwa,fq,fq,ref,fq_path+read1,fq_path+read2, fq+".sam", fq+".samlog")
    #read1,read2 = fq+'1',fq+'2'
    print(cmd)
    os.system(cmd)
    # nohup sh alignment.sh P492 & 
    sort_dup = 'sh alignment.sh {}'.format(fq)

####### 03. multiprocessing ##########
if args.align:
    check_ref_idx(ref)
    with Pool(t) as a:
        a.map(alignment,fqs)

