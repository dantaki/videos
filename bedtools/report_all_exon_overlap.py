#!/usr/bin/env python3
from collections import defaultdict
import sys
"""
the basic idea here is to create a data structure 
where a variant can point to all the genes it overlaps to
use a dictionary of dictionarys to store each overlap
  
  dict[variant] --> gene[gene_name]=number_of_exons_overlapped

note this would be more useful for CNV/SV calls that can span multiple genes
"""
infh = sys.argv[1]
# dictionary of dictionaries
ovr = defaultdict(dict)

with open(infh,'r') as f:
	for l in f:
		row = l.rstrip().split('\t')
		# here the key will be a string
		## tab delimited "chrom start end snp ref alt"
		variant = '\t'.join(row[0 : 6])
		# lazy debugging
		# print(variant)
		
		# parse the gene name from the last row entry
		## convert this info column into a dictionary
		## info[gene_name]->"SAMD11"
		info={}
		for x in row[-1].split(';'):
			# remove double quotes
			x=x.replace('"','')
			# convoluted list comprehension to remove empty ('') elements
			i = [y for y in x.split(' ') if y != ''] 
			# only process key->value pairs
			if len(i)==2: 
				info[i[0]]=i[1]
		# skip overlap if there is no gene_name
		if info.get('gene_name')==None: continue
		gene_name = info['gene_name']
		#print(variant,gene_name)
		
		# load the overlap dictionary
		if ovr[variant].get(gene_name)==None: 
			ovr[variant][gene_name]=1
		else: ovr[variant][gene_name]+=1

for variant in ovr:
	genes = ovr[variant].keys()
	# join by comma
	genes = ','.join(list(genes))
	"""
	# if you wanted to we could load the counts too
	counts = [] 
	for g  in ovr: counts.append(ovr[variant][g])
	"""
	# print out variant and genes
	out = '\t'.join((variant,genes))
	print(out)	
