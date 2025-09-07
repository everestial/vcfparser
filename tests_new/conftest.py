"""
Pytest configuration and shared fixtures for vcfparser tests.
"""
import pytest
import tempfile
import os
from pathlib import Path
from vcfparser import VcfParser, VCFWriter


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def sample_vcf_file(test_data_dir):
    """Path to a sample VCF file for testing."""
    return test_data_dir / "sample.vcf"


@pytest.fixture(scope="session")
def small_vcf_content():
    """Content for a small test VCF file."""
    return """##fileformat=VCFv4.2
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1	Sample2	Sample3
chr1	1000	.	A	G	30	PASS	AC=2;AF=0.33;AN=6;DP=100	GT:DP:GQ	0/1:20:30	0/0:25:40	1/1:30:50
chr1	2000	.	T	C	25	PASS	AC=1;AF=0.17;AN=6;DP=80	GT:DP:GQ	0/0:15:25	0/1:18:28	0/0:20:35
chr2	1500	.	G	A,T	40	PASS	AC=1,1;AF=0.17,0.17;AN=6;DP=120	GT:DP:GQ	0/1:22:32	0/2:28:38	0/0:35:45
"""


@pytest.fixture
def small_vcf_file(tmp_path, small_vcf_content):
    """Create a temporary small VCF file for testing."""
    vcf_file = tmp_path / "test_small.vcf"
    vcf_file.write_text(small_vcf_content)
    return vcf_file


@pytest.fixture
def vcf_parser(small_vcf_file):
    """Create a VcfParser instance with a small test file."""
    return VcfParser(str(small_vcf_file))


@pytest.fixture
def malformed_vcf_content():
    """Content for a malformed VCF file for error testing."""
    return """##fileformat=VCFv4.2
##INFO=<ID=DP,Number=1,Type=Integer,Description="Depth">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
chr1	1000	.	A	G	30	PASS	DP=100	GT	0/1
chr1	invalid_pos	.	T	C	25	PASS	DP=80	GT	0/0
"""


@pytest.fixture
def malformed_vcf_file(tmp_path, malformed_vcf_content):
    """Create a temporary malformed VCF file for error testing."""
    vcf_file = tmp_path / "test_malformed.vcf"
    vcf_file.write_text(malformed_vcf_content)
    return vcf_file


@pytest.fixture
def empty_vcf_content():
    """Content for an empty VCF file."""
    return """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
"""


@pytest.fixture
def empty_vcf_file(tmp_path, empty_vcf_content):
    """Create a temporary empty VCF file for testing."""
    vcf_file = tmp_path / "test_empty.vcf"
    vcf_file.write_text(empty_vcf_content)
    return vcf_file


@pytest.fixture
def gzipped_vcf_file(tmp_path, small_vcf_content):
    """Create a gzipped VCF file for testing."""
    import gzip
    vcf_file = tmp_path / "test_small.vcf.gz"
    with gzip.open(vcf_file, 'wt') as f:
        f.write(small_vcf_content)
    return vcf_file


@pytest.fixture
def temp_output_file(tmp_path):
    """Create a temporary output file for testing writers."""
    return tmp_path / "test_output.vcf"


@pytest.fixture
def vcf_writer(temp_output_file):
    """Create a VCFWriter instance with a temporary output file."""
    return VCFWriter(str(temp_output_file))


class TestUtils:
    """Utility functions for tests."""
    
    @staticmethod
    def create_record_data():
        """Create sample record data for testing."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'Sample1', 'Sample2']
        record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1;AF=0.5;DP=20', 'GT:DP', '0/1:10', '0/0:15']
        return record_keys, record_values
    
    @staticmethod
    def create_complex_record_data():
        """Create complex record data with multiple samples and formats."""
        record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'S1', 'S2', 'S3']
        record_values = ['chr2', '2000', 'rs123', 'T', 'C,G', '45', 'PASS', 'AC=2,1;AF=0.33,0.17;DP=60', 'GT:DP:GQ', '0/1:20:30', '1/2:25:35', '0/0:15:25']
        return record_keys, record_values


@pytest.fixture
def test_utils():
    """Provide TestUtils instance."""
    return TestUtils()
