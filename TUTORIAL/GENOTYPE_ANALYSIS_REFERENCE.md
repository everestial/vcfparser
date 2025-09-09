# GenotypeProperty Methods Reference

This document provides a complete reference for all methods available in the `GenotypeProperty` class.

## Overview

The `GenotypeProperty` class provides comprehensive genotype analysis functionality. Access it via:

```python
from vcfparser import VcfParser

# Use actual example files from the repository
vcf = VcfParser("examples/data/example.vcf")  # Small example (5 variants, 3 samples)
# Or use the larger tutorial dataset:
# vcf = VcfParser("examples/data/tutorial.vcf")  # Comprehensive dataset (612 variants, 7 samples)

for record in vcf.parse_records():
    gt = record.genotype_property  # GenotypeProperty instance
    # Use methods below...
```

## Method Categories

### 1. Basic Genotype Types
Methods that categorize samples by genotype type.

| Method | Returns | Description |
|--------|---------|-------------|
| `isHOMREF(tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with homozygous reference (0/0) |
| `isHOMVAR(tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with homozygous variant (1/1, 2/2) |
| `isHETVAR(tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with heterozygous variant (0/1, 1/2) |
| `isMissing(tag="GT")` | `Dict[str, str]` | Samples with missing genotypes (./.) |

**Example:**
```python
gt = record.genotype_property
homref = gt.isHOMREF()      # {'Sample01': '0/0', 'Sample02': '0/0'}
hetvar = gt.isHETVAR()      # {'Sample03': '0/1'}
homvar = gt.isHOMVAR()      # {'Sample04': '1/1'}
```

### 2. Variant Type Detection
Methods that determine the type of genomic variant.

| Method | Returns | Description |
|--------|---------|-------------|
| `hasSNP(tag="GT", bases="numeric")` | `bool` | True if record contains SNP variants |
| `hasINDEL()` | `bool` | True if record contains INDEL variants |

**Example:**
```python
if gt.hasSNP():
    print("This record contains SNP variants")
if gt.hasINDEL():
    print("This record contains INDEL variants")
```

### 3. Phase Information
Methods that analyze genotype phasing.

| Method | Returns | Description |
|--------|---------|-------------|
| `has_phased(tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with phased genotypes (0\|1) |
| `has_unphased(tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with unphased genotypes (0/1) |

**Example:**
```python
phased = gt.has_phased()    # {'Sample01': '0|1'}
unphased = gt.has_unphased()  # {'Sample02': '0/1', 'Sample03': '1/1'}
```

### 4. Allele and Variant Presence
Methods that search for specific alleles or genotypes.

| Method | Returns | Description |
|--------|---------|-------------|
| `hasAllele(allele="0", tag="GT", bases="numeric")` | `Dict[str, str]` | Samples containing specific allele |
| `hasVAR(genotype="0/0", tag="GT", bases="numeric")` | `Dict[str, str]` | Samples with specific genotype |
| `hasnoVAR(tag="GT")` | `Dict[str, str]` | Samples with empty/missing genotypes |

**Example:**
```python
ref_allele = gt.hasAllele(allele="0")       # Samples with reference allele
alt_allele = gt.hasAllele(allele="1")       # Samples with first alternate allele
homref_exact = gt.hasVAR(genotype="0/0")   # Samples with exactly 0/0
```

## Parameter Options

### `tag` Parameter
- **Default**: `"GT"` (genotype)
- **Options**: Any FORMAT field (e.g., "DP", "GQ", "PL")
- **Usage**: Analyze different FORMAT fields beyond genotype

### `bases` Parameter  
- **Default**: `"numeric"` 
- **Options**: `"numeric"` or `"iupac"`
- **Usage**: Return genotypes as numbers (0/1) or DNA bases (A/T)

**Example:**
```python
# Numeric format (default)
gt.isHETVAR(bases="numeric")  # {'Sample01': '0/1'}

# IUPAC format  
gt.isHETVAR(bases="iupac")    # {'Sample01': 'G/A'}

# Different FORMAT field
gt.isMissing(tag="DP")        # Samples with missing depth info
```

## Real Usage Examples

### Population Genetics Analysis
```python
# Use the comprehensive tutorial dataset with 7 samples
vcf = VcfParser("examples/data/tutorial.vcf")
variant_count = 0

for record in vcf.parse_records():
    gt = record.genotype_property
    
    # Calculate allele frequencies across 7 samples
    total_samples = len(record.get_format_to_sample_map())
    carriers = len(gt.isHETVAR()) + len(gt.isHOMVAR())
    allele_freq = carriers / total_samples if total_samples > 0 else 0
    
    if allele_freq > 0.1:  # Common variants (>10% in this small population)
        print(f"Common variant at {record.CHROM}:{record.POS}")
        print(f"  Heterozygous samples: {list(gt.isHETVAR().keys())}")
        print(f"  Homozygous variant samples: {list(gt.isHOMVAR().keys())}")
        print(f"  Allele frequency: {allele_freq:.2%}")
        
        variant_count += 1
        if variant_count >= 5:  # Limit output for demonstration
            break
```

### Quality Control
```python
# Use the basic example dataset for quality control demonstration
vcf = VcfParser("examples/data/example.vcf")

for record in vcf.parse_records():
    gt = record.genotype_property
    
    # Check for missing data
    missing = gt.isMissing()
    total_samples = len(record.get_format_to_sample_map())
    missing_rate = len(missing) / total_samples if total_samples > 0 else 0
    
    if missing_rate > 0.1:  # >10% missing data
        print(f"High missingness at {record.CHROM}:{record.POS}")
        print(f"  Missing samples: {list(missing.keys())}")
        print(f"  Missing rate: {missing_rate:.1%}")
    
    # Check phase consistency
    phased = gt.has_phased()
    unphased = gt.has_unphased()
    if phased or unphased:  # Only print if there's genotype data
        print(f"Variant {record.CHROM}:{record.POS} phasing: {len(phased)} phased, {len(unphased)} unphased")
```

### Variant Filtering
```python
# Use tutorial dataset for comprehensive filtering example
vcf = VcfParser("examples/data/tutorial.vcf")
filtered_variants = []

for record in vcf.parse_records():
    gt = record.genotype_property
    
    # Apply multiple filter criteria
    quality_ok = float(record.QUAL) > 100      # High quality variants
    has_carriers = len(gt.isHETVAR()) + len(gt.isHOMVAR()) >= 2  # At least 2 variant carriers
    low_missing = len(gt.isMissing()) <= 1     # Maximum 1 missing sample
    
    if quality_ok and has_carriers and low_missing:
        filtered_variants.append({
            'position': f"{record.CHROM}:{record.POS}",
            'variant_type': 'SNP' if gt.hasSNP() else 'INDEL',
            'het_samples': list(gt.isHETVAR().keys()),
            'hom_samples': list(gt.isHOMVAR().keys()),
            'quality': float(record.QUAL)
        })
        
        # Stop after finding 10 good variants for demonstration
        if len(filtered_variants) >= 10:
            break

print(f"Found {len(filtered_variants)} high-quality variants")
for variant in filtered_variants[:3]:  # Show first 3
    print(f"  {variant['position']}: {variant['variant_type']}, Q={variant['quality']:.1f}")
```

## Notes

1. **Return Types**: Most methods return `Dict[str, str]` where keys are sample names and values are genotype values
2. **Boolean Methods**: `hasSNP()` and `hasINDEL()` return boolean values
3. **Empty Results**: Methods return empty dictionaries `{}` when no samples match criteria
4. **Case Sensitivity**: All method names use camelCase (e.g., `isHOMREF`, not `is_homref`)
5. **Performance**: Methods are lazy-evaluated and efficient for large datasets

## See Also

- [examples/basic_usage.py](../examples/basic_usage.py) - Basic working examples with real data
- [examples/advanced_usage.py](../examples/advanced_usage.py) - Comprehensive genomics analysis tutorial
- [examples/data/example.vcf](../examples/data/example.vcf) - Small example dataset (5 variants, 3 samples)
- [examples/data/tutorial.vcf](../examples/data/tutorial.vcf) - Large example dataset (612 variants, 7 samples)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture and design details
- [README.md](../README.md) - Main documentation with quick start guide
