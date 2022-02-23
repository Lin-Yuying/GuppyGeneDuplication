import os,sys
with open(sys.argv[1],"r") as inf:
    for line in inf:
        line = line.rstrip("\n")
        fam,indv,dad,mom,sex,phen,*geno = line.split("\t")
        if "M" in fam:
            sex = "2"
            phen = "1"
            print(fam+"\t"+indv+"\t"+dad+"\t"+mom+"\t"+sex+"\t"+phen, end="\t")
            for i in range(len(geno)-1):
                print(geno[i], end = "\t")
            print(geno[-1])
        elif "F" in fam:
            sex = "1"
            phen = "2"
#            outf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}").format(fam,indv,str(dad),str(mom),sex,phen,geno)
            print(fam+"\t"+indv+"\t"+dad+"\t"+mom+"\t"+sex+"\t"+phen, end="\t")
            for i in range(len(geno)-1):
                print(geno[i], end = "\t")
            print(geno[-1])
        else:
            pass
