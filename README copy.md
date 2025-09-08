# vcfparser

[![PyPI version](https://img.shields.io/pypi/v/vcfparser.svg)](https://pypi.org/project/vcfparser/)
[![Tests](https://img.shields.io/badge/tests-160%20passing-brightgreen.svg)](https://github.com/everestial/vcfparser)
[![Type Hints](https://img.shields.io/badge/type%20hints-mypy%20✓-blue.svg)](https://mypy-lang.org/)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://vcfparser.readthedocs.io)

A modern, **type-safe** Python library for parsing and analyzing VCF (Variant Call Format) files with **zero external dependencies**.

```python
from vcfparser import VcfParser

# Parse VCF file with full type safety
vcf = VcfParser("example.vcf")
metadata = vcf.parse_metadata()
records = vcf.parse_records()

# Analyze genotypes with comprehensive methods
for record in records:
    genotypes = record.genotype_property
    homref_samples = genotypes.isHOMREF()    # Type: Dict[str, str]
    het_samples = genotypes.isHETVAR()       # Full IDE autocomplete
    snp_variants = genotypes.hasSNP()        # Static type checking
```

## ✨ **What's New in v2.0**

- 🔍 **Full Type Safety**: Comprehensive type hints with mypy validation
- 🏗️ **Modern Architecture**: Clean, modular design with clear separation of concerns  
- 🧪 **Robust Testing**: 160+ test cases with 100% success rate
- 📊 **Enhanced APIs**: New MetaDataViewer and VCFWriter with context manager support
- ⚡ **Performance Ready**: Cython optimization foundation built-in
- 📖 **Rich Documentation**: Architecture diagrams and comprehensive examples

## 🚀 **Key Features**

| Feature | Description | Benefit |
|---------|-------------|----------|
| **Zero Dependencies** | Pure Python 3.6+ implementation | Easy installation anywhere |
| **Type Safety** | Complete type hints + mypy validation | Fewer runtime errors, better IDE support |
| **Memory Efficient** | Lazy loading with iterator-based parsing | Handle large VCF files efficiently |
| **Comprehensive API** | Parse metadata, records, genotype analysis | One library for all VCF needs |
| **Modern Testing** | 160+ tests with automated quality checks | Production-ready reliability |
| **Extensible Design** | Clean architecture with extension points | Easy to customize and extend |

## 🏗️ **Architecture Overview**

vcfparser follows a clean, modular architecture designed for both ease of use and extensibility:

```
📁 VCF File
    │
    ▼
🔍 VcfParser("example.vcf")
    │
    ├─── parse_metadata() ──➤ 📊 MetaDataViewer ──➤ 📄 Export Files
    │                             │                      ├─ .json
    │                             │                      ├─ .table  
    │                             │                      └─ .dict
    │
    └─── parse_records() ───➤ 🧬 Record Objects ──➤ 🔬 Genotype Analysis
                                  │                      ├─ isHOMREF()
                                  │                      ├─ isHETVAR()
                                  │                      ├─ isHOMVAR()
                                  │                      ├─ hasSNP()
                                  │                      └─ hasINDEL()
                                  │
                                  └─── Sample Data ──➤ 📈 Statistics
```

**🎯 Three Main Use Cases:**
1. **📖 Reading & Analyzing**: `VCF Input → VcfParser → Analysis → Results`
2. **📊 Metadata Export**: `VCF Input → MetaDataViewer → Export → Reports` 
3. **✍️ Writing VCF Files**: `Your Data → VCFWriter → VCF Output`

> 📚 **Detailed Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for comprehensive technical diagrams and design documentation.

## 📦 **Installation**

### **Quick Install (Recommended)**
```bash
pip install vcfparser
```

### **Development Install**
```bash
# Clone the repository
git clone https://github.com/everestial/vcfparser.git
cd vcfparser

# Install in development mode
pip install -e .

# Run tests to verify installation
python run_tests.py
```

### **Requirements**
- **Python**: 3.6+ (tested on 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.13)
- **Dependencies**: None! Pure Python implementation
- **Optional**: mypy for type checking, pytest for testing

## Cythonize (optional but helpful)

The installed "vcfparser" package can be cythonized to optimize performance.
Cythonizing the package can increase the speed of the parser by about x.x - y.y (?) times.

TODO: Bhuwan - add required cython method in here

## Testing

vcfparser includes comprehensive test suites to ensure code quality and functionality. We provide both Python and bash test runners for cross-platform compatibility.

### Quick Testing
```bash
# Run critical tests (recommended for development)
python run_tests.py --quick

# Run all tests
python run_tests.py

# Pre-commit validation with benchmarks
python run_tests.py --commit-ready
```

For detailed testing information, see [TESTING.md](TESTING.md).

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

metainfo.filters_
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

#TODO: FIX - looks like this is now replaced by >>> first_record.get_format_to_sample_map()  
#NOTE: and it looks like that \n issue is also fixed 
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
        infos = record.get_info_as_dict()
        mapped_sample = record.get_mapped_samples()
```

- For more specific use cases please check the examples in the following section:
- For tutorials in metadata, please follow :ref:`Metadata Tutorial <metadata-tutorial>`.
- For tutorials in record parser, please follow :ref:`Record Parser Tutorial <record-parser-tutorial>`.
