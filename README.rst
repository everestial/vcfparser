=========
vcfparser
=========

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


Installation
------------
To install vcfparser, run this command in your terminal:

.. code-block:: console

    $ pip install vcfparser

In order to build from source, you can follow :doc:_`installation guide <./docs/installation.rst>`


Usage
-----

>>> from vcfparser import VcfParser
>>> vcf_obj = VcfParser('input_test.vcf')

Get meta information about the vcf file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> metainfo = vcf_obj.parse_metadata()
>>> metainfo.fileformat
'VCFv4.2'
>>> metainfo.filters_
[{'ID': 'LowQual', 'Description': 'Low quality'}, {'ID': 'my_indel_filter', 'Description': 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0'}, {'ID': 'my_snp_filter', 'Description': 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0'}]

>>> metainfo.alt_
[{'ID': 'NON_REF', 'Description': 'Represents any possible alternative allele at this location'}]
>>> metainfo.sample_names
['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
>>> metainfo.record_keys
['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']




Get Records from vcf file
^^^^^^^^^^^^^^^^^^^^^^^^^
>>> records = vcf_obj.parse_records() 
Here records is an generator.
>>> first_record = next(records)
>>> first_record.CHROM
'2'
>>> first_record.POS
'15881018'
>>> first_record.REF
'G'
>>> first_record.ALT
'A,C'
>>> first_record.QUAL
'5082.45'
>>> first_record.FILTER
['PASS']
>>> first_record.get_mapped_samples()
{'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.\n'}}


Similarly, we can loop over rest of the records by following for loop:

.. code-block:: bash

    for record in records:
        chrom = record.CHROM
        pos = record.POS
        id = record.ID
        ref = record.REF
        alt = record.ALT
        qual = record.QUAL
        filter = record.FILTER
        format_ = record.format_
        infos = record.get_info_dict()
        mapped_sample = record.get_mapped_samples()

