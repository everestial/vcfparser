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


def test_record():
    records = vcf_object.parse_records()
    first_record = next(records)

    assert first_record.CHROM == '2'
    assert first_record.POS == '15881018'
    assert str(first_record.INFO) == expected.first_rec_info

    assert first_record.ms01e == expected.first_sample_val