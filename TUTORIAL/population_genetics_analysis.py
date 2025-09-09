#!/usr/bin/env python3
"""
Comprehensive Population Genetics Analysis Tutorial

This tutorial demonstrates advanced population genetics analyses using vcfparser
with the intermediate.vcf dataset (3.3 MB, 25 samples, 5000 variants).

Topics covered:
1. Dataset overview and population structure
2. Allele frequency calculations
3. Hardy-Weinberg equilibrium testing
4. Genotype quality assessment
5. Population differentiation analysis
6. Variant filtering and quality control
7. Population-specific variant identification

Required: vcfparser (no external dependencies for basic analyses)
Optional: matplotlib, numpy (for visualization and advanced statistics)
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict, Counter
import math

# Add parent directory to path to import vcfparser
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcfparser import VcfParser

def analyze_dataset_overview():
    """Provide comprehensive overview of the tutorial dataset."""
    print("=" * 60)
    print("POPULATION GENETICS ANALYSIS TUTORIAL")
    print("=" * 60)
    print()
    
    # Load the intermediate dataset
    vcf_path = "TUTORIAL/data/intermediate.vcf"
    print(f"Loading dataset: {vcf_path}")
    
    if not Path(vcf_path).exists():
        print(f"Error: Dataset {vcf_path} not found!")
        print("Please run 'python TUTORIAL/create_large_dataset.py' first.")
        return None
    
    vcf = VcfParser(vcf_path)
    metadata = vcf.parse_metadata()
    
    # Basic dataset information
    print(f"Dataset size: {Path(vcf_path).stat().st_size / (1024*1024):.1f} MB")
    print(f"Total samples: {len(metadata.sample_names)}")
    print(f"VCF format: {metadata.fileformat}")
    print()
    
    # Population structure analysis
    populations = defaultdict(list)
    for sample in metadata.sample_names:
        pop = sample[:3]  # Extract population code (EUR, AFR, etc.)
        populations[pop].append(sample)
    
    print("Population Structure:")
    for pop, samples in sorted(populations.items()):
        print(f"  {pop}: {len(samples)} samples ({', '.join(samples[:3])}{'...' if len(samples) > 3 else ''})")
    print()
    
    return vcf, metadata, populations

def calculate_allele_frequencies(vcf, populations: Dict[str, List[str]]) -> Dict:
    """Calculate allele frequencies per population and overall."""
    print("1. ALLELE FREQUENCY ANALYSIS")
    print("-" * 40)
    
    # Initialize frequency tracking
    pop_frequencies = {pop: defaultdict(Counter) for pop in populations.keys()}
    overall_frequencies = defaultdict(Counter)
    
    variant_count = 0
    records = vcf.parse_records()
    
    # Analyze first 100 variants for demonstration
    for record in records:
        variant_count += 1
        if variant_count > 100:  # Limit for tutorial speed
            break
            
        variant_id = f"{record.CHROM}:{record.POS}"
        ref_allele = record.REF
        alt_alleles = record.ALT
        all_alleles = [ref_allele] + alt_alleles
        
        # Count alleles per population
        genotypes = record.genotype_property
        
        for pop, sample_list in populations.items():
            for sample in sample_list:
                try:
                    sample_idx = record.sample_names.index(sample)
                    gt_info = record.sample_vals[sample_idx].split(':')[0]  # Extract GT
                    
                    # Parse genotype (handle both / and | separators)
                    if '/' in gt_info:
                        alleles = gt_info.split('/')
                    elif '|' in gt_info:
                        alleles = gt_info.split('|')
                    else:
                        continue  # Skip malformed genotypes
                    
                    # Count alleles
                    for allele_idx in alleles:
                        if allele_idx.isdigit() and int(allele_idx) < len(all_alleles):
                            allele = all_alleles[int(allele_idx)]
                            pop_frequencies[pop][variant_id][allele] += 1
                            overall_frequencies[variant_id][allele] += 1
                            
                except (ValueError, IndexError):
                    continue  # Skip problematic samples
    
    # Calculate and display results
    print(f"Analyzed {variant_count} variants")
    
    # Show example allele frequencies
    example_variants = list(overall_frequencies.keys())[:5]
    
    for variant_id in example_variants:
        print(f"\nVariant {variant_id}:")
        
        # Overall frequencies
        total_alleles = sum(overall_frequencies[variant_id].values())
        if total_alleles > 0:
            print(f"  Overall allele frequencies:")
            for allele, count in overall_frequencies[variant_id].most_common():
                freq = count / total_alleles
                print(f"    {allele}: {count}/{total_alleles} ({freq:.3f})")
        
        # Population-specific frequencies
        for pop in sorted(populations.keys()):
            if variant_id in pop_frequencies[pop]:
                pop_total = sum(pop_frequencies[pop][variant_id].values())
                if pop_total > 0:
                    major_allele = pop_frequencies[pop][variant_id].most_common(1)[0]
                    freq = major_allele[1] / pop_total
                    print(f"    {pop} major allele: {major_allele[0]} ({freq:.3f})")
    
    return pop_frequencies, overall_frequencies

def test_hardy_weinberg_equilibrium(vcf, populations: Dict[str, List[str]]):
    """Test Hardy-Weinberg equilibrium for each population."""
    print("\n2. HARDY-WEINBERG EQUILIBRIUM TESTING")
    print("-" * 40)
    
    records = vcf.parse_records()
    hw_results = defaultdict(list)
    
    variant_count = 0
    for record in records:
        variant_count += 1
        if variant_count > 20:  # Test fewer variants for demonstration
            break
            
        variant_id = f"{record.CHROM}:{record.POS}"
        
        # Only analyze bi-allelic SNPs for HWE
        if len(record.ALT) != 1:
            continue
            
        print(f"\nTesting HWE for {variant_id}:")
        
        for pop, sample_list in populations.items():
            # Count genotypes in this population
            genotype_counts = {'RR': 0, 'RA': 0, 'AA': 0}  # ref/ref, ref/alt, alt/alt
            total_samples = 0
            
            for sample in sample_list:
                try:
                    sample_idx = record.sample_names.index(sample)
                    gt_info = record.sample_vals[sample_idx].split(':')[0]
                    
                    # Parse genotype
                    if '/' in gt_info:
                        alleles = gt_info.split('/')
                    elif '|' in gt_info:
                        alleles = gt_info.split('|')
                    else:
                        continue
                    
                    if len(alleles) == 2 and all(a.isdigit() for a in alleles):
                        a1, a2 = int(alleles[0]), int(alleles[1])
                        
                        if a1 == 0 and a2 == 0:
                            genotype_counts['RR'] += 1
                        elif (a1 == 0 and a2 == 1) or (a1 == 1 and a2 == 0):
                            genotype_counts['RA'] += 1
                        elif a1 == 1 and a2 == 1:
                            genotype_counts['AA'] += 1
                        
                        total_samples += 1
                        
                except (ValueError, IndexError):
                    continue
            
            if total_samples < 3:  # Need sufficient samples
                continue
                
            # Calculate allele frequencies
            total_alleles = total_samples * 2
            p = (2 * genotype_counts['RR'] + genotype_counts['RA']) / total_alleles  # ref frequency
            q = 1 - p  # alt frequency
            
            # Expected genotype frequencies under HWE
            expected_RR = p * p * total_samples
            expected_RA = 2 * p * q * total_samples
            expected_AA = q * q * total_samples
            
            # Simple chi-square test (without proper statistical libraries)
            chi_square = 0
            if expected_RR > 0:
                chi_square += (genotype_counts['RR'] - expected_RR) ** 2 / expected_RR
            if expected_RA > 0:
                chi_square += (genotype_counts['RA'] - expected_RA) ** 2 / expected_RA
            if expected_AA > 0:
                chi_square += (genotype_counts['AA'] - expected_AA) ** 2 / expected_AA
            
            print(f"  {pop} population (n={total_samples}):")
            print(f"    Observed: RR={genotype_counts['RR']}, RA={genotype_counts['RA']}, AA={genotype_counts['AA']}")
            print(f"    Expected: RR={expected_RR:.1f}, RA={expected_RA:.1f}, AA={expected_AA:.1f}")
            print(f"    Allele frequencies: p={p:.3f}, q={q:.3f}")
            print(f"    Chi-square: {chi_square:.3f}")
            
            # Store results for summary
            hw_results[pop].append({
                'variant': variant_id,
                'chi_square': chi_square,
                'total_samples': total_samples
            })

def assess_genotype_quality(vcf, populations: Dict[str, List[str]]):
    """Assess genotype quality metrics across populations."""
    print("\n3. GENOTYPE QUALITY ASSESSMENT")
    print("-" * 40)
    
    records = vcf.parse_records()
    quality_metrics = defaultdict(lambda: defaultdict(list))
    
    variant_count = 0
    for record in records:
        variant_count += 1
        if variant_count > 50:  # Analyze subset for demonstration
            break
        
        for pop, sample_list in populations.items():
            for sample in sample_list:
                try:
                    sample_idx = record.sample_names.index(sample)
                    format_fields = record.sample_vals[sample_idx].split(':')
                    
                    if len(format_fields) >= 4:  # GT:AD:DP:GQ format expected
                        gt, ad, dp, gq = format_fields[:4]
                        
                        # Extract quality metrics
                        if dp.isdigit():
                            quality_metrics[pop]['depth'].append(int(dp))
                        if gq.isdigit():
                            quality_metrics[pop]['genotype_quality'].append(int(gq))
                            
                except (ValueError, IndexError):
                    continue
    
    # Calculate and display quality statistics
    for pop in sorted(populations.keys()):
        print(f"\n{pop} Population Quality Metrics:")
        
        depths = quality_metrics[pop]['depth']
        gqs = quality_metrics[pop]['genotype_quality']
        
        if depths:
            avg_depth = sum(depths) / len(depths)
            min_depth = min(depths)
            max_depth = max(depths)
            print(f"  Coverage depth: avg={avg_depth:.1f}, min={min_depth}, max={max_depth}")
            
        if gqs:
            avg_gq = sum(gqs) / len(gqs)
            min_gq = min(gqs)
            max_gq = max(gqs)
            print(f"  Genotype quality: avg={avg_gq:.1f}, min={min_gq}, max={max_gq}")
            
        # Quality filtering recommendations
        low_depth = sum(1 for d in depths if d < 10)
        low_gq = sum(1 for g in gqs if g < 20)
        
        if depths:
            print(f"  Quality concerns: {low_depth}/{len(depths)} ({100*low_depth/len(depths):.1f}%) with depth < 10")
        if gqs:
            print(f"                   {low_gq}/{len(gqs)} ({100*low_gq/len(gqs):.1f}%) with GQ < 20")

def identify_population_specific_variants(vcf, populations: Dict[str, List[str]]):
    """Identify variants that are population-specific."""
    print("\n4. POPULATION-SPECIFIC VARIANT IDENTIFICATION")
    print("-" * 40)
    
    records = vcf.parse_records()
    pop_specific_variants = defaultdict(list)
    
    variant_count = 0
    for record in records:
        variant_count += 1
        if variant_count > 200:  # Analyze subset
            break
            
        variant_id = f"{record.CHROM}:{record.POS}"
        
        # Calculate alternate allele frequency per population
        pop_alt_freqs = {}
        
        for pop, sample_list in populations.items():
            alt_count = 0
            total_alleles = 0
            
            for sample in sample_list:
                try:
                    sample_idx = record.sample_names.index(sample)
                    gt_info = record.sample_vals[sample_idx].split(':')[0]
                    
                    if '/' in gt_info:
                        alleles = [int(a) for a in gt_info.split('/') if a.isdigit()]
                    elif '|' in gt_info:
                        alleles = [int(a) for a in gt_info.split('|') if a.isdigit()]
                    else:
                        continue
                    
                    alt_count += sum(1 for a in alleles if a > 0)
                    total_alleles += len(alleles)
                    
                except (ValueError, IndexError):
                    continue
            
            if total_alleles > 0:
                pop_alt_freqs[pop] = alt_count / total_alleles
        
        # Identify population-specific variants (frequency > 0.1 in one pop, < 0.05 in others)
        for pop, freq in pop_alt_freqs.items():
            if freq > 0.1:  # Present in this population
                other_freqs = [pop_alt_freqs[other_pop] for other_pop in pop_alt_freqs 
                              if other_pop != pop]
                
                if all(f < 0.05 for f in other_freqs):  # Rare in other populations
                    pop_specific_variants[pop].append({
                        'variant': variant_id,
                        'frequency': freq,
                        'ref': record.REF,
                        'alt': record.ALT[0] if record.ALT else 'N/A'
                    })
    
    # Display results
    for pop in sorted(populations.keys()):
        variants = pop_specific_variants[pop]
        print(f"\n{pop}-specific variants (n={len(variants)}):")
        
        # Show top 5 examples
        for var in sorted(variants, key=lambda x: x['frequency'], reverse=True)[:5]:
            print(f"  {var['variant']}: {var['ref']}->{var['alt']} (freq={var['frequency']:.3f})")
        
        if len(variants) > 5:
            print(f"  ... and {len(variants) - 5} more")

def perform_variant_filtering(vcf, populations: Dict[str, List[str]]):
    """Demonstrate variant filtering based on quality metrics."""
    print("\n5. VARIANT FILTERING AND QUALITY CONTROL")
    print("-" * 40)
    
    records = vcf.parse_records()
    
    filters = {
        'total_variants': 0,
        'low_quality': 0,
        'low_depth': 0,
        'high_missing': 0,
        'monomorphic': 0,
        'passed_filters': 0
    }
    
    quality_threshold = 30
    depth_threshold = 10
    missing_rate_threshold = 0.2
    
    print(f"Applying filters:")
    print(f"  Quality (QUAL) >= {quality_threshold}")
    print(f"  Average depth >= {depth_threshold}")
    print(f"  Missing data rate <= {missing_rate_threshold}")
    print(f"  Remove monomorphic variants")
    print()
    
    for record in records:
        filters['total_variants'] += 1
        
        if filters['total_variants'] > 500:  # Process subset for demonstration
            break
            
        # Filter 1: Quality score
        try:
            qual = float(record.QUAL)
            if qual < quality_threshold:
                filters['low_quality'] += 1
                continue
        except (ValueError, TypeError):
            filters['low_quality'] += 1
            continue
        
        # Filter 2: Depth and missing data
        total_samples = len(record.sample_names) if record.sample_names else 0
        valid_samples = 0
        total_depth = 0
        
        if record.sample_vals:
            for sample_info in record.sample_vals:
                try:
                    fields = sample_info.split(':')
                    if len(fields) >= 3:  # GT:AD:DP
                        gt, ad, dp = fields[:3]
                        
                        if gt not in ['./.', './|', '|/.', '.|.'] and dp.isdigit():
                            valid_samples += 1
                            total_depth += int(dp)
                            
                except (ValueError, IndexError):
                    continue
        
        # Check missing data rate
        missing_rate = (total_samples - valid_samples) / total_samples
        if missing_rate > missing_rate_threshold:
            filters['high_missing'] += 1
            continue
            
        # Check average depth
        if valid_samples > 0:
            avg_depth = total_depth / valid_samples
            if avg_depth < depth_threshold:
                filters['low_depth'] += 1
                continue
        
        # Filter 3: Remove monomorphic variants
        genotypes = record.genotype_property
        try:
            all_genotypes = genotypes.isHOMREF() + genotypes.isHETVAR() + genotypes.isHOMVAR()
            if len(genotypes.isHETVAR()) == 0 and len(genotypes.isHOMVAR()) == 0:
                filters['monomorphic'] += 1
                continue
        except:
            pass
        
        filters['passed_filters'] += 1
    
    # Display filtering results
    print("Filtering Results:")
    total = filters['total_variants']
    print(f"  Total variants processed: {total}")
    print(f"  Failed quality filter: {filters['low_quality']} ({100*filters['low_quality']/total:.1f}%)")
    print(f"  Failed depth filter: {filters['low_depth']} ({100*filters['low_depth']/total:.1f}%)")
    print(f"  Failed missing data filter: {filters['high_missing']} ({100*filters['high_missing']/total:.1f}%)")
    print(f"  Monomorphic variants: {filters['monomorphic']} ({100*filters['monomorphic']/total:.1f}%)")
    print(f"  Passed all filters: {filters['passed_filters']} ({100*filters['passed_filters']/total:.1f}%)")

def main():
    """Run the comprehensive population genetics tutorial."""
    
    # 1. Dataset overview
    result = analyze_dataset_overview()
    if result is None:
        return
        
    vcf, metadata, populations = result
    
    # 2. Allele frequency analysis
    pop_frequencies, overall_frequencies = calculate_allele_frequencies(vcf, populations)
    
    # 3. Hardy-Weinberg equilibrium testing
    test_hardy_weinberg_equilibrium(vcf, populations)
    
    # 4. Genotype quality assessment  
    assess_genotype_quality(vcf, populations)
    
    # 5. Population-specific variants
    identify_population_specific_variants(vcf, populations)
    
    # 6. Variant filtering
    perform_variant_filtering(vcf, populations)
    
    # Summary
    print("\n" + "=" * 60)
    print("TUTORIAL SUMMARY")
    print("=" * 60)
    print("This tutorial demonstrated:")
    print("1. ✓ Dataset overview and population structure")
    print("2. ✓ Allele frequency calculations across populations")
    print("3. ✓ Hardy-Weinberg equilibrium testing")
    print("4. ✓ Genotype quality assessment")
    print("5. ✓ Population-specific variant identification")
    print("6. ✓ Variant filtering and quality control")
    print()
    print("Next steps:")
    print("- Try the analysis with the larger population_genetics.vcf dataset")
    print("- Implement statistical tests with scipy")
    print("- Create visualizations with matplotlib")
    print("- Apply filtering to your own VCF data")
    print()
    print("For more tutorials, see TUTORIAL/README.md")

if __name__ == "__main__":
    main()
