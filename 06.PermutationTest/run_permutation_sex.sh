#!/bin/bash
sim = 1
while [ $sim -lt `1000 + 1` ]
do
	echo "############ Simulation ${sim} ###############" >> pop.perm.log
	# please check sample_120.txt for sample groups information
	# here, we grouped samples according to their sex
	python permutation.py sample_120.txt male_${sim}.txt female_${sim}.txt 
	vcftools --vcf sex_GQ30_0.9.recode.vcf --weir-fst-pop male_${sim}  --weir-fst-pop female_${sim}.txt --out pop.snp.${sim}
	sim=`expr ${sim} + 1`
done
# header
cat pop.snp.*.fst | grep -v CHROM > total.fst
cat pop.snp.0.fst | grep "CHROM"|uniq > header.txt
cat header.txt total.fst > pop.snp.fst
# sort SNPs correpsonding to the reference genomic location
python ./fst2csv.py pop.snp.fst pop.snp.sorted.fst 
# calculate P value for each SNP
python ./cal_pvalues_lin.py -in_fst pop.snp.sorted.fst -out pop.pvalue
