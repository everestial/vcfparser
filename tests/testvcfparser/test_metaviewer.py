import pytest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from io import StringIO

from vcfparser.metaviewer import MetaDataViewer, obj_to_dict, unpack_str
from vcfparser.meta_header_parser import MetaDataParser


class TestMetaDataViewer:
    """Test cases for MetaDataViewer class."""
    
    @pytest.fixture
    def sample_vcf_file(self):
        """Create a temporary VCF file for testing."""
        vcf_content = """##fileformat=VCFv4.3
##fileDate=20231201
##source=test
##reference=test.fasta
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
##FILTER=<ID=PASS,Description="All filters passed">
##FILTER=<ID=LowQual,Description="Low quality">
##contig=<ID=chr1,length=248956422>
##contig=<ID=chr2,length=242193529>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1	Sample2
chr1	123	.	A	T	60	PASS	DP=20;AF=0.5	GT:DP	1/1:20	0/1:15
chr2	456	rs456	G	C	80	PASS	DP=30;AF=0.3	GT:DP	0/0:25	1/1:30
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(vcf_content)
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for output files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def metaviewer(self, sample_vcf_file, temp_dir):
        """Create MetaDataViewer instance for testing."""
        output_file = os.path.join(temp_dir, "test_output")
        return MetaDataViewer(sample_vcf_file, filename=output_file)
    
    def test_init(self, sample_vcf_file, temp_dir):
        """Test MetaDataViewer initialization."""
        output_file = os.path.join(temp_dir, "test_init")
        viewer = MetaDataViewer(sample_vcf_file, filename=output_file)
        
        assert viewer.output_file == output_file
        assert viewer.metainfo is not None
        assert viewer.metadict is not None
        assert isinstance(viewer.metadict, dict)
    
    def test_init_default_filename(self, sample_vcf_file):
        """Test MetaDataViewer initialization with default filename."""
        viewer = MetaDataViewer(sample_vcf_file)
        assert viewer.output_file == "vcfmetafile"
    
    def test_save_as_table(self, metaviewer):
        """Test save_as_table method."""
        metaviewer.save_as_table()
        
        table_file = metaviewer.output_file + ".table"
        assert os.path.exists(table_file)
        
        with open(table_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that metadata sections are present
        assert "##VCFspec" in content or "##INFO" in content
        assert len(content.strip()) > 0
        
        # Clean up
        os.unlink(table_file)
    
    def test_save_as_table_with_empty_metadata(self, temp_dir):
        """Test save_as_table with minimal metadata."""
        # Create a minimal VCF with less metadata
        minimal_vcf = """##fileformat=VCFv4.3
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	123	.	A	T	60	PASS	DP=20
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(minimal_vcf)
            temp_vcf = f.name
        
        try:
            output_file = os.path.join(temp_dir, "minimal_test")
            viewer = MetaDataViewer(temp_vcf, filename=output_file)
            viewer.save_as_table()
            
            table_file = output_file + ".table"
            assert os.path.exists(table_file)
            
            # Clean up
            os.unlink(table_file)
        finally:
            os.unlink(temp_vcf)
    
    def test_save_as_json(self, metaviewer):
        """Test save_as_json method."""
        metaviewer.save_as_json()
        
        json_file = metaviewer.output_file + ".json"
        assert os.path.exists(json_file)
        
        # Verify JSON is valid
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Clean up
        os.unlink(json_file)
    
    def test_save_as_json_error_handling(self, metaviewer):
        """Test save_as_json error handling."""
        # Mock json.dump to raise an error
        with patch('vcfparser.metaviewer.json.dump', side_effect=TypeError("Test error")):
            with pytest.raises(TypeError):
                metaviewer.save_as_json()
    
    def test_save_as_orderdict(self, metaviewer):
        """Test save_as_orderdict method."""
        metaviewer.save_as_orderdict()
        
        dict_file = metaviewer.output_file + ".dict"
        assert os.path.exists(dict_file)
        
        with open(dict_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should contain OrderedDict structure
        assert "OrderedDict" in content
        assert len(content.strip()) > 0
        
        # Clean up
        os.unlink(dict_file)
    
    def test_save_as_orderdict_with_complex_data(self, metaviewer):
        """Test save_as_orderdict with complex nested data."""
        # Ensure there's complex data in metadict
        assert metaviewer.metadict is not None
        
        metaviewer.save_as_orderdict()
        
        dict_file = metaviewer.output_file + ".dict"
        assert os.path.exists(dict_file)
        
        # Clean up
        os.unlink(dict_file)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_requested_metadata(self, mock_stdout, metaviewer):
        """Test print_requested_metadata method."""
        # Test with existing metadata
        metaviewer.print_requested_metadata(["INFO", "FORMAT"])
        
        output = mock_stdout.getvalue()
        assert "##INFO" in output or "##FORMAT" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_requested_metadata_not_found(self, mock_stdout, metaviewer):
        """Test print_requested_metadata with non-existent metadata."""
        metaviewer.print_requested_metadata(["NonExistent"])
        
        output = mock_stdout.getvalue()
        assert "not found" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_requested_metadata_empty_list(self, mock_stdout, metaviewer):
        """Test print_requested_metadata with empty list."""
        metaviewer.print_requested_metadata([])
        
        output = mock_stdout.getvalue()
        assert output == ""
    
    def test_file_creation_permissions(self, sample_vcf_file):
        """Test file creation with permission issues."""
        # Try to create files in a non-existent directory
        bad_path = "/non/existent/path/output"
        viewer = MetaDataViewer(sample_vcf_file, filename=bad_path)
        
        # These should handle the error gracefully
        with pytest.raises(IOError):
            viewer.save_as_table()
        
        with pytest.raises(IOError):
            viewer.save_as_json()
        
        with pytest.raises(IOError):
            viewer.save_as_orderdict()


class TestUtilityFunctions:
    """Test cases for utility functions."""
    
    def test_unpack_str_with_list(self):
        """Test unpack_str with list input."""
        test_list = ["a", "b", "c", 1, 2.5]
        result = unpack_str(test_list)
        assert result == "a\tb\tc\t1\t2.5"
    
    def test_unpack_str_with_dict_keys(self):
        """Test unpack_str with dictionary keys."""
        test_dict = {"key1": "value1", "key2": "value2"}
        result = unpack_str(test_dict.keys())
        assert "key1" in result and "key2" in result
        assert "\t" in result
    
    def test_unpack_str_with_dict_values(self):
        """Test unpack_str with dictionary values."""
        test_dict = {"key1": "value1", "key2": "value2"}
        result = unpack_str(test_dict.values())
        assert "value1" in result and "value2" in result
        assert "\t" in result
    
    def test_unpack_str_empty_list(self):
        """Test unpack_str with empty list."""
        result = unpack_str([])
        assert result == ""
    
    def test_obj_to_dict(self):
        """Test obj_to_dict function."""
        # Create a mock metadata object
        mock_metainfo = MagicMock()
        mock_metainfo.VCFspec = "test_spec"
        mock_metainfo.format_ = ["format1", "format2"]
        mock_metainfo.infos_ = ["info1", "info2"]
        mock_metainfo.filters_ = ["filter1"]
        mock_metainfo.contig = ["contig1"]
        mock_metainfo.reference = "test.fasta"
        mock_metainfo.gatk_commands = []
        mock_metainfo.gvcf_blocks = []
        mock_metainfo.sample_with_pos = ["sample1", "sample2"]
        
        result = obj_to_dict(mock_metainfo)
        
        assert "VCFspec" in result
        assert "FORMAT" in result
        assert "INFO" in result
        assert "FILTER" in result
        assert "contig" in result
        assert "reference" in result
        assert "GATKCommandLine" in result
        assert "GVCFBlock" in result
        assert "samples" in result
        
        assert result["VCFspec"] == "test_spec"
        assert result["FORMAT"] == ["format1", "format2"]
        assert result["INFO"] == ["info1", "info2"]


class TestIntegration:
    """Integration tests for MetaDataViewer with real VCF parsing."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for output files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_complete_workflow(self, temp_dir):
        """Test complete workflow from VCF parsing to file export."""
        # Create a comprehensive VCF file
        vcf_content = """##fileformat=VCFv4.3
##fileDate=20231201
##source=test_suite
##reference=test.fasta
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">
##FILTER=<ID=PASS,Description="All filters passed">
##FILTER=<ID=LowQual,Description="Low quality">
##FILTER=<ID=HighMissing,Description="High missing rate">
##contig=<ID=chr1,length=248956422>
##contig=<ID=chr2,length=242193529>
##contig=<ID=chrX,length=156040895>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1	Sample2	Sample3
chr1	123	rs123	A	T	60	PASS	DP=20;AF=0.5;AC=3	GT:DP:GQ	1/1:20:60	0/1:15:45	1/1:18:55
chr2	456	.	G	C	80	PASS	DP=30;AF=0.3;AC=2	GT:DP:GQ	0/0:25:70	1/1:30:80	0/1:22:65
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(vcf_content)
            vcf_file = f.name
        
        try:
            output_base = os.path.join(temp_dir, "integration_test")
            viewer = MetaDataViewer(vcf_file, filename=output_base)
            
            # Test all export methods
            viewer.save_as_table()
            viewer.save_as_json()
            viewer.save_as_orderdict()
            
            # Verify all files were created
            assert os.path.exists(output_base + ".table")
            assert os.path.exists(output_base + ".json")
            assert os.path.exists(output_base + ".dict")
            
            # Verify JSON content is parseable
            with open(output_base + ".json", 'r') as f:
                json_data = json.load(f)
                assert isinstance(json_data, dict)
                assert "INFO" in json_data or "FORMAT" in json_data
            
            # Test print functionality
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                viewer.print_requested_metadata(["INFO", "FORMAT", "FILTER"])
                output = mock_stdout.getvalue()
                assert len(output) > 0
            
        finally:
            os.unlink(vcf_file)
    
    def test_error_resilience(self, temp_dir):
        """Test that MetaDataViewer handles various error conditions gracefully."""
        # Test with malformed VCF
        malformed_vcf = """##fileformat=VCFv4.3
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth"
##FILTER=<ID=PASS,Description="All filters passed">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	123	.	A	T	60	PASS
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(malformed_vcf)
            vcf_file = f.name
        
        try:
            output_base = os.path.join(temp_dir, "error_test")
            viewer = MetaDataViewer(vcf_file, filename=output_base)
            
            # These should not crash even with malformed input
            viewer.save_as_table()
            viewer.save_as_json()
            viewer.save_as_orderdict()
            
            # Files should still be created (though possibly with limited content)
            assert os.path.exists(output_base + ".table")
            assert os.path.exists(output_base + ".json")
            assert os.path.exists(output_base + ".dict")
            
        finally:
            os.unlink(vcf_file)


if __name__ == "__main__":
    pytest.main([__file__])
