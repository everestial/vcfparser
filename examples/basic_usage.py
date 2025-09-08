#!/usr/bin/env python3
"""
Basic vcfparser Usage Examples
===============================

This script demonstrates all the usage patterns from the README using the example.vcf file.
Run this script from the vcfparser root directory:
    python examples/basic_usage.py
"""

import sys
import os

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vcfparser import VcfParser
from vcfparser.metaviewer import MetaDataViewer
from vcfparser.vcf_writer import VCFWriter

def example_1_basic_parsing():
    """📖 Example 1: Basic VCF Parsing"""
    print("📖 Example 1: Basic VCF Parsing")
    print("=" * 40)
    
    # Initialize parser
    vcf = VcfParser("example.vcf")
    
    # Parse metadata (header information)
    metadata = vcf.parse_metadata()
    print(f"VCF version: {metadata.fileformat}")           
    print(f"Samples: {metadata.sample_names}")             
    print(f"INFO fields: {len(metadata.infos_)}")          
    print(f"FORMAT fields: {len(metadata.format_)}")       
    
    # Parse records (data lines) - returns iterator for memory efficiency
    records = vcf.parse_records()
    print("\nFirst 3 variants:")
    for i, record in enumerate(records):
        print(f"  Variant {i+1}: {record.CHROM}:{record.POS} {record.REF}→{record.ALT}")
        print(f"    Quality: {record.QUAL}, Filter: {record.FILTER}")
        if i >= 2:  # Just show first 3 records
            break
    print()

def example_2_genotype_analysis():
    """🧬 Example 2: Advanced Genotype Analysis"""
    print("🧬 Example 2: Advanced Genotype Analysis")
    print("=" * 45)
    
    vcf = VcfParser("example.vcf")
    records = vcf.parse_records()
    first_record = next(records)
    
    print(f"Analyzing variant: {first_record.CHROM}:{first_record.POS} {first_record.REF}→{first_record.ALT}")
    
    # Access genotype analysis methods
    gt = first_record.genotype_property
    
    # Find samples by genotype type (returns Dict[str, str])
    homref_samples = gt.isHOMREF()       
    hetvar_samples = gt.isHETVAR()       
    homvar_samples = gt.isHOMVAR()       
    missing_samples = gt.isMissing()     
    
    print(f"HOMREF samples: {homref_samples}")
    print(f"HETVAR samples: {hetvar_samples}")
    print(f"HOMVAR samples: {homvar_samples}")
    print(f"Missing samples: {missing_samples}")
    
    # Variant type analysis
    variant_types = []
    if gt.hasSNP():
        variant_types.append("SNP")
    if gt.hasINDEL():
        variant_types.append("INDEL")
    print(f"Variant types: {', '.join(variant_types) if variant_types else 'None detected'}")
        
    # Phase information
    phased_samples = gt.has_phased()     
    unphased_samples = gt.has_unphased() 
    
    print(f"Phased samples: {len(phased_samples)}")
    print(f"Unphased samples: {len(unphased_samples)}")
    print()

def example_3_metadata_export():
    """📊 Example 3: Metadata Export & Visualization"""
    print("📊 Example 3: Metadata Export & Visualization")
    print("=" * 50)
    
    # Create metadata viewer
    viewer = MetaDataViewer("example.vcf", "example_output")
    
    # Export metadata in multiple formats
    print("Exporting metadata to:")
    viewer.save_as_json()
    print("  ✓ example_output.json")
    
    viewer.save_as_table()
    print("  ✓ example_output.table")
    
    viewer.save_as_orderdict()
    print("  ✓ example_output.dict")
    
    # Print specific metadata sections
    print("\nINFO and FORMAT metadata:")
    viewer.print_requested_metadata(["INFO", "FORMAT"])
    
    # Programmatic access to organized metadata
    metadata_dict = viewer.metadict
    info_fields = metadata_dict["INFO"]
    format_fields = metadata_dict["FORMAT"]
    print(f"\nAvailable INFO tags: {[info['ID'] for info in info_fields]}")
    print(f"Available FORMAT tags: {[fmt['ID'] for fmt in format_fields]}")
    print()

