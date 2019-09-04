import pytest
from vcf_parser import VcfParser


def test_info_dict():
    vcf_object = VcfParser("input_test.vcf")
    metainfo = vcf_object.parse_metadata()
    assert metainfo.fileformat == "VCFv4.2"

    expected_filters = [
        {"ID": "LowQual", "Description": "Low quality"},
        {
            "ID": "my_indel_filter",
            "Description": "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0",
        },
        {
            "ID": "my_snp_filter",
            "Description": "QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0",
        },
    ]
    assert metainfo.filters_ == expected_filters

    expected_info = [
        {
            "ID": "AF",
            "Number": "A",
            "Type": "Float",
            "Description": "Allele Frequency, for each ALT allele, in the same order as listed",
        },
        {
            "ID": "BaseQRankSum",
            "Number": "1",
            "Type": "Float",
            "Description": "Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities",
        },
        {
            "ID": "ClippingRankSum",
            "Number": "1",
            "Type": "Float",
            "Description": "Z-score From Wilcoxon rank sum test of Alt vs. Ref number of hard clipped bases",
        },
        {
            "ID": "DP",
            "Number": "1",
            "Type": "Integer",
            "Description": "Approximate read depth; some reads may have been filtered",
        },
        {
            "ID": "DS",
            "Number": "0",
            "Type": "Flag",
            "Description": "Were any of the samples downsampled?",
        },
        {
            "ID": "END",
            "Number": "1",
            "Type": "Integer",
            "Description": "Stop position of the interval",
        },
        {
            "ID": "ExcessHet",
            "Number": "1",
            "Type": "Float",
            "Description": "Phred-scaled p-value for exact test of excess heterozygosity",
        },
        {
            "ID": "FS",
            "Number": "1",
            "Type": "Float",
            "Description": "Phred-scaled p-value using Fisher's exact test to detect strand bias",
        },
        {
            "ID": "HaplotypeScore",
            "Number": "1",
            "Type": "Float",
            "Description": "Consistency of the site with at most two segregating haplotypes",
        },
        {
            "ID": "InbreedingCoeff",
            "Number": "1",
            "Type": "Float",
            "Description": "Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation",
        },
        {
            "ID": "MLEAC",
            "Number": "A",
            "Type": "Integer",
            "Description": "Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed",
        },
        {
            "ID": "MLEAF",
            "Number": "A",
            "Type": "Float",
            "Description": "Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed",
        },
        {
            "ID": "MQ",
            "Number": "1",
            "Type": "Float",
            "Description": "RMS Mapping Quality",
        },
        {
            "ID": "MQRankSum",
            "Number": "1",
            "Type": "Float",
            "Description": "Z-score From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities",
        },
        {
            "ID": "QD",
            "Number": "1",
            "Type": "Float",
            "Description": "Variant Confidence/Quality by Depth",
        },
        {
            "ID": "RAW_MQ",
            "Number": "1",
            "Type": "Float",
            "Description": "Raw data for RMS Mapping Quality",
        },
        {
            "ID": "ReadPosRankSum",
            "Number": "1",
            "Type": "Float",
            "Description": "Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias",
        },
        {
            "ID": "SOR",
            "Number": "1",
            "Type": "Float",
            "Description": "Symmetric Odds Ratio of 2x2 contingency table to detect strand bias",
        },
        {
            "ID": "set",
            "Number": "1",
            "Type": "String",
            "Description": "Source VCF for the merged record in CombineVariants",
        },
        {
            "ID": "SF",
            "Number": ".",
            "Type": "String",
            "Description": "Source File (index to sourceFiles, f when filtered)",
        },
        {
            "ID": "AC",
            "Number": ".",
            "Type": "Integer",
            "Description": "Allele count in genotypes",
        },
        {
            "ID": "AN",
            "Number": "1",
            "Type": "Integer",
            "Description": "Total number of alleles in called genotypes",
        },
        {"ID": "TS", "Type": "Test", "Description": "Allele count in genotypes"},
    ]
    assert metainfo.infos_ == expected_info
