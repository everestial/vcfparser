#!/usr/bin/env python3
"""
Script to create tutorial.vcf from reference test data

This script generates a comprehensive tutorial VCF file with:
- 612 variant records from real genomics data
- 7 anonymized samples (Sample01-Sample07)  
- Rich metadata (23 INFO fields, 16 FORMAT fields)
- Privacy-safe data suitable for tutorials

Usage:
    python create_tutorial_vcf.py

The generated tutorial.vcf file is used by examples/advanced_tutorial.py
"""

import re
import os
from pathlib import Path

def create_tutorial_vcf():
    """Create tutorial.vcf from reference test data"""
    
    input_file = Path("../tests/testfiles/vcf_parser_input/reference_input_test.vcf")
    output_file = Path("data/tutorial.vcf")
    
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        print("This script requires the reference test data to be present.")
        return False
    
    # Sample name mapping for anonymization
    sample_mapping = {
        'ms01e': 'Sample01',
        'ms02g': 'Sample02', 
        'ms03g': 'Sample03',
        'ms04h': 'Sample04',
        'MA611': 'Sample05',
        'MA605': 'Sample06',
        'MA622': 'Sample07'
    }
    
    print("🧹 Creating tutorial.vcf file...")
    print(f"📖 Input: {input_file}")
    print(f"📝 Output: {output_file}")
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines_processed = 0
        lines_written = 0
        
        for line in infile:
            lines_processed += 1
            
            # Skip private GATK command line information
            if line.startswith('##GATKCommandLine') or (line.startswith('##reference=') and 'SeagateBackup' in line):
                continue
            
            # Sanitize reference path
            if line.startswith('##reference='):
                line = '##reference=file:///reference_genome/genome.fa\n'
            
            # Skip all scaffold contigs - we'll add standard chromosomes
            if line.startswith('##contig='):
                continue
            
            # Replace sample names throughout file
            for old_name, new_name in sample_mapping.items():
                if old_name in line:
                    line = line.replace(old_name, new_name)
            
            # Remove private file paths
            line = re.sub(r'/media/everestial007/[^"\s]*', '/data/', line)
            line = re.sub(r'/home/bkgiri/[^"\s]*', '/reference/', line)
            
            # Add standard contig information after ALT line
            if line.startswith('##ALT='):
                outfile.write(line)
                # Add chr01-08 contigs
                contig_data = [
                    ('chr01', 248956422), ('chr02', 242193529), ('chr03', 198295559), ('chr04', 190214555),
                    ('chr05', 181538259), ('chr06', 170805979), ('chr07', 159345973), ('chr08', 145138636)
                ]
                for chrom, length in contig_data:
                    outfile.write(f'##contig=<ID={chrom},length={length}>\n')
                lines_written += 1 + len(contig_data)
                continue
            
            # Convert chromosome 2 to chr02 in data records
            if not line.startswith('#') and line.strip():
                line = re.sub(r'^2\t', 'chr02\t', line)
                
            outfile.write(line)
            lines_written += 1
    
    # Fix any remaining sample name issues
    with open(output_file, 'r') as f:
        content = f.read()
    
    content = content.replace('SSample04', 'Sample04').replace('ample04', 'Sample04')
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Tutorial VCF created successfully!")
    print(f"📊 Statistics:")
    print(f"  • Lines processed: {lines_processed}")
    print(f"  • Lines written: {lines_written}")
    print(f"  • Sample names anonymized: {len(sample_mapping)}")
    print(f"  • Output file size: {output_file.stat().st_size:,} bytes")
    
    # Verify the file with vcfparser
    try:
        import sys
        sys.path.insert(0, '..')
        from vcfparser import VcfParser
        
        vcf = VcfParser(str(output_file))
        metadata = vcf.parse_metadata()
        records = list(vcf.parse_records())
        
        print(f"\n🔍 Verification:")
        print(f"  • VCF format: {metadata.fileformat}")
        print(f"  • Samples: {len(metadata.sample_names)} ({', '.join(metadata.sample_names)})")
        print(f"  • Total variants: {len(records)}")
        print(f"  • INFO fields: {len(metadata.infos_)}")
        print(f"  • FORMAT fields: {len(metadata.format_)}")
        
        print(f"\n🎯 Ready for advanced tutorial!")
        print(f"Run: python examples/advanced_tutorial.py")
        
    except ImportError:
        print(f"\n⚠️  Could not verify with vcfparser (not installed)")
        print(f"File created successfully - ready for use!")
    
    return True

if __name__ == "__main__":
    success = create_tutorial_vcf()
    if not success:
        exit(1)
