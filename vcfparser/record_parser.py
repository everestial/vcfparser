# import re
# from collections import OrderedDict
# from itertools import zip_longest


# class Record:
#     """
#     A class for to store and extract the data lines in the vcf file.
#     """

#     def __init__(self, line, header_line):
#         """
#         Initializes the class with record lines and header lines.

#         Parameters
#         ----------
#         line: str
#             tab separated data lines (records) lines below # CHROM in vcf file
#         header_line: str
#             a line in vcf starting with # CHROM
#         """
#         self.rec_line = line
#         self.record_vals = self.rec_line.strip("\n").split("\t")
#         self.record_keys = header_line.split("\t")
#         self.CHROM = self.record_vals[0]
#         self.POS = self.record_vals[1]
#         self.ID = self.record_vals[2]
#         self.REF = self.record_vals[3]
#         self.ALT = self.record_vals[4]
#         self.ref_alt = self.REF.split(",") + self.ALT.split(",")
#         self.QUAL = self.record_vals[5]
#         self.FILTER = self.record_vals[6].split(",")

#         self.info_str = self.record_vals[7]
#         self.format_ = self.record_vals[8].split(":")
#         self.sample_names = self.record_keys[9:] if len(self.record_keys) > 9 else None
#         self.sample_vals = self.record_vals[9:]
#         self.mapped_sample = self._map_fmt_to_samples()

#     def __str__(self):
#         return str(self.rec_line)

#     @staticmethod
#     def split_tag_from_samples(order_mapped_samples, tag, sample_names):
#         """ Splits the tags of given samples from order_dict of mapped_samples

#         Parameters
#         ----------
#         order_mapped_samples : OrderedDict
#         tag: str
#         sample_names: list

#         Returns
#         -------
#         list of list
#             list of list containing splitted tags

#         Examples
#         --------
#         >>> order_mapped_samples = OrderedDict([('ms01e',{'GT': './.', 'PI': '.'), ('MA622', 'GT': '0/0','PI': '.'})])
#         >>> tag = 'GT'
#         >>> sample_names = ['ms01e', 'MA622']
#         >>> split_tag_from_samples(order_mapped_samples, tag, sample_names)
#         [['.', '.'], ['0', '0']]

#         """

#         gt_vals = [order_mapped_samples[sample][tag] for sample in sample_names]
#         tag_vals = [re.split(r"[/|]", gt_val) for gt_val in gt_vals]
#         return tag_vals

#     def isHOMREF(self, tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having homoref

#         Examples
#         --------
#         >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

#         >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
#         >>> from record_parser import Record
#         >>> rec_obj = Record(rec_valeg, rec_keys_eg)
#         >>> rec_obj.isHOMREF(tag="GT", bases="iupac")
#         {'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}

#         """
#         homref_samples = []
#         tag_vals = self.split_tag_from_samples(
#             self.mapped_sample, tag, self.sample_names
#         )
#         for i, tag_val in enumerate(tag_vals):
#             if set(tag_val) == {"0"}:
#                 homref_samples.append(self.sample_names[i])
#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in homref_samples
#         }

#     def isHOMVAR(self, tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having homoref

#         """
#         homvar_samples = []
#         tag_vals = self.split_tag_from_samples(
#             self.mapped_sample, tag, self.sample_names
#         )
#         for i, tag_val in enumerate(tag_vals):
#             if (
#                 len(set(tag_val)) == 1
#                 and set(tag_val) != {"0"}
#                 and set(tag_val) != {"."}
#             ):
#                 homvar_samples.append(self.sample_names[i])
#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in homvar_samples
#         }

#     def isHETVAR(self, tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having homoref

#         """

#         hetvar_samples = []
#         tag_vals = self.split_tag_from_samples(
#             self.mapped_sample, tag, self.sample_names
#         )
#         for i, tag_val in enumerate(tag_vals):
#             if len(set(tag_val)) > 1:
#                 hetvar_samples.append(self.sample_names[i])
#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in hetvar_samples
#         }

