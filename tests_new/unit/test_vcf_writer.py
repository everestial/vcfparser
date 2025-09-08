"""
Unit tests for VCFWriter class.
"""
import pytest
import os
from vcfparser import VCFWriter


class TestVCFWriterInit:
    """Test VCFWriter initialization."""
    
    def test_init_with_filename(self, temp_output_file):
        """Test VCFWriter initialization."""
        writer = VCFWriter(str(temp_output_file))
        assert writer.w_file is not None
        writer.w_file.close()  # Clean up
        
    def test_init_creates_file(self, temp_output_file):
        """Test that initialization creates the output file."""
        writer = VCFWriter(str(temp_output_file))
        writer.w_file.close()  # Close to ensure file is created
        
        assert temp_output_file.exists()


class TestVCFWriterMetadataMethods:
    """Test VCFWriter metadata writing methods."""
    
    def test_add_normal_metadata(self, temp_output_file):
        """Test adding normal metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_normal_metadata("fileformat", "VCFv4.2")
        writer.add_normal_metadata("source", "test_program")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        assert "##fileformat=VCFv4.2" in content
        assert "##source=test_program" in content
        
    def test_add_info_metadata(self, temp_output_file):
        """Test adding INFO metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_info(
            id="AC", 
            num="A", 
            type="Integer", 
            desc="Allele count in genotypes"
        )
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes">'
        assert expected in content
        
    def test_add_info_with_defaults(self, temp_output_file):
        """Test adding INFO metadata with default values."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_info(id="TEST")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##INFO=<ID=TEST,Number=.,Type=.,Description="">'
        assert expected in content
        
    def test_add_format_metadata(self, temp_output_file):
        """Test adding FORMAT metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_format(
            id="GT", 
            num="1", 
            type="String", 
            desc="Genotype"
        )
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">'
        assert expected in content
        
    def test_add_filter_metadata(self, temp_output_file):
        """Test adding FILTER metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_filter(id="PASS", desc="All filters passed")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##FILTER=<ID=PASS,Description="All filters passed">'
        assert expected in content
        
    def test_add_filter_with_defaults(self, temp_output_file):
        """Test adding FILTER metadata with default description."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_filter(id="LowQual")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##FILTER=<ID=LowQual,Description="">'
        assert expected in content
        
    def test_add_filter_long(self, temp_output_file):
        """Test adding extended FILTER metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_filter_long(
            id="ComplexFilter", 
            num="1", 
            type="Float", 
            desc="Complex filter description"
        )
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = '##FILTER=<ID=ComplexFilter,Number=1,Type=Float,Description="Complex filter description">'
        assert expected in content
        
    def test_add_contig_metadata(self, temp_output_file):
        """Test adding contig metadata."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_contig(id="chr1", length="248956422")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        expected = "##contig=<ID=chr1,length=248956422>"
        assert expected in content


class TestVCFWriterRecordMethods:
    """Test VCFWriter record writing methods."""
    
    def test_add_header_line(self, temp_output_file):
        """Test adding header line."""
        writer = VCFWriter(str(temp_output_file))
        
        header = "#CHROM\\tPOS\\tID\\tREF\\tALT\\tQUAL\\tFILTER\\tINFO\\tFORMAT\\tSample1"
        writer.add_header_line(header)
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        assert header in content
        
    def test_add_record_value(self, temp_output_file):
        """Test adding record values."""
        writer = VCFWriter(str(temp_output_file))
        
        preheader = "chr1\\t1000\\t.\\tA\\tG\\t30\\tPASS"
        info = "AC=1;AF=0.5"
        format_str = "GT:DP"
        sample_str = "0/1:20"
        
        writer.add_record_value(preheader, info, format_str, sample_str)
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        # The method uses tab separation, so check for the components
        assert preheader in content
        assert info in content
        assert format_str in content
        assert sample_str in content


