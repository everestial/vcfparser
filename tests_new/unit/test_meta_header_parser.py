"""
Unit tests for MetaDataParser class.
"""
import pytest
from vcfparser.meta_header_parser import MetaDataParser, split_to_dict


class TestMetaDataParserInit:
    """Test MetaDataParser initialization."""
    
    def test_init_with_header_lines(self):
        """Test initialization with header lines."""
        header_lines = [
            "##fileformat=VCFv4.2\n",
            "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Depth\">\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        parser = MetaDataParser(header_lines)
        
        assert parser.infos_ == []
        assert parser.filters_ == []
        assert parser.fileformat is None
        assert parser.sample_names == []


class TestMetaDataParserParsing:
    """Test MetaDataParser parsing methods."""
    
    def setup_method(self):
        """Set up test data for parsing tests."""
        self.header_lines = [
            "##fileformat=VCFv4.2\n",
            "##reference=hg38\n",
            "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count\">\n",
            "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele frequency\">\n",
            "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Depth\">\n",
            "##FILTER=<ID=PASS,Description=\"All filters passed\">\n",
            "##FILTER=<ID=LowQual,Description=\"Low quality\">\n",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
            "##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Read depth\">\n",
            "##ALT=<ID=NON_REF,Description=\"Non-reference allele\">\n",
            "##contig=<ID=chr1,length=248956422>\n",
            "##contig=<ID=chr2,length=242193529>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\tSample2\n"
        ]
        
    def test_parse_fileformat(self):
        """Test fileformat parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert metadata.fileformat == "VCFv4.2"
        
    def test_parse_reference(self):
        """Test reference parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert "hg38" in metadata.reference
        
    def test_parse_info_fields(self):
        """Test INFO field parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.infos_) == 3
        
        info_ids = [info['ID'] for info in metadata.infos_]
        assert 'AC' in info_ids
        assert 'AF' in info_ids
        assert 'DP' in info_ids
        
        # Check specific INFO field details
        ac_info = next(info for info in metadata.infos_ if info['ID'] == 'AC')
        assert ac_info['Number'] == 'A'
        assert ac_info['Type'] == 'Integer'
        assert ac_info['Description'] == 'Allele count'
        
    def test_parse_filter_fields(self):
        """Test FILTER field parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.filters_) == 2
        
        filter_ids = [flt['ID'] for flt in metadata.filters_]
        assert 'PASS' in filter_ids
        assert 'LowQual' in filter_ids
        
    def test_parse_format_fields(self):
        """Test FORMAT field parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.format_) == 2
        
        format_ids = [fmt['ID'] for fmt in metadata.format_]
        assert 'GT' in format_ids
        assert 'DP' in format_ids
        
    def test_parse_alt_fields(self):
        """Test ALT field parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.alt_) == 1
        assert metadata.alt_[0]['ID'] == 'NON_REF'
        
    def test_parse_contig_fields(self):
        """Test contig parsing."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.contig) == 2
        
        contig_ids = [ctg['ID'] for ctg in metadata.contig]
        assert 'chr1' in contig_ids
        assert 'chr2' in contig_ids
        
    def test_parse_sample_names(self):
        """Test sample name extraction."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        expected_samples = ['Sample1', 'Sample2']
        assert metadata.sample_names == expected_samples
        
    def test_parse_record_keys(self):
        """Test record keys extraction."""
        parser = MetaDataParser(self.header_lines)
        metadata = parser.parse_lines()
        
        expected_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'Sample1', 'Sample2']
        assert metadata.record_keys == expected_keys


