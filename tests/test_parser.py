import pytest
from vcf_parser import VcfParser
import expected_config as expected

vcf_object = VcfParser("input_test.vcf")
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


def test_record():
    assert first_record.CHROM == '2'
    # assert first_record.POS == '15881018'
    assert str(first_record.get_info_dict()) == expected.first_rec_info

    # assert first_record.ms01e == expected.first_sample_val


def test_vars_for_gt():
    assert first_record.isMissing() == {'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
    assert first_record.isHOMVAR() == {'ms04h': '1/1'}
    assert first_record.isHOMREF() == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
    assert first_record.isHETVAR() == {}


def test_is_vars_for_iupac():
    assert first_record.isMissing(tag='PG') == {'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
    assert first_record.isHOMVAR(tag='PG', bases='iupac') == {'ms04h': 'A/A'}
    assert first_record.isHOMREF(tag='PG', bases='iupac') == {'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}
    assert first_record.isHETVAR(tag='PG', bases='iupac') == {}


def test_has_allele():
    assert first_record.hasAllele('0') == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
    assert first_record.hasAllele('1') == {'ms04h': '1/1'}
    assert first_record.hasAllele('2') == {}


def test_has_variant():
    assert first_record.hasVAR('0/0') == {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
    assert first_record.hasVAR('0/1') == {}
    assert first_record.hasVAR('1/1') == {'ms04h': '1/1'}


def test_missing_var():
    assert first_record.hasnoVAR() == {'ms01e': './.', 'ms02g': './.', 'ms03g': './.'}
