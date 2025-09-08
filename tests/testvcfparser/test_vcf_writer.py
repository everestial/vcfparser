import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open

from vcfparser.vcf_writer import VCFWriter


class TestVCFWriter:
    """Test cases for VCFWriter class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def temp_vcf_file(self, temp_dir):
        """Create a temporary VCF file path."""
        return os.path.join(temp_dir, "test_output.vcf")
    
    def test_init_default_mode(self, temp_vcf_file):
        """Test VCFWriter initialization with default mode."""
        with VCFWriter(temp_vcf_file) as writer:
            assert writer.filename == temp_vcf_file
            assert writer.w_file is not None
            assert not writer._is_closed
    
    def test_init_append_mode(self, temp_vcf_file):
        """Test VCFWriter initialization with append mode."""
        with VCFWriter(temp_vcf_file, mode="a") as writer:
            assert writer.filename == temp_vcf_file
            assert writer.w_file is not None
            assert not writer._is_closed
    
    def test_init_file_error(self):
        """Test VCFWriter initialization with invalid file path."""
        with pytest.raises(IOError):
            VCFWriter("/invalid/path/file.vcf")
    
    def test_context_manager(self, temp_vcf_file):
        """Test VCFWriter as context manager."""
        with VCFWriter(temp_vcf_file) as writer:
            assert writer.w_file is not None
            assert not writer._is_closed
        
        # After exiting context, file should be closed
        assert writer._is_closed
    
    def test_close(self, temp_vcf_file):
        """Test manual close method."""
        writer = VCFWriter(temp_vcf_file)
        assert not writer._is_closed
        
        writer.close()
        assert writer._is_closed
        
        # Multiple closes should not cause error
        writer.close()
        assert writer._is_closed
    
    def test_ensure_open_error(self, temp_vcf_file):
        """Test _ensure_open raises error when file is closed."""
        writer = VCFWriter(temp_vcf_file)
        writer.close()
        
        with pytest.raises(ValueError, match="File is not open for writing"):
            writer.add_normal_metadata("test", "value")

    def test_add_normal_metadata(self, temp_vcf_file):
        """Test add_normal_metadata method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_normal_metadata("fileformat", "VCFv4.3")
            writer.add_normal_metadata("fileDate", "20231201")
            writer.add_normal_metadata("reference", "test.fasta")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert "##fileformat=VCFv4.3" in content
        assert "##fileDate=20231201" in content
        assert "##reference=test.fasta" in content
    
    def test_add_info(self, temp_vcf_file):
        """Test add_info method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_info("DP", "1", "Integer", "Total read depth")
            writer.add_info("AF", "A", "Float", "Allele frequency")
            writer.add_info("AC", "A", "Integer", "Allele count", "INFO")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">' in content
        assert '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">' in content
        assert '##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count">' in content
    
    def test_add_info_defaults(self, temp_vcf_file):
        """Test add_info method with default values."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_info("TEST")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##INFO=<ID=TEST,Number=.,Type=.,Description="">' in content
    
    def test_add_format(self, temp_vcf_file):
        """Test add_format method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_format("GT", "1", "String", "Genotype")
            writer.add_format("DP", "1", "Integer", "Read depth")
            writer.add_format("GQ", "1", "Integer", "Genotype quality", "FORMAT")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' in content
        assert '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">' in content
        assert '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">' in content
    
    def test_add_format_defaults(self, temp_vcf_file):
        """Test add_format method with default values."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_format("TEST")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FORMAT=<ID=TEST,Number=.,Type=.,Description="">' in content
    
    def test_add_filter(self, temp_vcf_file):
        """Test add_filter method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_filter("PASS", "All filters passed")
            writer.add_filter("LowQual", "Low quality variants")
            writer.add_filter("Custom", "Custom filter", "FILTER")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FILTER=<ID=PASS,Description="All filters passed">' in content
        assert '##FILTER=<ID=LowQual,Description="Low quality variants">' in content
        assert '##FILTER=<ID=Custom,Description="Custom filter">' in content
    
    def test_add_filter_defaults(self, temp_vcf_file):
        """Test add_filter method with default values."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_filter("TEST")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FILTER=<ID=TEST,Description="">' in content
    
    def test_add_filter_long(self, temp_vcf_file):
        """Test add_filter_long method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_filter_long("CustomFilter", "1", "String", "Custom filtering")
            writer.add_filter_long("Test", ".", ".", "Test filter", "FILTER")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FILTER=<ID=CustomFilter,Number=1,Type=String,Description="Custom filtering">' in content
        assert '##FILTER=<ID=Test,Number=.,Type=.,Description="Test filter">' in content
    
    def test_add_filter_long_defaults(self, temp_vcf_file):
        """Test add_filter_long method with default values."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_filter_long("TEST")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert '##FILTER=<ID=TEST,Number=.,Type=.,Description="">' in content
    
    def test_add_contig(self, temp_vcf_file):
        """Test add_contig method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_contig("chr1", 248956422)
            writer.add_contig("chr2", "242193529")
            writer.add_contig("scaffold_591", 5806, "contig")
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert "##contig=<ID=chr1,length=248956422>" in content
        assert "##contig=<ID=chr2,length=242193529>" in content
        assert "##contig=<ID=scaffold_591,length=5806>" in content
    
    def test_add_header_line_string(self, temp_vcf_file):
        """Test add_header_line method with string input."""
        header = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1"
        
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_header_line(header)
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert header in content
    
    def test_add_header_line_list(self, temp_vcf_file):
        """Test add_header_line method with list input."""
        header_list = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "Sample1"]
        expected = "\t".join(header_list)
        
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_header_line(header_list)
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        assert expected in content
    
    def test_add_record_value(self, temp_vcf_file):
        """Test add_record_value method."""
        preheader = "chr1\t123\t.\tA\tT\t60\tPASS"
        info = "DP=20;AF=0.5"
        format_val = "GT:DP"
        sample_str = "1/1:20"
        
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_record_value(preheader, info, format_val, sample_str)
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        expected = f"{preheader}\t{info}\t{format_val}\t{sample_str}"
        assert expected in content
    
    def test_add_record_from_parts(self, temp_vcf_file):
        """Test add_record_from_parts method."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_record_from_parts(
                "chr1", 123, "rs123", "A", "T", "60", "PASS",
                "DP=20;AF=0.5", "GT:DP", "1/1:20", "0/1:15"
            )
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        expected = "chr1\t123\trs123\tA\tT\t60\tPASS\tDP=20;AF=0.5\tGT:DP\t1/1:20\t0/1:15"
        assert expected in content
    
    def test_add_record_from_parts_defaults(self, temp_vcf_file):
        """Test add_record_from_parts method with default values."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_record_from_parts("chr1", 123)
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        expected = "chr1\t123\t.\t.\t.\t.\t.\t."
        assert expected in content
    
    def test_add_record_from_parts_no_format_with_samples(self, temp_vcf_file):
        """Test add_record_from_parts with samples but no format."""
        with VCFWriter(temp_vcf_file) as writer:
            writer.add_record_from_parts(
                "chr1", 123, ".", "A", "T", "60", "PASS", "DP=20",
                "", "sample1_data", "sample2_data"
            )
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        expected = "chr1\t123\t.\tA\tT\t60\tPASS\tDP=20\t\tsample1_data\tsample2_data"
        assert expected in content
    
    def test_complete_vcf_creation(self, temp_vcf_file):
        """Test creating a complete VCF file with all components."""
        with VCFWriter(temp_vcf_file) as writer:
            # Add metadata
            writer.add_normal_metadata("fileformat", "VCFv4.3")
            writer.add_normal_metadata("fileDate", "20231201")
            writer.add_normal_metadata("reference", "test.fasta")
            
            # Add INFO fields
            writer.add_info("DP", "1", "Integer", "Total read depth")
            writer.add_info("AF", "A", "Float", "Allele frequency")
            
            # Add FORMAT fields
            writer.add_format("GT", "1", "String", "Genotype")
            writer.add_format("DP", "1", "Integer", "Read depth")
            
            # Add FILTER fields
            writer.add_filter("PASS", "All filters passed")
            writer.add_filter("LowQual", "Low quality variants")
            
            # Add contigs
            writer.add_contig("chr1", 248956422)
            writer.add_contig("chr2", 242193529)
            
            # Add header line
            writer.add_header_line(["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "Sample1", "Sample2"])
            
            # Add records
            writer.add_record_from_parts(
                "chr1", 123, "rs123", "A", "T", "60", "PASS",
                "DP=20;AF=0.5", "GT:DP", "1/1:20", "0/1:15"
            )
            writer.add_record_from_parts(
                "chr2", 456, ".", "G", "C", "80", "PASS",
                "DP=30;AF=0.3", "GT:DP", "0/0:25", "1/1:30"
            )
        
        with open(temp_vcf_file, 'r') as f:
            content = f.read()
        
        # Check metadata
        assert "##fileformat=VCFv4.3" in content
        assert "##fileDate=20231201" in content
        assert "##reference=test.fasta" in content
        
        # Check INFO
        assert '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">' in content
        assert '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">' in content
        
        # Check FORMAT
        assert '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' in content
        assert '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">' in content
        
        # Check FILTER
        assert '##FILTER=<ID=PASS,Description="All filters passed">' in content
        assert '##FILTER=<ID=LowQual,Description="Low quality variants">' in content
        
        # Check contigs
        assert "##contig=<ID=chr1,length=248956422>" in content
        assert "##contig=<ID=chr2,length=242193529>" in content
        
        # Check header
        assert "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\tSample2" in content
        
        # Check records
        assert "chr1\t123\trs123\tA\tT\t60\tPASS\tDP=20;AF=0.5\tGT:DP\t1/1:20\t0/1:15" in content
        assert "chr2\t456\t.\tG\tC\t80\tPASS\tDP=30;AF=0.3\tGT:DP\t0/0:25\t1/1:30" in content
    
    def test_destructor(self, temp_vcf_file):
        """Test that destructor closes file properly."""
        writer = VCFWriter(temp_vcf_file)
        assert not writer._is_closed
        
        # Manually call destructor
        writer.__del__()
        assert writer._is_closed


class TestVCFWriterErrors:
    """Test error conditions and edge cases for VCFWriter."""
    
    def test_write_after_close_error(self, temp_dir):
        """Test that writing after close raises appropriate errors."""
        temp_file = os.path.join(temp_dir, "test.vcf")
        writer = VCFWriter(temp_file)
        writer.close()
        
        # All write methods should raise ValueError
        with pytest.raises(ValueError):
            writer.add_normal_metadata("key", "value")
        
        with pytest.raises(ValueError):
            writer.add_info("test")
        
        with pytest.raises(ValueError):
            writer.add_format("test")
        
        with pytest.raises(ValueError):
            writer.add_filter("test")
        
        with pytest.raises(ValueError):
            writer.add_filter_long("test")
        
        with pytest.raises(ValueError):
            writer.add_contig("test", 1000)
        
        with pytest.raises(ValueError):
            writer.add_header_line("test")
        
        with pytest.raises(ValueError):
            writer.add_record_value("test", "test", "test", "test")
        
        with pytest.raises(ValueError):
            writer.add_record_from_parts("chr1", 123)
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__])
