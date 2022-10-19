import collections
import json
import pprint
import itertools
import sys
from typing import Dict, Iterator, List, Tuple


from vcfparser.meta_header_parser import MetaDataParser


def obj_to_dict(metainfo):
    """
    Convert the object metainfo of MetaDataParser into dict

    Parameters
    ----------
    metainfo : MetaDataParser
        obj of MetaDataParser

    Returns
    -------
    dict : dictionary of metainfo
    """
    metadict = collections.OrderedDict()
    metadict["VCFspec"] : List[Dict[str, str]] = metainfo.VCFspec
    metadict["FORMAT"] : List[Dict[List[Tuple[str, str]]]] = metainfo.format_
    metadict["INFO"] : List[Dict[str, str]] = metainfo.infos_
    metadict["FILTER"] : List[Dict[str, str]] = metainfo.filters_
    metadict["contig"] : List[Dict[str, str]] = metainfo.contig
    # metadict["ALT"] = metainfo.alt_
    metadict["reference"] : List[str] = metainfo.reference
    metadict["GATKCommandLine"] = metainfo.gatk_commands
    metadict["GVCFBlock"] = metainfo.gvcf_blocks
    metadict["samples"] = metainfo.sample_with_pos
    # metadict['Other'] = metainfo.other_lines
    return metadict


def unpack_str(s :List[str]):
    """
    Unpack the given list of string

    Parameters
    ----------
    s : list
        list of string 
    
    Returns
    -------
    str

    Examples
    --------
    >>> unpack_str(['vcf', 'parser'])
    >>> 'vcf\tparsre'
    """
    return "\t".join(map(str, s))


class MetaDataViewer:
    """
    Class to view meta data information of vcf file
    """
    def __init__(self, vcf_meta_file : Iterator[str], filename="vcfmetafile"):
        """
        Creates the MetaDataViewer Object

        Parameters
        ----------
        vcf_meta_file : str iterator 
            iterator to the vcf file header
        
        filename : str
            output file name
        """
        self.metainfo = MetaDataParser(vcf_meta_file).parse_lines()
        self.output_file = filename
        self.metadict = obj_to_dict(self.metainfo)

    def save_as_table(self):
        """
        write data to a file as text
        """
        print("\twriting metadata as table")
        with open(self.output_file + ".table", "w") as w_file:
            for key, val in self.metadict.items():
                w_file.write(f"##{key}\n")
                if isinstance(val[0], str):
                    w_file.write(f"{unpack_str(val)}\n")
                    w_file.write("\n")

                elif isinstance(val[0], dict):
                    if key in ("VCFspec", "Other"):
                        for item in val:
                            w_file.write(f"#{unpack_str(item.keys())}\n")
                            w_file.write(f"{unpack_str(item.values())}\n")
                            w_file.write("\n")

                    else:
                        w_file.write(f"#{unpack_str(val[0].keys())}\n\n")
                        for item in val:
                            w_file.write(f"{unpack_str(item.values())}\n")
                        w_file.write("\n")

    def save_as_json(self):
        """
        Convert the dictionary to a json object and write to a file
        """
        print("\twriting metadata as JSON")

        json_obj_string = json.dumps(self.metadict)
        datastore = json.loads(json_obj_string)

        with open("%s.json" % self.output_file, "w", encoding="utf-8") as write_as_json:
            json.dump(datastore, write_as_json, ensure_ascii=False, indent=4)

    def save_as_orderdict(self):

        """
        Converts the json type dictionary to 
        dictionary that has all the values under same keys in one list of values.
        """
        grouped_dict = collections.OrderedDict()
        for kyes, vyes in self.metadict.items():
            nested_dict = collections.OrderedDict()
            for elements in vyes:
                if isinstance(elements, dict):

                    for nes_ks, nes_vs in elements.items():
                        if nes_ks not in nested_dict:
                            nested_dict[nes_ks] = [nes_vs]
                        else:
                            nested_dict[nes_ks].append(nes_vs)
                else:
                    nested_dict[kyes] = vyes

            grouped_dict[kyes] = nested_dict

        ## Write the grouped dict to a file as shown in prettyprint
        print("\twriting metadata as dictionary.")
        with open("%s.dict" % self.output_file, "w", encoding="utf-8") as write_as_dict:
            pprint.pprint(grouped_dict, stream=write_as_dict)

    def print_requested_metadata(self, metadata_of_interest):
        """
        To print the value of requested MetaData

        Parameters
        ----------
        metadata_of_interest : list
            list of str
        
        Returns
        -------
        None

        Examples
        --------

        >>> meta = MetaDataViewer(itr_to_file, "input_file")
        >>> req = ['ALT', 'FILTER']
        >>> meta.print_requested_metadata(req)
        ##ALT=<ID=NON_REF,Description="Represents any possible alternative allele at this location">
        ##FILTER=<ID=LowQual,Description="Low quality">
        ##FILTER=<ID=my_indel_filter,Description="QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0">
        ##FILTER=<ID=my_snp_filter,Description="QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0">

        """
        metadict = self.metadict
        other_keys_list = [list(item.keys()) for item in metadict.get("Other",[])]
        other_keys_set = set(list(itertools.chain.from_iterable(other_keys_list)))
        for rq_metadata in metadata_of_interest:
            if metadict.get(rq_metadata):
                val = metadict.get(rq_metadata)
                print(f"##{rq_metadata}\n")
                if isinstance(val[0], str):
                    print(f"{unpack_str(val)}\n")

                elif isinstance(val[0], dict):
                    if rq_metadata in ("VCFspec", "Other"):
                        for item in val:
                            print(f"#{unpack_str(item.keys())}\n")
                            print(f"{unpack_str(item.values())}\n")

                    else:
                        print(f"#{unpack_str(val[0].keys())}\n\n")
                        for item in val:
                            print(f"{unpack_str(item.values())}")

            # check if metadata in Other
            else:
                if rq_metadata in other_keys_set:
                    print(f"##{rq_metadata}\n")
                    # print value of requested metadata from other field
                    # TODO: might need some correction to handle cases if items in metadict are not in dict
                    print(item.get(rq_metadata) for item in metadict["Other"])
