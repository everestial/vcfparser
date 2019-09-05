#!/usr/bin/env python
# coding: utf-8

from collections import namedtuple, OrderedDict
import shlex
import itertools
import warnings
import gzip


from meta_parser import _MetadataParser
from record_formatter import map_format_tags_to_sample_values
from meta_header_parser import MetaDataParser


class VcfParser:
    """
    Parses a given vcf file into and outputs metainfo and yields records.
    """

    def __init__(self, filename):
        self.filename = filename
        # assign to support gz compressed files
        self._open = gzip.open if self.filename.endswith(".gz") else open
        # to copies of file are created inorder to iterate over metadata and records separately
        self._file = self._open(filename, "rt")
        self._file_copy = self._open(filename, "rt")

    def parse_metadata(self):
        """ initialize variables to store meta infos"""
        # this produces a iterator of meta data lines (lines starting with '#')
        _raw_lines = itertools.takewhile(lambda x: x.startswith("#"), self._file)
        return MetaDataParser(_raw_lines)._parse_lines()
        

    def parse_records(self, iupac=None):
        """
        Parse records from file and yield it.
        """
        _record_lines = itertools.dropwhile(
            lambda x: x.startswith("##"), self._file_copy
        )
        header_line = next(_record_lines)
        record_keys = header_line.lstrip("#").strip("\n").split("\t")
        sample_names = record_keys[9:]

        for record_line in _record_lines:
            rec_dict = dict(zip(record_keys, record_line.strip("\n").split("\t")))
            info_str = rec_dict["INFO"]

            # inorder to encorpate those infos without "=" in records
            try:
                mapped_info = dict(s.split("=", 1) for s in info_str.split(";"))
            except ValueError:
                warnings.warn(
                    f"This info tag doesnot have '=' sign in info : {info_str}.\
                    Such keys will be populated with '.' values"
                )
                mapped_info = {}
                for s in info_str.split(";"):
                    if "=" in s:
                        k, v = s.split("=")
                        mapped_info[k] = v
                    else:
                        mapped_info[s] = "."
            mapped_dict = map_format_tags_to_sample_values(
                rec_dict, sample_names, iupac=iupac
            )
            mapped_dict["INFO"] = mapped_info
            record = namedtuple("Record", mapped_dict.keys())(**mapped_dict)
            yield record
