import shlex
import collections
import re


class _MetadataParser:
    """
    Parses meta information from vcf files.
    """

    def __init__(self, line, tag):
        self.lines = line
        self.tag = tag

    @staticmethod
    def split_to_dict(string):
        splitter = shlex.shlex(string, posix=True)
        splitter.whitespace_split = True
        splitter.whitespace = ","
        tags_dict = dict(pair.split("=", 1) for pair in splitter)
        return tags_dict

    def parse_gvcf_block(self):
        """extract the GVCF blocks"""
        # e.g: ##GVCFBlock55-56=minGQ=55(inclusive),maxGQ=56(exclusive)
        gvcf_block = re.search("##GVCFBlock(.*?)=", self.lines, 0).group(1)

        # update tags_dict
        to_replace = self.tag + gvcf_block + "="

        string = self.lines.rstrip("\n").rstrip(">").replace(to_replace, "")
        tags_dict = self.split_to_dict(string)
        tags_dict["Block"] = gvcf_block
        return tags_dict

    def parse_contigs(self):
        """find chromosomes/contig names in the input VCF file"""
        # e.g line: ##contig=<ID=scaffold_1118,length=1005>

        string = self.lines.rstrip("\n").rstrip(">").replace(self.tag, "")
        tags_dict = self.split_to_dict(string)
        return tags_dict

    def parse_reference_genome(self):
        """find the reference genome name used to generated the input VCF/GVCF"""
        # return reference genome name and file path
        # e.g: ##reference=file:///media/02_Alignment_To_Ref/GVCF_Calls_onGenes-RunningTest01/02-JointGenotyping_MySpF1/lyrata_genome.fa
        ref_genome = self.lines.rstrip("\n").replace(self.tag, "")
        return {"reference": ref_genome}

    def parse_gatk_commands(self):
        """find the GATK commands used to generate the input VCF"""
        ## e.g: ##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller....
        gatk_cmd_middle_string = re.search(
            "##GATKCommandLine(.*)=<ID=", self.lines
        ).group(1)
        to_replace = "##GATKCommandLine" + gatk_cmd_middle_string + "=<"
        string = self.lines.rstrip("\n").rstrip(">").replace(to_replace, "")
        tags_dict = self.split_to_dict(string)
        return tags_dict

    def parse_format_info_filter(self):
        """
        Parse the FORMAT, INFO, FILTER from the VCF file. 
        These tags contains same string structure so a single function suffices for all.
        """
        string = self.lines.rstrip("\n").rstrip(">").replace(self.tag, "")
        tags_dict = self.split_to_dict(string)
        return tags_dict
