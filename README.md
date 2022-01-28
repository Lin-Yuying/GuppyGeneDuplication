# GENE-DUPLICATION-TO-THE-Y-CHROMOSOME-IN-TRINIDADIAN-GUPPIES
Scripts for Y. Lin et al., Gene duplication to the Y chromosome in Trindadian guppies. in press: Mol Ecol. 2022

1. Quality control and adaptor removal
```
python 01.quality-control_fqs.py -fqs [/path/fq_files/] -o [./qc/] -t [10] -trim -qc
```

2. Align high-quality reads to female reference genome 
```
python 02.alignment_bwa.py -r [/path/ref_genome/] -bwa [bwa] -fq [./trim/] -a -t [10]
```

3. Fixmate, sort and mark duplciation
```
sh 03.align_postprocess.sh [sample_ID]
```

4. Genotyping using GATK, please check the pipeline before using it. 
```
sh 04.genotyping.sh [sample_ID]
```

5. SNP filtering and calculateing intersexual Fst (to be modified...)
```
# SNP filtering 

# Calculating intersexual Fst for each SNPs

#(1) SNPs with top 1% Fst 

#(2) Fisher's exact test, details please check 05.FisherExactTest folder
sh fisher_cds_vcf.sh
#(3) Permutation test, please check details on 06.permutation_test folder
sh run_permutation_sex.sh 
```