class TestVCFWriterIntegration:
    """Test VCFWriter integration scenarios."""
    
    def test_write_complete_vcf_file(self, temp_output_file):
        """Test writing a complete VCF file."""
        writer = VCFWriter(str(temp_output_file))
        
        # Add metadata
        writer.add_normal_metadata("fileformat", "VCFv4.2")
        writer.add_info("AC", "A", "Integer", "Allele count")
        writer.add_format("GT", "1", "String", "Genotype")
        writer.add_filter("PASS", "All filters passed")
        writer.add_contig("chr1", "248956422")
        
        # Add header
        header = "#CHROM\\tPOS\\tID\\tREF\\tALT\\tQUAL\\tFILTER\\tINFO\\tFORMAT\\tSample1"
        writer.add_header_line(header)
        
        # Add a record
        preheader = "chr1\\t1000\\t.\\tA\\tG\\t30\\tPASS"
        info = "AC=1"
        format_str = "GT"
        sample_str = "0/1"
        writer.add_record_value(preheader, info, format_str, sample_str)
        
        writer.w_file.close()
        
        # Verify the complete file
        content = temp_output_file.read_text()
        
        # Check metadata
        assert "##fileformat=VCFv4.2" in content
        assert '##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count">' in content
        assert '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' in content
        assert '##FILTER=<ID=PASS,Description="All filters passed">' in content
        assert "##contig=<ID=chr1,length=248956422>" in content
        
        # Check header and record
        assert header in content
        assert "chr1\\t1000" in content
        
    def test_multiple_metadata_entries(self, temp_output_file):
        """Test adding multiple metadata entries of same type."""
        writer = VCFWriter(str(temp_output_file))
        
        # Add multiple INFO fields
        writer.add_info("AC", "A", "Integer", "Allele count")
        writer.add_info("AF", "A", "Float", "Allele frequency")
        writer.add_info("DP", "1", "Integer", "Total depth")
        
        # Add multiple FORMAT fields
        writer.add_format("GT", "1", "String", "Genotype")
        writer.add_format("DP", "1", "Integer", "Read depth")
        
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        
        # Check all INFO fields are present
        assert '##INFO=<ID=AC,' in content
        assert '##INFO=<ID=AF,' in content
        assert '##INFO=<ID=DP,' in content
        
        # Check all FORMAT fields are present
        assert '##FORMAT=<ID=GT,' in content
        assert '##FORMAT=<ID=DP,' in content


class TestVCFWriterEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_descriptions(self, temp_output_file):
        """Test handling of empty descriptions."""
        writer = VCFWriter(str(temp_output_file))
        
        writer.add_info("TEST", desc="")
        writer.add_filter("TESTFILTER", desc="")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        
        assert 'Description=""' in content
        
    def test_special_characters_in_descriptions(self, temp_output_file):
        """Test handling of special characters in descriptions."""
        writer = VCFWriter(str(temp_output_file))
        
        # Test with quotes and commas in description
        desc_with_quotes = 'Description with "quotes" and commas, here'
        writer.add_info("SPECIAL", desc=desc_with_quotes)
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        
        # The description should be properly quoted
        assert f'Description="{desc_with_quotes}"' in content
        
    def test_custom_key_types(self, temp_output_file):
        """Test using custom key types instead of defaults."""
        writer = VCFWriter(str(temp_output_file))
        
        # Use custom key instead of default "INFO"
        writer.add_info("TEST", key="CUSTOM_INFO")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        
        assert "##CUSTOM_INFO=" in content
        assert "##INFO=" not in content
        
    def test_file_operations_after_close(self, temp_output_file):
        """Test behavior after file is closed."""
        writer = VCFWriter(str(temp_output_file))
        writer.w_file.close()
        
        # Operations after close should not crash but may not work
        # This tests the robustness of the implementation
        try:
            writer.add_normal_metadata("test", "value")
        except ValueError:
            # Expected behavior - writing to closed file
            pass
        
    def test_file_permissions(self, tmp_path):
        """Test handling of file permission issues."""
        # Create a directory where we can't write
        restricted_path = tmp_path / "nonexistent_dir" / "test.vcf"
        
        # This should raise an exception
        with pytest.raises((FileNotFoundError, PermissionError)):
            writer = VCFWriter(str(restricted_path))


class TestVCFWriterFileHandling:
    """Test file handling aspects of VCFWriter."""
    
    def test_append_mode(self, temp_output_file):
        """Test that VCFWriter opens files in append mode."""
        # Write something first
        temp_output_file.write_text("Initial content\\n")
        
        # Use VCFWriter
        writer = VCFWriter(str(temp_output_file))
        writer.add_normal_metadata("test", "value")
        writer.w_file.close()
        
        content = temp_output_file.read_text()
        
        # Both initial content and new content should be present
        assert "Initial content" in content
        assert "##test=value" in content
        
    def test_file_exists_before_writing(self, temp_output_file):
        """Test that file handle is properly created."""
        writer = VCFWriter(str(temp_output_file))
        
        # File handle should be created and writable
        assert writer.w_file is not None
        assert not writer.w_file.closed
        
        writer.w_file.close()
