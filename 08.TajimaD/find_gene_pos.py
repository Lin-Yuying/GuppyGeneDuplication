import sys
def read_gene_ids(gene_id_file):
    with open(gene_id_file,'r') as inf:
        geneids = []
        for line in inf:
            line = line.rstrip("\n")
            geneids.append(line)
    return geneids

def find_pos(geneid,gff):
    with open(gff,'r') as infile:
        for line in infile:
            if line.startswith("#"):
                pass
            else:
                chrom,facility,gene,start,end,*_,info = line.split("\t")
                if gene == "gene":
                    if info.split(";")[0].split(":")[1] == geneid:
                        print("{}\t{}\t{}\t{}\t{}".format(chrom,gene,start,end,geneid))
                    else:
                        pass
                else:
                    pass 

if __name__ == "__main__":
    geneids = read_gene_ids(sys.argv[1])
    for geneid in geneids:
        find_pos(geneid,sys.argv[2])
