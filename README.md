# vcfparser

Python parser for parsing the genomics and transcriptomics VCF data.

## Installation  and setup

1. **Clone this repo**

``` bash
git clone https://github.com/everestial/vcfparser
cd vcfparser
```

## Usage

```python
from vcf_parser import VcfParser
# instantiate a vcf object by passing file name
filepath = 'input_test.vcf'
vcf_object = VcfParser(filepath)
```

### Get MetaInfo about the vcf file

```python
metainfo = vcf_object.parse_metadata()
print(f'Fileformat for given vcf is : {metainfo.fileformat}')
print(f'Filters for given vcf are : {metainfo.filters_}')
print(f' Contig lines are : {metainfo.contig}')
print(f' Dictionary of infos is : {metainfo.infos_}')
print(f' Sample names are : {metainfo.sample_names}')
print("Raw lines are:")
print(metainfo.raw_meta_data)
```

## Get Records from vcf file

```python
records = vcf_object.parse_records() # this creates a generator object

for record in records:
    # you can access methods and attributes of record object as
    chrom = record.CHROM
    pos = record.POS
    id = record.ID
    ref = record.REF
    alt = record.ALT
    qual = record.QUAL
    filter = record.FILTER

```
