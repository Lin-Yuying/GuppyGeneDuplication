import pandas as pd
import sys
data = pd.DataFrame(pd.read_csv(sys.argv[1],sep = '\s+'))
res = data.sort_values(by=["CHROM","POS"])
res.to_csv(sys.argv[2],index=False,sep="\t")
