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



Python (version >=3.6) package for parsing the genomics and transcriptomics VCF data.


* Free software: MIT license
* Documentation: https://vcfparser.readthedocs.io.


Features
--------
- No external dependency except python (version >=3.6).
- Minimalistic in nature.
- Provides a lot of features to API users.
- Cython compiling is provided to optimize performance.


Installation
------------

`VCFsimplify <https://github.com/everestial/VCF-Simplify>`_ **uses vcfparser API, so the package is readily available if VCFsimplify is already installed.**

Navigate to the VCFsimplify directory -> 
activate python -> 
call the 'vcfparser' package.

.. code-block:: console

    $ C:\Users\>cd VCF-Simplify
    $ C:\Users\>cd VCF-Simplify>dir
      Volume in drive C is StorageDrive
      Volume Serial Number is .........

      Directory of C:\Users\VCF-Simplify

      07/12/2020  10:14 AM    <DIR>          .
      07/12/2020  10:14 AM    <DIR>          ..
      07/12/2020  08:55 AM    <DIR>          .github
      ............................
      ............................
      07/12/2020  10:42 AM    <DIR>          vcfparser
      07/12/2020  08:55 AM             1,494 VcfSimplify.py
              11 File(s)     20,873,992 bytes
              13 Dir(s)  241,211,793,408 bytes free
    
    $ C:\Users\VCF-Simplify>python
    Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 22:39:24) [MSC v.1916 (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from vcfparser import VcfParser
    >>>

| 

**The standalone "vcfparser" package is available via pip.**

This is the preferred method of installing and using "vcfparser" if custom python scripts/app are being developed.

.. code-block:: console

    $ pip install vcfparser

In order to build from source, you can follow `advanced tutorial <advanced-install>`
TODO Bhuwan/Gopal - Do we have an advanced tutorial? 

Cythonize (optional but helpful)
--------------------------------
The installed "vcfparser" package can be cythonized to optimize performance.
Cythonizing the package can increase the speed of the parser by about x.x - y.y (?) times. 

TODO: Bhuwan - add required cython method in here



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
# Note: Records are returned as generator. 
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
TODO: Bhuwan (priority - high)
The very last example "first_record.get_mapped_samples()" is returning the value of the last sample/key with "\n". 
i.e: 'PC': '.\n'
Please fix that issue - strip('\n') in the line before parsing. 

|

Similarly, we can loop over each record by using a for-loop:

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

For more specific use cases please check the examples in the following section:

tutorial on MetaData # TODO (Gopal) - add link here
tutorial on record parser # TODO - add link here 