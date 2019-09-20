import re
import shlex
from collections import OrderedDict


class MetaDataParser:
    """Parses a meta lines of the vcf files."""

    def __init__(self, header_file):
        self.header_file = header_file
        self.infos_ = []
        self.filters_ = []
        self.contig = []
        self.format_ = []
        self.alt_ = []
        self.other_lines = []

        self.fileformat = None
        self.reference = None
        self.sample_names = []
        self.is_gvcf = False
        self.gvcf_blocks = []
        self.record_keys = []

        # to write of header lines only
        self.raw_meta_data = ''

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

    @staticmethod
    def _parse_gvcf_block(lines):
        """extract the GVCF blocks"""
        # e.g: ##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)
        # converts to {'minGQ': '55(inclusive)', 'maxGQ': '56(exclusive)', 'Block': '55-56'}
        gvcf_block = re.search("##GVCFBlock(.*?)=", lines, 0).group(1)

        # update tags_dict
        to_replace = '##GVCFBlock' + gvcf_block + "="

        string = lines.rstrip(">").replace(to_replace, "")
        tags_dict = dict(pair.split("=") for pair in string.split(','))
        tags_dict["Block"] = gvcf_block
        return tags_dict

    def parse_lines(self):
        """Parse a vcf metadataline"""
        for line in self.header_file:
            self.raw_meta_data += line
            if line.startswith('##'):

                line = line.rstrip()
                line_info = line[2:].split("=", 1)

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
                    self.contig.append(self.split_to_dict(line_info[1]))

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

                elif line_info[0].startswith('GVCF'):
                    self.is_gvcf = True
                    self.gvcf_blocks.append(self._parse_gvcf_block(line))

                else:
                    match = self.meta_pattern.match(line)
                    if not match:
                        raise SyntaxError(
                            "One of the meta data lines is malformed: {0}".format(line)
                        )

                    self.other_lines.append({match.group("key"): match.group("val")})
            else:
                self.record_keys = line.lstrip(r"#").strip('\n').split('\t')
                self.sample_names = self.record_keys[9:] if len(self.record_keys) > 9 else None
        return self
