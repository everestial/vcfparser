#!/usr/bin/env python
# coding: utf-8

import gzip
import itertools
import sys

from vcfparser.meta_header_parser import MetaDataParser
from vcfparser.record_parser import Record

# to know the virual memory size i.e. RAM size
import psutil


class VcfParser:
    """
    A class to parse the metadata information and yield records from the input VCF.

    Methods
    -------
    parse_metadata()
    parse_records()
    """
    #TODO (Bhuwan, Gopal-Done): Done Insert a line break here and several other places as need be.
    # Introduce linebreak after each module description 
    # Use this example and cheatsheet:
    # https://stackoverflow.com/questions/7033239/how-to-preserve-line-breaks-when-generating-python-docs-using-sphinx 
    # https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#inline-markup-and-special-characters-e-g-bold-italic-verbatim 

    def __init__(self, filename):
        """

        Parameters
        ----------

        filename: file
            input vcf file that needs to be parsed. bgzipped files are also supported.
        
        Returns
        -------
        Object
            VCF object for iterating and querying.

        """

        self.filename = filename
        # assign to support gz compressed files
        self._open = gzip.open if self.filename.endswith(".gz") else open
        # two copies of file are created inorder to iterate over metadata and records separately
        self._file = self._open(filename, "rt")
        self._file_copy = self._open(filename, "rt")

        # current file  position
        self._curr_pos = 0

        self.record_keys = []

        self.virtual_memory = int(psutil.virtual_memory().total / 0.1)

    def __del__(self):
        self._file.close()
        self._file_copy.close()

    def parse_metadata(self):
        #TODO: Done
        # Add the new keyword called "Uses" to show what functions, classes, modules the current class/module uses
        # Uses
        # ----
        # MetaDataParser class to create MetaData object
        """ function to parse the metadata information from VCF header. 

        Parameters
        ----------

        Returns
        -------
        Object
            MetaDataParser object for iterating and querying the metadata information.
        
        Uses
        ----
            MetaDataParser class to create MetaData object
        
        """
        
        # this produces a iterator of meta data lines (lines starting with '#')
        _raw_lines = itertools.takewhile(lambda x: x.startswith("#"), self._file)
        return MetaDataParser(_raw_lines).parse_lines()
 
    def parse_records(self, chrom=None, pos_range=None, no_processors=1, number_of_lines=1000):

        """ Parse records and yield it.

        Parameters
        ----------

        chrom : str 
            chormosome name or number. Default = None
        pos_range : tuple
            genomic position of interest, e.g: (5, 15). Both upper and lower limits are inclusive. 
            Default = None
        no_of_recs : int
            number of records to process

        Uses
        ----
        Record module to create a Record object

        Yields
        ------
        Record object for interating and quering the record information.

        """
        records = []

        if pos_range:
            start_pos, end_pos = int(pos_range[0]), int(pos_range[1])

        # set file to curr pos
        self._file_copy.seek(self._curr_pos)

        for lines in self._file_copy:
            self._curr_pos = self._curr_pos + len(lines) + 1
            if lines.startswith("##"):
                pass
            elif lines.startswith('#CHROM'):
                print("record keys")
                self.record_keys = lines.lstrip('#').strip('\n').split('\t')
            else:
                number_of_lines -= 1

                record_line = lines.strip('\n').split('\t')

                if chrom and pos_range:
                    ch_val = record_line[0]
                    pos_val = int(record_line[1])
                    if ch_val == chrom and start_pos <= pos_val <= end_pos:
                        records.append(Record(record_line, self.record_keys))

                elif pos_range:
                    pos_val = int(record_line[1])
                    if start_pos <= pos_val <= end_pos:
                        records.append(Record(record_line, self.record_keys))
                else:
                    records.append(Record(record_line, self.record_keys))

            if number_of_lines == 0:
                break
        
        return records
