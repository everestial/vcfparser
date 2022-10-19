import re
import shlex
from typing import Dict, Iterator, List, Pattern, Tuple, Union


class MetaDataParser:
    """Parses a meta lines of the vcf files."""

    def __init__(self, header_file):
        self.header_file : Iterator[str] = header_file
        self.infos_ : List[Dict[str, str]] = []
        self.filters_ : List[Dict[str, str]] = []
        self.contig : List[Dict[str, str]] = []
        self.format_ : List[Dict[List[Tuple[str, str]]]] = []
        self.alt_ : List[Dict[str, str]] = []
        self.other_lines : List[Dict[str, str]]  = []
        self.fileformat : str = None
        self.reference : List[str] = []
        self.sample_names : Union[List[str], None] = []
        self.is_gvcf : bool = False
        self.gvcf_blocks : List[Dict[str, str]] = [] 
        self.record_keys : List[str] = [] 
        self.VCFspec : List[Dict[str, str]] = []
        self.gatk_commands : List[Dict[str, str]] = [] # add

        # to write header lines only
        self.raw_meta_data : str = ""

        self._format_pattern : Pattern[str] = re.compile(
            r"""\#\#FORMAT=<
            ID=(?P<id>.+),\s*
            Number=(?P<number>-?\d+|\.|[AGR]),\s*
            Type=(?P<type>.+),\s*
            Description="(?P<desc>.*)"
            >""",
            re.VERBOSE,
        )
        self._meta_pattern = re.compile(r"""##(?P<key>.+?)=(?P<val>.+)""")

    @staticmethod
    def _parse_gvcf_block(lines) -> Dict[str, str]:
        """
        extract the GVCF blocks

        Parameters
        ----------
        lines : str
            str of GVCFBlock
        
        Returns
        -------
        dict :  
            key value pair of extracted GVCFBlock

        Examples
        --------
        >>> meta = MetaDataParser(header_files)
        >>> lines = "##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)"
        >>> meta._parse_gvcf_block(lines)
        {'minGQ': '55(inclusive)', 'maxGQ': '56(exclusive)', 'Block': '55-56'}

        """
        # e.g input: ##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)
        # output: {'minGQ': '55(inclusive)', 'maxGQ': '56(exclusive)', 'Block': '55-56'}
        gvcf_block : str = re.search("##GVCFBlock(.*?)=", lines, 0).group(1) # => answer will be "55-56"

        # update tags_dict
        to_replace : str = "##GVCFBlock" + gvcf_block + "="

        string : str = lines.rstrip(">").replace(to_replace, "")
        tags_dict : Dict[str, str] = split_to_dict(string)
        tags_dict["Block"] = gvcf_block
        return tags_dict

    @staticmethod
    def _parse_gatk_commands(lines):
        """
        find the GATK commands used to generate the input 

        Parameters
        ----------
        lines : str
            str of GVCFBlock
        
        Returns
        -------
        dict :  
            key value pair of extracted GVCFBlock

        Examples
        --------
        """
        ## e.g: ##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller....
        gatk_cmd_middle_string : str = re.search("##GATKCommandLine(.*)=<ID=", lines).group(1)
        to_replace : str = "##GATKCommandLine" + gatk_cmd_middle_string + "=<"
        string : str = lines.rstrip("\n").rstrip(">").replace(to_replace, "")
        tags_dict : Dict[str, str] = split_to_dict(string)
        return tags_dict

    def parse_lines(self):
        """
        Parse a vcf metadataline

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for line in self.header_file:
            self.raw_meta_data += line
            if line.startswith("##"):

                line = line.rstrip()
                line_info : List[str] = line[2:].split("=", 1)

                if line_info[0] == "fileformat":
                    try:
                        self.fileformat = line_info[1]
                        self.VCFspec.append({"fileformat": self.fileformat})
                    except IndexError:
                        raise SyntaxError("fileformat must have a value")

                elif line_info[0] == "reference":
                    try:
                        self.reference.append(line_info[1])
                    except IndexError:
                        raise SyntaxError("Refrence value is not provided")

                elif line_info[0] == "INFO":
                    self.infos_.append(split_to_dict(line_info[1]))

                elif line_info[0] == "FILTER":
                    self.filters_.append(split_to_dict(line_info[1]))

                elif line_info[0] == "contig":
                    self.contig.append(split_to_dict(line_info[1]))

                elif line_info[0] == "FORMAT":
                    match = self._format_pattern.match(line)
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
                    self.format_.append(dict(list(zip(form_keys, matches)))) # List[Dict[List[Tuple[str, str]]]]

                elif line_info[0] == "ALT":
                    self.alt_.append(split_to_dict(line_info[1]))

                elif line_info[0].startswith("GVCF"):
                    if not self.is_gvcf:
                        self.is_gvcf = True
                        self.VCFspec.append({"GVCF": self.is_gvcf})
                    self.gvcf_blocks.append(self._parse_gvcf_block(line))

                elif line_info[0].startswith("GATKCommandLine"):
                    self.gatk_commands.append(self._parse_gatk_commands(line))

                else:
                    match = self._meta_pattern.match(line)
                    if not match:
                        raise SyntaxError(
                            "One of the meta data lines is malformed: {0}".format(line)
                        )

                    self.other_lines.append({match.group("key"): match.group("val")})
            else:
                self.record_keys = line.lstrip(r"#").strip("\n").split("\t")
                self.sample_names = (
                    self.record_keys[9:] if len(self.record_keys) > 9 else None
                )
                pos_list = list(range(10, len(self.record_keys) + 1))
                self.sample_with_pos = [
                    {"name": x, "position": y}
                    for x, y in zip(self.sample_names, pos_list)
                ]
        return self


# function to split the string at "," and create key-value pair at "="
# mainly aimed for parsing VCF metadata lines and create dictionary
def split_to_dict(string):
    """
    Split the string by ,

    Parameters
    ----------
    string : str
        string that requires split

    Returns
    -------
    dict :
        dict of tags

    Examples
    --------
    """
    string = string.lstrip("<").rstrip(">")
    splitter = shlex.shlex(string, posix=True)
    splitter.whitespace_split = True
    splitter.whitespace = ","
    tags_dict = dict(pair.split("=", maxsplit=1) for pair in splitter)
    return tags_dict
