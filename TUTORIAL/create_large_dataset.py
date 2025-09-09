#!/usr/bin/env python3
"""
Create Large VCF Dataset for Population Genetics Tutorials

This script generates a comprehensive ~10MB VCF dataset suitable for 
population genetics tutorials by:
1. Expanding the existing tutorial.vcf with more samples
2. Adding more chromosomes and variants
3. Introducing realistic population structure and diversity
4. Including various types of variants (SNPs, INDELs)
"""

import sys
import random
import gzip
from pathlib import Path
from typing import List, Dict, Tuple

def read_vcf_header_and_records(vcf_path: str) -> Tuple[List[str], List[str]]:
    """Read VCF file and separate header from records."""
    header_lines = []
    record_lines = []
    
    opener = gzip.open if vcf_path.endswith('.gz') else open
    
    with opener(vcf_path, 'rt') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                header_lines.append(line)
            elif line:
                record_lines.append(line)
    
    return header_lines, record_lines

def expand_samples(header_lines: List[str], num_samples: int = 50) -> List[str]:
    """Expand the sample list to include more samples for population analysis."""
    new_header = []
    
    for line in header_lines:
        if line.startswith('#CHROM'):
            # Parse the header line
            fields = line.split('\t')
            # Keep standard VCF columns
            standard_cols = fields[:9]  # CHROM to FORMAT
            
            # Generate sample names representing different populations
            populations = ['EUR', 'AFR', 'EAS', 'AMR', 'SAS']  # European, African, East Asian, American, South Asian
            sample_names = []
            
            for i in range(1, num_samples + 1):
                pop = populations[(i-1) % len(populations)]
                sample_names.append(f"{pop}{i:03d}")
            
            # Reconstruct header line
            new_line = '\t'.join(standard_cols + sample_names)
            new_header.append(new_line)
        else:
            new_header.append(line)
    
    return new_header

