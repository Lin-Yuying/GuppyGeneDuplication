cds_fst=$1
out=$2

vcftools --vcf ${1} --plink --out ${2}
python3 change_sex_phen.py ${2}.ped > ${2}_new.ped 
mv ${2}.ped ${2}_original.ped
mv ${2}_new.ped ${2}.ped
/Users/evolutioneco/Downloads/Software/plink_mac_20200921/plink --file ${2} --make-bed --out ${2}
######## fisher's exact test ############
/Users/evolutioneco/Downloads/Software/plink_mac_20200921/plink --file ${2} --assoc fisher

#./plink --file cds --fisher
