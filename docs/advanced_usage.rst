
=========================
Tutorial on record parser
=========================

Advanced Tutorial on vcf parser module showing most of the functions.

Let's first import ``VcfParser`` module and instantiate an vcf object by 
passing vcf file as an argument.

Initial setup:
^^^^^^^^^^^^^^

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

We can also pass gzipped vcf file as an argument.

>>> vcf_obj = VcfParser('input_test.vcf.gz')

``VcfParser`` module  has two main methods:
- parse_metadata: It contains information related the header lines 
- parse_records: It contains methods to retrieve record values from the vcf file.


Parsing metadata:
^^^^^^^^^^^^^^^^^

To parse the metadata information:

>>> metainfo = vcf_obj.parse_metadata()

Metainfo provides several attributes/objects to mine. These informations are provided as a list or dictionary.

To list all the available attributes within metainfo, we can write:

>>> metainfo.__dir__()
['header_file', 'infos_', 'filters_', 'contig', 'format_', 'alt_', 'other_lines', 'testA', 'fileformat', 'reference', 'sample_names', 'is_gvcf', 'gvcf_blocks', 'record_keys', 'VCFspec', 'gatk_commands', 'raw_meta_data', '_format_pattern', '_meta_pattern', 'sample_with_pos', '__module__', '__doc__', '__init__', '_parse_gvcf_block', '_parse_gatk_commands', 'parse_lines', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

or we can also give following command:

>>> dir(metainfo) 
['VCFspec', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_format_pattern', '_meta_pattern', '_parse_gatk_commands', '_parse_gvcf_block', 'alt_', 'contig', 'fileformat', 'filters_', 'format_', 'gatk_commands', 'gvcf_blocks', 'header_file', 'infos_', 'is_gvcf', 'other_lines', 'parse_lines', 'raw_meta_data', 'record_keys', 'reference', 'sample_names', 'sample_with_pos', 'testA']

We can also call specific attributes from metainfo like:

>>> metainfo.VCFspec
[{'fileformat': 'VCFv4.2'}, {'GVCF': True}]

>>> metainfo.infos_ 
[{'ID': 'AF', 'Number': 'A', 'Type': 'Float', 'Description': 'Allele Frequency, for each ALT allele, in the same order as listed'}, {'ID': 'BaseQRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities'}, {'ID': 'ClippingRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score From Wilcoxon rank sum test of Alt vs. Ref number of hard clipped bases'}, {'ID': 'DP', 'Number': '1', 'Type': 'Integer', 'Description': 'Approximate read depth; some reads may have been filtered'}, 
{'ID': 'DS', 'Number': '0', 'Type': 'Flag', 'Description': 'Were any of the samples downsampled?'}, {'ID': 'END', 'Number': '1', 'Type': 'Integer', 'Description': 'Stop position of the interval'}, {'ID': 'ExcessHet', 'Number': '1', 'Type': 'Float', 'Description': 'Phred-scaled p-value for exact test of excess heterozygosity'}, {'ID': 'FS', 'Number': '1', 'Type': 'Float', 'Description': "Phred-scaled p-value using Fisher's exact test to detect strand bias"}, {'ID': 'HaplotypeScore', 'Number': '1', 'Type': 'Float', 'Description': 'Consistency of the site with at most two segregating haplotypes'}, {'ID': 'InbreedingCoeff', 'Number': '1', 'Type': 'Float', 'Description': 'Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation'}, {'ID': 'MLEAC', 'Number': 'A', 'Type': 'Integer', 'Description': 'Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed'}, {'ID': 'MLEAF', 'Number': 'A', 'Type': 'Float', 'Description': 'Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed'}, {'ID': 'MQ', 'Number': '1', 'Type': 'Float', 'Description': 'RMS Mapping Quality'}, {'ID': 'MQRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities'}, {'ID': 'QD', 'Number': '1', 'Type': 'Float', 'Description': 'Variant Confidence/Quality by Depth'}, {'ID': 'RAW_MQ', 'Number': '1', 'Type': 'Float', 'Description': 'Raw data for RMS Mapping 
Quality'}, {'ID': 'ReadPosRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias'}, {'ID': 'SOR', 'Number': '1', 'Type': 'Float', 'Description': 'Symmetric Odds Ratio of 2x2 contingency table to detect strand bias'}, {'ID': 'set', 'Number': '1', 'Type': 'String', 'Description': 'Source VCF for the merged record in CombineVariants'}, {'ID': 'SF', 'Number': '.', 'Type': 'String', 'Description': 'Source File (index to sourceFiles, f when filtered)'}, {'ID': 'AC', 'Number': '.', 
'Type': 'Integer', 'Description': 'Allele count in genotypes'}, {'ID': 'AN', 'Number': '1', 'Type': 'Integer', 'Description': 'Total number of alleles in called genotypes'}, {'ID': 'TS', 'Type': 'Test', 'Description': 'Allele count in genotypes'}]

>>> metainfo.record_keys
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

**Note: Similarly other attributes can be called from "metainfo" object**


Accessing VCF records:
^^^^^^^^^^^^^^^^^^^

>>> records = vcf_obj.parse_records() 

Here, records is an generator object and applying next(records) yields the first record and 
we can access methods of ``Record`` class.

>>> first_record = next(records)

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
