
.. _metadata-tutorial:

.. TODO (Bhuwan, Gopal, priority - high): introduce line break between documentation paragraphs.

=========================
Tutorial on MetaData
=========================

Advanced tutorial on vcf parser module showing available methods for parsing metadata.

First import :py:class:`~vcfparser.vcf_parser.VcfParser` module and instantiate an vcf object by 
passing vcf file as an argument.


Initial setup:
^^^^^^^^^^^^^^

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

We can also pass gzipped vcf file as an argument.

>>> vcf_obj = VcfParser('input_test.vcf.gz')

|

:py:class:`~vcfparser.vcf_parser.VcfParser` **module  has two main methods:** 

    - **parse_metadata:** It contains methods for extracting information related to the metadata header. 
    - **parse_records:** It contains methods for retrieving the record values from the vcf file.


Parsing VCF metadata:
^^^^^^^^^^^^^^^^^^^^^

To parse the metadata information we can call :py:meth:`~vcfparser.vcf_parser.VcfParser.parse_metadata()`:

>>> # pass the VCF object to the 'parse_metadata()' function
>>> metainfo = vcf_obj.parse_metadata()

|

  - Metainfo provides several attributes and objects that helps in extracting specific metadata information. 
  - These informations are reported as a list or dictionary.

|  

To list all the available attributes within metainfo do:

>>> metainfo.__dir__()
['header_file', 'infos_', 'filters_', 'contig', 'format_', 'alt_', 'other_lines', 'fileformat', 'reference', 'sample_names', 'is_gvcf', 'gvcf_blocks', 'record_keys', 'VCFspec', 'gatk_commands', 'raw_meta_data', '_format_pattern', '_meta_pattern', 'sample_with_pos', '__module__', '__doc__', '__init__', '_parse_gvcf_block', '_parse_gatk_commands', 'parse_lines', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
>>> # or
>>> dir(metainfo) 
['VCFspec', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_format_pattern', '_meta_pattern', '_parse_gatk_commands', '_parse_gvcf_block', 'alt_', 'contig', 'fileformat', 'filters_', 'format_', 'gatk_commands', 'gvcf_blocks', 'header_file', 'infos_', 'is_gvcf', 'other_lines', 'parse_lines', 'raw_meta_data', 'record_keys', 'reference', 'sample_names', 'sample_with_pos', 'testA']

|  

To call the specific objects and attributes do:

>>> metainfo.VCFspec
[{'fileformat': 'VCFv4.2'}, {'GVCF': True}]

|

>>> metainfo.infos_ 
[{'ID': 'AF', 'Number': 'A', 'Type': 'Float', 'Description': 'Allele Frequency, for each ALT allele, in the same order as listed'}, {'ID': 'BaseQRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities'}, {'ID': 'ClippingRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score From Wilcoxon rank sum test of Alt vs. Ref number of hard clipped bases'}, {'ID': 'DP', 'Number': '1', 'Type': 'Integer', 'Description': 'Approximate read depth; some reads may have been filtered'}, 
{'ID': 'DS', 'Number': '0', 'Type': 'Flag', 'Description': 'Were any of the samples downsampled?'}, {'ID': 'END', 'Number': '1', 'Type': 'Integer', 'Description': 'Stop position of the interval'}, {'ID': 'ExcessHet', 'Number': '1', 'Type': 'Float', 'Description': 'Phred-scaled p-value for exact test of excess heterozygosity'}, {'ID': 'FS', 'Number': '1', 'Type': 'Float', 'Description': "Phred-scaled p-value using Fisher's exact test to detect strand bias"}, {'ID': 'HaplotypeScore', 'Number': '1', 'Type': 'Float', 'Description': 'Consistency of the site with at most two segregating haplotypes'}, {'ID': 'InbreedingCoeff', 'Number': '1', 'Type': 'Float', 'Description': 'Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation'}, {'ID': 'MLEAC', 'Number': 'A', 'Type': 'Integer', 'Description': 'Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed'}, {'ID': 'MLEAF', 'Number': 'A', 'Type': 'Float', 'Description': 'Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed'}, {'ID': 'MQ', 'Number': '1', 'Type': 'Float', 'Description': 'RMS Mapping Quality'}, {'ID': 'MQRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities'}, {'ID': 'QD', 'Number': '1', 'Type': 'Float', 'Description': 'Variant Confidence/Quality by Depth'}, {'ID': 'RAW_MQ', 'Number': '1', 'Type': 'Float', 'Description': 'Raw data for RMS Mapping 
Quality'}, {'ID': 'ReadPosRankSum', 'Number': '1', 'Type': 'Float', 'Description': 'Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias'}, {'ID': 'SOR', 'Number': '1', 'Type': 'Float', 'Description': 'Symmetric Odds Ratio of 2x2 contingency table to detect strand bias'}, {'ID': 'set', 'Number': '1', 'Type': 'String', 'Description': 'Source VCF for the merged record in CombineVariants'}, {'ID': 'SF', 'Number': '.', 'Type': 'String', 'Description': 'Source File (index to sourceFiles, f when filtered)'}, {'ID': 'AC', 'Number': '.', 
'Type': 'Integer', 'Description': 'Allele count in genotypes'}, {'ID': 'AN', 'Number': '1', 'Type': 'Integer', 'Description': 'Total number of alleles in called genotypes'}, {'ID': 'TS', 'Type': 'Test', 'Description': 'Allele count in genotypes'}]

|

>>> metainfo.record_keys
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
