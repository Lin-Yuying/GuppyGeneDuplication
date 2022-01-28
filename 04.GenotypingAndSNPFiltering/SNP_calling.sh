ref=Poecilia_reticulata.Guppy_female_1.0_MT.dna_sm.toplevel.fa
bam_file=bamlist.txti #please change when use
region_name=$1 #batch calling, I seperate it into 4 regions.
/Linux/samtools-1.9/bin/bcftools mpileup -Ou -q 20 -Q 20 -R ${region_name}.txt --skip-indels -a FORMAT/AD,FORMAT/DP -f $ref -b $bam_file | /Linux/samtools-1.9/bin/bcftools call -mv -Oz -f GQ -o ${region_name}.vcf.gz
