## GuppyGeneDuplication
Scripts for Lin, Y., Darolti, I., Furman, B. L. F., Almeida, P., Sandkam, B. A., et al., Breden, F., Wright, A. E., Mank, J. E. (2022) Gene duplication to the Y chromosome in Trindadian Guppies. https://doi.org/10.1111/mec.16355

1. Quality control
```
python 01.quality_control_fqs.py -fqs [/path/fq_files/] -o [./qc/] -t [10] -trim -qc
```

2. Align high-quality reads to female reference genome 
```
python 02.alignment_bwa.py -r [/path/ref_genome/] -bwa [bwa] -fq [./trim/] -a -t [10]
```

3. Fixmate, sort and mark duplications
```
sh 03.align_postprocess.sh [sample_ID]
```

4. Genotyping,SNP filtering and calculateing intersexual Fst. 

#(1) Genotyping using SAMtools
```
sh 04.GenotypingAndSNPFiltering/SNP_calling.sh [sample_ID] [region_name]
```

#(2) SNP filtering using VCFtools
```
vcftools --gzvcf [input] --maf 0.05 --mac 1 --min-alleles 2 --max-alleles 2 --max-missing 0.9 --min-meanDP 10 
--max-meanDP 100 --bed guppy_cds_coords.txt --recode --recode-INFO-all --minGQ 25 --out [output]
```

#(3) Calculating intersexual Fst for each SNPs using VCFtools
```
vcftools --vcf [vcf] --weir-fst-pop [female.txt] --weir-fst-pop [male.txt] --out [output]
```

#(4) SNPs with top 1% Fst 

#(5) Fisher's exact test, please check details on 05.FisherExactTest folder
```
sh 05.FisherExactTest/fisher_cds_vcf.sh
```

#(6) Permutation test, please check details on 06.PermutationTest folder
```
sh 06.permutation_test/run_permutation_sex.sh
``` 

5. Male-to-Female read depth ratio 
```
sh 07.M2FReadDepth/MFReadDepth.sh
```

6. Tajima's D
```
#(1) exclude genes with immune and MHC function in reference genome based on Biomart info from Ensembl on http://uswest.ensembl.org/biomart/martview/4c439c138f54b451b2fea301544e731a
python 08.TajimaD/exclude_immune_MHC.py [immune_MHC.bed] [outprefix.csv] 
#(2) calculate gene-based Tajima's D
python 08.TajimaD/gene_TajimaD [gene_boundary.csv] [site.TajimaD] [outprefix.csv]
```

7. Relatedness Inference 

```
#(a) ngsRelate 
ngsrelate  -h [VCF.gz] -O [vcf.res]

#(b) KING 
king -b [my.bed] --fam [my.fam] --bim [my.bim] --related
```

