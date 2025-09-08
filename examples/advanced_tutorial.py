#!/usr/bin/env python3
"""
Advanced vcfparser Tutorial
============================

This tutorial uses the more comprehensive examples/data/tutorial.vcf file (612 variants, 7 samples)
to demonstrate advanced vcfparser features and real-world genomics workflows.

The examples/data/tutorial.vcf file contains sanitized genomics data with:
- 7 anonymized samples (Sample01-Sample07)
- 612 variant records on chromosome 2
- Rich metadata with 23 INFO fields and 16 FORMAT fields
- Various types of variants (SNPs, INDELs, complex variants)

Run this script from the vcfparser root directory:
    python examples/advanced_tutorial.py
"""

import sys
import os
from collections import defaultdict
from typing import Dict, List, Iterator, Set

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vcfparser import VcfParser
from vcfparser.metaviewer import MetaDataViewer
from vcfparser.record_parser import Record

def tutorial_1_comprehensive_overview():
    """🔍 Tutorial 1: Comprehensive Dataset Overview"""
    print("🔍 Tutorial 1: Comprehensive Dataset Overview")
    print("=" * 55)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    metadata = vcf.parse_metadata()
    
    print("📋 Dataset Summary:")
    print(f"  VCF Format: {metadata.fileformat}")
    print(f"  Total Samples: {len(metadata.sample_names)}")
    print(f"  Sample Names: {', '.join(metadata.sample_names)}")
    print(f"  INFO Fields: {len(metadata.infos_)}")
    print(f"  FORMAT Fields: {len(metadata.format_)}")
    print(f"  FILTER Fields: {len(metadata.filters_)}")
    
    # Count total variants
    records = list(vcf.parse_records())
    print(f"  Total Variants: {len(records)}")
    
    # Analyze chromosome distribution
    chroms = set(record.CHROM for record in records)
    print(f"  Chromosomes: {', '.join(sorted(chroms))}")
    
    # Position range
    positions = [int(record.POS) for record in records]
    print(f"  Position Range: {min(positions):,} - {max(positions):,}")
    
    print("\n✨ This is a rich dataset perfect for exploring advanced genomics patterns!\n")

def tutorial_2_variant_classification():
    """🧬 Tutorial 2: Advanced Variant Classification"""
    print("🧬 Tutorial 2: Advanced Variant Classification")
    print("=" * 50)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    records = list(vcf.parse_records())
    
    # Classify variants by type
    snp_count = 0
    indel_count = 0
    complex_count = 0
    multiallelic_count = 0
    
    variant_types = defaultdict(int)
    
    for record in records:
        gt = record.genotype_property
        
        # Count basic types
        if gt.hasSNP():
            snp_count += 1
        if gt.hasINDEL():
            indel_count += 1
            
        # Check for multiallelic variants
        alt_alleles = record.ALT if isinstance(record.ALT, list) else [record.ALT]
        if len(alt_alleles) > 1:
            multiallelic_count += 1
            
        # Classify by complexity
        ref_len = len(record.REF)
        for alt in alt_alleles:
            alt_len = len(alt)
            if ref_len == 1 and alt_len == 1:
                variant_types['SNP'] += 1
            elif abs(ref_len - alt_len) == 1:
                variant_types['Simple INDEL'] += 1
            elif abs(ref_len - alt_len) > 1:
                variant_types['Complex INDEL'] += 1
            else:
                variant_types['Other'] += 1
    
    print("🎯 Variant Classification Results:")
    print(f"  SNPs: {snp_count} variants")
    print(f"  INDELs: {indel_count} variants")
    print(f"  Multiallelic: {multiallelic_count} variants")
    
    print("\n📊 Detailed Breakdown:")
    for vtype, count in sorted(variant_types.items()):
        percentage = (count / sum(variant_types.values())) * 100
        print(f"  {vtype}: {count} ({percentage:.1f}%)")
    
    print()

