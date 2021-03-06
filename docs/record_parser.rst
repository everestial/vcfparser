
.. _record-parser-tutorial:

.. TODO (Bhuwan, Gopal-Done, priority - high): introduce line break between documentation paragraphs.
.. Line breaks are introduced by using "|  " or using a new line or setting up a main.rst file with settings

=========================
Tutorial on record parser
=========================

Advanced tutorial on vcf parser module showing available methods for parsing records.

First import :py:class:`~vcfparser.vcf_parser.VcfParser` module and instantiate an vcf object by 
passing vcf file as an argument.

Initial setup:
^^^^^^^^^^^^^^

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

.. TODO (Bhuwan, Gopal-Done; priority - high) - check the gzipped file read/write works on both Linux and Windows

|  We can also pass gzipped vcf file as an argument.  

>>> vcf_obj = VcfParser('input_test.vcf.gz')

|

:py:class:`~vcfparser.vcf_parser.VcfParser` module  has two main methods:
  - **parse_metadata:** to extract the metadata information from VCF metadata header.
  - **parse_records:** to retrieve the record values from the VCF record lines.


Accessing VCF records:
^^^^^^^^^^^^^^^^^^^^^^

**Step 01:**  

>>> # pass the VCF object to the 'parse_records()' function
>>> records = vcf_obj.parse_records() 

|  

**Step 02:**  

**Yield record values - Method A: using next()**

  - records is an generator object. Therefore, applying ``next(records)`` yields the very first record as Record object. 
  - Subsequent ``next(records)`` will yield subsequent records after that first record from the VCF.  
  - :py:meth:`~vcfparser.vcf_parser.VcfParser.parse_records()` uses the :py:class:`~vcfparser.record_parser.Record` class which can be used directly if ``record_keys`` and ``record_vals`` are handy. 

For more info about Record visit :py:class:`~vcfparser.record_parser.Record`.

.. TODO: Done Hyperlink the word ``Record`` (above), so it takes us to the 'Record' class documentation.

>>> first_record = next(records)
>>> print(first_record)
2       15881224        .       T       G       143.24  PASS    AC=0;AF=0.036;AN=12;BaseQRankSum=1.75;ClippingRankSum=0.00;DP=591;ExcessHet=3.0103;FS=3.522;InbreedingCoeff=-0.1072;MLEAC=1;MLEAF=0.036;MQ=41.48;MQRankSum=0.366;QD=15.92;ReadPosRankSum=0.345;SF=0,1,2,3,4,5,6;SOR=2.712;set=HignConfSNPs   GT:PM:PG:GQ:AD:PW:PI:PL:PC:PB:DP       ./.:.:./.:.:0:./.:.:.,.,.:.:.:0 0/0:.:0/0:3:1:0/0:.:.,.,.:.:.:1        0/0:.:0/0:12:4:0/0:.:.,.,.:.:.:4        0/0:.:0/0:3:4:0/0:.:.,.,.:.:.:4        0/0:.:0/0:30:17,0:0/0:.:0,30,450:.:.:17 0/0:.:0/0:15:7,0:0/0:.:0,15,225:.:.:7  0/0:.:0/0:39:25,0:0/0:.:0,39,585:.:.:25

|  

**Yield record values - Method B: using for-loop**

Each record in the VCF can also be accessed on a for-loop 

>>> for record in records:
...     print(record)
...     record.POS
...     break
... 
2       15881018        .       G       A,C     5082.45 PASS    AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs     
        GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC        0/1:5:.:0|1:.:./.:0,0:0,0,0,.,.,.:0:.:.        ./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:. ./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.        1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.        0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.        0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.        0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.
'15881018'

|  

**Step 03: Extract data using Record object attribute and methods**

Record object also has several attributes and methods which allows us to extract the record values as list or dictionary.

>>> " list of available attribute and methods "
>>> dir(first_record)  # or print(dir(record)) on a for loop 
['ALT', 'CHROM', 'FILTER', 'ID', 'POS', 'QUAL', 'REF', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_map_fmt_to_samples', '_to_iupac', 'deletion_overlapping_variant', 'format_', 'get_info_as_dict', 'get_mapped_samples', 'get_mapped_tag_list', 'hasAllele', 
'hasINDEL', 'hasSNP', 'hasVAR', 'has_phased', 'has_unphased', 'hasnoVAR', 'info_str', 'isHETVAR', 'isHOMREF', 'isHOMVAR', 'isMissing', 'iupac_to_numeric', 'map_records_long', 'mapped_format_to_sample', 'rec_line', 'record_keys', 'record_vals', 'ref_alt', 'sample_names', 'sample_vals', 'get_tag_values_from_samples', 'unmap_fmt_samples_dict', 'vTest']