#     def isMissing(self, tag="GT"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')

#         Returns
#         -------
#          dict
#             dict of sample with values having homoref

#         """

#         missing_tag_sample = []
#         tag_vals = self.split_tag_from_samples(
#             self.mapped_sample, tag, self.sample_names
#         )
#         for i, tag_val in enumerate(tag_vals):
#             if set(tag_val) == {"."}:
#                 missing_tag_sample.append(self.sample_names[i])
#         return {
#             sample: self.mapped_sample[sample][tag] for sample in missing_tag_sample
#         }

#     def hasSNP(self):
#         # TODO : need to implement
#         if len(self.REF) == 1:
#             return True

#     def hasINDEL(self):
#         # TODO : need to implement

#         if len(self.REF) > 1:
#             return True

#     def hasAllele(self, allele="0", tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         allele : str
#             allele to check if it is present in given samples(default = '0')
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having given allele

#         """

#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in self.sample_names
#             if allele in self.mapped_sample[sample][tag]
#         }

#     def hasVAR(self, genotype="0/0", tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         genotype : str
#             genotype to check if it is present in given samples(default = '0/0')
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having given genotype

#         """

#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in self.sample_names
#             if genotype
#             in self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#         }

#     def hasnoVAR(self, tag="GT"):
#         """ Returns samples with empty genotype """

#         return {
#             sample: self.mapped_sample[sample][tag]
#             for sample in self.sample_names
#             if self.mapped_sample[sample][tag] in (".", "./.", ".|.")
#         }

#     def has_unphased(self, tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#          dict
#             dict of sample with values having '/' in samples formats

#         Examples
#         --------

#         >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

#         >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
#         >>> from record_parser import Record
#         >>> rec_obj = Record(rec_valeg, rec_keys_eg)
#         >>> rec_obj.has_unphased(tag="GT", bases="iupac")
#         {'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}


#         """
#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in self.sample_names
#             if "/" in self.mapped_sample[sample][tag]
#         }

#     def has_phased(self, tag="GT", bases="numeric"):
#         """

#         Parameters
#         ----------
#         tag: str
#             format tags of interest (default = 'GT')
#         bases: str
#             iupac or numeric (default = 'numeric')

#         Returns
#         -------
#         dict
#             dict of sample with values having '/' in samples formats

#         Examples
#         --------

#         >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

#         >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
#         >>> from record_parser import Record
#         >>> rec_obj = Record(rec_valeg, rec_keys_eg)
#         >>> rec_obj.has_phased(tag="GT", bases="iupac")
#         {}

#         """

#         return {
#             sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in self.sample_names
#             if "|" in self.mapped_sample[sample][tag]
#         }

#     def _map_fmt_to_samples(self):

#         """Private method to map samples with format"""

#         mapped_sample_fmt = OrderedDict()
#         for i, name in enumerate(self.sample_names):
#             mapped_sample_fmt[name] = dict(
#                 zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")
#             )
#         return mapped_sample_fmt

#     def get_mapped_samples(self, sample_names=None, formats=None, bases="numeric"):
#         """

#         Parameters
#         ----------
#         sample_names : list
#             list of sample names that needs to be filtered (default = all samples will be filtered)

#         formats : list
#             list of format tags that needs to be filtered (default = all formats will be filtered)

#         Returns
#         -------
#         dict
#             dict of filtered sample names along with filtered formats

#         Examples
#         --------

#         >>> mapped_sample = {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
#         >>> get_mapped_samples(self, sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'])
#         {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}}

#         """
#         sample_names = sample_names if sample_names else self.sample_names
#         required_format = formats if formats else self.format_
#         # return {
#         #     sample: dict(
#         #         (fmt, self.mapped_sample[sample][fmt]) for fmt in required_format
#         #     )
#         #     for sample in sample_names
#         # }
#         return {
#             sample: dict(
#                 (
#                     fmt,
#                     self._to_iupac(
#                         self.ref_alt, self.mapped_sample[sample][fmt], bases
#                     ),
#                 )
#                 for fmt in required_format
#             )
#             for sample in sample_names
#         }

