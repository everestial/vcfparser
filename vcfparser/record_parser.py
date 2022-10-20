import re
from typing import Dict, Iterator, List, Set, Tuple, Union
import warnings
from collections import OrderedDict
from itertools import zip_longest
import sys

# Note: A very good example for handling inheritance among classes
# https://pythonspot.com/inner-classes/


class Record:
    """
    A class that converts the record lines from input VCF into accessible record object.
    """

    def __init__(self, record_values : List[str], record_keys : List[str]):
        """
        Initializes the class with header keys and record values.

        Parameters
        ----------
        record_keys: list
            - list of record keys generated for the record values
            - generated from string in the VCF that starts with #CHROM
            - stays the same for a particular VCF file
        record_values: list
            - list of record values generated from the VCF record line 
            - genrated from the lines below # CHROM in VCF file
            - values are dynamically updated in each for-loop        
        """
        self.rec_line : str = "\t".join(record_values)
        self.record_values : List[str] = record_values # values of chrom
        self.record_keys : List[str] = record_keys # header 
        self.CHROM : str = self.record_values[0]
        self.POS : str = self.record_values[1]
        self.ID : str = self.record_values[2]
        self.REF : str = self.record_values[3] # 'G'
        self.ALT : List[str] = self.record_values[4].split(",") # ['A', 'C']
        self.ref_alt : List[str] = self.REF.split(",") + self.ALT # ['G', 'A', 'C']
        self.QUAL : str = self.record_values[5]
        self.FILTER : List[str] = self.record_values[6].split(",")
        self.info_str : str = self.record_values[7]
        
        
        # PUT this code to another function and don't do heavy taks in the __init__() method
        
        self.samples_state : bool = True
        try :
            self.format_ : List[str] = self.record_values[8].split(":")
            self.sample_names : Union[List[str], None] = self.record_keys[9:] if len(self.record_keys) > 9 else None
        except IndexError:
            self.samples_state = False

        try:
            self.sample_vals : List[str] = self.record_values[9:]
        except IndexError:
            warnings.warn(
                "Sample values are not presented correctly in given vcf file."
            )
            
            
            
        # """
        #     After analyzing the complexity stat of vcfparser and cyvcf2, I saw that vcfparser is calling "_map_format_tags_to_sample_values()" 
        #     each time while constructing the Record class instance. The value returned by this method is not used in the constructor 
        #     so I decided to strip this computational heavy code from the constructor and now users need to explicitly call this method when they need the samples' values. 
        #     By doing this we remove the overhead of calling this method while creating each record instance and gain an improvement in the performance of over 50%.
        # """
        self.mapped_format_to_sample : Union[Dict[str, Dict[str, str]], None] = None
        # if self.samples_state : self.mapped_format_to_sample = dict(zip(self.sample_names, [dict(zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")) for i, name in enumerate(self.sample_names)]))
        # if self.samples_state : self.mapped_format_to_sample = self._map_format_tags_to_sample_values()
        
        

        # instance attributes to get genotype and allele level information
        self.genotype_property : GenotypeProperty = GenotypeProperty(self)
        # self.allele_property = AlleleProperty(self)


    def __str__(self):
        return str(self.rec_line)



