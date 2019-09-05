import re
import shlex
from collections import OrderedDict


class MetaDataParser:
    """Parses a meta lines of the vcf files."""

    def __init__(self, header_file):
        self.header_file = header_file
        self.infos_ = []
        self.filters_= []
        self.contig_ = []
        self.format_ = []
        self.alt_= []
        self.other_lines = []

        self.header = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        self.header_keys = {
            "info": ["ID", "Number", "Type", "Description"],
            "form": ["ID", "Number", "Type", "Description"],
            "filt": ["ID", "Description"],
            "alt": ["ID", "Description"],
            "contig": ["ID", "length"],
        }
        self.fileformat = None
        self.reference = None
        self.sample_names = []

        self.format_pattern = re.compile(r'''\#\#FORMAT=<
            ID=(?P<id>.+),\s*
            Number=(?P<number>-?\d+|\.|[AGR]),\s*
            Type=(?P<type>.+),\s*
            Description="(?P<desc>.*)"
            >''', re.VERBOSE)
        self.meta_pattern = re.compile(r'''##(?P<key>.+?)=(?P<val>.+)''')

    @staticmethod
    def split_to_dict(string):
        string = string.lstrip('<').rstrip('>')
        splitter = shlex.shlex(string, posix=True)
        splitter.whitespace_split = True
        splitter.whitespace = ","
        tags_dict = dict(pair.split("=") for pair in splitter)
        return tags_dict


    def _parse_lines(self):
        """Parse a vcf metadataline"""
        for line in self.header_file:
            if line.startswith('##'):            
                
                line = line.rstrip()
                line_info = line[2:].split("=",1)
                match = False

                if line_info[0] == "fileformat":
                    try:
                        self.fileformat = line_info[1]
                    except IndexError:
                        raise SyntaxError("fileformat must have a value")

                if line_info[0] == "reference":
                    try:
                        self.reference = line_info[1]
                    except IndexError:
                        raise SyntaxError("Refrence value is not provided")

                elif line_info[0] == "INFO":
                    self.infos_.append(self.split_to_dict(line_info[1]))

                elif line_info[0] == "FILTER":
                    self.filters_.append(self.split_to_dict(line_info[1]))

                elif line_info[0] == "contig":
                    self.contig_.append(self.split_to_dict(line_info[1]))

                elif line_info[0] == "FORMAT":
                    match = self.format_pattern.match(line)
                    if not match:
                        raise SyntaxError(
                            "One of the FORMAT lines is malformed: {0}".format(line)
                        )

                    matches = [
                        match.group("id"),
                        match.group("number"),
                        match.group("type"),
                        match.group("desc"),
                    ]
                    form_keys = ["ID", "Number", "Type", "Description"]
                    self.format_.append(dict(list(zip(form_keys, matches))))


                elif line_info[0] == "ALT":
                    self.alt_.append(self.split_to_dict(line_info[1]))

                else:
                    match = self.meta_pattern.match(line)
                    if not match:
                        raise SyntaxError(
                            "One of the meta data lines is malformed: {0}".format(line)
                        )

                    self.other_lines.append({match.group("key"): match.group("val")})
            else:
                self.record_keys = line.strip('\n').split('\t')
                self.sample_names = self.record_keys[9:] if len(self.record_keys)> 9 else None
        return self
        
