
=========================
Tutorial on record parser
=========================

Advanced tutorial on vcf parser module showing most of the functions.

Let's first import ``VcfParser`` module and instantiate an vcf object by 
passing vcf file as an argument.

Initial setup:
^^^^^^^^^^^^^^

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

We can also pass gzipped vcf file as an argument.

>>> vcf_obj = VcfParser('input_test.vcf.gz')

| 

``VcfParser`` module  has two main methods:
  - **parse_metadata:** to extract the information from VCF metadata header.
  - **parse_records:** to retrieve the record values from the vcf file.


Accessing VCF records:
^^^^^^^^^^^^^^^^^^^^^^

>>> records = vcf_obj.parse_records() 

Here, records is an generator object and applying next(records) yields the first record and 
we can access methods of ``Record`` class.

>>> first_record = next(records)
>>> print(first_record)
2       15881224        .       T       G       143.24  PASS    AC=0;AF=0.036;AN=12;BaseQRankSum=1.75;ClippingRankSum=0.00;DP=591;ExcessHet=3.0103;FS=3.522;InbreedingCoeff=-0.1072;MLEAC=1;MLEAF=0.036;MQ=41.48;MQRankSum=0.366;QD=15.92;ReadPosRankSum=0.345;SF=0,1,2,3,4,5,6;SOR=2.712;set=HignConfSNPs   GT:PM:PG:GQ:AD:PW:PI:PL:PC:PB:DP       ./.:.:./.:.:0:./.:.:.,.,.:.:.:0 0/0:.:0/0:3:1:0/0:.:.,.,.:.:.:1        0/0:.:0/0:12:4:0/0:.:.,.,.:.:.:4        0/0:.:0/0:3:4:0/0:.:.,.,.:.:.:4        0/0:.:0/0:30:17,0:0/0:.:0,30,450:.:.:17 0/0:.:0/0:15:7,0:0/0:.:0,15,225:.:.:7  0/0:.:0/0:39:25,0:0/0:.:0,39,585:.:.:25

Record_keys are also available within record object.
**Note: The record_keys provided by metainfo object and the record object are the same**

>>> print(first_record.record_keys) 
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

Record also has several attributes available to extract the record values as list or dictionary.

>>> dir(first_record)
['ALT', 'CHROM', 'FILTER', 'ID', 'POS', 'QUAL', 'REF', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_map_fmt_to_samples', '_to_iupac', 'deletion_overlapping_variant', 'format_', 'get_info_dict', 'get_mapped_samples', 'get_mapped_tag_list', 'hasAllele', 
'hasINDEL', 'hasSNP', 'hasVAR', 'has_phased', 'has_unphased', 'hasnoVAR', 'info_str', 'isHETVAR', 'isHOMREF', 'isHOMVAR', 'isMissing', 'iupac_to_numeric', 'map_records_long', 'mapped_sample', 'rec_line', 'record_keys', 'record_vals', 'ref_alt', 'sample_names', 'sample_vals', 'split_tag_from_samples', 'unmap_fmt_samples_dict', 'vTest']

Each subsequent record can also be accessed on a for-loop 

>>> for record in records:
...     print(record)
...     record.POS
...     break
... 
2       15881018        .       G       A,C     5082.45 PASS    AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs     
        GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC        0/1:5:.:0|1:.:./.:0,0:0,0,0,.,.,.:0:.:.        ./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:. ./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.        1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.        0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.        0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.        0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.

'15881018'

**Note: Following attributes from the "record" object can be called directly.**

CHROM, POS, REF, ALT, ref_alt, QUAL, FILTER, info_str, format_, sample_names, sample_vals, mapped_sample

It should return the vcf record header.

>>> first_record = next(records)                                 
>>> first_record.record_keys 

It should return the value for the record keys.

>>> first_record.record_vals

For convenience "record_keys" can be accessed in each loop.

>>> first_record.record_keys    
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

To generate the record values of a particular record line as a list.

>>> first_record.record_vals
['2', '15881106', '.', 'C', 'CA', '33.32', 'PASS', 'AC=0;AF=0.042;AN=6;BaseQRankSum=0.253;ClippingRankSum=0.00;DP=654;ExcessHet=3.0103;FS=0.000;InbreedingCoeff=-0.0469;MLEAC=1;MLEAF=0.042;MQ=60.00;MQRankSum=0.00;QD=6.66;ReadPosRankSum=0.253;SF=4,5,6;SOR=0.223;set=HignConfSNPs', 'GT:AD:PI:PW:PG:PM:GQ:DP:PB:PC:PL', '.', '.', '.', '.', '0/0:20,0:.:0/0:0/0:.:54:20:.:.:0,54,810', '0/0:6,0:.:0/0:0/0:.:18:6:.:.:0,18,206', '0/0:27,0:.:0/0:0/0:.:72:27:.:.:0,72,1080']

**Note: all the remaining example of data extraction is based on this record value**

The record object containts several attributes and functions to further parse the record using several function.

