import pytest
import filecmp
import os
import collections
import sys
import json
import csv

from vcfparser import MetaDataParser
header_file = ""
meta_header_parser_obj = MetaDataParser(header_file)
#1 MetaDataParser._parse_gvcf_block
def test_parse_gvcf_block():
    pass
    # line = ""
    # data = meta_header_parser_obj._parse_gvcf_block(line)
    # write_data_and_check(1, data)
#2 MetaDataParser._parse_gatk_commands
def test_parse_gatk_commands():
    pass
    # line = ""
    # data = meta_header_parser_obj._parse_gatk_commands(line)
    # write_data_and_check(2, data)
#3 MetaDataParser.parse_lines
def test_parse_lines():
    pass
    # data = meta_header_parser_obj.parse_lines()
    # write_data_and_check(3, data)
#4 split_to_dict
def test_split_to_dict():
    # pass
    string = "<ID=HQ,Number=2,Type=Integer,Description='Haplotype Quality'>"
    data = meta_header_parser_obj.split_to_dict(string)
    write_data_and_check(4, data)

#Helping functions
def write_data_and_check(i, data):
    output_file  = f'tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}'
    with open(output_file + ".txt", "w") as w_file:
        for key, val in data.items():
            w_file.write(f"{key}\n")
            w_file.write(f"{val}\n")
            w_file.write("\n")

    assert is_same_file(f"tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}.txt", 
                        f"tests/testfiles/vcf_parser_reference/meta_header_parser_test_ref{i}.txt") is True

    os.remove(f"tests/testfiles/vcf_parser_output/meta_header_parser_test_result{i}.txt")
#Compare files
def is_same_file(file1, file2):
    return filecmp.cmp(file1, file2)