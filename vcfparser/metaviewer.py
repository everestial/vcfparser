import collections
import json
import pprint
import itertools
import sys
from typing import Dict, List, Any, Union, Optional, TextIO

from vcfparser.meta_header_parser import MetaDataParser


def obj_to_dict(metainfo: Any) -> collections.OrderedDict[str, Any]:
    """
    Convert MetaDataParser object to OrderedDict for easier processing.
    
    Parameters
    ----------
    metainfo : MetaDataParser
        Parsed VCF metadata object
        
    Returns
    -------
    collections.OrderedDict[str, Any]
        Dictionary containing organized metadata
    """
    metadict: collections.OrderedDict[str, Any] = collections.OrderedDict()
    metadict["VCFspec"] = metainfo.VCFspec
    metadict["FORMAT"] = metainfo.format_
    metadict["INFO"] = metainfo.infos_
    metadict["FILTER"] = metainfo.filters_
    metadict["contig"] = metainfo.contig
    # metadict["ALT"] = metainfo.alt_
    metadict["reference"] = metainfo.reference
    metadict["GATKCommandLine"] = metainfo.gatk_commands
    metadict["GVCFBlock"] = metainfo.gvcf_blocks
    metadict["samples"] = metainfo.sample_with_pos
    # metadict['Other'] = metainfo.other_lines
    return metadict


def unpack_str(s: Any) -> str:
    """
    Convert a list, dict, or other iterable to tab-separated string.
    
    Parameters
    ----------
    s : Any
        Iterable to convert (list, dict keys/values, tuple, etc.)
        
    Returns
    -------
    str
        Tab-separated string representation
    """
    return "\t".join(map(str, s))