>>> first_record.sample_names
['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

Generate the mapped FORMAT tags to SAMPLE.

>>> first_record.mapped_sample
OrderedDict([('ms01e', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 
'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms02g', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms03g', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms04h', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('MA611', {'GT': '0/0', 'AD': '20,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '54', 'DP': '20', 'PB': '.', 'PC': '.', 'PL': '0,54,810'}), ('MA605', 
{'GT': '0/0', 'AD': '6,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '18', 'DP': '6', 'PB': '.', 'PC': '.', 'PL': '0,18,206'}), ('MA622', {'GT': '0/0', 'AD': '27,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '72', 'DP': '27', 'PB': '.', 'PC': '.', 'PL': '0,72,1080'})])


Generate REF and ALT allele together.

>>> first_record.ref_alt
['C', 'CA']

Methods on record object
^^^^^^^^^^^^^^^^^^^^^^^^

You can filter infos you want from vcf. By default, all info will be returned as dictionary.

>>> first_record.get_info_dict()
{'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}
>>> first_record.get_info_dict(required_keys= ['AC', 'AF'])
{'AC': '2,0', 'AF': '1.00'}

Similarly, you can also filter formats and samples of interest from records. This allows you to 
retrieve the fields that you need.

>>> first_record.get_mapped_samples(sample_names= ['ms01e', 'MA611'], formats= ['GT','PG', 'PC', 'PI'])
{'ms01e': {'GT': './.', 'PG': './.', 'PC': '.', 'PI': '.'}, 'MA611': {'GT': '0/0', 'PG': '0/0', 'PC': '.', 'PI': '.'}}
>>> first_record.get_mapped_samples( formats= ['GT','PG'])
{'ms01e': {'GT': './.', 'PG': './.'}, 'ms02g': {'GT': './.', 'PG': './.'}, 'ms03g': {'GT': './.', 'PG': './.'}, 'ms04h': {'GT': '1/1', 'PG': '1/1'}, 'MA611': {'GT': '0/0', 'PG': '0/0'}, 'MA605': {'GT': '0/0', 'PG': '0/0'}, 'MA622': {'GT': '0/0', 'PG': '0/0'}}
>>> first_record.get_mapped_samples(sample_names =['ms02g'])
{'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}}


You can parse the FORMAT-SAMPLE fields like:

>>> first_record.split_tag_from_samples(mapped_data, tag = 'GT', sample_names = ['ms01e', 'ms02g']) 
[['.'], ['.']]

>>> first_record.split_tag_from_samples(mapped_data, tag = 'GQ', sample_names = ['ms01e', 'ms02g', 'MA622'])  
[['.'], ['.'], ['72']]

You can also check if any sample have alleles of your interest.

>>> first_record.hasAllele(allele='1', tag= 'GT', bases = 'iupac')
{'ms04h': 'A/A'}
>>> first_record.hasAllele(allele='1', tag= 'GT', bases = 'numeric')
{'ms04h': '1/1'}
>>> first_record.hasAllele(allele='1', tag= 'PG', bases = 'numeric')
{'ms04h': '1/1'}
>>> first_record.hasAllele(allele='0', tag= 'PG', bases = 'numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.hasAllele(allele='0', tag= 'PG', bases = 'iupac')
{'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

To check if samples mapped with format tags contains genotype specified :

>>> first_record.hasVAR(genotype='0/0', tag= 'PG', bases = 'numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.hasVAR(genotype='G/G', tag= 'PG', bases = 'iupac')
{'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}
>>> first_record.hasVAR(genotype='1/1', tag= 'PG', bases = 'numeric')
{'ms04h': '1/1'}
>>> first_record.hasVAR(genotype='A/A', tag= 'PG', bases = 'iupac')
{'ms04h': 'A/A'}

We can also query genotype in phased state.

>>> first_record.hasVAR(genotype='0|0', tag='GT', bases='numeric')  
{}
>>> first_record.hasVAR(genotype='0/0', tag='GT', bases='iupac')
{}

To check if samples have phased genotype or unphased genotype:

>>> first_record.has_phased()
{}
>>> first_record.has_unphased()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.has_unphased(tag= 'PG')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.has_unphased(tag='PG', bases='numeric') 
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.has_unphased(tag= 'PG', bases = 'iupac')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': 'A/A', 'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

This returns samples with no variants (i.e. contains './.', '.|.', '.') 

>>> first_record.hasnoVAR()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
>>> first_record.hasnoVAR(tag='GT')                                
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.'}
>>> first_record.hasnoVAR(tag= 'PG')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}

Samples with homozygous reference genotypes can be retrieved by:

>>> first_record.isHOMREF(tag='GT', bases='numeric')                                                       
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.isHOMREF(tag='GT', bases='iupac')   
{'MA611': 'C/C', 'MA605': 'C/C', 'MA622': 'C/C'}

If another FORMAT tag also represents a genotype:

>>> first_record.isHOMREF(tag='PG', bases='numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.isHOMREF(tag='PG', bases='iupac')                                                         
{'MA611': 'C/C', 'MA605': 'C/C', 'MA622': 'C/C'}

Similarly, samples with homozygous variant genotypes can be retrieved by:

>>> first_record.isHOMVAR()
{'ms04h': '1/1'}
>>> first_record.isHOMVAR(tag= 'PG', bases= 'iupac')
{'ms04h': 'A/A'}

Samples with heterozygous variant genotypes in given record"

>>> first_record.isHETVAR()
{}

This returns samples with missing variants for certain FORMAT tags(i.e. contains './.', '.|.', '.'). Currently we used 'GT' tag as default.  

>>> first_record.isMissing()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}

Other tags can be specified as well like following:

>>> first_record.isMissing(tag = 'PI')
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.', 'MA611': '.', 'MA605': '.', 'MA622': '.'}

>>> first_record.isMissing(tag='GQ') 
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.'}
map_records_long method maps all the record with the header lines. This also maps format with samples and
info fields into dictionary.

>>> first_record.map_records_long()
{'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'}}}
