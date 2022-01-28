'''
Replace chr IDs from LG1 to 1, for runing Fisher's exact test with Plink.
Note: Chr23 is the sex chromosome in human genome which will affect the exact test,
      Please keep it as it is. 
'''
import sys,os
with open(sys.argv[1],'r') as inf, open(sys.argv[2],'w') as outf:
    for line in inf:
        if line.startswith("#"):
            outf.write(line)
        elif line.startswith("LG"):
        	if line.startswith("LG23"):
        		outf.write(line)	
        	else:
        		line = line.replace("LG","")
        		outf.write(line)
