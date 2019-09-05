import pytest
from vcf_parser import VcfParser


vcf_object = VcfParser("input_test.vcf")
metainfo = vcf_object.parse_metadata()  

def test_fileformat():
     assert metainfo.fileformat == "VCFv4.2"


def test_filters():  

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

def test_formats():
    expected_format = [{'ID': 'AD', 'Number': 'R', 'Type': 'Integer', 'Description': 'Allelic depths for the ref and alt alleles in the order listed'}, {'ID': 'DP', 'Number': '1', 'Type': 'Integer', 'Description': 'Approximate read depth (reads with MQ=255 or with bad mates are filtered)'}, {'ID': 'GQ', 'Number': '1', 'Type': 'Integer', 'Description': 'Genotype Quality'}, {'ID': 'GT', 'Number': '1', 'Type': 'String', 'Description': 'Genotype'}, {'ID': 'MIN_DP', 'Number': '1', 'Type': 'Integer', 'Description': 'Minimum DP observed within the GVCF block'}, {'ID': 'PGT', 'Number': '1', 'Type': 'String', 'Description': 'Physical phasing haplotype information, describing how the alternate alleles are phased in relation to one another'}, {'ID': 'PID', 'Number': '1', 'Type': 'String', 'Description': 'Physical phasing ID information, where each unique ID within a given sample (but not across samples) connects records within a phasing group'}, {'ID': 'PL', 'Number': 'G', 'Type': 'Integer', 'Description': 'Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification'}, {'ID': 'RGQ', 'Number': '1', 'Type': 'Integer', 'Description': 'Unconditional reference genotype confidence, encoded as a phred quality -10*log10 p(genotype call is wrong)'}, {'ID': 'SB', 'Number': '4', 'Type': 'Integer', 'Description': "Per-sample component statistics which comprise the Fisher's Exact Test to detect strand bias."}, {'ID': 'PG', 'Number': '1', 'Type': 'String', 'Description': 'phASER Local Genotype'}, {'ID': 'PB', 'Number': '1', 'Type': 'String', 'Description': 'phASER Local Block'}, {'ID': 'PI', 'Number': '1', 'Type': 'String', 'Description': 'phASER Local Block Index (unique for each block)'}, {'ID': 'PM', 'Number': '1', 'Type': 'String', 'Description': 'phASER Local Block Maximum Variant MAF'}, {'ID': 'PW', 'Number': '1', 'Type': 'String', 'Description': 'phASER Genome Wide Genotype'}, {'ID': 'PC', 'Number': '1', 'Type': 'String', 'Description': 'phASER Genome Wide Confidence'}]    
    assert metainfo.format_ == expected_format

def test_info():
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

def test_sample_names():
    expected_samples = ['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']
    assert metainfo.sample_names == expected_samples


def test_record():
    records = vcf_object.parse_records()
    first_record = next(records)

    assert first_record.CHROM == '2'
    assert first_record.POS == '15881018'
    first_rec_info =  "{'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}"
    assert str(first_record.INFO) == first_rec_info
    first_sample_val = {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}

    assert first_record.ms01e == first_sample_val