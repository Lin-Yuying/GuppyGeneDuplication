## GuppyGeneDuplication
Scripts for Lin, Y., Darolti, I., Furman, B. L. F., Almeida, P., Sandkam, B. A., et al., Breden, F., Wright, A. E., Mank, J. E. (2022) Gene duplication to the Y chromosome in Trindadian Guppies. https://doi.org/10.1111/mec.16355

1. Quality control
```
python 01.quality-control_fqs.py -fqs [/path/fq_files/] -o [./qc/] -t [10] -trim -qc
```

2. Align high-quality reads to female reference genome 
```
python 02.alignment_bwa.py -r [/path/ref_genome/] -bwa [bwa] -fq [./trim/] -a -t [10]
```

3. Fixmate, sort and mark duplications
```
sh 03.align_postprocess.sh [sample_ID]
```

4. Genotyping using SAMtools, please check the pipeline before using it. 
```
sh 04.GenotypingAndSNPFiltering/SNP_calling.sh [sample_ID] [region_name]
```

5. SNP filtering and calculateing intersexual Fst

#(1) SNP filtering
```
vcftools --gzvcf [input] --maf 0.05 --mac 1 --min-alleles 2 --max-alleles 2 --max-missing 0.9 --min-meanDP 10 
--max-meanDP 100 --bed guppy_cds_coords.txt --recode --recode-INFO-all --minGQ 25 --out [output]
```


#(2) Calculating intersexual Fst for each SNPs
```
vcftools --vcf [vcf] --weir-fst-pop [female.txt] --weir-fst-pop [male.txt] --out [output]
```

#(3) SNPs with top 1% Fst 

#(4) Fisher's exact test, please check details on 05.FisherExactTest folder
```
sh 05.FisherExactTest/fisher_cds_vcf.sh
```

#(5) Permutation test, please check details on 06.PermutationTest folder
```
sh 06.permutation_test/run_permutation_sex.sh
``` 

6. Male-to-Female read depth ratio (to be modified...)

7. Tajima's D  (to be modified...)

8. Relatedness Inference  (to be modified...)