def generate_realistic_genotype(ref: str, alt_alleles: List[str], sample_idx: int, variant_idx: int) -> str:
    """Generate realistic genotype with population structure."""
    alleles = [ref] + alt_alleles
    
    # Simple population structure simulation
    # Population 0 (EUR): more likely to have reference alleles
    # Population 1 (AFR): more diversity
    # Population 2 (EAS): some population-specific variants
    # etc.
    pop = sample_idx % 5
    
    # Simulate allele frequencies based on population
    if pop == 0:  # EUR
        ref_freq = 0.7
    elif pop == 1:  # AFR
        ref_freq = 0.5
    elif pop == 2:  # EAS
        ref_freq = 0.6
    elif pop == 3:  # AMR
        ref_freq = 0.65
    else:  # SAS
        ref_freq = 0.55
    
    # Add some variant-specific effects
    variant_effect = (variant_idx % 100) / 100.0 * 0.2  # 0-20% effect
    ref_freq += variant_effect - 0.1
    ref_freq = max(0.1, min(0.9, ref_freq))  # Keep between 10-90%
    
    # Generate genotype
    allele1 = 0 if random.random() < ref_freq else random.randint(1, len(alleles) - 1)
    allele2 = 0 if random.random() < ref_freq else random.randint(1, len(alleles) - 1)
    
    # Add some phasing information and quality scores
    phased = random.choice(['/', '|'])
    if phased == '|':
        gt = f"{allele1}|{allele2}"
    else:
        gt = f"{allele1}/{allele2}"
    
    # Add realistic FORMAT fields (GT:AD:DP:GQ:PL)
    depth = random.randint(8, 50)
    gq = random.randint(20, 99)
    
    # Allele depth (AD)
    if allele1 == allele2 == 0:  # Homozygous reference
        ad = [depth, 0]
    elif allele1 != 0 and allele2 != 0 and allele1 == allele2:  # Homozygous alternate
        ad = [0, depth]
    else:  # Heterozygous
        ref_depth = random.randint(depth//4, 3*depth//4)
        alt_depth = depth - ref_depth
        ad = [ref_depth, alt_depth]
    
    ad_str = ','.join(map(str, ad[:2]))  # Keep it simple with ref,alt
    
    # Phred-scaled likelihoods (simplified)
    if allele1 == allele2 == 0:
        pl = "0,30,300"
    elif allele1 != 0 and allele2 != 0:
        pl = "300,30,0"
    else:
        pl = "30,0,30"
    
    return f"{gt}:{ad_str}:{depth}:{gq}:{pl}"

def expand_records(record_lines: List[str], num_samples: int = 50, target_variants: int = 50000) -> List[str]:
    """Expand records to include more samples and variants."""
    expanded_records = []
    
    # First, expand existing records
    for i, line in enumerate(record_lines):
        fields = line.split('\t')
        if len(fields) < 9:
            continue
            
        # Keep standard VCF columns
        chrom, pos, var_id, ref, alt, qual, filter_col, info, format_col = fields[:9]
        
        # Parse ALT alleles
        alt_alleles = alt.split(',')
        
        # Generate genotypes for all samples
        new_genotypes = []
        for sample_idx in range(num_samples):
            genotype = generate_realistic_genotype(ref, alt_alleles, sample_idx, i)
            new_genotypes.append(genotype)
        
        # Reconstruct record
        new_record = '\t'.join(fields[:9] + new_genotypes)
        expanded_records.append(new_record)
        
        if len(expanded_records) >= target_variants:
            break
    
    # If we need more variants, generate additional ones
    if len(expanded_records) < target_variants:
        print(f"Generating {target_variants - len(expanded_records)} additional variants...")
        
        # Generate additional variants on different chromosomes
        chromosomes = [f"{i:02d}" for i in range(1, 23)] + ['X', 'Y']
        
        for var_num in range(len(expanded_records), target_variants):
            chrom = random.choice(chromosomes)
            pos = random.randint(1000000, 200000000)
            var_id = f"rs{random.randint(100000, 9999999)}"
            
            # Generate realistic variants
            bases = ['A', 'T', 'G', 'C']
            ref = random.choice(bases)
            
            # 80% SNPs, 20% INDELs
            if random.random() < 0.8:  # SNP
                alt = random.choice([b for b in bases if b != ref])
            else:  # INDEL
                if random.random() < 0.5:  # Deletion
                    alt = ref
                    ref = ref + random.choice(bases)
                else:  # Insertion
                    alt = ref + random.choice(bases)
            
            qual = str(random.randint(30, 1000))
            filter_col = "PASS"
            info = f"AF={random.uniform(0.01, 0.99):.3f};AC={random.randint(1, num_samples*2)}"
            format_col = "GT:AD:DP:GQ:PL"
            
            # Generate genotypes
            alt_alleles = alt.split(',')
            genotypes = []
            for sample_idx in range(num_samples):
                genotype = generate_realistic_genotype(ref, alt_alleles, sample_idx, var_num)
                genotypes.append(genotype)
            
            record = f"{chrom}\t{pos}\t{var_id}\t{ref}\t{alt}\t{qual}\t{filter_col}\t{info}\t{format_col}\t" + '\t'.join(genotypes)
            expanded_records.append(record)
    
    return expanded_records

def create_large_vcf_dataset():
    """Create a large VCF dataset for population genetics tutorials."""
    
    # Input and output paths
    input_vcf = "examples/data/tutorial.vcf"
    output_vcf = "TUTORIAL/data/population_genetics.vcf"
    
    print("Creating large VCF dataset for population genetics tutorials...")
    print(f"Input: {input_vcf}")
    print(f"Output: {output_vcf}")
    
    # Read existing VCF
    if not Path(input_vcf).exists():
        print(f"Error: Input VCF file {input_vcf} not found!")
        sys.exit(1)
    
    header_lines, record_lines = read_vcf_header_and_records(input_vcf)
    print(f"Read {len(header_lines)} header lines and {len(record_lines)} records")
    
    # Expand to 50 samples
    num_samples = 50
    expanded_header = expand_samples(header_lines, num_samples)
    print(f"Expanded to {num_samples} samples representing 5 populations")
    
    # Expand to ~50,000 variants for substantial analysis
    target_variants = 50000
    expanded_records = expand_records(record_lines, num_samples, target_variants)
    print(f"Generated {len(expanded_records)} variants")
    
    # Write output VCF
    output_path = Path(output_vcf)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_vcf, 'w') as f:
        # Write header
        for line in expanded_header:
            f.write(line + '\n')
        
        # Write records
        for record in expanded_records:
            f.write(record + '\n')
    
    # Check file size
    file_size = output_path.stat().st_size
    size_mb = file_size / (1024 * 1024)
    
    print(f"Created {output_vcf}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"Contains {len(expanded_records)} variants across {num_samples} samples")
    print("Dataset represents 5 populations: EUR, AFR, EAS, AMR, SAS")

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    # Create the large dataset
    create_large_vcf_dataset()
    
    # Also create a smaller intermediate dataset (5MB) for lighter tutorials
    print("\n" + "="*50)
    print("Creating intermediate dataset for lighter tutorials...")
    
    # Modify parameters for smaller dataset
    input_vcf = "examples/data/tutorial.vcf"
    output_vcf = "TUTORIAL/data/intermediate.vcf"
    
    header_lines, record_lines = read_vcf_header_and_records(input_vcf)
    
    # 25 samples, 5000 variants
    num_samples = 25
    target_variants = 5000
    
    expanded_header = expand_samples(header_lines, num_samples)
    expanded_records = expand_records(record_lines, num_samples, target_variants)
    
    # Write intermediate dataset
    output_path = Path(output_vcf)
    with open(output_vcf, 'w') as f:
        for line in expanded_header:
            f.write(line + '\n')
        for record in expanded_records:
            f.write(record + '\n')
    
    file_size = output_path.stat().st_size
    size_mb = file_size / (1024 * 1024)
    
    print(f"Created {output_vcf}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"Contains {len(expanded_records)} variants across {num_samples} samples")
