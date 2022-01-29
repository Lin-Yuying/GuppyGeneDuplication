import random
import sys 
import collections
import os

def getID(popfile):
    pop = []
    with open(popfile,'r') as inFH:
        for i in inFH:
            i = i.strip("\n").split('\t')[0]
            pop.append(i)
    return pop
        
def random_assign_indvs(pop):
    pop1 = []
    pop2 = []
    pop1 = random.sample(pop,60)
    pop2 = [x for x in pop if x not in pop1]
    with open(sys.argv[2],"w") as pop1_FH, open(sys.argv[3],"w") as pop2_FH:
        for i in pop1:
            pop1_FH.write(i)
            pop1_FH.write("\n")
        for i in pop2:
            pop2_FH.write(i)
            pop2_FH.write("\n")
    return pop1,pop2

pop = getID(sys.argv[1])
random_assign_indvs(pop)
