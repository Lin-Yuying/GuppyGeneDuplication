'''
This script will sort, fixmate and mark duplications for .sam files using samtools 1.9

bwa-0.7.15

samtools 1.9 : /Linux/samtools-1.9/bin/samtools 

Usage : sh alignment_postprocess.sh [sampleID]

Date: 28-Mar-2020
'''

#ref=$1
prefix=$1 # sample ID

###########1. index the genome#########

#bwa-0.7.15 index $ref

#/Linux/samtools-1.9/bin/samtools faxid $ref

 

########## 2.mapping_PE150 ########

#bwa-0.7.15 mem -M -R "@RG\tPL:Illumina\tID:$prefix\tSM:$prefix" $ref ../02.trim/${prefix}_R1.fq.gz ../02.trim/${prefix}_R2.fq.gz > $prefix.sam 2>$prefix.samlog 

#########  3. sam2bam ############
# skip 
#/Linux/samtools-1.9/bin/samtools view -bS $prefix.sam > $prefix.bam


####### 4.samtools fixmate_removing unusual FLAG information on SAM records #####

/Linux/samtools-1.9/bin/samtools fixmate -@ 5 -m -O bam $prefix.sam $prefix.fixmate.bam


######### 5. sort and mark duplications #########

/Linux/samtools-1.9/bin/samtools sort -o $prefix.sorted.bam $prefix.fixmate.bam

/Linux/samtools-1.9/bin/samtools markdup $prefix.sorted.bam $prefix.sort_mkdup.bam