#     def get_mapped_tag_list(self, sample_names=None, tag=None, bases="numeric"):
#         mapped_list = [
#             self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
#             for sample in sample_names
#         ]
#         return mapped_list

#     def unmap_fmt_samples_dict(self, mapped_dict):
#         """ Converts mapped dict again into string to write into the file.
#         """

#         sample_str_all = ""
#         for sample in self.sample_names:
#             # TODO make format compute only once
#             format_str = ":".join(key for key in mapped_dict[sample])
#             sample_str = ":".join(val for val in mapped_dict[sample].values())
#             sample_str_all.join(sample_str + "\t")

#         return format_str, sample_str_all

#     @staticmethod
#     def _to_iupac(ref_alt, numeric_genotype, bases="numeric"):
#         if bases == "numeric":
#             return numeric_genotype

#         numric_g_list = re.split(r"[/|]", numeric_genotype)
#         sep = "/" if "/" in numeric_genotype else "|"
#         iupac_vals = [ref_alt[int(i)] if i != "." else "." for i in numric_g_list]
#         return sep.join(iupac_vals)

#     def get_info_dict(self, required_keys=None):
#         """
#         Convert Info to dict for required keys

#         Parameters
#         ----------
#         required_keys: list
#             Keys of interest (default = all keys will be mapped)

#         Returns
#         -------
#         dict
#             key: value pair of only required keys

#         Notes
#         -----
#         If '=' isn't present then it will return its value as '.'.

#         Examples
#         --------
#         >>> info_str = 'AC=2,0;AF=1.00;AN=8;BaseQRankSum'
#         >>> required_keys= ['AC', 'BaseQRankSum']
#         >>> get_info_dict(self, required_keys)
#         {'AC':2, 'BaseQRankSum' : '.'}


#         """
#         mapped_info = dict(
#             s.split("=", 1) if "=" in s else (s, ".") for s in self.info_str.split(";")
#         )
#         if isinstance(required_keys, list):
#             # convert list to set for faster lookup
#             required_keys_set = set(required_keys)
#             return {
#                 key: value
#                 for key, value in mapped_info.items()
#                 if key in required_keys_set
#             }
#         else:
#             return mapped_info

#     def map_records_long(self):
#         """ Maps record values with record keys.

#         Returns
#         -------
#         dict
#             dict with key value pair with sample and infos modified
#         """
#         mapped_records = dict(zip(self.record_keys, self.record_vals))
#         mapped_records["INFO"] = self.get_info_dict()
#         mapped_records["samples"] = self.get_mapped_samples()
#         return mapped_records

#     # functions to add later
#     def iupac_to_numeric(self):
#         # TODO
#         pass

#     def deletion_overlapping_variant(self):
#         # TODO
#         pass

import re
import warnings
from collections import OrderedDict
from itertools import zip_longest
import sys


