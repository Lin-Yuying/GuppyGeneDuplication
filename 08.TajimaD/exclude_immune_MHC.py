'''
This script will remove genomic position of immune and MHC for downstream Tajima'D analysis.
'''
import sys,os
#autosome = sys.argv[2]
def get_immune(immune):
	with open(immune,'r') as infile:
		for line in infile:
			line = line.rstrip()
			tmp_1 = line.split('\t')
			yield tmp_1

large_list = []
with open(sys.argv[2],'r') as inf:
	for line in inf:
		line = line.rstrip()
		tmp = line.split('\t')
		new_tmp = tmp[:3]
		large_list.append(new_tmp)
	for i in get_immune(sys.argv[1]):
		#print(i)
		if i in large_list:
			large_list.remove(i)
		else:
			print(i)
#debug
#print(len(large_list))
#print(large_list)

	

