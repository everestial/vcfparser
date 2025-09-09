import pytest
from vcfparser import VcfParser
import expected_config as expected
from vcfparser.record_parser import GenotypeProperty

vcf_object = VcfParser("tests/testfiles/vcf_parser_input/reference_input_test.vcf")
metainfo = vcf_object.parse_metadata()


def test_fileformat():
    assert metainfo.fileformat == "VCFv4.2"


def test_filters():
    assert metainfo.filters_ == expected.filters_


def test_formats():
    assert metainfo.format_ == expected.format_


def test_gvcf_blocks():
    assert metainfo.gvcf_blocks == expected.gvcf_block


def test_info():
    assert metainfo.infos_ == expected.info_


def test_sample_names():
    expected_samples = ['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
    assert metainfo.sample_names == expected_samples


records = vcf_object.parse_records()
first_record = next(records)

def get_genotype_property(record):
    return record.genotype_property

genotype_property = get_genotype_property(first_record)

def test_record():
    assert first_record.CHROM == '2'
    # assert first_record.POS == '15881018'
    assert str(first_record.get_info_as_dict()) == expected.first_rec_info

    # assert first_record.ms01e == expected.first_sample_val


def test_vars_for_gt():
    assert genotype_property.isMissing() == {'ms02g': './.', 'ms03g': './.'}  
    assert genotype_property.isHOMVAR() == {'ms04h': '1/1'}
    assert genotype_property.isHOMREF() == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
    assert genotype_property.isHETVAR() == {'ms01e': '0/1'}


def test_is_vars_for_iupac():
    assert genotype_property.isMissing(tag='PG') == {'ms02g': './.', 'ms03g': './.'}  
    assert genotype_property.isHOMVAR(tag='PG', bases='iupac') == {'ms04h': 'A/A'}
    assert genotype_property.isHOMREF(tag='PG', bases='iupac') == {'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}
    assert genotype_property.isHETVAR(tag='PG', bases='iupac') == {'ms01e': 'G|A'}


def test_has_allele():
    assert genotype_property.hasAllele('0') == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0', 'ms01e': '0/1'}  
    assert genotype_property.hasAllele('1') == {'ms04h': '1/1', 'ms01e': '0/1'}
    assert genotype_property.hasAllele('2') == {}


def test_has_variant():
    assert genotype_property.hasVAR('0/0') == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}  
    assert genotype_property.hasVAR('0/1') == {'ms01e': '0/1'}
    assert genotype_property.hasVAR('1/1') == {'ms04h': '1/1'}


def test_missing_var():
    assert genotype_property.hasnoVAR() == {'ms02g': './.', 'ms03g': './.'}
