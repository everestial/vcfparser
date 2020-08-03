import pytest
import filecmp
import os
import collections
import sys
import json
import csv
import itertools

from vcfparser import VcfParser

vcf_obj = VcfParser("tests/testfiles/vcf_parser_input/reference_input_test.vcf")
metainfo_output_file = (
    "tests/testfiles/vcf_parser_output/vcfparser_metainfo_test_result"
)
records_output_file = "tests/testfiles/vcf_parser_output/vcfparser_records_test_result"


def test_get_metainfo():
    metainfo = vcf_obj.parse_metadata()

    data = dict(
        zip(
            ["fileformat", "filters", "alt", "sample_names", "record_keys"],
            [
                metainfo.fileformat,
                metainfo.filters_,
                metainfo.alt_,
                metainfo.sample_names,
                metainfo.record_keys,
            ],
        )
    )
    with open(metainfo_output_file + ".txt", "w") as w_file:
        for key, val in data.items():
            w_file.write(f"{key}\n")
            w_file.write(f"{val}\n")
            w_file.write("\n")

    assert (
        is_same_file(
            "tests/testfiles/vcf_parser_output/vcfparser_metainfo_test_result.txt",
            f"tests/testfiles/vcf_parser_reference/vcfparser_metainfo_test_ref.txt",
        )
        is True
    )

    os.remove(f"tests/testfiles/vcf_parser_output/vcfparser_metainfo_test_result.txt")


def test_get_records():
    records = vcf_obj.parse_records()

    records_list = []
    for record in records:
        chrom = record.CHROM
        pos = record.POS
        id = record.ID
        ref = record.REF
        alt = record.ALT
        qual = record.QUAL
        filter = record.FILTER
        format_ = record.format_
        infos = record.get_info_as_dict()
        mapped_sample = record.mapped_format_to_sample

        temp_dict = {}
        temp_dict["Chrom"] = chrom
        temp_dict["pos"] = pos
        temp_dict["id"] = id
        temp_dict["ref"] = ref
        temp_dict["alt"] = alt
        temp_dict["qual"] = qual
        temp_dict["filter"] = filter
        temp_dict["format"] = format_
        temp_dict["infos"] = infos
        temp_dict["mapped_sample"] = mapped_sample
        records_list.append(temp_dict)

    columns = [key for key in records_list[0]]
    with open(records_output_file + ".txt", "w") as w_file:
        writer = csv.DictWriter(w_file, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(records_list)

    assert (
        is_same_file(
            "tests/testfiles/vcf_parser_output/vcfparser_records_test_result.txt",
            f"tests/testfiles/vcf_parser_reference/vcfparser_records_test_ref.txt",
        )
        is True
    )

    os.remove(f"tests/testfiles/vcf_parser_output/vcfparser_records_test_result.txt")

##TODO:Bishwa - Need to test all if else case inside parse_records.
# def test_parse_records():
#     records = vcf_obj.parse_records()

#     for record in records:

    


##TODO: Bishwa - Could not raise StopIteration
# def test_get_records_error():
#     vcf_obj1 = VcfParser("tests/testfiles/vcf_parser_input/reference_input_test_no_header.vcf")
    
#     with pytest.raises(StopIteration):

#         _record_lines = itertools.dropwhile(
#             lambda x: x.startswith("##"), vcf_obj1._file_copy
#         )
#         try:
#             header_line = next(_record_lines)
#         except StopIteration:
#             print("File doesnot contain header line.")
#         record_keys = header_line.lstrip("#").strip("\n")

def is_same_file(file1, file2):
    return filecmp.cmp(file1, file2)