def example_4_writing_vcf():
    """✍️ Example 4: Writing VCF Files"""
    print("✍️ Example 4: Writing VCF Files")
    print("=" * 35)
    
    output_file = "examples/example_output.vcf"
    
    # Modern context manager approach (recommended)
    with VCFWriter(output_file) as writer:
        # Add metadata
        writer.add_normal_metadata("fileformat", "VCFv4.3")
        writer.add_normal_metadata("fileDate", "20240108")
        
        # Add INFO field definitions
        writer.add_info("DP", "1", "Integer", "Total read depth")
        writer.add_info("AF", "A", "Float", "Allele frequency")
        
        # Add FORMAT field definitions  
        writer.add_format("GT", "1", "String", "Genotype")
        writer.add_format("DP", "1", "Integer", "Read depth")
        
        # Add FILTER definitions
        writer.add_filter("PASS", "All filters passed")
        writer.add_filter("LowQual", "Low quality variant")
        
        # Add reference contigs
        writer.add_contig("chr1", 248956422)
        writer.add_contig("chr2", 242193529)
        
        # Add column header
        writer.add_header_line(["#CHROM", "POS", "ID", "REF", "ALT", 
                               "QUAL", "FILTER", "INFO", "FORMAT", "Sample01"])
        
        # Add variant records
        writer.add_record_from_parts(
            "chr1", 123456, "rs123", "A", "T", 
            "60", "PASS", "DP=20;AF=0.5", 
            "GT:DP", "1/1:20"  # all positional arguments
        )
        
    print(f"✓ VCF file written successfully: {output_file}")
    
    # Verify the file was created
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            lines = f.readlines()
        print(f"  File contains {len(lines)} lines")
    print()

def example_5_sample_data():
    """📈 Example 5: Working with Sample Data"""
    print("📈 Example 5: Working with Sample Data")
    print("=" * 40)
    
    vcf = VcfParser("example.vcf")
    records = vcf.parse_records()
    record = next(records)
    
    print(f"Analyzing variant: {record.CHROM}:{record.POS} {record.REF}→{record.ALT}")
    
    # Get sample format mapping
    sample_data = record.get_format_to_sample_map()
    print(f"Total samples: {len(sample_data)}")
    
    print("\nSample details:")
    for sample_name, format_values in sample_data.items():
        genotype = format_values.get('GT', './.')
        depth = format_values.get('DP', '0')
        quality = format_values.get('GQ', '.')
        print(f"  {sample_name}: GT={genotype}, DP={depth}, GQ={quality}")
    
    # Filter samples by specific criteria
    samples_with_coverage = {
        sample: data for sample, data in sample_data.items() 
        if int(data.get('DP', '0')) >= 5
    }
    print(f"\nSamples with DP ≥ 5: {list(samples_with_coverage.keys())}")
    
    # Get INFO field as dictionary
    info_dict = record.get_info_as_dict()
    allele_freq = info_dict.get('AF', 'Not available')
    total_depth = info_dict.get('DP', 'Not available')
    print(f"Allele frequency: {allele_freq}")
    print(f"Total depth: {total_depth}")
    print()

def example_6_type_safe_development():
    """🔍 Example 6: Type-Safe Development"""
    print("🔍 Example 6: Type-Safe Development")
    print("=" * 40)
    
    from typing import Dict, Iterator
    from vcfparser.record_parser import Record
    
    def analyze_variants(vcf_file: str) -> Dict[str, int]:
        """Analyze variants with full type safety."""
        vcf: VcfParser = VcfParser(vcf_file)
        records: Iterator[Record] = vcf.parse_records()
        
        stats: Dict[str, int] = {
            'total': 0, 'snp': 0, 'indel': 0, 
            'homref': 0, 'hetvar': 0, 'homvar': 0
        }
        
        for record in records:
            stats['total'] += 1
            
            # Type hints provide IDE autocompletion
            gt = record.genotype_property
            if gt.hasSNP():
                stats['snp'] += 1
            if gt.hasINDEL():
                stats['indel'] += 1
                
            # Dict[str, str] return types are guaranteed
            stats['homref'] += len(gt.isHOMREF())
            stats['hetvar'] += len(gt.isHETVAR())
            stats['homvar'] += len(gt.isHOMVAR())
        
        return stats
    
    # mypy will catch any type errors at development time!
    result: Dict[str, int] = analyze_variants("example.vcf")
    print(f"Analysis results: {result}")
    print()

def main():
    """Run all examples"""
    print("🚀 vcfparser Usage Examples")
    print("=" * 60)
    print("This script demonstrates all usage patterns from the README.\n")
    
    # Check if example.vcf exists
    if not os.path.exists("example.vcf"):
        print("❌ Error: example.vcf not found!")
        print("Please run this script from the vcfparser root directory.")
        return
    
    try:
        example_1_basic_parsing()
        example_2_genotype_analysis()
        example_3_metadata_export()
        example_4_writing_vcf()
        example_5_sample_data()
        example_6_type_safe_development()
        
        print("🎉 All examples completed successfully!")
        print("\nGenerated files:")
        generated_files = [
            "example_output.json", "example_output.table", "example_output.dict",
            "examples/example_output.vcf"
        ]
        for f in generated_files:
            if os.path.exists(f):
                print(f"  ✓ {f}")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
