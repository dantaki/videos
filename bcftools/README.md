# bcftools
-----------

[bcftools](https://samtools.github.io/bcftools/bcftools.html)

[expressions](https://samtools.github.io/bcftools/bcftools.html#expressions)

Sudmant et al. 2015
[1000 Genomes SV VCF](ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz)
[1000 Genomes SV VCF Tabix index](ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz.tbi)

* [view](https://github.com/dantaki/videos/tree/master/bcftools#view)
* [query](https://github.com/dantaki/videos/tree/master/bcftools#query)

------------------------

## view

View opens a VCF file.

```
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz
```

There are tons of options and filters

```
# output in bgzip format
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -Oz

# restrict to a sample
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -s NA12878

# use a file of samples, one per line
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -S samples.txt
```

Subset VCF to a region

```
# all variants on chromosome 22
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -r 22

# variants on chromosomes 21 and 22
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -r 21,22

# variants between positions 13Mb to 14Mb on chromosome 1
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -r 1:13000000-14000000

# chain two or more regions with commas
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -r 1:13000000-14000000,2:40000000-41000000

# can combine regions and chromosomes
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -r 1:13000000-14000000,2:40000000-41000000,3
```

Subset VCF to many regions using a BED file or similar file
```
# use a BED file (must end with .bed and be 0-base positions)
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -R regions.bed

# use a "regions" file, similar format to BED but 1-base position
bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -R regions_1base.txt
```

You can use expressions to filter variants

https://samtools.github.io/bcftools/bcftools.html#expressions

```
# get variants with PASS in the FILTER column

bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -i'FILTER=="PASS"'

# parse out information from the INFO column
# get variants with SVTYPE=="DEL"

bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -i'INFO/SVTYPE=="DEL"'

# remove variants with any missing genotypes ("." or "./." or ".|." or "./0")
# the ~ is a matches operator, different from ==

bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -e'GT~"\."'

# print variants where the number of ALT alleles is the cohort is equal to 1
## in other words, one person is 0/1 and the rest are 0/0

bcftools view ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz -i'AC==1'



----------------

## query

Query is a tool that allows you to re-format the VCF into a text file for analysis

Common operations include

* convert a VCF of SVs into a BED file

```
bcftools query -f'%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\n' ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz
```

# only look at DEL
bcftools query -f'%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\n' -i'INFO/SVTYPE=="DEL"' ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz


# get genotypes for each sample, one-per-line
bcftools query -f'[%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\t%SAMPLE\t%GT\n]' -i'INFO/SVTYPE=="DEL"' ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz

# get genotypes for NA12878 but only ALT variants
bcftools query -f'[%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\t%SAMPLE\t%GT\n]' -i'GT=="ALT"' -s NA12878 ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz

# get genotypes for NA12878 but only ALT homozygous variants (1/1)
bcftools query -f'[%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\t%SAMPLE\t%GT\n]' -i'GT=="AA"' -s NA12878 ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz

# same as above, but you might need to change | for / depending on your VCF
bcftools query -f'[%CHROM\t%POS0\t%INFO/END\t%INFO/SVTYPE\t%SAMPLE\t%GT\n]' -i'GT=="1|1"' -s NA12878 ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz

```

* print out all the sample names

```
bcftools query -l ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz
```
