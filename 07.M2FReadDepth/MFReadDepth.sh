'''
This script will calculate average Male-to-Female Read depth ratio in each gene, 
only including CDS region.

If you want to calculate Male-to-Female read depth ratio including all sites across genome.
Please start from BAM files.
'''
#################### 1. calcualte read depth across males and females, respectively
vcftools --vcf [filter_CDS.vcf] --site-depth --keep [female.txt] --out [female.cds] 
vcftools --vcf [filter_CDS.vcf] --site-depth --keep [male.txt] --out [male.cds] 

# output male.cds.ldepth and female.cds.ldepth
# header "CHROM   POS     SUM_DEPTH       SUMSQ_DEPTH"

#################### 2. calculate MF read depth ratio ##########################
# (log2(male) - log2(female))
python gene_coverage.py gene_boundary.bed male.cds.ldepth female.cds.ldepth

