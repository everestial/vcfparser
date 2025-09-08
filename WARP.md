# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**vcfparser** is a minimalistic Python library for parsing genomics and transcriptomics VCF (Variant Call Format) data. It's designed to be dependency-free (Python 3.6+ only) and provides a clean API for extracting metadata and record information from VCF files.

This project is part of a larger VCF-Simplify ecosystem and serves as the core parsing engine that should be integrated into the main VCF-Simplify application.

## Architecture

### Core Modules

The library follows a modular design with clear separation of concerns:

```
vcfparser/
├── vcf_parser.py          # Main VcfParser class - entry point for parsing
├── meta_header_parser.py  # MetaDataParser - handles VCF header metadata  
├── record_parser.py       # Record & GenotypeProperty - processes VCF records
├── vcf_writer.py          # VCFWriter - writes VCF files
└── metaviewer.py          # MetaDataViewer - visualization utilities
```

### Key Classes

1. **VcfParser** - Main entry point providing `parse_metadata()` and `parse_records()` methods
2. **MetaDataParser** - Handles parsing of VCF header lines (##INFO, ##FORMAT, etc.)
3. **Record** - Represents a single VCF record with attributes (CHROM, POS, REF, ALT, etc.)
4. **GenotypeProperty** - Provides genotype analysis methods (isHOMREF, isHETVAR, etc.)
5. **VCFWriter** - Creates new VCF files with proper metadata and records

### Data Flow

```
VCF File → VcfParser → MetaDataParser (for headers)
                   → Record objects (for data lines)
                   → GenotypeProperty (for genotype analysis)
```

## Development Workflow

### Environment Setup

The project uses a virtual environment located at `.venv/`:

```bash
# Activate virtual environment
source .venv/bin/activate

# Verify installation
python -c "import vcfparser; print('vcfparser import successful')"
```

### Running Tests

The project has comprehensive test coverage with 48 tests across multiple modules:
- **tests/test_parser.py**: 12 integration tests 
- **tests/testvcfparser/**: 36 unit tests across 4 modules
  - test_meta_header_parser.py: 4 tests
  - test_record_parser.py: 22 tests
  - test_vcf_parser.py: 2 tests  
  - test_vcf_writer.py: 8 tests

```bash
# Run all tests
source .venv/bin/activate && python -m pytest tests/ -v

# Run just integration tests
python -m pytest tests/test_parser.py -v

# Run specific module tests
python -m pytest tests/testvcfparser/test_record_parser.py -v

# Run tests with coverage (if pytest-cov installed)
python -m pytest tests/ --cov=vcfparser
```

### Building and Installation

```bash
# Development installation
pip install -e .

# Build package
python setup.py sdist bdist_wheel

# Install from source
python setup.py install
```

### Testing with Sample Data

The repository includes test VCF files:
- `input_test.vcf` - Main test file used by the test suite
- `full_vcf43.vcf.gz` - Compressed VCF example
- `write_test.vcf` - Output file for write operations

## Common Development Tasks

### Adding New Features

1. **Parser Extensions**: Add methods to `Record` class for new genotype analysis
2. **Metadata Support**: Extend `MetaDataParser` for new VCF header types
3. **Writer Features**: Add methods to `VCFWriter` for new output formats

### Debugging VCF Parsing Issues

The library provides detailed error messages and supports both regular and gzipped VCF files. Check the `VcfParser.__init__` method for file handling logic.

### Performance Optimization

The codebase is designed for Cython compilation (mentioned in README). Key performance areas:
- Record parsing loop in `parse_records()`
- Metadata line processing in `MetaDataParser.parse_lines()`
- Genotype analysis methods in `GenotypeProperty`

## Integration Notes

### VCF-Simplify Integration

This library is intended to replace duplicate parsing code in the VCF-Simplify project. See `DEVELOPMENT_STRATEGY.md` for the integration roadmap.

### API Usage Examples

```python
from vcfparser import VcfParser

# Basic usage
vcf_obj = VcfParser('input.vcf')
metadata = vcf_obj.parse_metadata()
records = vcf_obj.parse_records()

# Get first record
first_record = next(records)
print(f"Position: {first_record.CHROM}:{first_record.POS}")

# Genotype analysis
genotype_info = first_record.genotype_property
homref_samples = genotype_info.isHOMREF()
```

## Code Quality Standards

### Testing Requirements
- All new features must include corresponding tests
- Maintain current test coverage (48+ tests)
- Tests should cover both metadata and record parsing functionality

### Documentation
- Follow existing docstring format with Parameters, Returns, and Examples sections
- Update RST documentation files in `docs/` for API changes
- README.md should reflect any new functionality

### Error Handling
- Use appropriate exceptions for file access and parsing errors
- Provide informative error messages for malformed VCF files
- Handle both regular and compressed (.gz) VCF files

## Project Dependencies

The library intentionally has **no external dependencies** beyond Python 3.6+. This minimalistic approach should be maintained for:
- Easy installation in research environments  
- Reduced compatibility issues
- Better performance characteristics

Optional development dependencies:
- `pytest` for testing
- `sphinx` for documentation generation
- `tox` for multi-Python version testing (configured but not installed)

## File Structure Context

- `/tests/` - Comprehensive test suite with sample data expectations
- `/docs/` - Sphinx documentation with detailed tutorials
- `setup.py` & `pyproject.toml` - Package configuration
- `tox.ini` - Multi-environment testing configuration
- `requirements.txt` - Empty (no runtime dependencies)
- `DEVELOPMENT_STRATEGY.md` - Strategic roadmap for VCF-Simplify integration

## Known Issues

1. **Newline handling**: There's a known issue with trailing newlines in sample parsing (mentioned in README line 139)
2. **GenotypeProperty methods**: Some methods in the `record_parser.py` appear incomplete (around line 400)
3. **Cython optimization**: Setup for Cython compilation is mentioned but not fully implemented
