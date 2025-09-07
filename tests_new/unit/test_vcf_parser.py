"""
Unit tests for VcfParser class.
"""
import pytest
import gzip
from unittest.mock import patch, mock_open
from vcfparser import VcfParser
from vcfparser.vcf_parser import VcfParser as VcfParserClass


class TestVcfParserInit:
    """Test VcfParser initialization."""
    
    def test_init_regular_vcf_file(self, small_vcf_file):
        """Test initialization with regular VCF file."""
        parser = VcfParser(str(small_vcf_file))
        assert parser.filename == str(small_vcf_file)
        assert parser._open == open
        
    def test_init_gzipped_vcf_file(self, gzipped_vcf_file):
        """Test initialization with gzipped VCF file."""
        parser = VcfParser(str(gzipped_vcf_file))
        assert parser.filename == str(gzipped_vcf_file)
        assert parser._open == gzip.open
        
    def test_init_file_not_found(self):
        """Test initialization with non-existent file."""
        with pytest.raises(FileNotFoundError):
            VcfParser("non_existent_file.vcf")
            
    def test_destructor_closes_files(self, small_vcf_file):
        """Test that destructor properly closes file handles."""
        parser = VcfParser(str(small_vcf_file))
        # Files should be opened
        assert not parser._file.closed
        assert not parser._file_copy.closed
        # Delete parser
        del parser


class TestVcfParserParseMetadata:
    """Test metadata parsing functionality."""
    
    def test_parse_metadata_basic(self, vcf_parser):
        """Test basic metadata parsing."""
        metadata = vcf_parser.parse_metadata()
        
        assert metadata.fileformat == "VCFv4.2"
        assert len(metadata.infos_) == 4  # AC, AF, AN, DP
        assert len(metadata.format_) == 3  # GT, DP, GQ
        assert metadata.sample_names == ['Sample1', 'Sample2', 'Sample3']
        
    def test_parse_metadata_info_fields(self, vcf_parser):
        """Test INFO field parsing."""
        metadata = vcf_parser.parse_metadata()
        
        info_ids = [info['ID'] for info in metadata.infos_]
        assert 'AC' in info_ids
        assert 'AF' in info_ids
        assert 'AN' in info_ids
        assert 'DP' in info_ids
        
    def test_parse_metadata_format_fields(self, vcf_parser):
        """Test FORMAT field parsing."""
        metadata = vcf_parser.parse_metadata()
        
        format_ids = [fmt['ID'] for fmt in metadata.format_]
        assert 'GT' in format_ids
        assert 'DP' in format_ids
        assert 'GQ' in format_ids
        
    def test_parse_metadata_sample_names(self, vcf_parser):
        """Test sample name extraction."""
        metadata = vcf_parser.parse_metadata()
        
        expected_samples = ['Sample1', 'Sample2', 'Sample3']
        assert metadata.sample_names == expected_samples
        
    def test_parse_metadata_record_keys(self, vcf_parser):
        """Test record keys extraction."""
        metadata = vcf_parser.parse_metadata()
        
        expected_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'Sample1', 'Sample2', 'Sample3']
        assert metadata.record_keys == expected_keys


class TestVcfParserParseRecords:
    """Test record parsing functionality."""
    
    def test_parse_records_basic(self, vcf_parser):
        """Test basic record parsing."""
        records = list(vcf_parser.parse_records())
        
        assert len(records) == 3
        assert records[0].CHROM == "chr1"
        assert records[0].POS == "1000"
        assert records[0].REF == "A"
        assert records[0].ALT == ["G"]
        
    def test_parse_records_multiple_alt_alleles(self, vcf_parser):
        """Test parsing records with multiple ALT alleles."""
        records = list(vcf_parser.parse_records())
        
        # Third record has multiple ALT alleles
        multi_alt_record = records[2]
        assert multi_alt_record.ALT == ["A", "T"]
        
    def test_parse_records_info_parsing(self, vcf_parser):
        """Test INFO field parsing in records."""
        records = list(vcf_parser.parse_records())
        
        first_record = records[0]
        info_dict = first_record.get_info_as_dict()
        
        assert info_dict['AC'] == '2'
        assert info_dict['AF'] == '0.33'
        assert info_dict['AN'] == '6'
        assert info_dict['DP'] == '100'
        
    def test_parse_records_format_parsing(self, vcf_parser):
        """Test FORMAT field parsing in records."""
        records = list(vcf_parser.parse_records())
        
        first_record = records[0]
        assert first_record.format_ == ['GT', 'DP', 'GQ']
        
    def test_parse_records_sample_data(self, vcf_parser):
        """Test sample data parsing."""
        records = list(vcf_parser.parse_records())
        
        first_record = records[0]
        sample_map = first_record.mapped_format_to_sample
        
        assert 'Sample1' in sample_map
        assert sample_map['Sample1']['GT'] == '0/1'
        assert sample_map['Sample1']['DP'] == '20'
        assert sample_map['Sample1']['GQ'] == '30'
        
    def test_parse_records_with_chrom_filter(self, vcf_parser):
        """Test parsing records filtered by chromosome."""
        records = list(vcf_parser.parse_records(chrom='chr1'))
        
        assert len(records) == 2
        assert all(record.CHROM == 'chr1' for record in records)
        
    def test_parse_records_with_position_range(self, vcf_parser):
        """Test parsing records filtered by position range."""
        records = list(vcf_parser.parse_records(pos_range=(1000, 1500)))
        
        assert len(records) == 2  # chr1:1000 and chr2:1500
        
    def test_parse_records_with_chrom_and_position_filter(self, vcf_parser):
        """Test parsing records with both chromosome and position filters."""
        records = list(vcf_parser.parse_records(chrom='chr1', pos_range=(1000, 2000)))
        
        assert len(records) == 2
        assert all(record.CHROM == 'chr1' for record in records)
        assert all(1000 <= int(record.POS) <= 2000 for record in records)


class TestVcfParserErrors:
    """Test error handling in VcfParser."""
    
    def test_empty_file_handling(self, empty_vcf_file):
        """Test handling of empty VCF files."""
        parser = VcfParser(str(empty_vcf_file))
        metadata = parser.parse_metadata()
        records = list(parser.parse_records())
        
        assert metadata.fileformat == "VCFv4.2"
        assert len(records) == 0
        
    def test_malformed_position_handling(self):
        """Test handling of malformed position data."""
        # This would be tested with more complex error scenarios
        pass


class TestVcfParserIntegration:
    """Integration tests for VcfParser."""
    
    def test_complete_workflow(self, vcf_parser):
        """Test complete parsing workflow."""
        # Parse metadata
        metadata = vcf_parser.parse_metadata()
        assert metadata is not None
        
        # Parse records
        records = list(vcf_parser.parse_records())
        assert len(records) > 0
        
        # Verify consistency between metadata and records
        assert len(metadata.sample_names) == len(records[0].sample_names)
        
    def test_multiple_parse_calls(self, vcf_parser):
        """Test that multiple parse calls work correctly."""
        # First parse
        metadata1 = vcf_parser.parse_metadata()
        records1 = list(vcf_parser.parse_records())
        
        # Create new parser instance (simulating multiple calls)
        vcf_parser2 = VcfParser(vcf_parser.filename)
        metadata2 = vcf_parser2.parse_metadata()
        records2 = list(vcf_parser2.parse_records())
        
        # Results should be identical
        assert metadata1.fileformat == metadata2.fileformat
        assert len(records1) == len(records2)
