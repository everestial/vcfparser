#!/usr/bin/env python
# coding: utf-8

"""
VCF Parser Module

This module provides the main VcfParser class for parsing VCF (Variant Call Format) files.
Supports both regular and gzipped VCF files, with filtering capabilities for chromosomes
and genomic position ranges.

Classes
-------
VcfParser : Main VCF parsing class
    Provides methods to parse metadata and records from VCF files.

Examples
--------
>>> from vcfparser import VcfParser
>>> vcf = VcfParser("sample.vcf")
>>> metadata = vcf.parse_metadata()
>>> for record in vcf.parse_records():
...     print(record.CHROM, record.POS, record.REF, record.ALT)
"""

import gzip
import itertools
import sys
from typing import Optional, Tuple, Iterator, Union, TextIO, Callable, Any
from pathlib import Path

from vcfparser.meta_header_parser import MetaDataParser
from vcfparser.record_parser import Record

__all__ = ['VcfParser']


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

    def __init__(self, filename: Union[str, Path]) -> None:
        """
        Initialize VcfParser with VCF file.

        Parameters
        ----------
        filename: Union[str, Path]
            Input VCF file path that needs to be parsed. Bgzipped files (.gz) are also supported.
        
        Returns
        -------
        None
        
        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        
        Examples
        --------
        >>> parser = VcfParser("sample.vcf")
        >>> parser = VcfParser("sample.vcf.gz")
        """
        self.filename: str = str(filename)  # Convert Path to string if needed
        # Assign function to support gz compressed files
        self._open: Any = gzip.open if self.filename.endswith(".gz") else open
        # Two copies of file are created to iterate over metadata and records separately
        self._file: TextIO = self._open(self.filename, "rt")
        self._file_copy: TextIO = self._open(self.filename, "rt")

    def __del__(self) -> None:
        """Clean up file handles when object is destroyed."""
        if hasattr(self, '_file'):
            self._file.close()
        if hasattr(self, '_file_copy'):
            self._file_copy.close()

    def parse_metadata(self) -> MetaDataParser:
        """Parse the metadata information from VCF header.

        Returns
        -------
        MetaDataParser
            MetaDataParser object for iterating and querying the metadata information.
        
        Uses
        ----
        MetaDataParser class to create metadata object
        
        Examples
        --------
        >>> vcf = VcfParser("sample.vcf")
        >>> metadata = vcf.parse_metadata()
        >>> print(metadata.fileformat)
        'VCFv4.2'
        """
        # This produces an iterator of metadata lines (lines starting with '#')
        _raw_lines = itertools.takewhile(lambda x: x.startswith("#"), self._file)
        return MetaDataParser(_raw_lines).parse_lines()

    # TODO (Bhuwan, low priority) - Could multiprocessing be invoked here?? with -n flag
    # multiprocessing should however follow the order (genomic position)
    # TODO (Bhuwan-Done, Gopal) Done properly render the "Uses" flag in this function too. 
    def parse_records(
        self, 
        chrom: Optional[str] = None, 
        pos_range: Optional[Tuple[int, int]] = None, 
        no_processors: int = 1
    ) -> Iterator[Record]:
        """Parse records and yield them.

        Parameters
        ----------
        chrom : Optional[str], default=None
            Chromosome name or number to filter records. If None, all chromosomes are included.
        pos_range : Optional[Tuple[int, int]], default=None
            Genomic position range of interest, e.g: (5, 15). Both upper and lower limits are inclusive. 
            If None, all positions are included.
        no_processors : int, default=1
            Number of processors to use (currently not implemented, reserved for future use).

        Yields
        ------
        Record
            Record object for iterating and querying the record information.
            
        Uses
        ----
        Record module to create Record objects
        
        Examples
        --------
        >>> vcf = VcfParser("sample.vcf")
        >>> # Parse all records
        >>> for record in vcf.parse_records():
        ...     print(record.CHROM, record.POS)
        >>> # Parse records from specific chromosome
        >>> for record in vcf.parse_records(chrom="chr1"):
        ...     print(record.CHROM, record.POS)
        >>> # Parse records in position range
        >>> for record in vcf.parse_records(pos_range=(1000, 2000)):
        ...     print(record.CHROM, record.POS)
        """
        #TODO: Done 
        # the Uses is not being rendered properly.

        #TODO Done (Bhuwan, Bishwa; priority = high)
        #the no_of_recs is not being used. 
        # Keep or delete or use it? 

        ## NOTE: we start parsing the data from file (copy version), after dropping lines that start with ##
        _record_lines = itertools.dropwhile(
            lambda x: x.startswith("##"), self._file_copy
        )

        # TODO - ask with Bhuwan: What is this try/StopIteration doing?
        # Do we need the code - if _record_lines.startswith("#CHROM")

        ## NOTE: we start parsing the data from file (copy version), starting at #CHROM line
        try:
            header_line = next(_record_lines)  # if _record_lines.startswith("#CHROM")
        except StopIteration:
            print("File doesnot contain the record header line.")
            sys.exit(0)
        record_keys = header_line.lstrip("#").strip("\n").split("\t")

        if pos_range:
            start_pos, end_pos = int(pos_range[0]), int(pos_range[1])

        for record_line_str in _record_lines:
            record_line_fields = record_line_str.strip("\n").split("\t")

            # in order to select only selected chrom values
            if chrom and pos_range:
                ch_val = record_line_fields[0]
                pos_val = int(record_line_fields[1])
                if ch_val == chrom and start_pos <= pos_val <= end_pos:
                    yield Record(record_line_fields, record_keys)

            elif chrom:
                ch_val = record_line_fields[0]
                if ch_val == chrom:
                    yield Record(record_line_fields, record_keys)

            ## NOTE/TODO: Do we need to parse file and extract data if only pos_range is given?
            elif pos_range:
                pos_val = int(record_line_fields[1])
                start_pos, end_pos = int(pos_range[0]), int(pos_range[1])
                if start_pos <= pos_val <= end_pos:
                    yield Record(record_line_fields, record_keys)

            else:
                yield Record(record_line_fields, record_keys)
