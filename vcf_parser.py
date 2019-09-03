#!/usr/bin/env python
# coding: utf-8

from collections import namedtuple,OrderedDict
import shlex
import itertools
import gzip


from meta_parser import  _MetadataParser
from record_formatter import map_format_tags_to_sample_values


class VcfParser:
    """
    Parses a given vcf file into and outputs metainfo and yields records.
    """
    def __init__(self, filename):
        self.filename = filename
        # assign to support gz compressed files
        self._open = gzip.open if self.filename.endswith('.gz') else open
        # to copies of file are created inorder to iterate over metadata and records separately
        self._file = self._open(filename, 'rt')
        self._file_copy = self._open(filename, 'rt')

        
    def parse_metadata(self):
        """ initialize variables to store meta infos"""        
        self.raw_header = ''
        self.gvcf_blocks = []
        self.formats_ = []
        self.infos_ = []
        self.filters_ = []
        self.gatk_commands = []
        self.reference_genome = []
        self.contig = []
        self.is_gvcf = False
        # this produces a iterator of meta data lines (lines starting with '#')
        _raw_lines = itertools.takewhile(lambda x : x.startswith('#'), self._file)
        for lines in _raw_lines:
            # store the raw headers to print if needed
            self.raw_header += lines

            # get the file version of vcf file
            if lines.startswith('##fileformat'):
                self.fileformat = lines.strip('##fileformat=')

            elif lines.startswith(r"##GVCFBlock"):
                self.is_gvcf = True

                # parse the GVCF blocks data
                _gvcf_block = _MetadataParser(
                    lines, tag=r"##GVCFBlock"
                ).parse_gvcf_block()
                self.gvcf_blocks.append(_gvcf_block)

                ## extract existing FORMAT, INFO and FILTER tags
            elif lines.startswith(r"##FORMAT"):
                self.formats_.append(
                    _MetadataParser(
                        lines, tag=r"##FORMAT=<"
                    ).parse_format_info_filter()
                    )
            elif lines.startswith(r"##INFO"):
                self.infos_.append(
                    _MetadataParser(
                        lines, tag=r"##INFO=<"
                    ).parse_format_info_filter()
                    )
            elif lines.startswith(r"##FILTER"):
                self.filters_.append(
                    _MetadataParser(
                        lines, tag=r"##FILTER=<"
                    ).parse_format_info_filter()
                )

            ## extract contig/chromosomes included in the VCF file
            elif lines.startswith(r"##contig"):
                self.contig.append(
                    _MetadataParser(lines, tag=r"##contig=<").parse_contigs()
                )

            ## extract the name/path of the reference genome
            elif lines.startswith(r"##reference"):
                self.reference_genome.append(
                    _MetadataParser(
                        lines, tag=r"##reference="
                    ).parse_reference_genome()
                )

            ## extract the GATK commands used so far in the preparation of the VCF file
            elif lines.startswith(r"##GATKCommandLine"):
                self.gatk_commands.append(
                    _MetadataParser(
                        lines, tag=r"##GATKCommandLine"
                    ).parse_gatk_commands()
                )

            ## extract sample names
            elif lines.startswith("#CHROM"):
                # self.parse_sample_names(lines)
                self.record_keys = lines.strip('\n').split('\t')
                self.sample_names = self.record_keys[9:]  
                        
        return self
    
        
    def parse_records(self, iupac = None):  
        """
        Parse records from file and yield it.
        """
        _record_lines = itertools.dropwhile(lambda x : x.startswith('##'), self._file_copy)
        header_line = next(_record_lines)
        record_keys = header_line.lstrip('#').strip('\n').split('\t')
        sample_names = record_keys[9:]
        

        for record_line in _record_lines:
            rec_dict =dict(zip(record_keys, record_line.strip('\n').split('\t')))
            mapped_info = dict(s.split('=',1) for s in rec_dict['INFO'].split(';') if '=' in s)
            mapped_dict = map_format_tags_to_sample_values(rec_dict, sample_names, iupac= iupac)
            mapped_dict['INFO'] = mapped_info
            record = namedtuple('Record', mapped_dict.keys())(**mapped_dict)
            yield record
            






