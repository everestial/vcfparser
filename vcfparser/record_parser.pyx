import re
from itertools import zip_longest
import warnings
import sys
from collections import OrderedDict
cimport cython

cdef class GenotypeProperty:
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

    cdef Record record_obj 


    def __init__(self, Record record_obj):
        self.record_obj = record_obj
        # pass

    # TODO (Bishwa) all this genotype parsing should be kept as a separate class ?
    # @property
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
        allele_obj = Alleles(self.record_obj.mapped_format_to_sample,tag)

        # allele_obj = 
        homref_samples = allele_obj.hom_ref_samples
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
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
        allele_obj = Alleles(self.record_obj.mapped_format_to_sample,tag)
        homvar_samples = allele_obj.hom_var_samples

        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
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
        allele_obj = Alleles(self.record_obj.mapped_format_to_sample,tag)
        hetvar_samples = allele_obj.het_var_samples

        #TODO: only do this dict comprehension if bases = 'iupac'
        # apply this method on other similar functions
        return {
            sample: self.record_obj._to_iupac(self.record_obj.ref_alt, self.record_obj.mapped_format_to_sample[sample][tag], bases)
            for sample in hetvar_samples
        }

    # TODO: illustrate that it can be use for any FORMAT tags, not just "GT"
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
        allele_obj = Alleles(self.record_obj.mapped_format_to_sample,tag)
        missing_tag_sample = allele_obj.missing_samples
        return {
            sample: self.record_obj.mapped_format_to_sample[sample][tag] for sample in missing_tag_sample
        }

    # TODO: may be 'tag' and 'bases' flag is not required
    def hasSNP(self, tag="GT", bases="numeric"):
        # TODO (Bhuwa, Bishwa, high priority) - may need to add a tag="GT" option
        # **Note: this needs to be implemented properly
        # The length of the REF and ALT both needs to be just 1.
        if len(self.record_obj.REF) == 1:
            return True

    def hasINDEL(self):
        # TODO Bishwa : need to implement properly

        if len(self.record_obj.REF) > 1:
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
    def hasnoVAR(self, tag="GT"):
        """ Returns samples with empty genotype """

        return {
            sample: self.record_obj.mapped_format_to_sample[sample][tag]
            for sample in self.record_obj.sample_names
            if self.record_obj.mapped_format_to_sample[sample][tag] in (".", "./.", ".|.")
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

# Constants (optional performance boost)
cdef class Record:
    """
    A class that converts the record lines from input VCF into accessible record object.
    """

    cdef str rec_line
    cdef list record_values
    cdef list record_keys
    cdef public str CHROM, POS, ID, REF, QUAL
    cdef public list ALT, FILTER, format_, sample_names, sample_vals
    cdef dict mapped_format_to_sample
    cdef public GenotypeProperty genotype_property
    cdef readonly ref_alt
    cdef public str info_str

    def __init__(self, list record_values, list record_keys):
 
        self.rec_line = "\t".join(record_values)
        self.record_values = record_values
        self.record_keys = record_keys
        self.CHROM = self.record_values[0] if len(self.record_values) > 0 else None
        self.POS = self.record_values[1] if len(self.record_values) > 1 else None
        self.ID = self.record_values[2] if len(self.record_values) > 2 else None
        self.REF = self.record_values[3] if len(self.record_values) > 3 else None
        self.ALT = self.record_values[4].split(",") if len(self.record_values) > 4 else []
        self.ref_alt = (self.REF.split(",") + self.ALT) if self.REF else self.ALT
        self.QUAL = self.record_values[5] if len(self.record_values) > 5 else None
        self.FILTER = self.record_values[6].split(",") if len(self.record_values) > 6 else []
        self.info_str = self.record_values[7] if len(self.record_values) > 7 else None
        self.format_ = self.record_values[8].split(":") if len(self.record_values) > 8 else []
        self.sample_names = self.record_keys[9:] if len(self.record_keys) > 9 else []

        try:
            self.sample_vals = self.record_values[9:]
        except IndexError:
            warnings.warn("Sample values are not presented correctly in given vcf file.")

        self.mapped_format_to_sample = self._map_format_tags_to_sample_values()
        self.genotype_property = GenotypeProperty(self)

    def __str__(self):
        return self.rec_line

    def _map_format_tags_to_sample_values(self):
        """Optimized version of mapping format tags to sample values"""
        cdef dict mapped_data = {}
        cdef int i
        for i, name in enumerate(self.sample_names):
            mapped_data[name] = dict(
                zip_longest(self.format_, self.sample_vals[i].split(":"), fillvalue=".")
            )
        return mapped_data

    # TODO: Other methods can be cythonized similarly by adding specific types to variables
    # TODO (Bhuwan) Done - if required this should be a lazy method too. 
    def get_format_to_sample_map(self, list sample_names=None, list formats=None, list convert_to_iupac=None):
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

        Examples
        --------
        >>> import vcfparser.vcf_parser as vcfparse
        >>> myvcf = vcfparse.VcfParser("input_test.vcf") 
        >>> records = myvcf.parse_records()
        >>> record = first(record) # TODO: Why first?
        >>> record.mapped_format_to_sample = {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
        >>> record.get_format_to_sample_map(self, sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'])
        {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}} 

        >>> record.get_format_to_sample_map(self, sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC', 'PG'], convert_to_iupac= ['GT', 'PG'])
        {'ms01e': {'GT': './.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PC': '.'}}
        #TODO: the GT output should have been in IUPAC.

        """
        sample_names = sample_names if sample_names else self.sample_names
        required_format = formats if formats else self.format_

        filtered_sample_format = {
            sample: dict(
                (fmt, self.mapped_format_to_sample[sample][fmt]) for fmt in required_format
            )
            for sample in sample_names
        }

        if convert_to_iupac is None:
            return filtered_sample_format

        else:
            # update the genotype values for the tags requested in "iupac" format
            multi_genotype_as_iupac_bases = {}
            genotype_output_format = "iupac"

            for genotype_tag in convert_to_iupac:
                # if genotype_output_format == "iupac":
                try:
                    # convert the genotype from numeric to iupac format
                    sample_genotype_as_iupac = {
                        sample: {
                            genotype_tag
                            + "_iupac": self._to_iupac(
                                self.ref_alt,
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
                    raise KeyError(f'The format tag "{genotype_tag}" is not available in one or multiple VCF record.')
                    # TODO (Bhuwan) Done - Why is object being returned even after warning is raised. 
                    # after warning the parsing on a forloop should stop? is this happening? 

            # update the mapped sample dictionary
            for ks, vals in multi_genotype_as_iupac_bases.items():
                filtered_sample_format[ks].update(vals)

            return filtered_sample_format

 
    @staticmethod
    # def split_tag_from_samples(order_mapped_samples, tag, sample_names):
    def get_tag_values_from_samples(order_mapped_samples, tag, sample_names, split_at=None):

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

        Examples
        --------
        >>> order_mapped_samples = OrderedDict([('ms01e',{'GT': './.', 'PI': '.'}), ('MA622', {'GT': '0/0','PI': '.'})])
        >>> tag = 'GT'
        >>> sample_names = ['ms01e', 'MA622']
        >>> record.get_tag_values_from_samples(order_mapped_samples, tag, sample_names)
        [['./.'], ['0/0']]
        >>> # using "/|"  # to split at GT values at both | and / 
        >>> get_tag_values_from_samples(order_mapped_samples, tag, sample_names, split_at= "/|")
        [['.', '.'], ['0', '0']]

        """
        # gt_vals = [order_mapped_samples[sample][tag] for sample in sample_names]
        # tag_vals = [re.split(r"[/|]", gt_val) for gt_val in gt_vals]
        # return tag_vals

        format_tag_values = [order_mapped_samples[sample][tag] for sample in sample_names]
        
        if split_at is not None:
            # tag_vals = [re.split(r"[/|]", gt_val) for gt_val in format_tag_values]
            splitted_tag_vals = [re.split(r"[/|]", value) for value in format_tag_values]
            return splitted_tag_vals
        return format_tag_values
        
    def get_mapped_tag_list(self, sample_names=None, tag=None, bases="numeric"):
        if sample_names:
            mapped_list = [
                self._to_iupac(self.ref_alt, self.mapped_format_to_sample[sample][tag], bases)
                for sample in sample_names 
            ]

            return mapped_list
        return []


    @staticmethod
    def _to_iupac(ref_alt, numeric_genotype, bases="numeric"):
        if bases == "numeric":
            return numeric_genotype
        # if numeric_genotype == ".":
        #     return numeric_genotype

        numeric_g_list = re.split(r"[/|]", numeric_genotype)
        sep = "/" if "/" in numeric_genotype else "|"
        iupac_vals = [ref_alt[int(i)] if i != "." else "." for i in numeric_g_list]
        return sep.join(iupac_vals)

    @staticmethod
    def split_genotype_tags():
        # TODO: BISHWA make a function to split the genotype tags 
        pass

    def get_info_as_dict(self, info_keys=None):
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
        mapped_info = dict(
            s.split("=", 1) if "=" in s else (s, ".") for s in self.info_str.split(";")
        )
        if isinstance(info_keys, list):
            # convert list to set for faster lookup
            info_keys_set = set(info_keys)
            return {
                key: value
                for key, value in mapped_info.items()
                if key in info_keys_set
            }
        else:
            return mapped_info

    def get_full_record_map(self, convert_to_iupac=None):
    
        """ Maps record values with record keys.

        Parameters
        ----------
        convert_to_iupac: list
            list of genotpye tags that needs to be converted into iupac bases (default tag = 'GT', default output = numeric bases)

        Returns
        -------
        dict
            dict with key value pair with sample and infos modified

        TODO: Done (Gopal) Add example input and output 

        Examples
        --------
        >>> record.get_full_record_map()
        {'CHROM': '2', 'POS': '15881018', 'ID': '.', 'REF': 'G', 'ALT': 'A,C', 'QUAL': '5082.45', 'FILTER': 'PASS', 'INFO': {'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, 'FORMAT': 'GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', 'ms01e': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms02g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms03g': './.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.', 'ms04h': '1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.', 'MA611': '0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.', 'MA605': '0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.', 'MA622': '0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.', 'samples': {'ms01e': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms02g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms03g': {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, 'ms04h': {'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, 'MA605': {'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'}}}
        
        """
        mapped_records = dict(zip(self.record_keys, self.record_values))
        mapped_records["INFO"] = self.get_info_as_dict()
        mapped_records["samples"] = self.get_format_to_sample_map(convert_to_iupac= convert_to_iupac)
        return mapped_records

    def unmap_fmt_samples_dict(self, mapped_dict):
        """ Converts mapped dict again into string to write into the file.
        """

        sample_str_all = ""
        format_str = ""
        for sample in self.sample_names:
            # TODO make format compute only once
            format_str = ":".join(key for key in mapped_dict[sample])
            sample_str = ":".join(val for val in mapped_dict[sample].values())
            sample_str_all.join(sample_str + "\t")

        return format_str, sample_str_all

    ## TODO: Done Revert mapped record into record string
    def mapped_rec_to_str(self, mapped_sample_dict):
        record_val_upto_info = self.record_values[:8]
        record_str = ''
        str_up_to_info = '\t'.join(record_val_upto_info)
        format_str, sample_str_all = self.unmap_fmt_samples_dict(mapped_sample_dict)
        record_str = str_up_to_info+ '\t' +format_str + '\t'+ sample_str_all
        return record_str


    # TODO: functions to add later Done
    def iupac_to_numeric(self, ref_alt, genotype_in_iupac):
        # input parameters should be ref_alt, iupac_bases = []
        # returns: list of numeric bases 
        # required for buildVCF ??
        # For ref_alt = ['G', 'A', 'C']
        # genotype_in_iupac = 'G/A' it should return '0/1'

        iupac_g_list = re.split(r"[/|]", genotype_in_iupac)
        sep = "/" if "/" in genotype_in_iupac else "|"
        numeric_vals = [ref_alt.index(i) if i != "." else "." for i in iupac_g_list]
        return sep.join(numeric_vals)

    def deletion_overlapping_variant(self):
        # TODO
        pass





allele_delimiter = re.compile(r'''[|/]''')
# allele_obj = Alleles(mapped_format_to_sample,tag)
## ASK: If this needs to be named allele or genotype
cdef class Alleles:
    cdef list hom_ref_samples, hom_var_samples, het_var_samples, missing_samples, phased_samples
    cdef dict mapped_samples
    cdef str tag

    def __init__(self, dict mapped_samples, str tag='GT'):
        """
        This class stores sample names and their genotype types.
        """
        self.hom_ref_samples = []
        self.hom_var_samples = []
        self.het_var_samples = []
        self.missing_samples = []
        self.phased_samples = []
        self.mapped_samples = mapped_samples
        self.tag = tag

        cdef str sample, tag_val
        cdef object genotype_val

        # Iterate over the sample keys and store the genotype types
        for sample in mapped_samples.keys():
            tag_val = mapped_samples.get(sample, {}).get(tag, None)
            if tag_val is not None:
                genotype_val = GenotypeVal(tag_val)
                if genotype_val.phased:
                    self.phased_samples.append(sample)
                if genotype_val._ismissing:
                    self.missing_samples.append(sample)
                elif genotype_val.gt_type == 'hom_ref':
                    self.hom_ref_samples.append(sample)
                elif genotype_val.gt_type == 'hom_var':
                    self.hom_var_samples.append(sample)
                elif genotype_val.gt_type == 'het_var':
                    self.het_var_samples.append(sample)
            else:
                warnings.warn(f'{sample} has no mapped value for {tag} tag')
    def homref_samples(self):
        pass

## ASK: What to do if following scenario arises?
## Are they homref, hetvar './.' , '.', './0', '0/.'

cdef class GenotypeVal:
    cdef public list _alleles
    cdef public str gt_type
    cdef public bint phased, _ismissing  

    def __init__(self, str allele):
        """
        For a given genotype data like ('0/0', '1|1', '0/1'), this class computes
        and stores whether it is hom_ref, hom_var, or het_var.
        """
        self.phased = False
        self.gt_type = None

        # Split the allele string and replace "." with None
        self._alleles = [(al if al != '.' else None) for al in allele_delimiter.split(allele)]
        self._ismissing = not any(al is not None for al in self._alleles)

        if '|' in allele:
            self.phased = True

        # Determine the genotype type (hom_ref, hom_var, het_var)
        cdef list alleles_list = self._alleles
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