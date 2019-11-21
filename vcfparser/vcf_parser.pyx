#!/usr/bin/env python
# coding: utf-8

import gzip
import itertools

from vcfparser.meta_header_parser import MetaDataParser
from vcfparser.record_parser import Record


class VcfParser:
    """
    Parses a given vcf file into and outputs metainfo and yields records.

    Methods
    -------
    parse_metadata()
    parse_records()

    """

    def __init__(self, filename):
        """

        Parameters
        ----------
        filename: file
            input vcf file that needs to be parsed. bzip files are also supported.

        """
        self.filename = filename
        # assign to support gz compressed files
        self._open = gzip.open if self.filename.endswith(".gz") else open
        # to copies of file are created inorder to iterate over metadata and records separately
        self._file = self._open(filename, "rt")
        self._file_copy = self._open(filename, "rt")

    def __del__(self):
        self._file.close()
        self._file_copy.close()

    def parse_metadata(self):
        """ initialize variables to store meta infos"""
        # this produces a iterator of meta data lines (lines starting with '#')
        _raw_lines = itertools.takewhile(lambda x: x.startswith("#"), self._file)
        return MetaDataParser(_raw_lines).parse_lines()

    def parse_records(self, chrom=None, pos_range=None, no_of_recs=1):
        """ Parse records from file and yield it.

        Parameters
        ----------
        chrom : str
        pos_range : str
        no_of_recs : int

        Yields
        ------
        Record object on which we can perform different operations and extract required values

        """

        _record_lines = itertools.dropwhile(
            lambda x: x.startswith("##"), self._file_copy
        )
        header_line = next(_record_lines)
        record_keys = header_line.lstrip("#").strip("\n")

        for record_line in _record_lines:
            # in order to select only selected chrom values
            if chrom or pos_range:
                ch_val = record_line.split('\t')[0]
                pos_val = int(record_line.split('\t')[1])
                start_pos, end_pos = int(pos_range[0]), int(pos_range[1])

                if ch_val in chrom and start_pos <= pos_val <= end_pos:
                    yield Record(record_line, record_keys)

            else:
                yield Record(record_line, record_keys)