class TestMetaDataParserGVCF:
    """Test GVCF-specific parsing."""
    
    def test_parse_gvcf_blocks(self):
        """Test GVCF block parsing."""
        gvcf_lines = [
            "##fileformat=VCFv4.2\n",
            "##GVCFBlock0-1=minGQ=0(inclusive),maxGQ=1(exclusive)\n",
            "##GVCFBlock1-2=minGQ=1(inclusive),maxGQ=2(exclusive)\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(gvcf_lines)
        metadata = parser.parse_lines()
        
        assert metadata.is_gvcf is True
        assert len(metadata.gvcf_blocks) == 2
        
        # Check first GVCF block
        block1 = metadata.gvcf_blocks[0]
        assert block1['Block'] == '0-1'
        assert 'minGQ' in block1
        assert 'maxGQ' in block1
        
    def test_parse_gatk_commands(self):
        """Test GATK command line parsing."""
        gatk_lines = [
            "##fileformat=VCFv4.2\n",
            "##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller,Version=4.0,Date=\"2020-01-01\",Epoch=1577836800,CommandLineOptions=\"--output test.vcf\">\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(gatk_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.gatk_commands) == 1
        
        gatk_cmd = metadata.gatk_commands[0]
        assert gatk_cmd['ID'] == 'HaplotypeCaller'
        assert gatk_cmd['Version'] == '4.0'


class TestMetaDataParserErrors:
    """Test error handling in MetaDataParser."""
    
    def test_missing_fileformat_value(self):
        """Test handling of missing fileformat value."""
        bad_lines = [
            "##fileformat=\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(bad_lines)
        with pytest.raises(SyntaxError, match="fileformat must have a value"):
            parser.parse_lines()
            
    def test_missing_reference_value(self):
        """Test handling of missing reference value."""
        bad_lines = [
            "##fileformat=VCFv4.2\n",
            "##reference=\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(bad_lines)
        with pytest.raises(SyntaxError, match="Reference value is not provided"):
            parser.parse_lines()
            
    def test_malformed_format_line(self):
        """Test handling of malformed FORMAT lines."""
        bad_lines = [
            "##fileformat=VCFv4.2\n",
            "##FORMAT=<ID=GT,Type=String,Description=\"Genotype\">\n",  # Missing Number
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(bad_lines)
        with pytest.raises(SyntaxError, match="One of the FORMAT lines is malformed"):
            parser.parse_lines()
            
    def test_malformed_metadata_line(self):
        """Test handling of malformed metadata lines."""
        bad_lines = [
            "##fileformat=VCFv4.2\n",
            "##INVALID_LINE_WITHOUT_EQUALS\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(bad_lines)
        with pytest.raises(SyntaxError, match="One of the meta data lines is malformed"):
            parser.parse_lines()


class TestSplitToDict:
    """Test split_to_dict utility function."""
    
    def test_basic_split(self):
        """Test basic string splitting to dictionary."""
        test_string = "<ID=DP,Number=1,Type=Integer,Description=\"Depth\">"
        result = split_to_dict(test_string)
        
        expected = {
            'ID': 'DP',
            'Number': '1',
            'Type': 'Integer',
            'Description': 'Depth'
        }
        
        assert result == expected
        
    def test_split_with_quotes(self):
        """Test string splitting with quoted values."""
        test_string = '<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes, for each ALT allele">'
        result = split_to_dict(test_string)
        
        assert result['Description'] == 'Allele count in genotypes, for each ALT allele'
        
    def test_split_with_commas_in_description(self):
        """Test handling of commas within quoted descriptions."""
        test_string = '<ID=TEST,Number=1,Type=String,Description="Test field, with commas">'
        result = split_to_dict(test_string)
        
        assert result['Description'] == 'Test field, with commas'
        
    def test_split_without_brackets(self):
        """Test splitting string without angle brackets."""
        test_string = 'ID=DP,Number=1,Type=Integer,Description="Depth"'
        result = split_to_dict(test_string)
        
        expected = {
            'ID': 'DP',
            'Number': '1',
            'Type': 'Integer',
            'Description': 'Depth'
        }
        
        assert result == expected


class TestMetaDataParserStaticMethods:
    """Test static methods of MetaDataParser."""
    
    def test_parse_gvcf_block_static(self):
        """Test _parse_gvcf_block static method."""
        line = "##GVCFBlock10-20=minGQ=10(inclusive),maxGQ=20(exclusive)"
        result = MetaDataParser._parse_gvcf_block(line)
        
        expected = {
            'Block': '10-20',
            'minGQ': '10(inclusive)',
            'maxGQ': '20(exclusive)'
        }
        
        assert result == expected
        
    def test_parse_gatk_commands_static(self):
        """Test _parse_gatk_commands static method."""
        line = '##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller,Version=4.0,Date="2020-01-01">'
        result = MetaDataParser._parse_gatk_commands(line)
        
        expected = {
            'ID': 'HaplotypeCaller',
            'Version': '4.0',
            'Date': '2020-01-01'
        }
        
        assert result == expected


class TestMetaDataParserEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_empty_header_lines(self):
        """Test parsing with minimal header."""
        minimal_lines = [
            "##fileformat=VCFv4.2\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(minimal_lines)
        metadata = parser.parse_lines()
        
        assert metadata.fileformat == "VCFv4.2"
        assert len(metadata.infos_) == 0
        assert len(metadata.format_) == 0
        assert metadata.sample_names == ['Sample1']
        
    def test_other_metadata_lines(self):
        """Test parsing of other metadata lines not specifically handled."""
        other_lines = [
            "##fileformat=VCFv4.2\n",
            "##source=myProgram\n",
            "##phasing=partial\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
        ]
        
        parser = MetaDataParser(other_lines)
        metadata = parser.parse_lines()
        
        assert len(metadata.other_lines) == 2
        
        # Check that other lines are captured
        other_keys = [list(line.keys())[0] for line in metadata.other_lines]
        assert 'source' in other_keys
        assert 'phasing' in other_keys
        
    def test_sample_with_pos_mapping(self):
        """Test sample position mapping."""
        lines_with_samples = [
            "##fileformat=VCFv4.2\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\tS2\tS3\n"
        ]
        
        parser = MetaDataParser(lines_with_samples)
        metadata = parser.parse_lines()
        
        assert len(metadata.sample_with_pos) == 3
        
        # Check position mapping
        sample_pos_map = {item['name']: item['position'] for item in metadata.sample_with_pos}
        assert sample_pos_map['S1'] == 10
        assert sample_pos_map['S2'] == 11
        assert sample_pos_map['S3'] == 12
