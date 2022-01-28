import sys,os
def correct(gt):
	GT,PL,DP,AD = gt.split(':')
	if GT == '0/1':
		ref_alle, alt_alle = gt.split(':')[-1].split(",")
		if int(ref_alle)/int(DP) < 0.2 or int(alt_alle)/int(DP) < 0.2 or int(DP) <= 5:
			return ':'.join(['./.', PL, DP, AD])
		else:
			return ':'.join([GT, PL, DP, AD])
	else:
		return ':'.join([GT, PL, DP, AD])

with open(sys.argv[1],'r') as infile:
	for line in infile:
		line = line.rstrip('\n')
		if line.startswith('#'):
			print(line)
		else:
			Info = line.split('\t')[:9]
			indvs = line.split('\t')[9:]
			print('\t'.join(Info), end = '\t')
			for i in range(len(indvs)):
				if i < len(indvs) - 1:
					print(correct(indvs[i]), end = '\t')
				else:
					print(correct(indvs[i]))



			

