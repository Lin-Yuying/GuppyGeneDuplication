'''
This script generate .gvcf for each sample and SNP calling for all the samples
Date: 10-June-2020
'''
################################ 00. setup ###############################
gatk=/Linux/gatk-4.1.2.0/gatk-package-4.1.2.0-local.jar


################### 01.gvcf_Haplotyper_individual_sample #################
java1.8 -Xmx64G -jar $gatk HaplotypeCaller \
       -R genome.fa \
       -I sample1.markdup.bam \
       -O sample1.gvcf \
       -ERC GVCF
      
############################## 02. database ###############################
##### list all samples with parameter '--variant' ######
java1.8 -Xmx64G -jar $gatk CombineGVCFs \
       -R genome.fa \
       --variant sample1.gvcf.gz \
       --variant sample2.gvcf.gz \
       --variant ... \
       -O cohort.g.vcf.gz

################################ 03. joint_genotype #######################
java1.8 -Xmx64G -jar $gatk GenotypeGVCFs \
        -R genome.fa \
        -V cohort.g.vcf.gz \
        -O out.vcf.gz




