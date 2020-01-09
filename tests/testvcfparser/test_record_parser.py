import pytest
import filecmp
import os
import csv
from collections import OrderedDict

from vcfparser import Record
output_file01  = 'tests/testfiles/vcf_parser_output/record_parser_test_result01'
rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'
rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
rec_obj = Record(rec_valeg, rec_keys_eg)
# 01 Record.split_tag_from_samples
def test_split_tag_from_samples():
    pass
    # FIXME: invalid syntax error shown in order_mapped_samples
    # order_mapped_samples = OrderedDict([('ms01e',{'GT': './.', 'PI': '.'), ('MA622', 'GT': '0/0','PI': '.'})])
    # tag = 'GT'
    # sample_names = ['ms01e', 'MA622']
    # data = Record.split_tag_from_samples(order_mapped_samples, tag, sample_names)
    # with open(output_file + ".txt", "w") as w_file:
    #     w_file.write(f"{data}")
    # with open(output_file + ".txt", "w") as w_file:
    #         for key, val in data.items():
    #             w_file.write(f"{key}\n")
    #             w_file.write(f"{val}\n")
    #             w_file.write("\n")

    # assert is_same_file("tests/testfiles/vcf_parser_output/record_parser_test_result01.txt", 
    #                     f"tests/testfiles/vcf_parser_reference/vcfparser_metainfo_test_ref.txt") is True
    
    # os.remove(f"tests/testfiles/vcf_parser_output/record_parser_test_result01.txt")
    
# 02 Record.isHOMREF
def test_isHOMREF():  
    data = rec_obj.isHOMREF(tag="GT", bases="iupac")
    write_data_and_check(2, data)

# 03 Record.isHOMVAR
def test_isHOMVAR():
    data = rec_obj.isHOMVAR(tag="GT", bases="numeric")
    write_data_and_check(3, data)
# 04 Record.isHETVAR
def test_isHETVAR():
    data = rec_obj.isHETVAR(tag="GT", bases="numeric")
    write_data_and_check(4, data)
# 05 Record.isMissing
def test_isMissing():
    data = rec_obj.isMissing(tag="GT")
    write_data_and_check(5, data)
# 06 Record.hasSNP
def test_hasSNP():
    #TODO:need to implement
    pass
# 07 Record.hasINDEL
def test_hasINDEL():
    #TODO:need to implement
    pass
# 08 Record.hasAllele
def test_hasAllele():
    data = rec_obj.hasAllele(allele="0",tag="GT", bases="numeric")
    write_data_and_check(8, data)
# 09 Record.hasVAR
def test_hasVAR():
    data = rec_obj.hasVAR(genotype="0/0", tag="GT", bases="numeric")
    write_data_and_check(9, data)
# 10 Record.hasnoVAR
def test_hasnoVAR():
    data = rec_obj.hasnoVAR(tag="GT")
    write_data_and_check(10, data)
# 11 Record.has_unphased
def test_has_unphased():
    data = rec_obj.has_unphased(tag="GT", bases="iupac")
    write_data_and_check(11, data)

# 12 Record.has_phased
def test_has_phased():
    data = rec_obj.has_phased(tag="GT", bases="iupac")
    write_data_and_check(12, data)

# 13 Record._map_fmt_to_samples
def test_map_fmt_to_samples():
    data = rec_obj._map_fmt_to_samples()
    write_data_and_check(13, data)
# 14 Record.get_mapped_samples
def test_get_mapped_samples():
    pass
    #FIXME: keyerror: "ms01e"
    # # mapped_sample = {'ms01e': {'GT': './.','PI': '.', 'PC': '.'}, 'MA622': {'GT': '0/0', 'PI': '.', 'PC': '.'}, 'MA611': {'GT': '0/0', 'PI': '.', 'PC': '.'}}
    # rec_keys_eg = 'CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	ms01e	ms02g	ms03g	ms04h	MA611	MA605	MA622'
    # rec_valeg = '2	15881018	.	G	A,C	5082.45	PASS	AC=2,0;AF=1.00;AN=8;BaseQRankSum=-7.710e-01;ClippingRankSum=0.00;DP=902;ExcessHet=0.0050;FS=0.000;InbreedingCoeff=0.8004;MLEAC=12,1;MLEAF=0.462,0.038;MQ=60.29;MQRankSum=0.00;QD=33.99;ReadPosRankSum=0.260;SF=0,1,2,3,4,5,6;SOR=0.657;set=HignConfSNPs	GT:PI:GQ:PG:PM:PW:AD:PL:DP:PB:PC	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	./.:.:.:./.:.:./.:0,0:0,0,0,.,.,.:0:.:.	1/1:.:6:1/1:.:1/1:0,2:49,6,0,.,.,.:2:.:.	0/0:.:78:0/0:.:0/0:29,0,0:0,78,1170,78,1170,1170:29:.:.	0/0:.:9:0/0:.:0/0:3,0,0:0,9,112,9,112,112:3:.:.	0/0:.:99:0/0:.:0/0:40,0,0:0,105,1575,105,1575,1575:40:.:.'
    # rec_obj = Record(rec_keys_eg, rec_valeg)
    # data = rec_obj.get_mapped_samples(sample_names= ['ms01e', 'MA611'], formats= ['GT', 'PC'], bases = 'numeric')
    # write_data_and_check(14, data)

# 15 Record.get_mapped_tag_list
def test_get_mapped_tag_list():
    pass
    #TODO: Fill sample_names and tag and run test
    # sample_names = []
    # tag = []
    # data = rec_obj.get_mapped_tag_list(sample_names, tag, bases="numeric")
    # write_data_and_check(15, data)
# 16 Record.unmap_fmt_samples_dict
def test_unmap_fmt_samples_dict():
    pass
    #TODO:Fill up the values in mapped_dict and run test
    # mapped_dict = {}
    # data = rec_obj.unmap_fmt_samples_dict(mapped_dict)
    # write_data_and_check(16, data)
# 17 Record._to_iupac
def test_to_iupac():
    pass
    #TODO: Fill up the values of ref_alt, numeric_genotype and run test
    # ref_alt = []
    # numeric_genotype = []
    # data = rec_obj._to_iupac(ref_alt, numeric_genotype, bases ="numeric"):
    # write_data_and_check(17, data)
# 18 Record.get_info_dict
def test_get_info_dict():
    # info_str = 'AC=2,0;AF=1.00;AN=8;BaseQRankSum'
    required_keys= ['AC', 'BaseQRankSum']
    data = rec_obj.get_info_dict(required_keys)
    write_data_and_check(18, data)
# 19 Record.map_records_long
def test_map_records_long():
    data = rec_obj.map_records_long()
    write_data_and_check(19, data)
# 20 Record.iupac_to_numeric
def test_iupac_to_numeric():
    #TODO:
    pass
# 21 Record.deletion_overlapping_variant
def test_deletion_overlapping_variant():
    #TODO:
    pass


#Helping functions
def write_data_and_check(i, data):
    output_file  = f'tests/testfiles/vcf_parser_output/record_parser_test_result{i}'
    with open(output_file + ".txt", "w") as w_file:
        for key, val in data.items():
            w_file.write(f"{key}\n")
            w_file.write(f"{val}\n")
            w_file.write("\n")

    assert is_same_file(f"tests/testfiles/vcf_parser_output/record_parser_test_result{i}.txt", 
                        f"tests/testfiles/vcf_parser_reference/record_parser_test_ref{i}.txt") is True

    os.remove(f"tests/testfiles/vcf_parser_output/record_parser_test_result{i}.txt")
#Compare files
def is_same_file(file1, file2):
    return filecmp.cmp(file1, file2)