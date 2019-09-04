import pytest
from vcf_parser import VcfParser


vcf_object = VcfParser("input_test.vcf")

def test_info_dict():
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

    assert metainfo.sample_names == ['ms01e', 'ms02g', 'ms03g', 'ms04h', 'MA611', 'MA605', 'MA622']


def test_record():
    records = vcf_object.parse_records()
    first_record = next(records)

    expected_record = "Record(CHROM='2', POS='15881018', ID='.', REF='G', ALT='A,C', QUAL='5082.45', FILTER='PASS', INFO={'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}, FORMAT='GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC', ms01e=, ms02g={'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, ms03g={'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}, ms04h={'GT': '1/1', 'PI': '.', 'GQ': '6', 'PG': '1/1', 'PM': '.', 'PW': '1/1', 'AD': '0,2', 'PL': '49,6,0,.,.,.', 'DP': '2', 'PB': '.', 'PC': '.'}, MA611={'GT': '0/0', 'PI': '.', 'GQ': '78', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '29,0,0', 'PL': '0,78,1170,78,1170,1170', 'DP': '29', 'PB': '.', 'PC': '.'}, MA605={'GT': '0/0', 'PI': '.', 'GQ': '9', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '3,0,0', 'PL': '0,9,112,9,112,112', 'DP': '3', 'PB': '.', 'PC': '.'}, MA622={'GT': '0/0', 'PI': '.', 'GQ': '99', 'PG': '0/0', 'PM': '.', 'PW': '0/0', 'AD': '40,0,0', 'PL': '0,105,1575,105,1575,1575', 'DP': '40', 'PB': '.', 'PC': '.'})"

    assert first_record.CHROM == '2'
    assert first_record.POS == '15881018'
    first_rec_info =  "{'AC': '2,0', 'AF': '1.00', 'AN': '8', 'BaseQRankSum': '-7.710e-01', 'ClippingRankSum': '0.00', 'DP': '902', 'ExcessHet': '0.0050', 'FS': '0.000', 'InbreedingCoeff': '0.8004', 'MLEAC': '12,1', 'MLEAF': '0.462,0.038', 'MQ': '60.29', 'MQRankSum': '0.00', 'QD': '33.99', 'ReadPosRankSum': '0.260', 'SF': '0,1,2,3,4,5,6', 'SOR': '0.657', 'set': 'HignConfSNPs'}"
    assert str(first_record.INFO) == first_rec_info
    first_sample_val = {'GT': './.', 'PI': '.', 'GQ': '.', 'PG': './.', 'PM': '.', 'PW': './.', 'AD': '0,0', 'PL': '0,0,0,.,.,.', 'DP': '0', 'PB': '.', 'PC': '.'}

    assert first_record.ms01e == first_sample_val