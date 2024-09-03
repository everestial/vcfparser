# vcfparser

![PyPI version](https://img.shields.io/pypi/v/vcfparser.svg)  
[![Travis Build Status](https://img.shields.io/travis/everestial/vcfparser.svg)](https://travis-ci.org/everestial/vcfparser)  
[![Read the Docs](https://readthedocs.org/projects/vcfparser/badge/?version=latest)](https://vcfparser.readthedocs.io/en/latest/?badge=latest)

Python (version >=3.6) package for parsing the genomics and transcriptomics VCF data.

- Free software: MIT license
- Documentation: https://vcfparser.readthedocs.io.

## Features

- No external dependency except python (version >=3.6).
- Minimalistic in nature.
- Provides a lot of features to API users.
- Cython compiling is provided to optimize performance.

## Installation

**Method A:**

`VCFsimplify <https://github.com/everestial/VCF-Simplify>`\_ uses vcfparser API, so the package is readily available if VCFsimplify is already installed.

This is only preferred while developing/optimizing **VcfSimplify** along with **vcfparser**.

Navigate to the VCFsimplify directory ->
activate python ->
call the 'vcfparser' package.

```console

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
```

**Method B (preferred method):**
Pip is the preferred method of installing and using **vcfparser** API if custom python scripts/app are being developed.

```console
    $ pip install vcfparser
```

**Method C:**

For offline install, or in order to build from the source code, follow :ref:`advance install <advanced-install>`.

## Cythonize (optional but helpful)

The installed "vcfparser" package can be cythonized to optimize performance.
Cythonizing the package can increase the speed of the parser by about x.x - y.y (?) times.

TODO: Bhuwan - add required cython method in here

## Usage

```bash
from vcfparser import VcfParser
vcf_obj = VcfParser('input_test.vcf')
```

### Get metadata information from the vcf file

```python
metainfo = vcf_obj.parse_metadata()
metainfo.fileformat
# Output: 'VCFv4.2'

metainfo.filters
# Output: [{'ID': 'LowQual', 'Description': 'Low quality'}, {'ID': 'my_indel_filter', 'Description': 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0'}, {'ID': 'my_snp_filter', 'Description': 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0'}]

metainfo.alt_
# Output: [{'ID': 'NON_REF', 'Description': 'Represents any possible alternative allele at this location'}]

metainfo.sample_names
# Output: ['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']

metainfo.record_keys
# Output: ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
```

### Get Records from the vcf file

```python
records = vcf_obj.parse_records()
# Note: Records are returned as a generator.

first_record = next(records)
first_record.CHROM
# Output: '2'

first_record.POS
# Output: '15881018'

first_record.REF
# Output: 'G'

first_record.ALT
# Output: 'A,C'

first_record.QUAL
# Output: '5082.45'

first_record.FILTER
# Output: ['PASS']

first_record.get_mapped_samples()
# Output: {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'},
#           'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'},
#           'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'},
#           'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'},
#           'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'},
#           'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'},
#           'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.\n'}}
```

TODO: Bhuwan (priority - high)
The very last example "first_record.get_mapped_samples()" is returning the value of the last sample/key with "\n".
i.e: 'PC': '.\n'
Please fix that issue - strip('\n') in the line before parsing.

|

Alternately, we can loop over each record by using a for-loop:

```bash

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
```

- For more specific use cases please check the examples in the following section:
- For tutorials in metadata, please follow :ref:`Metadata Tutorial <metadata-tutorial>`.
- For tutorials in record parser, please follow :ref:`Record Parser Tutorial <record-parser-tutorial>`.
