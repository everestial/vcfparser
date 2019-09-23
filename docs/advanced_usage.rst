
=========================
Tutorial on record parser
=========================

Advanced Tutorial on vcf parser module showing most of the functions.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Let's first import ``VcfParser`` module and instantiate an vcf object by 
passing vcf file as an argument.

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

``VcfParser`` module  has two main methods:
- parse_metadata: It contains information related the header lines 
- parse_records: It contains methods to retrieve record values from the vcf file.

>>> metainfo = vcf_obj.parse_metadata()
>>> records = vcf_obj.parse_records() 

Here, records is an generator object and applying next(records) yields the first record and 
we can access methods of ``Record`` class.

>>> first_record = next(records)

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

To check if samples have phased genotype or unphased genotype:

>>> first_record.has_phased()
{}
>>> first_record.has_unphased()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.has_unphased(tag= 'PG')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.has_unphased(tag= 'PG', bases = 'iupac')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': 'A/A', 'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

This returns samples with no variants (i.e. contains './.', '.|.', '.') 

>>> first_record.hasnoVAR()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
>>> first_record.hasnoVAR(tag= 'PG')
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}

Samples with homozygous reference genotypes can be retrieved by:

>>> first_record.isHOMREF()
{'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
>>> first_record.isHOMREF(tag= 'PG', bases= 'iupac')
{'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

Similarly, samples with homozygous variant genotypes can be retrieved by:

>>> first_record.isHOMVAR()
{'ms04h': '1/1'}
>>> first_record.isHOMVAR(tag= 'PG', bases= 'iupac')
{'ms04h': 'A/A'}

Samples with heterozygous variant genotypes in given record"

>>> first_record.isHETVAR()
{}

This returns samples with missing variants (i.e. contains './.', '.|.', '.') 

>>> first_record.isMissing()
{'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
>>> first_record.isMissing(tag = 'PI')
{'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.', 'MA611': '.', 'MA605': '.', 'MA622': '.'}

map_records_long method maps all the record with the header lines. This also maps format with samples and
info fields into dictionary.

>>> first_record.map_records_long()
{'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'}}}
