input=$1
output=$2
vcftools --gzvcf ${input} \
--maf 0.05 \
--mac 1 \
--min-alleles 2 \
--max-alleles 2 \
--max-missing 0.9 \
--min-meanDP 10 \
--max-meanDP 100 \
--bed guppy_cds_coords.txt \ #CDS coords from genome annotation
--recode \
--recode-INFO-all \
--minGQ 25 \
--out ${output}