class MetaDataViewer:
    """
    A class for viewing and exporting VCF metadata in different formats.
    
    This class provides methods to save VCF metadata as table, JSON, 
    or ordered dictionary formats, and to print specific metadata sections.
    """
    
    # Instance attributes
    metainfo: Any
    output_file: str
    metadict: collections.OrderedDict[str, Any]
    
    def __init__(self, vcf_meta_file: str, filename: str = "vcfmetafile") -> None:
        """
        Initialize MetaDataViewer with VCF metadata file.
        
        Parameters
        ----------
        vcf_meta_file : str
            Path to VCF file to parse metadata from
        filename : str, optional
            Base name for output files (default: "vcfmetafile")
        """
        # Read the VCF file to get header lines
        with open(vcf_meta_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.metainfo = MetaDataParser(lines).parse_lines()
        self.output_file = filename
        self.metadict = obj_to_dict(self.metainfo)

    def save_as_table(self) -> None:
        """
        Write metadata to a file as formatted table text.
        
        Creates a .table file with metadata organized in a readable format.
        Each metadata section is clearly labeled and formatted.
        """
        print("\twriting metadata as table")
        try:
            with open(self.output_file + ".table", "w", encoding="utf-8") as w_file:
                for key, val in self.metadict.items():
                    if not val:  # Skip empty values
                        continue
                        
                    w_file.write(f"##{key}\n")
                    
                    # Handle different value types safely
                    if isinstance(val, (list, tuple)) and len(val) > 0:
                        if isinstance(val[0], str):
                            w_file.write(f"{unpack_str(val)}\n")
                            w_file.write("\n")
                        elif isinstance(val[0], dict):
                            if key in ("VCFspec", "Other"):
                                for item in val:
                                    if isinstance(item, dict):
                                        w_file.write(f"#{unpack_str(item.keys())}\n")
                                        w_file.write(f"{unpack_str(item.values())}\n")
                                        w_file.write("\n")
                            else:
                                w_file.write(f"#{unpack_str(val[0].keys())}\n\n")
                                for item in val:
                                    if isinstance(item, dict):
                                        w_file.write(f"{unpack_str(item.values())}\n")
                                w_file.write("\n")
                    elif isinstance(val, dict):
                        w_file.write(f"#{unpack_str(val.keys())}\n")
                        w_file.write(f"{unpack_str(val.values())}\n")
                        w_file.write("\n")
        except IOError as e:
            print(f"Error writing table file: {e}")
            raise

    def save_as_json(self) -> None:
        """
        Convert the metadata dictionary to JSON format and write to file.
        
        Creates a .json file with properly formatted and indented JSON.
        Uses UTF-8 encoding to handle special characters.
        """
        print("\twriting metadata as JSON")
        
        try:
            # Convert OrderedDict to regular dict for JSON serialization
            json_data = dict(self.metadict)
            
            with open(f"{self.output_file}.json", "w", encoding="utf-8") as write_as_json:
                json.dump(json_data, write_as_json, ensure_ascii=False, indent=4)
        except (IOError, TypeError) as e:
            print(f"Error writing JSON file: {e}")
            raise

    def save_as_orderdict(self) -> None:
        """
        Convert metadata to grouped OrderedDict and save to file.
        
        Groups all values under the same keys into lists,
        making it easier to analyze metadata patterns.
        Creates a .dict file with pretty-printed output.
        """
        grouped_dict: collections.OrderedDict[str, Any] = collections.OrderedDict()
        
        for keys, values in self.metadict.items():
            nested_dict: collections.OrderedDict[str, Any] = collections.OrderedDict()
            
            if isinstance(values, (list, tuple)):
                for element in values:
                    if isinstance(element, dict):
                        for nested_key, nested_value in element.items():
                            if nested_key not in nested_dict:
                                nested_dict[nested_key] = [nested_value]
                            else:
                                nested_dict[nested_key].append(nested_value)
                    else:
                        # Handle non-dict elements
                        if keys not in nested_dict:
                            nested_dict[keys] = [element]
                        else:
                            nested_dict[keys].append(element)
            else:
                # Handle non-list values
                nested_dict[keys] = values
            
            grouped_dict[keys] = nested_dict
        
        # Write the grouped dict to a file using pretty print
        print("\twriting metadata as dictionary.")
        try:
            with open(f"{self.output_file}.dict", "w", encoding="utf-8") as write_as_dict:
                pprint.pprint(grouped_dict, stream=write_as_dict)
        except IOError as e:
            print(f"Error writing dictionary file: {e}")
            raise

    def print_requested_metadata(self, metadata_of_interest: List[str]) -> None:
        """
        Print specific metadata sections to console.
        
        Parameters
        ----------
        metadata_of_interest : List[str]
            List of metadata section names to print
            
        Notes
        -----
        If a requested metadata section is not found in main sections,
        it will search in the 'Other' section.
        """
        metadict = self.metadict
        
        # Build set of keys from 'Other' section for efficient lookup
        other_section = metadict.get("Other", [])
        other_keys_list = []
        if isinstance(other_section, list):
            other_keys_list = [list(item.keys()) for item in other_section if isinstance(item, dict)]
        other_keys_set = set(itertools.chain.from_iterable(other_keys_list))
        
        for rq_metadata in metadata_of_interest:
            metadata_value = metadict.get(rq_metadata)
            
            if metadata_value:
                print(f"##{rq_metadata}\n")
                
                # Handle different value types safely
                if isinstance(metadata_value, (list, tuple)) and len(metadata_value) > 0:
                    if isinstance(metadata_value[0], str):
                        print(f"{unpack_str(metadata_value)}\n")
                    elif isinstance(metadata_value[0], dict):
                        if rq_metadata in ("VCFspec", "Other"):
                            for item in metadata_value:
                                if isinstance(item, dict):
                                    print(f"#{unpack_str(item.keys())}")
                                    print(f"{unpack_str(item.values())}\n")
                        else:
                            if isinstance(metadata_value[0], dict):
                                print(f"#{unpack_str(metadata_value[0].keys())}\n")
                                for item in metadata_value:
                                    if isinstance(item, dict):
                                        print(f"{unpack_str(item.values())}")
                elif isinstance(metadata_value, dict):
                    print(f"#{unpack_str(metadata_value.keys())}")
                    print(f"{unpack_str(metadata_value.values())}")
                else:
                    print(str(metadata_value))
                    
            # Check if metadata is in 'Other' section
            elif rq_metadata in other_keys_set:
                print(f"##{rq_metadata}\n")
                # Print values from 'Other' section
                for item in other_section:
                    if isinstance(item, dict) and rq_metadata in item:
                        print(item.get(rq_metadata))
            else:
                print(f"Metadata '{rq_metadata}' not found.")