def tutorial_3_quality_analysis():
    """📈 Tutorial 3: Quality and Filtering Analysis"""
    print("📈 Tutorial 3: Quality and Filtering Analysis")
    print("=" * 50)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    records = list(vcf.parse_records())
    
    # Quality score analysis
    qualities = []
    filter_counts = defaultdict(int)
    
    for record in records:
        if record.QUAL != '.' and record.QUAL != 'QUAL':
            try:
                qualities.append(float(record.QUAL))
            except ValueError:
                pass
                
        # Count filter status
        filters = record.FILTER if isinstance(record.FILTER, list) else [record.FILTER]
        for filt in filters:
            filter_counts[filt] += 1
    
    # Calculate quality statistics
    if qualities:
        qualities.sort()
        n = len(qualities)
        min_qual = min(qualities)
        max_qual = max(qualities)
        mean_qual = sum(qualities) / n
        median_qual = qualities[n//2] if n % 2 == 1 else (qualities[n//2-1] + qualities[n//2]) / 2
        
        print("🎯 Quality Score Analysis:")
        print(f"  Variants with Quality Scores: {len(qualities)}")
        print(f"  Min Quality: {min_qual:.2f}")
        print(f"  Max Quality: {max_qual:.2f}")
        print(f"  Mean Quality: {mean_qual:.2f}")
        print(f"  Median Quality: {median_qual:.2f}")
        
        # Quality quartiles
        q1 = qualities[n//4]
        q3 = qualities[3*n//4]
        print(f"  Q1 (25th percentile): {q1:.2f}")
        print(f"  Q3 (75th percentile): {q3:.2f}")
    
    print("\n🚦 Filter Status Distribution:")
    total_filters = sum(filter_counts.values())
    for filt, count in sorted(filter_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_filters) * 100
        print(f"  {filt}: {count} ({percentage:.1f}%)")
    
    print()

def tutorial_4_population_genetics():
    """👥 Tutorial 4: Population Genetics Analysis"""
    print("👥 Tutorial 4: Population Genetics Analysis")
    print("=" * 45)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    records = list(vcf.parse_records())
    
    # Sample-level statistics
    sample_stats = defaultdict(lambda: {'homref': 0, 'hetvar': 0, 'homvar': 0, 'missing': 0})
    
    # Overall population statistics
    total_variants_analyzed = 0
    allele_frequency_dist = []
    
    for record in records:
        gt = record.genotype_property
        total_variants_analyzed += 1
        
        # Get genotype counts for each sample
        homref = gt.isHOMREF()
        hetvar = gt.isHETVAR() 
        homvar = gt.isHOMVAR()
        missing = gt.isMissing()
        
        # Update per-sample statistics
        for sample in homref:
            sample_stats[sample]['homref'] += 1
        for sample in hetvar:
            sample_stats[sample]['hetvar'] += 1
        for sample in homvar:
            sample_stats[sample]['homvar'] += 1
        for sample in missing:
            sample_stats[sample]['missing'] += 1
            
        # Calculate allele frequency for this variant
        total_alleles = 2 * (len(homref) + len(hetvar) + len(homvar))  # Diploid
        if total_alleles > 0:
            alt_alleles = len(hetvar) + 2 * len(homvar)
            allele_freq = alt_alleles / total_alleles
            allele_frequency_dist.append(allele_freq)
    
    print("🧬 Per-Sample Genotype Distribution:")
    print(f"{'Sample':<10} {'HOMREF':<8} {'HETVAR':<8} {'HOMVAR':<8} {'Missing':<8} {'Call Rate':<10}")
    print("-" * 65)
    
    for sample in sorted(sample_stats.keys()):
        stats = sample_stats[sample]
        total_calls = sum(stats.values())
        call_rate = ((total_calls - stats['missing']) / total_calls) * 100 if total_calls > 0 else 0
        
        print(f"{sample:<10} {stats['homref']:<8} {stats['hetvar']:<8} {stats['homvar']:<8} {stats['missing']:<8} {call_rate:<10.1f}%")
    
    # Allele frequency spectrum
    if allele_frequency_dist:
        print(f"\n📊 Allele Frequency Spectrum (n={len(allele_frequency_dist)} variants):")
        
        # Categorize by frequency
        rare = sum(1 for af in allele_frequency_dist if 0 < af <= 0.01)
        low_freq = sum(1 for af in allele_frequency_dist if 0.01 < af <= 0.05)
        common = sum(1 for af in allele_frequency_dist if 0.05 < af < 0.95)
        high_freq = sum(1 for af in allele_frequency_dist if 0.95 <= af < 1.0)
        fixed = sum(1 for af in allele_frequency_dist if af == 1.0)
        
        print(f"  Rare (0-1%): {rare} variants")
        print(f"  Low frequency (1-5%): {low_freq} variants")
        print(f"  Common (5-95%): {common} variants") 
        print(f"  High frequency (95-99%): {high_freq} variants")
        print(f"  Fixed (100%): {fixed} variants")
    
    print()

def tutorial_5_advanced_metadata_exploration():
    """📚 Tutorial 5: Advanced Metadata Exploration"""
    print("📚 Tutorial 5: Advanced Metadata Exploration")
    print("=" * 50)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    metadata = vcf.parse_metadata()
    
    print("🎯 INFO Field Analysis:")
    print(f"Total INFO fields defined: {len(metadata.infos_)}")
    
    # Categorize INFO fields by type and number
    info_by_type = defaultdict(list)
    info_by_number = defaultdict(list)
    
    for info in metadata.infos_:
        info_by_type[info.get('Type', 'Unknown')].append(info['ID'])
        info_by_number[info.get('Number', 'Unknown')].append(info['ID'])
    
    print("\nBy Data Type:")
    for data_type, fields in sorted(info_by_type.items()):
        print(f"  {data_type}: {len(fields)} fields ({', '.join(fields[:5])}{'...' if len(fields) > 5 else ''})")
    
    print("\nBy Number:")
    for number, fields in sorted(info_by_number.items()):
        print(f"  {number}: {len(fields)} fields")
    
    print(f"\n🎯 FORMAT Field Analysis:")
    print(f"Total FORMAT fields defined: {len(metadata.format_)}")
    
    format_by_type = defaultdict(list)
    for fmt in metadata.format_:
        format_by_type[fmt.get('Type', 'Unknown')].append(fmt['ID'])
    
    print("By Data Type:")
    for data_type, fields in sorted(format_by_type.items()):
        print(f"  {data_type}: {', '.join(fields)}")
    
    # Show contig information
    if hasattr(metadata, 'contig') and metadata.contig:
        print(f"\n🗺️ Reference Contigs: {len(metadata.contig)} defined")
        for contig in metadata.contig[:3]:  # Show first 3
            print(f"  {contig['ID']}: {contig.get('length', 'Unknown')} bp")
        if len(metadata.contig) > 3:
            print(f"  ... and {len(metadata.contig) - 3} more")
    else:
        print("\n🗺️ Reference Contigs: None defined")
    
    print()

def tutorial_6_advanced_filtering():
    """🔎 Tutorial 6: Advanced Filtering and Selection"""
    print("🔎 Tutorial 6: Advanced Filtering and Selection")
    print("=" * 50)
    
    vcf = VcfParser("examples/data/tutorial.vcf")
    records = list(vcf.parse_records())
    
    print("🎯 Applying Various Filtering Criteria:")
    
    # Filter 1: High-quality SNPs
    hq_snps = []
    for record in records:
        if (record.genotype_property.hasSNP() and 
            record.FILTER == ['PASS'] and
            record.QUAL != '.' and float(record.QUAL) >= 30):
            hq_snps.append(record)
    
    print(f"  High-quality SNPs (QUAL≥30, PASS): {len(hq_snps)}")
    
    # Filter 2: Variants with good coverage
    good_coverage = []
    for record in records:
        info_dict = record.get_info_as_dict()
        if 'DP' in info_dict:
            try:
                depth = int(info_dict['DP'])
                if depth >= 10:
                    good_coverage.append(record)
            except ValueError:
                pass
    
    print(f"  Variants with depth ≥10: {len(good_coverage)}")
    
    # Filter 3: Variants with low allele frequency
    rare_variants = []
    for record in records:
        info_dict = record.get_info_as_dict()
        if 'AF' in info_dict:
            try:
                af = float(info_dict['AF'])
                if af <= 0.05:  # 5% or less
                    rare_variants.append(record)
            except ValueError:
                pass
    
    print(f"  Rare variants (AF≤5%): {len(rare_variants)}")
    
    # Filter 4: Variants called in all samples
    complete_call_variants = []
    for record in records:
        gt = record.genotype_property
        missing = gt.isMissing()
        if len(missing) == 0:  # No missing calls
            complete_call_variants.append(record)
    
    print(f"  Variants with complete calls: {len(complete_call_variants)}")
    
    # Show example of a high-quality variant
    if hq_snps:
        example = hq_snps[0]
        print(f"\n📋 Example High-Quality SNP:")
        print(f"  Position: {example.CHROM}:{example.POS}")
        print(f"  Alleles: {example.REF} → {example.ALT}")
        print(f"  Quality: {example.QUAL}")
        print(f"  Filter: {example.FILTER}")
        
        # Show genotypes for this variant
        sample_data = example.get_format_to_sample_map()
        print("  Genotypes:")
        for sample, data in list(sample_data.items())[:4]:  # Show first 4 samples
            gt = data.get('GT', './.')
            dp = data.get('DP', '.')
            gq = data.get('GQ', '.')
            print(f"    {sample}: GT={gt}, DP={dp}, GQ={gq}")
    
    print()

def tutorial_7_data_export():
    """💾 Tutorial 7: Data Export and Visualization"""
    print("💾 Tutorial 7: Data Export and Visualization")
    print("=" * 45)
    
    # Export metadata in multiple formats
    viewer = MetaDataViewer("examples/data/tutorial.vcf", "examples/output/tutorial_output")
    
    print("📤 Exporting metadata:")
    viewer.save_as_json()
    print("  ✓ examples/output/tutorial_output.json")
    
    viewer.save_as_table()
    print("  ✓ examples/output/tutorial_output.table")
    
    # Create custom summary report
    vcf = VcfParser("examples/data/tutorial.vcf")
    records = list(vcf.parse_records())
    
    with open("examples/output/tutorial_variant_summary.txt", "w") as f:
        f.write("VCF Variant Summary Report\n")
        f.write("=" * 30 + "\n\n")
        
        f.write(f"Total variants: {len(records)}\n")
        f.write(f"Chromosomes: {', '.join(set(r.CHROM for r in records))}\n")
        
        # Write first 10 variants
        f.write("\nFirst 10 variants:\n")
        f.write("CHROM\tPOS\tREF\tALT\tQUAL\tFILTER\n")
        for i, record in enumerate(records[:10]):
            f.write(f"{record.CHROM}\t{record.POS}\t{record.REF}\t{record.ALT}\t{record.QUAL}\t{record.FILTER}\n")
    
    print("  ✓ examples/output/tutorial_variant_summary.txt")
    
    print("\n📊 Generated files contain:")
    print("  • Complete metadata in JSON format")
    print("  • Formatted metadata tables") 
    print("  • Custom variant summary report")
    
    print()

def main():
    """Run the advanced tutorial"""
    print("🚀 Advanced vcfparser Tutorial")
    print("=" * 60)
    print("This tutorial demonstrates advanced vcfparser features using a")
    print("comprehensive dataset with 612 variants and 7 samples.\n")
    
    # Check if examples/data/tutorial.vcf exists
    if not os.path.exists("examples/data/tutorial.vcf"):
        print("❌ Error: examples/data/tutorial.vcf not found!")
        print("Please ensure examples/data/tutorial.vcf is in the current directory.")
        print("You can create it by running: python examples/create_tutorial_vcf.py")
        return
    
    try:
        tutorial_1_comprehensive_overview()
        tutorial_2_variant_classification()
        tutorial_3_quality_analysis()
        tutorial_4_population_genetics()
        tutorial_5_advanced_metadata_exploration()
        tutorial_6_advanced_filtering()
        tutorial_7_data_export()
        
        print("🎉 Advanced tutorial completed successfully!")
        print("\n📚 What you learned:")
        print("  • Comprehensive dataset analysis")
        print("  • Variant classification and typing")
        print("  • Quality assessment and filtering")
        print("  • Population genetics calculations")
        print("  • Advanced metadata exploration")
        print("  • Complex filtering strategies")
        print("  • Data export and reporting")
        
        print("\n🎯 Next steps:")
        print("  • Try modifying the filtering criteria")
        print("  • Explore other INFO fields in your data")
        print("  • Implement custom analysis workflows")
        print("  • Scale these methods to larger datasets")
        
    except Exception as e:
        print(f"❌ Error running tutorial: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
