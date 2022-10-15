from vcfparser import VcfParser
import cProfile

vcf = VcfParser("input_test.vcf")
record1 = vcf.parse_records()