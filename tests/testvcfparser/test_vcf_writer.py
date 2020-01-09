import pytest
import filecmp
import os
import collections
import sys
import json
import csv

from vcfparser import VCFWriter
infilename = "tests/testfiles/vcf_parser_input/reference_input_test.vcf"
outfilename = "tests/testfiles/vcf_parser_ouput/writer_output_test.txt"
id = ""
writer_obj = VCFWriter(infilename)
#1 VCFWriter.add_normal_metadata
def test_add_normal_metadata():
    pass
    # key = ""
    # value = ""
    # writer_obj.add_normal_metadata(key, value)
#2 VCFWriter.add_info
def test_add_info():
    pass
    # writer_obj.add_info(id, num=".", type=".", desc="", key="INFO")
#3 VCFWriter.add_format
def test_add_format():
    pass
    # writer_obj.add_format(id, num=".", type=".", desc="", key="FORMAT")
#4 VCFWriter.add_filter
def test_add_filter():
    pass
    # writer_obj.add_filter(id, desc="", key="FILTER")
#5 VCFWriter.add_filter_long
def test_add_filter_long():
    pass
    # writer_obj.add_filter_long(id, num=".", type=".", desc="", key="FILTER")
#6 VCFWriter.add_contig
def test_add_contig():
    pass
    # length = ""
    # writer_obj.add_contig(id, length, key="contig")
#7 VCFWriter.add_header_line
def test_add_header_line():
    pass
    # record_keys = ""
    # writer_obj.add_header_line(record_keys)
#8 VCFWriter.add_record_value
def test_add_record_value():
    pass
    # preheader = ""
    # info = ""
    # format_ = ""
    # sample_str = ""
    # writer_obj.add_record_value(preheader, info, format_, sample_str)

# #Helping functions
# def write_data_and_check(i, data):
#     output_file  = f'tests/testfiles/vcf_parser_output/writer_parser_test_result{i}'
#     with open(output_file + ".txt", "w") as w_file:
#         for key, val in data.items():
#             w_file.write(f"{key}\n")
#             w_file.write(f"{val}\n")
#             w_file.write("\n")

#     assert is_same_file(f"tests/testfiles/vcf_parser_output/writer_parser_test_result{i}.txt", 
#                         f"tests/testfiles/vcf_parser_reference/writer_parser_test_ref{i}.txt") is True

#     os.remove(f"tests/testfiles/vcf_parser_output/writer_parser_test_result{i}.txt")
# #Compare files
# def is_same_file(file1, file2):
#     return filecmp.cmp(file1, file2)