#!/usr/bin/env python
# coding: utf-8

import gzip
import itertools
import sys

from vcfparser.meta_header_parser import MetaDataParser
from vcfparser.record_parser import Record


class VcfParser:
    """
    A class to parse the metadata information and yield records from the input VCF.

    Methods
    -------
    parse_metadata()
    parse_records()
    """
    #TODO (Bhuwan, Gopal): Done Insert a line break here and several other places as need be.
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

    # TODO (Bhuwan, low priority) - Could multiprocessing be invoked here?? with -n flag
    # multiprocessing should however follow the order (genomic position)
    # TODO (Bhuwan, Gopal) Done properly render the "Uses" flag in this function too. 
    def parse_records(self, chrom=None, pos_range=None, no_processors=1):
        # TODO (Bhuwan, mid priority, research item)(Research Done ; Not implemented)
        # may be replce "no_of_recs" with "nt" i.e number of threads

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
        #TODO: Done 
        # the Uses is not being rendered properly.

        #TODO Done (Bhuwan, Bishwa; priority = high)
        #the no_of_recs is not being used. 
        # Keep or delete or use it? 

        _record_lines = itertools.dropwhile(
            lambda x: x.startswith("##"), self._file_copy
        )

        # TODO - ask with Bhuwan: What is this try/StopIteration doing?
        # Do we need the code - if _record_lines.startswith("#CHROM")
        try:
            header_line = next(_record_lines)  # if _record_lines.startswith("#CHROM")
        except StopIteration:
            print("File doesnot contain the record header line.")
            sys.exit(0)
        record_keys = header_line.lstrip("#").strip("\n").split("\t")

        if pos_range:
            start_pos, end_pos = int(pos_range[0]), int(pos_range[1])

        for record_line in _record_lines:
            record_line = record_line.strip("\n").split("\t")

            # in order to select only selected chrom values
            if chrom and pos_range:
                ch_val = record_line[0]
                pos_val = int(record_line[1])
                if ch_val == chrom and start_pos <= pos_val <= end_pos:
                    yield Record(record_line, record_keys)

            elif chrom:
                ch_val = record_line[0]
                if ch_val == chrom:
                    yield Record(record_line, record_keys)

            elif pos_range:
                pos_val = int(record_line[1])
                start_pos, end_pos = int(pos_range[0]), int(pos_range[1])
                if start_pos <= pos_val <= end_pos:
                    yield Record(record_line, record_keys)

            else:
                yield Record(record_line, record_keys)
