import re
import shlex
from typing import List, Dict, Any, Optional, Union, Pattern


class MetaDataParser:
    """Parses a meta lines of the vcf files."""

    def __init__(self, header_file: List[str]) -> None:
        self.header_file: List[str] = header_file
        self.infos_: List[Dict[str, str]] = []
        self.filters_: List[Dict[str, str]] = []
        self.contig: List[Dict[str, str]] = []
        self.format_: List[Dict[str, str]] = []
        self.alt_: List[Dict[str, str]] = []
        self.other_lines: List[Dict[str, str]] = []
        self.fileformat: Optional[str] = None
        self.reference: List[str] = []
        self.sample_names: Optional[List[str]] = []
        self.is_gvcf: bool = False
        self.gvcf_blocks: List[Dict[str, str]] = []
        self.record_keys: List[str] = []
        self.VCFspec: List[Dict[str, Any]] = []
        self.gatk_commands: List[Dict[str, str]] = []
        self.sample_with_pos: List[Dict[str, Union[str, int]]] = []

        # to write header lines only
        self.raw_meta_data: str = ""

        self._format_pattern: Pattern[str] = re.compile(
            r"""\#\#FORMAT=<
            ID=(?P<id>.+),\s*
            Number=(?P<number>-?\d+|\.|[AGR]),\s*
            Type=(?P<type>.+),\s*
            Description="(?P<desc>.*)"
            >""",
            re.VERBOSE,
        )
        self._meta_pattern: Pattern[str] = re.compile(r"""##(?P<key>.+?)=(?P<val>.+)""")

    @staticmethod
    def _parse_gvcf_block(lines: str) -> Dict[str, str]:
        """extract the GVCF blocks
        
        Parameters
        ----------
        lines : str
            GVCF block line from VCF header
            
        Returns
        -------
        Dict[str, str]
            Dictionary containing GVCF block information
            
        Examples
        --------
        >>> line = "##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)"
        >>> result = MetaDataParser._parse_gvcf_block(line)
        >>> result['Block']
        '55-56'
        """
        # e.g input: ##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)
        # output: {'minGQ': '55(inclusive)', 'maxGQ': '56(exclusive)', 'Block': '55-56'}
        gvcf_block_match = re.search("##GVCFBlock(.*?)=", lines, 0)
        if not gvcf_block_match:
            raise ValueError(f"Invalid GVCF block line format: {lines}")
        gvcf_block = gvcf_block_match.group(1)

        # update tags_dict
        to_replace = "##GVCFBlock" + gvcf_block + "="

        string = lines.rstrip(">").replace(to_replace, "")
        tags_dict = split_to_dict(string)
        tags_dict["Block"] = gvcf_block
        return tags_dict

    @staticmethod
    def _parse_gatk_commands(lines: str) -> Dict[str, str]:
        """find the GATK commands used to generate the input VCF
        
        Parameters
        ----------
        lines : str
            GATK command line from VCF header
            
        Returns
        -------
        Dict[str, str]
            Dictionary containing GATK command information
            
        Examples
        --------
        >>> line = '##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller,Version=4.0>'
        >>> result = MetaDataParser._parse_gatk_commands(line)
        >>> result['ID']
        'HaplotypeCaller'
        """
        # e.g: ##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller....
        gatk_match = re.search("##GATKCommandLine(.*)=<ID=", lines)
        if not gatk_match:
            raise ValueError(f"Invalid GATK command line format: {lines}")
        gatk_cmd_middle_string = gatk_match.group(1)
        to_replace = "##GATKCommandLine" + gatk_cmd_middle_string + "=<"
        string = lines.rstrip("\n").rstrip(">").replace(to_replace, "")
        tags_dict = split_to_dict(string)
        return tags_dict

    def parse_lines(self) -> 'MetaDataParser':
        """Parse a vcf metadataline
        
        Returns
        -------
        MetaDataParser
            Self instance for method chaining
            
        Raises
        ------
        SyntaxError
            If required metadata values are missing or malformed
        """
        for line in self.header_file:
            self.raw_meta_data += line
            if line.startswith("##"):

                line = line.rstrip()
                line_info = line[2:].split("=", 1)

                if line_info[0] == "fileformat":
                    try:
                        value = line_info[1].strip()
                        if not value:
                            raise SyntaxError("fileformat must have a value")
                        self.fileformat = value
                        self.VCFspec.append({"fileformat": self.fileformat})
                    except IndexError:
                        raise SyntaxError("fileformat must have a value")

                elif line_info[0] == "reference":
                    try:
                        value = line_info[1].strip()
                        if not value:
                            raise SyntaxError("Reference value is not provided")
                        self.reference.append(value)
                    except IndexError:
                        raise SyntaxError("Reference value is not provided")

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
                    self.format_.append(dict(list(zip(form_keys, matches))))

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
                    for x, y in zip(self.sample_names or [], pos_list)
                ]
        return self


def split_to_dict(string: str) -> Dict[str, str]:
    """Split string at "," and create key-value pairs at "="
    
    Mainly aimed for parsing VCF metadata lines and creating dictionaries.
    
    Parameters
    ----------
    string : str
        Input string to split, typically VCF metadata content
        
    Returns
    -------
    Dict[str, str]
        Dictionary with parsed key-value pairs
        
    Examples
    --------
    >>> result = split_to_dict('<ID=DP,Number=1,Type=Integer,Description="Depth">')
    >>> result['ID']
    'DP'
    """
    string = string.lstrip("<").rstrip(">")
    splitter = shlex.shlex(string, posix=True)
    splitter.whitespace_split = True
    splitter.whitespace = ","
    tags_dict: Dict[str, str] = dict(pair.split("=", maxsplit=1) for pair in splitter)
    return tags_dict