# This function should be looked after as it is much slower than other and bottleneck lies here
    def map_format_tags_to_sample_values(self) -> Union[Dict[str, Dict[str, str]], None]:
        """
        Method to map format tags to sample values of Record Objects

        Returns
        -------
        dict 
            dict of samples with their associate format mapped with their value
        
        Examples
        --------
        >>> import vcfparser.vcf_parser as vcfparse
        >>> myvcf = vcfparse.VcfParser("input_test.vcf") 
        >>> records = myvcf.parse_records()
        >>> record = next(records)
        >>> mapped = record.map_format_tags_to_sample_values()
        >>> print(mapped)
        {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
        >>> print(mapped.mapped_format_to_sample)
        {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}


        """
        # mapped_data = {}
        # for i, name in enumerate(self.sample_names):
        #     mapped_data[name] = dict(
        #         zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")
        #     )
        # return mapped_data
        if self.samples_state :
            self.mapped_format_to_sample = dict(zip(self.sample_names, [dict(zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")) for i, name in enumerate(self.sample_names)]))
            return self.mapped_format_to_sample
        else :
            return None

    # TODO (Bhuwan) Done - if required this should be a lazy method too. 
    def get_format_to_sample_map(self, sample_names: List[str]=None, formats: List[str]=None, convert_to_iupac: List[str]=None) -> Dict[str, Dict[str, str]]:
        """

        Parameters
        ----------
        sample_names : list
            list of sample names that needs to be processed (default = all samples are processed)
            
        formats : list
            list of format tags that needs to be processed (default = all format tags are processed)

        convert_to_iupac : list
            list of tags (from FORMAT) that needs to be converted into iupac bases (default tag = 'GT', default output = numeric bases)


        Returns
        -------
        dict
            dict of filtered sample names along with filtered format "tags:values"

        Uses
        ----
            _to_iupac(ref_alt : List[str], numeric_genotype : str, bases : str ="numeric") -> str function for iupac conversion

        Examples
        --------
        >>> import vcfparser.vcf_parser as vcfparse
        >>> myvcf = vcfparse.VcfParser("input_test.vcf")
        >>> records = myvcf.parser_records()
        >>> record = next(records)
        >>> record.map_format_tags_to_sample_values()
        {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
        >>> record.get_format_to_smaple_map(samples_names = ['ms01e', 'MA611'], formats = ['GT', 'PC']) # you 'll only get GT and PI values
        {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}} 
        >>> record.ref_alt
        ['G', 'A', 'C']
        >>> record.get_format_to_smaple_map(samples_names = ['ms01e', 'MA611'], formats = ['GT', 'PC', 'PI'], convert_to_iupac = ['GT', 'PI'])
        {'ms01e': {'GT': './.','PI': '.', 'PC': '.', 'GT_iupac': './.', 'PI_iupac': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.', 'GT_iupac': 'G/G', 'PI_iupac': '.'}}

        """
        sample_names : List[str] = sample_names if sample_names else self.sample_names
        required_format : List[str] = formats if formats else self.format_


        # filetered sample format contains the new value just like record.mapped_format_to_sample but filtered version of it.
        filtered_sample_format : Dict[str, Dict[str, str]] = {
            sample: dict(
                (fmt, self.mapped_format_to_sample[sample][fmt]) for fmt in required_format
            )
            for sample in sample_names
        }

        # if no need to convert to iupac format then simply return those filtered sample format.
        if convert_to_iupac is None:
            return filtered_sample_format

        else:
            # update the genotype values for the tags requested in "iupac" format
            multi_genotype_as_iupac_bases : Dict[str, Dict[str, str]] = {}
            genotype_output_format : str = "iupac"

            # for genotype_tag in ['GT', 'PG']:
            # let go for 'GT'
            for genotype_tag in convert_to_iupac:
                # if genotype_output_format == "iupac":
                try:
                    # convert the genotype from numeric to iupac format
                    # This block of code will run for each sample for particular vlaue of genotype_tag. For instance say 'GT'
                    sample_genotype_as_iupac : Dict[str, Dict[str, str]] = {
                        sample: {
                            genotype_tag + "_iupac" : # 'ms010': { 'GT_iupac' : } 
                                self._to_iupac(  # -> it takes .ref value for that chrom, mse102 sample ko 'GT' ko vlaue and will loop for every sample and genotype format, 
                                self.ref_alt,    # output format i.e. "iupac"
                                self.mapped_format_to_sample[sample][genotype_tag],
                                genotype_output_format,
                            )
                        }
                        for sample in sample_names
                    }

                    if len(multi_genotype_as_iupac_bases) == 0:
                        multi_genotype_as_iupac_bases.update(
                            sample_genotype_as_iupac
                        )
                    else:
                        {
                            multi_genotype_as_iupac_bases[ks].update(
                                sample_genotype_as_iupac[ks]
                            )
                            for ks, vs in sample_genotype_as_iupac.items()
                        }

                except KeyError:
                    warnings.warn(
                        'The format tag "%s" is not available in one or multiple VCF record. '
                        % genotype_tag
                    )
                    sys.exit(0)
                    # TODO (Bhuwan) Done - Why is object being returned even after warning is raised. 
                    # after warning the parsing on a forloop should stop? is this happening? 

            # update the mapped sample dictionary
            for ks, vals in multi_genotype_as_iupac_bases.items():
                filtered_sample_format[ks].update(vals)

            return filtered_sample_format

 
    @staticmethod
    # def split_tag_from_samples(order_mapped_samples, tag, sample_names):
    def get_tag_values_from_samples(order_mapped_samples : OrderedDict, tag : str, sample_names : list, split_at : str =None) -> Union[List[str], List[List[str]]]:

        """ Splits the tags of given samples from order_dict of mapped_samples

        Parameters
        ----------
        order_mapped_samples : OrderedDict
            Ordered dictionary of FORMAT tags mapped to SAMPLE values.
        tag : str
            One of the FORMAT tag.
        sample_names : list
            Name of the samples to extract the values from.
        split_at : str
            Character to split the value string at. e.g "|", "/", "," etc.

        Returns
        -------
        list of list
            List of list containing SAMPLE value for the FORMAT tag

        Uses
        ----
            _to_iupac(ref_alt : List[str], numeric_genotype : str, bases : str ="numeric") -> str function for iupac conversion

        Examples
        --------
        >>> order_mapped_samples = OrderedDict([('ms01e',{'GT': './.', 'PI': '.'}), ('MA622', {'GT': '0/0','PI': '.'})])
        >>> tag = 'GT'
        >>> sample_names = ['ms01e', 'MA622']
        >>> record.get_tag_values_from_samples(order_mapped_samples, tag, sample_names)
        [['./.'], ['0/0']]
        ['./.', '0/0']
        >>> # using "/|"  # to split at GT values at both | and / 
        >>> get_tag_values_from_samples(order_mapped_samples, tag, sample_names, split_at= "/|")
        [['.', '.'], ['0', '0']]

        """
        # gt_vals = [order_mapped_samples[sample][tag] for sample in sample_names]
        # tag_vals = [re.split(r"[/|]", gt_val) for gt_val in gt_vals]
        # return tag_vals

        format_tag_values : List[str] = [order_mapped_samples[sample][tag] for sample in sample_names] # = ['./.', '0/0']
        
        if split_at is not None:
            # tag_vals = [re.split(r"[/|]", gt_val) for gt_val in format_tag_values]
            splitted_tag_vals : List[List[str]] = [re.split(r"[/|]", value) for value in format_tag_values] # = [['.', '.'], ['0', '0']]
            return splitted_tag_vals
        return format_tag_values
        
    def get_mapped_tag_list(self, sample_names : List[str]=None, tag : str=None, bases="numeric") -> List[str]:
        """
        To get list of sample's particular tag value with an option of iupac conversion

        Parameters
        ----------
        samples_names : List
            List of sample names whose tag value is needed
        tag : str
            One of the FORMAT tag whose correspoding value needs to be converted to iupac
        bases : str
            Conversion scheme for iupac
        
        Returns
        -------
        list
            List containing iupac converted FORMAT tag value for each sample in samples_name

        Uses
        ----
            _to_iupac(ref_alt : List[str], numeric_genotype : str, bases : str ="numeric") -> str function for iupac conversion
        
        Examples
        --------
        >>> record.map_format_tags_to_sample_values()
        {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
        >>> record.ref_alt
        ['G', 'A', 'C']
        >>> record.get_mapped_tag_list(['MA622', 'MA611'], 'GT', "other")
        ['G/G', 'G/G']
        >>> record.get_mapped_tag_list(['MA622', 'MA611'], 'GT', "numeric")
        ['0/0', '0/0']
        """
        mapped_list : List[str] = [
            self._to_iupac(self.ref_alt, self.mapped_format_to_sample[sample][tag], bases)
            for sample in sample_names 
        ] 
        return mapped_list




    @staticmethod
    # if input is ref_alt = ['G', 'T'] and numeric_genotype = "0/1" or "1/1" any other
    # for fist chrom of input_test.vcf ref_alt = ['G', 'A', 'C']
    # output will be 
    def _to_iupac(ref_alt : List[str], numeric_genotype : str, bases : str ="numeric") -> str:
        """
        Convert tag value to iupac bases

        Parameters
        ----------
        ref_alt : list
            List containing REF and ALT values
        numeric_genotype : str
            numeric vlaue of genotype e.g. "0/1"
        bases : str
            conversion base for iupac

        Returns
        -------
        str
            Converted version of iupac e.g. "0/1" --> "G/T" or "0/1"

        Examples
        --------
        >>> _to_iupac(['G', 'A', 'C'], "0/1", "other")
        "G/A"

        """
        if bases == "numeric":
            return numeric_genotype
        # if numeric_genotype == ".":
        #     return numeric_genotype

        numeric_g_list : List[str] = re.split(r"[/|]", numeric_genotype) # = ['0', '1']
        sep : str = "/" if "/" in numeric_genotype else "|"
        iupac_vals : List[str] = [ref_alt[int(i)] if i != "." else "." for i in numeric_g_list] # = ['G', 'T']
        return sep.join(iupac_vals) # = "G/T"
    
    

    @staticmethod
    def split_genotype_tags():
        # TODO: BISHWA make a function to split the genotype tags 
        pass

    def get_info_as_dict(self, info_keys : List[str]=None) -> Dict[str, str]:
        """
        Convert Info to dict for required keys

        Parameters
        ----------
        info_keys: list
            Keys of interest (default = all keys will be mapped)

        Returns
        -------
        dict
            key: value pair of only required keys 

        Notes
        -----
        If '=' isn't present then it will return its value as '.'.

        Examples
        --------
        >>> info_str = 'AC=2,0;AF=1.00;AN=8;BaseQRankSum'
        >>> info_keys= ['AC', 'BaseQRankSum']
        >>> record.get_info_as_dict(info_keys)
        {'AC': '2,0', 'BaseQRankSum': '-7.710e-01'} 

        """
        mapped_info : Dict[str, str] = dict(
            s.split("=", 1) if "=" in s else (s, ".") for s in self.info_str.split(";")
        )       # = {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '.'}
        
        if isinstance(info_keys, list):
            # convert list to set for faster lookup
            info_keys_set : Set[str] = set(info_keys)
            return {
                key: value
                for key, value in mapped_info.items()
                if key in info_keys_set
            } # = {'AC': '2,0', 'BaseQRankSum': '.'}
        else:
            return mapped_info

    def get_full_record_map(self, convert_to_iupac : List[str]=None) -> Dict[str, str]:
    
        """ Maps record values with record keys.

        Parameters
        ----------
        convert_to_iupac: list
            list of genotpye tags that needs to be converted into iupac bases (default tag = 'GT', default output = numeric bases)

        Returns
        -------
        dict
            dict with key value pair with sample and infos modified

        Uses
        ----
            get_info_as_dict() and get_format_to_sample_map(convert_to_iupac : List[str]) function in the process

        TODO: Done (Gopal) Add example input and output 

        Examples
        --------
        >>> record.get_full_record_map()
        {'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'}}}
        
        """
        mapped_records : Dict[str, str] = dict(zip(self.record_keys, self.record_values)) # = { "CHROM" : "2", "POS": "89834", "POS": '.', ...}
        mapped_records["INFO"] = self.get_info_as_dict() # it is overridden 
        mapped_records["samples"] = self.get_format_to_sample_map(convert_to_iupac= convert_to_iupac) # it is added as new key, value in dict
        return mapped_records

    def unmap_fmt_samples_dict(self, mapped_dict : Dict) -> Tuple[str, str]:
        """ 
        Converts mapped dict again into string to write into the file.

        Parameters
        ----------
        mapped_dict : dict
            Dict of Dict with sample mapped with their format and format's value
        
        Returns
        -------
        str
            format string of genotype tag value
        str
            each sample's values concatenated

        Examples
        --------

        >>> mapped_dict = mapped_dict = {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '0/0'}}
        >>> record.unmap_fmt_samples_dict(mapped_dict)
        >>> ('GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', './.:.:.:./.:.:./.:...      ./.:.:.:./.:.:./.:..0/0')
        """

        sample_str_all : str = ""
        for sample in self.sample_names:    # mapped_dict = {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, ...}}
            # TODO make format compute only once
            format_str : str = ":".join(key for key in mapped_dict[sample]) # = 'GT:PI:GQ:PG:PM:PW:...'
            sample_str : str = ":".join(val for val in mapped_dict[sample].values()) # = './.:.:.:./.:.:./.:...'
            sample_str_all.join(sample_str + "\t")  # = './.:.:.:./.:.:./.:...      ./.:.:.:./.:.:./.:...       ./.:.:.:./.:.:./.:... '

        return format_str, sample_str_all

    ## TODO: Done Revert mapped record into record string
    def mapped_rec_to_str(self, mapped_sample_dict : Dict[str, Dict[str, str]]) -> str:
        """
        Convert information in Object field of Record into string to make VCF file

        Parameters
        ----------
        mapped_sample_dict : dict
            Dict of Dict with sample mapped with their format and format's value
        
        Returns
        -------
        str
            Complete line of VCF file for particular CHROM's position

        Uses
        ----
            unmap_fmt_samples_dict(mapped_sample_dict: Dict[str, Dict[str, str]]) to get format and sample values

        Examples
        --------
        >>> mapped_dict = mapped_dict = {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '0/0'}}
        >>> record.mapped_rec_to_str(mapped_dict)
        2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:...      ./.:.:.:./.:.:./.:..0/0
        
        --------
        """
        record_val_upto_info : List[str] = self.record_values[:8] 
        record_str : str = ''
        str_up_to_info : str = '\t'.join(record_val_upto_info)
        format_str, sample_str_all = self.unmap_fmt_samples_dict(mapped_sample_dict)
        record_str = str_up_to_info+ '\t' +format_str + '\t'+ sample_str_all
        return record_str 


    # TODO: functions to add later Done
    def iupac_to_numeric(self, ref_alt : List[str], genotype_in_iupac) -> str:
        # input parameters should be ref_alt, iupac_bases = []
        # returns: list of numeric bases 
        # required for buildVCF ??
        # For ref_alt = ['G', 'A', 'C']
        # genotype_in_iupac = 'G/A' it should return '0/1'
        """
        Convert tag value to iupac bases

        Parameters
        ----------
        ref_alt : list
            List containing REF and ALT values
        genotype_in_iupac : str
            iupac vlaue of genotype e.g. "G/A"

        Returns
        -------
        str
            Converted version of iupac to numeric e.g. "G/A" --> "0/1"

        Examples
        --------
        >>> iupac_to_numeric(['G', 'A', 'C'], "G/A",)
        "0/1"
        """

        iupac_g_list : List[str] = re.split(r"[/|]", genotype_in_iupac) # = ['G', 'A']
        sep = "/" if "/" in genotype_in_iupac else "|"
        numeric_vals = [ref_alt.index(i) if i != "." else "." for i in iupac_g_list] # = ['0', '1']
        return sep.join(numeric_vals) # = "0/1"

    def deletion_overlapping_variant(self):
        # TODO
        pass

class GenotypeProperty:
    '''
    Class for parsing the property of the genotype.
    e.g: if the genotype is a SNP, InDel, Homozygous Variant (HomVAR) etc.
    Following would be considered a property of a particular genotype:
    SNP, InDel (Insertion, Deletion), HomRef, HomVar, HetVar, Missing, etc.


    '''
    ########################################################################
    #### parsing of genotype property begins ####
    # allele_obj = self.Alleles(self.mapped_format_to_sample, tag)

    # def _allele_obj(self):
    #     allele_obj = Alleles(self.mapped_format_to_sample, tag='GT')
    #     return allele_obj

    # allele_obj = _allele_obj


    def __init__(self, record_obj : Record):
        self.record_obj : Record = record_obj
        # pass

    # TODO (Bishwa) all this genotype parsing should be kept as a separate class ?
    # @property
    def isHOMREF(self, tag : str ="GT", bases : str ="numeric") -> Dict[str, str] :
        """
        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having homoref

        Uses
        ----
            Alleles class to create it's object
            _to_iupac(...) function to convert ----- to iupac format

        Examples
        --------
        >>> rec_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
        >>> rec_values = ['2', '15881018', '.', 'G', 'A,C', '5082.45', 'PASS', 'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs', 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.']
        >>> from vcfparser.record_parser import Record
        >>> rec_obj = Record(rec_values, rec_keys)
        >>> rec_obj.isHOMREF(tag="GT", bases="iupac")
        {'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}  

        """
        # homref_samples = []
        # tag_vals = self.get_tag_values_from_samples(
        #     self.mapped_format_to_sample, tag, self.sample_names, split_at="|/"
        # )
        # for i, tag_val in enumerate(tag_vals):
        #     if set(tag_val) == {"0"}:
        #         homref_samples.append(self.sample_names[i])
        # allele_obj = Alleles(self.mapped_format_to_sample,tag)
        allele_obj : Alleles = Alleles(self.record_obj.mapped_format_to_sample,tag)

        # allele_obj = 
        homref_samples : List[str] = allele_obj.hom_ref_samples
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in homref_samples
        }


    def isHOMVAR(self, tag : str ="GT", bases : str ="numeric") -> Dict[str, str]:
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having homoref

        Uses
        ----
            Alleles class to create it's object
            _to_iupac(...) function to convert ----- to iupac format

        Examples
        --------
        >>> record.isHOMVAR(tag="GT", bases="iupac")
        {'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': 'A/A', 'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}
        
        """
        # homvar_samples = []
        # tag_vals = self.get_tag_values_from_samples(
        #     self.mapped_format_to_sample, tag, self.sample_names, split_at="|/"
        # )
        # for i, tag_val in enumerate(tag_vals):
        #     if (
        #         len(set(tag_val)) == 1
        #         and set(tag_val) != {"0"}
        #         and set(tag_val) != {"."}
        #     ):
        #         homvar_samples.append(self.sample_names[i])
        allele_obj : Alleles = Alleles(self.record_obj.mapped_format_to_sample,tag)
        homvar_samples : List[str] = allele_obj.hom_var_samples

        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in homvar_samples
        }

    def isHETVAR(self, tag : str ="GT", bases : str ="numeric") -> Dict[str, str]:
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having homoref

        Uses
        ----
            Alleles class to create it's object
            _to_iupac(...) function to convert ----- to iupac format

        Examples
        --------
        >>> record.isHETVAR(tag="GT", bases="numeric")
        {}
        
        """
        

        # hetvar_samples = []
        # tag_vals = self.get_tag_values_from_samples(
        #     self.mapped_format_to_sample, tag, self.sample_names, split_at= "|/"
        # )
        # for i, tag_val in enumerate(tag_vals):
        #     if len(set(tag_val)) > 1:
        #         hetvar_samples.append(self.sample_names[i])
        allele_obj : Alleles = Alleles(self.record_obj.mapped_format_to_sample,tag)
        hetvar_samples : List[str] = allele_obj.het_var_samples

        #TODO: only do this dict comprehension if bases = 'iupac'
        # apply this method on other similar functions
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in hetvar_samples
        }

    # TODO: illustrate that it can be use for any FORMAT tags, not just "GT"
    def isMissing(self, tag : str ="GT") -> Dict[str, str]:
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')

        Returns
        -------
         dict
            dict of sample with values having homoref

        Uses
        ----
            Alleles class to create it's object

        Examples
        --------
        >>> record.isMissing(tag='PI') 
        {'ms01e': '.', 'ms02g': '.', 'ms03g': '.', 'ms04h': '.', 'MA611': '.', 'MA605': '.', 'MA622': '.'}
        
        """

        # missing_tag_sample = []
        # tag_vals = self.get_tag_values_from_samples(
        #     self.mapped_format_to_sample, tag, self.sample_names, split_at= "|/"
        # )
        # for i, tag_val in enumerate(tag_vals):
        #     if set(tag_val) == {"."}:
        #         missing_tag_sample.append(self.sample_names[i])
        allele_obj : Alleles = Alleles(self.record_obj.mapped_format_to_sample,tag)
        missing_tag_sample : List[str] = allele_obj.missing_samples
        return {
            sample: self.record_obj.mapped_format_to_sample[sample][tag] for sample in missing_tag_sample
        }

    # TODO: may be 'tag' and 'bases' flag is not required
    def hasSNP(self, tag : str ="GT", bases : str ="numeric") -> bool:
        # TODO (Bhuwa, Bishwa, high priority) - may need to add a tag="GT" option
        # **Note: this needs to be implemented properly
        # The length of the REF and ALT both needs to be just 1.
        if len(self.record_obj.REF) == 1:
            return True

    def hasINDEL(self) -> bool:
        # TODO Bishwa : need to implement properly

        if len(self.record_obj.REF) > 1:
            return True

    def hasAllele(self, allele : str ="0", tag : str ="GT", bases : str ="numeric") -> Dict[str, str]:
        """

        Parameters
        ----------
        allele : str
            allele to check if it is present in given samples(default = '0')
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having given allele

        Uses
        ----
            _to_iupac(...) function to convert ----- to iupac format

        Example
        -------
        >>> record.hasAllele(allele='0', tag='GT', bases='numeric')
        {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
        
        """

        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in self.record_obj.sample_names
            if allele in self.record_obj.mapped_format_to_sample[sample][tag]
        }

    # TODO: make it compatible with polyploid genotype 
    def hasVAR(self, genotype : str ="0/0", tag : str ="GT", bases : str ="numeric") -> Dict[str, str]:
        """

        Parameters
        ----------
        genotype : str
            genotype to check if it is present in given samples(default = '0/0')
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having given genotype

        Uses
        ----
            _to_iupac(...) function to convert ----- to iupac format

        Example
        -------
        >>> record.hasVAR(genotype='0/0') 
        
        {'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}
        """
        # TODO: The return could be shortened
        # only do comprehension if bases = 'iupac'
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in self.record_obj.sample_names
            if (
                genotype
                in self.record_obj._to_iupac(
                    self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases="numeric"
                )
            )
            or (
                genotype
                in self.record_obj._to_iupac(
                    self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases="iupac"
                )
            )
        }

    # TODO (future): make it compatible with polyploid genotype
    def hasnoVAR(self, tag : str ="GT") -> Union[Dict[str, str], None]:
        """ Returns samples with empty genotype """

        return {
            sample: self.record_obj.mapped_format_to_sample[sample][tag]
            for sample in self.record_obj.sample_names
            if self.record_obj.mapped_format_to_sample[sample][tag] in (".", "./.", ".|.")
        }

    def has_unphased(self, tag : str ="GT", bases : str ="numeric") -> Union[Dict[str, str], None]:
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
         dict
            dict of sample with values having '/' in samples formats

        Uses
        ----
            Alleles class to create it's object
            _to_iupac(...) function to convert ----- to iupac format

        Examples
        --------
        >>> rec_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
        >>> rec_values = ['2', '15881018', '.', 'G', 'A,C', '5082.45', 'PASS', 'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs', 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.']
        >>> from vcfparser.record_parser import Record
        >>> rec_obj = Record(rec_values, rec_keys)
        >>> rec_obj.has_unphased(tag="GT", bases="iupac")
        {'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': 'A/A', 'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}


        """
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in self.record_obj.sample_names
            if "/" in self.record_obj.mapped_format_to_sample[sample][tag]
        }

    def has_phased(self, tag : str="GT", bases : str="numeric") -> Dict[str, str]:
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')
        bases: str
            iupac or numeric (default = 'numeric')

        Returns
        -------
        dict
            dict of sample with values having '/' in samples formats

        Uses
        ----
            Alleles class to create it's object
            _to_iupac(...) function to convert ----- to iupac format

        Examples
        --------

        >>> rec_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
        >>> rec_values = ['2', '15881018', '.', 'G', 'A,C', '5082.45', 'PASS', 'AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs', 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.']
        >>> from vcfpaser.record_parser import Record
        >>> rec_obj = Record(rec_values, rec_keys)
        >>> rec_obj.has_phased(tag="GT", bases="iupac")
        {}

        """

        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in self.record_obj.sample_names
            if "|" in self.record_obj.mapped_format_to_sample[sample][tag]
        }


    # TODO: Bishwa (Priority high)
    # Make sure all the genotype parsing methods are compatible with non diploid genomes 





allele_delimiter = re.compile(r'''[|/]''')
# allele_obj = Alleles(mapped_format_to_sample,tag)
## ASK: If this needs to be named allele or genotype
class Alleles: # TODO : Rename to something like GenotypeProperty?
    def __init__(self,mapped_samples, tag= 'GT'): # TODO - may be add another flag #### => mapped_samples = {{'ms01e',{'GT': './.', 'PI': '.'}}, {'MA622', {'GT': '0/0','PI': '.'}}, ... }
        """
        This class is used to store sample names with their types.
        """
        self.hom_ref_samples : List[str] = []
        self.hom_var_samples : List[str] = []
        self.het_var_samples : List[str] = []
        self.missing_samples : List[str] = []
        self.phased_samples  : List[str] = [] # TODO - this probably is a duplicate method? fix it?

        # TODO: add new genotype property checks?
        # is_SNP, is_INDEL, is_SV, etc. 

        # REF = self.REF



        for sample in mapped_samples.keys():      #     => mapped_samples = {{'ms01e',{'GT': './.', 'PI': '.'}}, {'MA622', {'GT': '0/0','PI': '.'}}, ... }
            tag_val : str = mapped_samples.get(sample, {}).get(tag, None) # => tag_val will get value of GT key's value for samples "samples" in mapped_samples. eg for samples = "ms01e" and tag = 'GT' you'll get './.'
            if tag_val is not None:
                genotype_val : GenotypeVal = GenotypeVal(tag_val)
                if genotype_val.phased: # => means | is sep
                    self.phased_samples.append(sample)
                if genotype_val._ismissing:  # => means . is value "./." or "."
                    self.missing_samples.append(sample)
                if genotype_val.gt_type == 'hom_ref':  
                    self.hom_ref_samples.append(sample)
                elif genotype_val.gt_type == 'hom_var':
                    self.hom_var_samples.append(sample)
                elif genotype_val.gt_type == 'het_var':
                    self.het_var_samples.append(sample)
                else:
                    pass
            else:
                warnings.warn(f'{sample} has no mapped value for {tag} tag')
        

        def homref_samples(self):
            pass

## ASK: What to do if following scenario arises?
## Are they homref, hetvar './.' , '.', './0', '0/.'

class GenotypeVal:
    def __init__(self,allele : str):
        """"
        For a given genotype data like ('0/0', '1|1', '0/1'); this class computes and store values
        like whether it is homref, hom_alt or hetvar
        """
        # TODO: add new genotype property checks?
        # is_SNP, is_INDEL, is_SV, etc. 

        # here gt_type store either homvar, hetvar, or homref

        self.gt_type : str = None
        self.phased : bool = False
        self._alleles : List[str] = [(al if al != '.' else None) for al in allele_delimiter.split(allele)]
        self._ismissing : bool = not any(al is not None for al in self._alleles)
        if '|' in allele:
            self.phased = True

        # hetvar 
        alleles_list : List[str] = self._alleles
        if not self._ismissing:
            if len(set(alleles_list)) == 1:
                if alleles_list[0] == '0':
                    self.gt_type = 'hom_ref'
                else:
                    self.gt_type = 'hom_var'
            else:
                self.gt_type = 'het_var'
        else:
            self.gt_type = 'missing'