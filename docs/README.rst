==========
vcfparser
==========


.. image:: https://img.shields.io/pypi/v/vcfparser.svg
        :target: https://pypi.python.org/pypi/vcfparser

.. image:: https://img.shields.io/travis/everestial/vcfparser.svg
        :target: https://travis-ci.org/everestial/vcfparser

.. image:: https://readthedocs.org/projects/vcfparser/badge/?version=latest
        :target: https://vcfparser.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python parser for parsing the genomics and transcriptomics VCF data.


* Free software: MIT license
* Documentation: https://vcfparser.readthedocs.io.


Features
--------
- No external dependency except python
- Minimalistic in nature
- With lots of control to api users


Examples
--------
>>> from vcf_parser import VcfParser
>>> vcf_object = VcfParser('input_test.vcf')


### Get MetaInfo about the vcf file

>>> 

>>> print(f'Fileformat for given vcf is : {metainfo.fileformat}')

>>> print(f'Filters for given vcf are : {metainfo.filters_}')

>>> print(f' Contig lines are : {metainfo.contig}')

>>> print(f' Dictionary of infos is : {metainfo.infos_}')

>>> print(f' Sample names are : {metainfo.sample_names}')

>>> print("Raw lines are:")

>>> print(metainfo.raw_meta_data)

Get Records from vcf file:

>>> records = vcf_object.parse_records() # this creates a generator object

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