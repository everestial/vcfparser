"""
Unit tests for Record and GenotypeProperty classes.
"""
import pytest
from vcfparser.record_parser import Record, GenotypeProperty


class TestRecordInit:
    """Test Record class initialization."""
    
    def test_record_initialization(self, test_utils):
        """Test basic Record initialization."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        assert record.CHROM == 'chr1'
        assert record.POS == '1000'
        assert record.REF == 'A'
        assert record.ALT == ['G']
        assert record.QUAL == '30'
        assert record.FILTER == ['PASS']
        
    def test_record_with_multiple_alt_alleles(self, test_utils):
        """Test Record with multiple ALT alleles."""
        record_keys, record_values = test_utils.create_complex_record_data()
        record = Record(record_values, record_keys)
        
        assert record.ALT == ['C', 'G']
        assert record.ref_alt == ['T', 'C', 'G']
        
    def test_record_sample_parsing(self, test_utils):
        """Test sample data parsing."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        assert record.sample_names == ['Sample1', 'Sample2']
        assert len(record.sample_vals) == 2
        assert record.sample_vals[0] == '0/1:10'
        assert record.sample_vals[1] == '0/0:15'
        
    def test_record_format_parsing(self, test_utils):
        """Test FORMAT field parsing."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        assert record.format_ == ['GT', 'DP']


class TestRecordInfoMethods:
    """Test Record INFO parsing methods."""
    
    def test_get_info_as_dict_all_keys(self, test_utils):
        """Test getting all INFO keys as dict."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        info_dict = record.get_info_as_dict()
        expected_keys = ['AC', 'AF', 'DP']
        
        assert all(key in info_dict for key in expected_keys)
        assert info_dict['AC'] == '1'
        assert info_dict['AF'] == '0.5'
        assert info_dict['DP'] == '20'
        
    def test_get_info_as_dict_specific_keys(self, test_utils):
        """Test getting specific INFO keys."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        info_dict = record.get_info_as_dict(['AC', 'DP'])
        
        assert len(info_dict) == 2
        assert info_dict['AC'] == '1'
        assert info_dict['DP'] == '20'
        assert 'AF' not in info_dict
        
    def test_get_info_as_dict_flag_values(self):
        """Test INFO fields that are flags (no '=' present)."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'Sample1']
        record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1;DB;DP=20', 'GT', '0/1']
        record = Record(record_values, record_keys)
        
        info_dict = record.get_info_as_dict()
        
        assert info_dict['DB'] == '.'  # Flag fields get '.' as value


class TestRecordFormatMethods:
    """Test Record FORMAT parsing methods."""
    
    def test_format_to_sample_mapping(self, test_utils):
        """Test mapping FORMAT tags to sample values."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        mapped_data = record.mapped_format_to_sample
        
        assert 'Sample1' in mapped_data
        assert 'Sample2' in mapped_data
        assert mapped_data['Sample1']['GT'] == '0/1'
        assert mapped_data['Sample1']['DP'] == '10'
        assert mapped_data['Sample2']['GT'] == '0/0'
        assert mapped_data['Sample2']['DP'] == '15'
        
    def test_get_format_to_sample_map_filtered(self, test_utils):
        """Test filtered FORMAT to sample mapping."""
        record_keys, record_values = test_utils.create_complex_record_data()
        record = Record(record_values, record_keys)
        
        filtered_map = record.get_format_to_sample_map(
            sample_names=['S1', 'S2'], 
            formats=['GT', 'DP']
        )
        
        assert len(filtered_map) == 2
        assert 'S1' in filtered_map
        assert 'S2' in filtered_map
        assert 'GT' in filtered_map['S1']
        assert 'DP' in filtered_map['S1']
        assert 'GQ' not in filtered_map['S1']  # Not requested


class TestRecordConversionMethods:
    """Test Record conversion methods."""
    
    def test_to_iupac_conversion(self):
        """Test numeric to IUPAC base conversion."""
        ref_alt = ['A', 'G', 'T']
        result = Record._to_iupac(ref_alt, '0/1', 'iupac')
        assert result == 'A/G'
        
        result = Record._to_iupac(ref_alt, '1|2', 'iupac')
        assert result == 'G|T'
        
    def test_to_iupac_missing_data(self):
        """Test IUPAC conversion with missing data."""
        ref_alt = ['A', 'G']
        result = Record._to_iupac(ref_alt, './.', 'iupac')
        assert result == './.'
        
    def test_to_iupac_numeric_passthrough(self):
        """Test that numeric format passes through unchanged."""
        ref_alt = ['A', 'G']
        result = Record._to_iupac(ref_alt, '0/1', 'numeric')
        assert result == '0/1'
        
    def test_iupac_to_numeric(self, test_utils):
        """Test IUPAC to numeric conversion."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        ref_alt = ['A', 'G', 'T']
        result = record.iupac_to_numeric(ref_alt, 'A/G')
        assert result == '0/1'
        
        result = record.iupac_to_numeric(ref_alt, 'G|T')
        assert result == '1|2'


