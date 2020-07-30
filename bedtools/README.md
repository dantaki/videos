```
#!/bin/sh

# get 1000 genomes omni SNPs
## CONVERT VCF -> BED
grep -v "#" 1000G_omni2.5.b37.sites.vcf  | awk '{ print $1"\t"$2-1"\t"$2"\t"$3"\t"$4"\t"$5 }' >1kgp_omni2.5.hg19.bed

# sort BED file """inplace"""
sort -k1,1 -k2,2n 1kgp_omni2.5.hg19.bed >tmp; mv tmp 1kgp_omni2.5.hg19.bed

# bgzip and tabix to save disk space
bgzip 1kgp_omni2.5.hg19.bed
tabix -p bed 1kgp_omni2.5.hg19.bed.gz

# split bed file by chromosome
zcat 1kgp_omni2.5.hg19.bed.gz | awk '{ print $0 >>"1kgp_omni2.5."$1".hg19.bed" }'
wc -l *hg19.bed | sort -rnk 1

# this file contains regions of the genome
## that make it difficult to map short-reads uniquely too. these segmental
## duplications are scattered throughout the genome and are usually >10kb in length
## and homologs have >90% sequence idenity
##-----------------------------------------
## tl;dr: omit variants that are in segdups

# inplace sort
sort -k1,1 -k2,2n segdup.hg19.bed >tmp; mv tmp segdup.hg19.bed

# merge bed file
mergeBed -i segdup.hg19.bed >segdup.merged.hg19.bed
wc -l segdup.*

# intersect 1kgp omni snps to segdups
## -wa : write entry in A (default report the overlap positions)
## -f 0.5 : write overlaps of 50% of A regions to B regions (default: any overlap)
## -v : report the oppposite (here: A regions that do NOT overlap 50% to B).
### note -v is a nod to grep -v option
intersectBed -a 1kgp_omni2.5.hg19.bed.gz -b segdup.merged.hg19.bed -wa -f 0.5 -v >1kgp_omni2.5.filtered.hg19.bed

# check counts
zcat 1kgp_omni2.5.hg19.bed.gz | wc -l
wc -l 1kgp_omni2.5.filtered.hg19.bed

# get exons from gencode gtf
zcat gencode.v34lift37.annotation.gtf.gz | \
grep "protein_coding" | \
awk '{if($3 == "exon") { print $1"\t"$4-1"\t"$5"\t"$0 }}'  | \
cut -f 1-3,12 | \
sort -k1,1 -k2,2n >gencode_exons.hg19.bed

# remove chr from beginning of file
perl -pi -e 's/^chr//g' gencode_exons.hg19.bed
# bgzip and tabix
bgzip gencode_exons.hg19.bed
tabix -p bed gencode_exons.hg19.bed.gz

# intersect filtered variants to exons
intersectBed -a 1kgp_omni2.5.filtered.hg19.bed -b gencode_exons.hg19.bed.gz -wa -wb -sorted >1kgp_omni2.5.filtered.exonic.hg19.bed
# report overlap to all unique genes
python report_all_exon_overlap.py 1kgp_omni2.5.filtered.exonic.hg19.bed >1kgp_omni2.5.filtered.unique_genes.bed
# make a UCSC genome browser track
less 1kgp_omni2.5.filtered.unique_genes.bed | cut -f 1-4 >1kgp_omni2.5.filtered.unique_genes.ucsc.bed
# add the chr prefix
perl -pi -e 's/^/chr/g' 1kgp_omni2.5.filtered.unique_genes.ucsc.bed
```