class Record:
    """
    A class for to store and extract the data lines in the vcf file.
    """

    def __init__(self, record_line, record_keys):
        """
        Initializes the class with record lines and header lines.

        Parameters
        ----------
        record_line: str
            tab separated data lines (records) lines below # CHROM in vcf file
        record_keys: list
            a line in vcf starting with # CHROM
        """
        self.rec_line = record_line
        self.record_vals = self.rec_line.strip("\n").split("\t")
        self.record_keys = record_keys
        self.CHROM = self.record_vals[0]
        self.POS = self.record_vals[1]
        self.ID = self.record_vals[2]
        self.REF = self.record_vals[3]
        self.ALT = self.record_vals[4]
        self.ref_alt = self.REF.split(",") + self.ALT.split(",")
        self.QUAL = self.record_vals[5]
        self.FILTER = self.record_vals[6].split(",")
        self.info_str = self.record_vals[7]
        self.format_ = self.record_vals[8].split(":")
        self.sample_names = self.record_keys[9:] if len(self.record_keys) > 9 else None

        try:
            self.sample_vals = self.record_vals[9:]
        except IndexError:
            warnings.warn(
                "Sample values are not presented correctly in given vcf file."
            )

        # TODO for this line
        # (Bhuwan, high priority): add error message (not exit)
        # that vcf lacks sample information or samples are represented not at right position

        self.mapped_sample = self._map_fmt_to_samples()

    def __str__(self):
        return str(self.rec_line)

    @staticmethod
    def split_tag_from_samples(order_mapped_samples, tag, sample_names):
        """ Splits the tags of given samples from order_dict of mapped_samples

        Parameters
        ----------
        order_mapped_samples : OrderedDict
        tag: str
        sample_names: list

        Returns
        -------
        list of list
            list of list containing splitted tags

        Examples
        --------
        >>> order_mapped_samples = OrderedDict([('ms01e',{'GT': './.', 'PI': '.'), ('MA622', 'GT': '0/0','PI': '.'})])
        >>> tag = 'GT'
        >>> sample_names = ['ms01e', 'MA622']
        >>> split_tag_from_samples(order_mapped_samples, tag, sample_names)
        [['.', '.'], ['0', '0']]

        """

        gt_vals = [order_mapped_samples[sample][tag] for sample in sample_names]
        tag_vals = [re.split(r"[/|]", gt_val) for gt_val in gt_vals]
        return tag_vals

    def isHOMREF(self, tag="GT", bases="numeric"):
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

        Examples
        --------
        >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

        >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
        >>> from record_parser import Record
        >>> rec_obj = Record(rec_valeg, rec_keys_eg)
        >>> rec_obj.isHOMREF(tag="GT", bases="iupac")
        {'MA611': 'G/G', 'MA605': 'G/G', 'MA622': 'G/G'}  
        
        """
        homref_samples = []
        tag_vals = self.split_tag_from_samples(
            self.mapped_sample, tag, self.sample_names
        )
        for i, tag_val in enumerate(tag_vals):
            if set(tag_val) == {"0"}:
                homref_samples.append(self.sample_names[i])
        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in homref_samples
        }

    def isHOMVAR(self, tag="GT", bases="numeric"):
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

        """
        homvar_samples = []
        tag_vals = self.split_tag_from_samples(
            self.mapped_sample, tag, self.sample_names
        )
        for i, tag_val in enumerate(tag_vals):
            if (
                len(set(tag_val)) == 1
                and set(tag_val) != {"0"}
                and set(tag_val) != {"."}
            ):
                homvar_samples.append(self.sample_names[i])
        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in homvar_samples
        }

    def isHETVAR(self, tag="GT", bases="numeric"):
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

        """

        hetvar_samples = []
        tag_vals = self.split_tag_from_samples(
            self.mapped_sample, tag, self.sample_names
        )
        for i, tag_val in enumerate(tag_vals):
            if len(set(tag_val)) > 1:
                hetvar_samples.append(self.sample_names[i])
        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in hetvar_samples
        }

    def isMissing(self, tag="GT"):
        """

        Parameters
        ----------
        tag: str
            format tags of interest (default = 'GT')

        Returns
        -------
         dict
            dict of sample with values having homoref

        """

        missing_tag_sample = []
        tag_vals = self.split_tag_from_samples(
            self.mapped_sample, tag, self.sample_names
        )
        for i, tag_val in enumerate(tag_vals):
            if set(tag_val) == {"."}:
                missing_tag_sample.append(self.sample_names[i])
        return {
            sample: self.mapped_sample[sample][tag] for sample in missing_tag_sample
        }

    def hasSNP(
        self
    ):  # TODO (Bhuwa, Bishwa, high priority) - may need to add a tag="GT" option
        # **Note: this needs to be implemented properly
        # The length of the REF and ALT both needs to be just 1.
        if len(self.REF) == 1:
            return True

    def hasINDEL(self):
        # TODO Bishwa : need to implement properly

        if len(self.REF) > 1:
            return True

    def hasAllele(self, allele="0", tag="GT", bases="numeric"):
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

        """

        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in self.sample_names
            if allele in self.mapped_sample[sample][tag]
        }

    # TODO: Bhuwan, Bishwa, high priority
    # bases='iupac' is not returing data.
    def hasVAR(self, genotype="0/0", tag="GT", bases="numeric"):
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

        """

        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in self.sample_names
            if (
                genotype
                in self._to_iupac(
                    self.ref_alt, self.mapped_sample[sample][tag], bases="numeric"
                )
            )
            or (
                genotype
                in self._to_iupac(
                    self.ref_alt, self.mapped_sample[sample][tag], bases="iupac"
                )
            )
        }

    def hasnoVAR(self, tag="GT"):
        """ Returns samples with empty genotype """

        return {
            sample: self.mapped_sample[sample][tag]
            for sample in self.sample_names
            if self.mapped_sample[sample][tag] in (".", "./.", ".|.")
        }

    def has_unphased(self, tag="GT", bases="numeric"):
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

        Examples
        --------

        >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

        >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
        >>> from record_parser import Record
        >>> rec_obj = Record(rec_valeg, rec_keys_eg)
        >>> rec_obj.has_unphased(tag="GT", bases="iupac")
        {'ms01e': './.', 'ms02g': './.', 'ms03g': './.', 'ms04h': '1/1', 'MA611': '0/0', 'MA605': '0/0', 'MA622': '0/0'}


        """
        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in self.sample_names
            if "/" in self.mapped_sample[sample][tag]
        }

    def has_phased(self, tag="GT", bases="numeric"):
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

        Examples
        --------

        >>> rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'

        >>> rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
        >>> from record_parser import Record
        >>> rec_obj = Record(rec_valeg, rec_keys_eg)
        >>> rec_obj.has_phased(tag="GT", bases="iupac")
        {}

        """

        return {
            sample: self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in self.sample_names
            if "|" in self.mapped_sample[sample][tag]
        }

    def _map_fmt_to_samples(self):

        """Private method to map format tags to sample values"""

        mapped_sample_fmt = OrderedDict()
        for i, name in enumerate(self.sample_names):
            mapped_sample_fmt[name] = dict(
                zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")
            )
        return mapped_sample_fmt

    # def get_mapped_samples(self, sample_names=None, formats=None, bases="numeric"):
    # def get_mapped_samples(self, sample_names=None, formats=None, gt_bases=(["GT", "numeric"],)):
    def get_mapped_samples(self, sample_names=None, formats=None, gt_bases=None):
        # formats=None, gt_base=(['GT:numeric'])
        """

        Parameters
        ----------
        sample_names : list
            list of sample names that needs to be filtered (default = all samples will be filtered)
            
        formats : list
            list of format tags that needs to be filtered (default = all formats will be filtered)

        Returns
        -------
        dict
            dict of filtered sample names along with filtered formats

        Examples
        --------

        >>> mapped_sample = {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
        >>> get_mapped_samples(self, sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'])
        {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}} 

        # TODO Bishwa - make this new example workable 
        >>> get_mapped_samples(self, sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC', 'PG'], gt_base=['GT:iupac', 'PG:iupac'])
        {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}} 
        # TODO Bishwa - update the output 

        """
        sample_names = sample_names if sample_names else self.sample_names

        required_format = formats if formats else self.format_
        # TODO Bishwa: this may need changing. If no format tag (i.e GT, PG) is given, it just returns numeric, rite??
        # TODO another issue: The sample is not generated as "key" in the mapped dictonary. This is fixed? but quirky !

        filtered_sample_format = {
            sample: dict(
                (fmt, self.mapped_sample[sample][fmt]) for fmt in required_format
            )
            for sample in sample_names
        }

        if gt_bases is None:
            return filtered_sample_format

        else:
            # update the genotype values for the tags requested in "iupac" format
            multi_genotype_as_iupac_bases = {}
            for (genotype_tag, genotype_output_format) in gt_bases:
                if genotype_output_format == "iupac":
                    try:
                        # convert the genotype from numeric to iupac format
                        sample_genotype_as_iupac = {
                            sample: {
                                genotype_tag
                                + "_iupac": self._to_iupac(
                                    self.ref_alt,
                                    self.mapped_sample[sample][genotype_tag],
                                    genotype_output_format,
                                )
                            }
                            for sample in sample_names
                        }

                        # TODO Bhuwan : improve this for-loop method if need be
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
                        # TODO Bhuwan/Gopal: Add warning message
                        print(
                            'The format tag "%s" is not available in one or multiple VCF record. '
                            % genotype_tag
                        )
                        print("Exiting VCF record parsing.")
                        sys.exit(0)

            # update the mapped sample dictionary
            for ks, vals in multi_genotype_as_iupac_bases.items():
                filtered_sample_format[ks].update(vals)

            # print('debugging')
            # print(filtered_sample_format)
            # sys.exit()
            return filtered_sample_format

        # TODO Bhuwan :
        # I tried using this method of returning. It just got too complicated for me.
        # Update as need be.
        # return {
        #     sample: dict(
        #         (
        #             fmt,
        #             self._to_iupac(
        #                 self.ref_alt, self.mapped_sample[sample][fmt], bases
        #                 # self.ref_alt, self.mapped_sample[sample][fmt], bases, gt_tags
        #             ),
        #         )
        #         for fmt in required_format #gt_tags
        #     )
        #     for sample in sample_names
        # }

    def get_mapped_tag_list(self, sample_names=None, tag=None, bases="numeric"):
        mapped_list = [
            self._to_iupac(self.ref_alt, self.mapped_sample[sample][tag], bases)
            for sample in sample_names
        ]
        return mapped_list

    def unmap_fmt_samples_dict(self, mapped_dict):
        """ Converts mapped dict again into string to write into the file.
        """

        sample_str_all = ""
        for sample in self.sample_names:
            # TODO make format compute only once
            format_str = ":".join(key for key in mapped_dict[sample])
            sample_str = ":".join(val for val in mapped_dict[sample].values())
            sample_str_all.join(sample_str + "\t")

        return format_str, sample_str_all

    @staticmethod
    def _to_iupac(ref_alt, numeric_genotype, bases="numeric"):
        # TODO - continue ....
        # print('ref_alt, numeric_genotype, bases')
        # print(ref_alt, numeric_genotype, bases)
        # sys.exit(0)

        if bases == "numeric":
            return numeric_genotype
        # if numeric_genotype == ".":
        #     return numeric_genotype

        numric_g_list = re.split(r"[/|]", numeric_genotype)
        sep = "/" if "/" in numeric_genotype else "|"
        iupac_vals = [ref_alt[int(i)] if i != "." else "." for i in numric_g_list]
        return sep.join(iupac_vals)

    def get_info_dict(self, required_keys=None):
        """
        Convert Info to dict for required keys

        Parameters
        ----------
        required_keys: list
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
        >>> required_keys= ['AC', 'BaseQRankSum']
        >>> get_info_dict(self, required_keys)
        {'AC':2, 'BaseQRankSum' : '.'}

        
        """
        mapped_info = dict(
            s.split("=", 1) if "=" in s else (s, ".") for s in self.info_str.split(";")
        )
        if isinstance(required_keys, list):
            # convert list to set for faster lookup
            required_keys_set = set(required_keys)
            return {
                key: value
                for key, value in mapped_info.items()
                if key in required_keys_set
            }
        else:
            return mapped_info

    def map_records_long(self, gt_bases=None):
        """ Maps record values with record keys.

        Returns
        -------
        dict
            dict with key value pair with sample and infos modified
        TODO: Add input and output 
        """
        mapped_records = dict(zip(self.record_keys, self.record_vals))
        mapped_records["INFO"] = self.get_info_dict()
        mapped_records["samples"] = self.get_mapped_samples(gt_bases=gt_bases)
        return mapped_records

    # functions to add later
    def iupac_to_numeric(self):
        # required for buildVCF ??
        # TODO
        pass

    def deletion_overlapping_variant(self):
        # TODO
        pass