class TestRecordStaticMethods:
    """Test Record static methods."""
    
    def test_get_tag_values_from_samples(self):
        """Test extracting tag values from samples."""
        from collections import OrderedDict
        
        sample_data = OrderedDict([
            ('S1', {'GT': '0/1', 'DP': '20'}),
            ('S2', {'GT': '0/0', 'DP': '25'})
        ])
        
        tag_values = Record.get_tag_values_from_samples(sample_data, 'GT', ['S1', 'S2'])
        assert tag_values == ['0/1', '0/0']
        
    def test_get_tag_values_with_splitting(self):
        """Test extracting and splitting tag values."""
        from collections import OrderedDict
        
        sample_data = OrderedDict([
            ('S1', {'GT': '0/1'}),
            ('S2', {'GT': '0|0'})
        ])
        
        tag_values = Record.get_tag_values_from_samples(
            sample_data, 'GT', ['S1', 'S2'], split_at='/|'
        )
        assert tag_values == [['0', '1'], ['0', '0']]


class TestGenotypeProperty:
    """Test GenotypeProperty class methods."""
    
    def setup_method(self):
        """Set up test data for GenotypeProperty tests."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'S1', 'S2', 'S3', 'S4']
        record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=2;DP=20', 'GT:DP', '0/0:10', '0/1:15', '1/1:20', './.:.']
        self.record = Record(record_values, record_keys)
        self.genotype_prop = self.record.genotype_property
        
    def test_is_homref(self):
        """Test homozygous reference identification."""
        homref_samples = self.genotype_prop.isHOMREF()
        assert 'S1' in homref_samples
        assert homref_samples['S1'] == '0/0'
        assert 'S2' not in homref_samples  # Het
        assert 'S3' not in homref_samples  # HomVar
        
    def test_is_homref_iupac(self):
        """Test homozygous reference in IUPAC format."""
        homref_samples = self.genotype_prop.isHOMREF(bases='iupac')
        assert 'S1' in homref_samples
        assert homref_samples['S1'] == 'A/A'
        
    def test_is_homvar(self):
        """Test homozygous variant identification."""
        homvar_samples = self.genotype_prop.isHOMVAR()
        assert 'S3' in homvar_samples
        assert homvar_samples['S3'] == '1/1'
        assert 'S1' not in homvar_samples  # HomRef
        
    def test_is_hetvar(self):
        """Test heterozygous variant identification."""
        hetvar_samples = self.genotype_prop.isHETVAR()
        assert 'S2' in hetvar_samples
        assert hetvar_samples['S2'] == '0/1'
        assert 'S1' not in hetvar_samples  # HomRef
        assert 'S3' not in hetvar_samples  # HomVar
        
    def test_is_missing(self):
        """Test missing genotype identification."""
        missing_samples = self.genotype_prop.isMissing()
        assert 'S4' in missing_samples
        assert missing_samples['S4'] == './.'
        
    def test_has_allele(self):
        """Test allele presence checking."""
        samples_with_0 = self.genotype_prop.hasAllele('0')
        assert 'S1' in samples_with_0  # 0/0
        assert 'S2' in samples_with_0  # 0/1
        assert 'S3' not in samples_with_0  # 1/1
        
        samples_with_1 = self.genotype_prop.hasAllele('1')
        assert 'S2' in samples_with_1  # 0/1
        assert 'S3' in samples_with_1  # 1/1
        assert 'S1' not in samples_with_1  # 0/0
        
    def test_has_var(self):
        """Test specific genotype checking."""
        samples_with_00 = self.genotype_prop.hasVAR('0/0')
        assert 'S1' in samples_with_00
        assert len(samples_with_00) == 1
        
        samples_with_11 = self.genotype_prop.hasVAR('1/1')
        assert 'S3' in samples_with_11
        assert len(samples_with_11) == 1
        
    def test_has_no_var(self):
        """Test missing variant identification."""
        no_var_samples = self.genotype_prop.hasnoVAR()
        assert 'S4' in no_var_samples
        assert no_var_samples['S4'] == './.'


class TestRecordEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_samples(self):
        """Test record with no samples."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
        record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1', 'GT']
        record = Record(record_values, record_keys)
        
        assert record.sample_names is None
        
    def test_malformed_info_field(self):
        """Test handling of malformed INFO fields."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
        record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1;MALFORMED;DP=20']
        record = Record(record_values, record_keys)
        
        info_dict = record.get_info_as_dict()
        assert info_dict['MALFORMED'] == '.'  # INFO Fields without '=' get '.' value
        
    def test_string_representation(self, test_utils):
        """Test string representation of Record."""
        record_keys, record_values = test_utils.create_record_data()
        record = Record(record_values, record_keys)
        
        record_str = str(record)
        assert 'chr1' in record_str
        assert '1000' in record_str
        assert 'A' in record_str
        assert 'G' in record_str
