# Population Genetics Tutorials

This directory contains comprehensive tutorials for population genetics analysis using vcfparser. These tutorials go beyond basic usage examples to demonstrate real-world genomics analyses with substantial datasets.

## Tutorial Datasets

### Data Files

Located in `TUTORIAL/data/`:

- **intermediate.vcf** (3.3 MB)
  - 5,000 variants across 25 samples
  - 5 populations: EUR, AFR, EAS, AMR, SAS (5 samples each)
  - Ideal for learning and testing workflows
  - Contains both SNPs and INDELs with realistic quality scores

- **population_genetics.vcf** (60 MB)
  - 50,000 variants across 50 samples  
  - 5 populations: EUR, AFR, EAS, AMR, SAS (10 samples each)
  - Suitable for comprehensive population genetics analyses
  - Simulated population structure and diversity patterns

### Dataset Creation

Both datasets are created using `create_large_dataset.py`, which:
- Expands existing tutorial data with realistic population structure
- Generates additional variants across multiple chromosomes
- Adds proper FORMAT fields (GT:AD:DP:GQ:PL)
- Simulates population-specific allele frequencies
- Includes both phased and unphased genotypes

## Tutorial Structure

### Core Tutorials

1. **[GENOTYPE_ANALYSIS_REFERENCE.md](GENOTYPE_ANALYSIS_REFERENCE.md)**
   - Complete reference for GenotypeProperty methods
   - Basic genotype classification examples
   - Using real example data

2. **Population Genetics Analysis** (planned)
   - Allele frequency calculations
   - Hardy-Weinberg equilibrium testing
   - Population differentiation (Fst)
   - Linkage disequilibrium analysis

3. **Data Visualization** (planned)
   - Exporting data for matplotlib/seaborn
   - Allele frequency plots
   - Genotype distribution heatmaps
   - Quality score distributions

4. **Multi-Sample Analysis** (planned)
   - Population-scale VCF analysis
   - Cross-population comparisons
   - Population-specific variant identification

5. **Quality Control & Filtering** (planned)
   - Filtering by depth and quality scores
   - Missing data rate analysis
   - Allele balance assessment
   - Population genetics QC metrics

6. **Performance Optimization** (planned)
   - Large VCF file handling strategies
   - Memory management tips
   - Batch processing examples

## Population Codes

The tutorial datasets use standard population codes:

- **EUR**: European ancestry
- **AFR**: African ancestry  
- **EAS**: East Asian ancestry
- **AMR**: American ancestry (admixed)
- **SAS**: South Asian ancestry

Samples are named as `{POP}{NUMBER}`, e.g., `EUR001`, `AFR015`, `EAS023`.

## Usage Recommendations

### Choose Your Dataset

- Use **intermediate.vcf** for:
  - Learning new concepts
  - Testing workflows
  - Quick analyses
  - Tutorial development

- Use **population_genetics.vcf** for:
  - Comprehensive population analyses
  - Performance benchmarking
  - Large-scale genomics workflows
  - Production-like scenarios

### Tutorial Progression

1. Start with basic genotype analysis using `GENOTYPE_ANALYSIS_REFERENCE.md`
2. Progress through population genetics tutorials
3. Apply concepts to your own VCF data
4. Optimize performance for large datasets

## Requirements

- Python 3.6+
- vcfparser library
- Optional: matplotlib, seaborn (for visualization tutorials)
- Optional: numpy, scipy (for statistical analyses)

## Getting Started

```python
# Load a tutorial dataset
from vcfparser import VcfParser

# Start with the intermediate dataset
vcf = VcfParser('TUTORIAL/data/intermediate.vcf')
metadata = vcf.parse_metadata()
records = vcf.parse_records()

# Get basic dataset info
print(f"Samples: {len(metadata.sample_names)}")
print(f"Sample names: {metadata.sample_names[:10]}...")  # First 10

# Analyze first record
first_record = next(records)
genotypes = first_record.genotype_property
print(f"Homozygous reference samples: {len(genotypes.isHOMREF())}")
```

## Contributing

When adding new tutorials:

1. Use realistic genomics scenarios
2. Include code examples with expected outputs
3. Provide clear explanations of concepts
4. Test with both datasets when appropriate
5. Document performance considerations

## File Organization

```
TUTORIAL/
├── README.md                           # This file
├── GENOTYPE_ANALYSIS_REFERENCE.md     # Genotype analysis methods
├── create_large_dataset.py            # Dataset creation script
├── data/
│   ├── intermediate.vcf               # 3.3 MB dataset
│   └── population_genetics.vcf        # 60 MB dataset
└── [future tutorial scripts]
```

This tutorial collection provides a comprehensive learning path from basic genotype analysis to advanced population genetics workflows using vcfparser.