|

**Attributes**

>>> # available attributes in the "record" object are: 
CHROM, POS, REF, ALT, ref_alt, QUAL, FILTER, info_str, format_, sample_names, sample_vals, mapped_format_to_sample

|  

>>> "Access simple position level attribute values as"
>>> first_record.CHROM
'2'
>>> first_record.POS 
'15881018'
>>> first_record.REF, first_record.ALT, first_record.QUAL, first_record.FILTER
('G', ['A', 'C'], '5082.45', ['PASS'])
>>> first_record.ref_alt  # call REF and ALT allele together
['C', 'CA']

|  

>>> # keys represented in the "CHROM" line of the VCF
>>> first_record.record_keys
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
>>> # Note: "record_keys" available within record object are same as the one from metainfo object.
>>> metainfo.record_keys  # from "parse_metadata()"
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
>>> 
>>> first_record.record_values  # record values as list
['2', '15881018', '.', 'G', 'A,C', '5082.45', 'PASS', 'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs', 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.']


|  

>>> "Population level information is provided by the INFO key"
>>> # accessed using 'info_str'
>>> first_record.info_str   # info values as string
'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs'

|  

>>> "Sample level infomation are extracted by matching the FORMAT tags with their corresponding values in the SAMPLE"
>>> first_record.format_  # available tags in FORMAT
['GT', 'PI', 'GQ', 'PG', 'PM', 'PW', 'AD', 'PL', 'DP', 'PB', 'PC']

|

>>> first_record.sample_names  # sample names
['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

|

>>> first_record.sample_vals  # sample values as list
['./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.']

|

>>> # a default full map of the FORMAT tags to SAMPLE values
>>> first_record.mapped_format_to_sample 
OrderedDict([('ms01e', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 
'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms02g', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms03g', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('ms04h', {'GT': '.', 'AD': '.', 'PI': '.', 'PW': '.', 'PG': '.', 'PM': '.', 'GQ': '.', 'DP': '.', 'PB': '.', 'PC': '.', 'PL': '.'}), ('MA611', {'GT': '0/0', 'AD': '20,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '54', 'DP': '20', 'PB': '.', 'PC': '.', 'PL': '0,54,810'}), ('MA605', 
{'GT': '0/0', 'AD': '6,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '18', 'DP': '6', 'PB': '.', 'PC': '.', 'PL': '0,18,206'}), ('MA622', {'GT': '0/0', 'AD': '27,0', 'PI': '.', 'PW': '0/0', 'PG': '0/0', 'PM': '.', 'GQ': '72', 'DP': '27', 'PB': '.', 'PC': '.', 'PL': '0,72,1080'})])

|  

**Methods on record object**

Very specific parsing of the record object can be done using the provided methods.
These methods take several args and kwargs to narrow down the information available in the :py:class:`~vcfparser.record_parser.Record` object.

|

>>> "Parse the INFO string data using get_info_as_dict()"
>>> first_record.info_str   # the original info values as string
'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs'
>>> first_record.get_info_as_dict() # info values as dictionary 
{'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}

|

>>> # info_keys can be provided extract specific keys:value
>>> first_record.get_info_as_dict(info_keys= ['AC', 'AF'])
{'AC': '2,0', 'AF': '1.00'}

|

>>> "More controlled FORMAT tag to SAMPLE value mapping can be done using get_format_to_sample_map()"
>>> # it helps to extract specific FORMAT tag values from specific SAMPLE
>>> first_record.get_format_to_sample_map(sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'])       
{'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}}

|

>>> "the mapped genotype values can be converted to IUPAC bases using the convert_to_iupac flag"
>>> first_record.get_format_to_sample_map(sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'], convert_to_iupac=['GT'])
{'ms01e': {'GT': './.', 'PC': '.', 'GT_iupac': './.'}, 'MA611': {'GT': '0/0', 'PC': '.', 'GT_iupac': 'G/G'}}
>>> first_record.get_format_to_sample_map(sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'], convert_to_iupac=['GT', 'PG']) 
{'ms01e': {'GT': './.', 'PC': '.', 'GT_iupac': './.', 'PG_iupac': './.'}, 'MA611': {'GT': '0/0', 'PC': '.', 'GT_iupac': 'G/G', 'PG_iupac': 'G/G'}}

|

>>> # get a full mapping for all the record_keys and FORMAT within SAMPLE
>>> # Note: This mapping is only activated when called with lazy instantiation 

.. # TODO (Bhuwan, Bishwa) - 
   # does "get_full_record_map()" only run computation after requested? 
   # if not - add "get_full_record_map()" as lazy instantiation/call?? 
   # Used this examples if need be:
  .. https://stackoverflow.com/questions/15226721/python-class-member-lazy-initialization 
  .. http://theorangeduck.com/page/lazy-python 
  .. https://stackoverflow.com/questions/7151890/python-lazy-variables-or-delayed-expensive-computation

>>> first_record.get_full_record_map()
{'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'}}}

|

>>> # full mapping has the option to convert genotype bases to IUPAC
>>> first_record.get_full_record_map(convert_to_iupac= ['GT'])
{'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.', 'GT_iupac': './.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.', 'GT_iupac': './.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.', 'GT_iupac': './.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.', 'GT_iupac': 'A/A'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.', 'GT_iupac': 'G/G'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.', 'GT_iupac': 'G/G'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.', 'GT_iupac': 'G/G'}}}
>>> # Note: "convert_to_iupac" will add the genotype tag with suffix "_iupac" to show the genotype in IUPAC bases. 

|  

**Genotype parsing**

Genotype checks and parsing are one of most important use case of VCF data. 
:py:class:`~vcfparser.vcf_parser.VcfParser` provides several methods to do those checks and extract data. 

  - Check samples that have alleles of your interest.

|

>>> first_record.hasAllele(allele='1', tag= 'GT', bases = 'iupac')
{'ms04h': 'A/A'}

|

>>> first_record.hasAllele(allele='1', tag= 'GT', bases = 'numeric')
{'ms04h': '1/1'}

|

>>> first_record.hasAllele(allele='1', tag= 'PG', bases = 'numeric')
{'ms04h': '1/1'}

|

>>> first_record.hasAllele(allele='0', tag= 'PG', bases = 'numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}

|

>>> first_record.hasAllele(allele='0', tag= 'PG', bases = 'iupac')
{'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

.. TODO (Bhuwan, priority - high): Fix this issue 
  The output should come if hasAllele is requesting and IUPAC allele. 
  >>> first_record.hasAllele(allele='A', tag= 'GT', bases = 'iupac') 
  {}  # output should be {'ms04h': 'A/A'}
  >>> first_record.hasAllele(allele='A', tag= 'GT', bases = 'numeric') 
  {}  # output should be {'ms04h': '1/1'}

|

  - Check samples with specific genotype. Both numeric and iupac checks are available. 

>>> first_record.hasVAR(genotype='0/0', tag= 'PG', bases = 'numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.hasVAR(genotype='G/G', tag= 'PG', bases = 'iupac')
{'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}
>>> first_record.hasVAR(genotype='1/1', tag= 'PG', bases = 'numeric')
{'ms04h': '1/1'}
>>> first_record.hasVAR(genotype='A/A', tag= 'PG', bases = 'iupac')
{'ms04h': 'A/A'}

|

>>> # genotypes can be checked in phased state 
>>> first_record.hasVAR(genotype='0|0', tag='GT', bases='numeric')  
{}

| 

  - Check phased vs unphased genotype. Specific genotype tag can be checked; default is 'GT'.

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

|  

  - Return samples with no variants (i.e. contains './.', '.|.', '.') 

>>> first_record.hasnoVAR()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
>>> first_record.hasnoVAR(tag='GT')                                
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.'}
>>> first_record.hasnoVAR(tag= 'PG')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}

|  

  - Samples with homozygous reference genotypes can be retrieved as.

>>> first_record.isHOMREF(tag='GT', bases='numeric')                                                       
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.isHOMREF(tag='GT', bases='iupac')   
{'MA611': 'C/C', 'MA605': 'C/C', 'MA622': 'C/C'}

|

>>> #if another FORMAT tag also represents a genotype, specific the FORMAT tag
>>> first_record.isHOMREF(tag='PG', bases='numeric')
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.isHOMREF(tag='PG', bases='iupac')                                                         
{'MA611': 'C/C', 'MA605': 'C/C', 'MA622': 'C/C'}

|  

  - Similarly, samples with homozygous variant genotypes can also be retrieved.

>>> first_record.isHOMVAR()
{'ms04h': '1/1'}
>>> first_record.isHOMVAR(tag= 'PG', bases= 'iupac')
{'ms04h': 'A/A'}

|  

  - Samples with heterozygous variant genotypes in given record"

>>> first_record.isHETVAR()
{}

|  

  - This returns samples with missing variants for certain FORMAT tags(i.e. contains './.', '.|.', '.'). Currently we used 'GT' tag as default.  

>>> first_record.isMissing()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}

|

>>> # missing checks can be applied to other FORMAT tags too.
>>> first_record.isMissing(tag = 'PI')
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.', 'MA611': '.', 'MA605': '.', 'MA622': '.'}

|

>>> first_record.isMissing(tag='GQ') 
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.'}

