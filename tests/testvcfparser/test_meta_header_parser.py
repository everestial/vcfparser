import pytest
import filecmp
import os
import collections
import sys
import json
import csv

from vcfparser import MetaDataParser
from vcfparser.meta_header_parser import split_to_dict

header_file = "tests/testfiles/vcf_parser_input/reference_input_test.vcf"
meta_header_parser_obj = MetaDataParser(header_file)
# 1 MetaDataParser._parse_gvcf_block
def test_parse_gvcf_block():
    pass
    # line = ""
    # data = meta_header_parser_obj._parse_gvcf_block(line)
    # write_data_and_check(1, data)


# 2 MetaDataParser._parse_gatk_commands
def test_parse_gatk_commands():
    pass
    # line = ""
    # data = meta_header_parser_obj._parse_gatk_commands(line)
    # write_data_and_check(2, data)


# 3 MetaDataParser.parse_lines
def test_parse_lines():
    pass
    # data = meta_header_parser_obj.parse_lines()
    # write_data_and_check(3, data)

##TODO:Bishwa - Problem in creating error file.
# def test_parse_lines_exit1():
#     fileformat_error = "tests/testfiles/vcf_parser_input/reference_input_test_fileformat_check.vcf"
#     meta_header_parser_obj2 = MetaDataParser(fileformat_error)
#     with pytest.raises(IndexError):
#         meta_header_parser_obj1.parse_lines()

##TODO:Bishwa - Problem in creating error file.
# def test_parse_lines_exit2():
#     reference_error = "tests/testfiles/vcf_parser_input/reference_input_test_reference_check.vcf"
#     meta_header_parser_obj2 = MetaDataParser(reference_error)
#     with pytest.raises(IndexError):
#         meta_header_parser_obj2.parse_lines()

##TODO:Bishwa - Problem in creating error file.
# def test_parse_lines_exit3():
#     format_error = "tests/testfiles/vcf_parser_input/reference_input_test_format_check.vcf"
#     meta_header_parser_obj3 = MetaDataParser(format_error)
#     with pytest.raises(IndexError):
#         meta_header_parser_obj3.parse_lines()

##TODO:Bishwa - Problem in creating error file.
# def test_parse_lines_exit4():
#     error = "tests/testfiles/vcf_parser_input/reference_input_test_error.vcf"
#     meta_header_parser_obj4 = MetaDataParser(error)
#     with pytest.raises(SyntaxError):
#         meta_header_parser_obj4.parse_lines()

# 4 split_to_dict
def test_split_to_dict():
    # pass
    string = "<ID=HQ,Number=2,Type=Integer,Description='Haplotype Quality'>"
    data = split_to_dict(string)
    write_data_and_check(4, data)


# Helping functions
def write_data_and_check(i, data):
    output_file = f"tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}"
    with open(output_file + ".txt", "w") as w_file:
        for key, val in data.items():
            w_file.write(f"{key}\n")
            w_file.write(f"{val}\n")
            w_file.write("\n")

    assert (
        is_same_file(
            f"tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}.txt",
            f"tests/testfiles/vcf_parser_reference/meta_header_parser_test_ref{i}.txt",
        )
        is True
    )

    os.remove(
        f"tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}.txt"
    )


# Compare files
def is_same_file(file1, file2):
    return filecmp.cmp(file1, file2)
