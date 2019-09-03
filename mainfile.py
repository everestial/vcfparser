from vcf_parser import VcfParser

# instantiate a vcf object by passing file name
vcf_object = VcfParser('full_vcf43.vcf.gz')

# read metadata 

metainfo = vcf_object.parse_metadata()
# print(metainfo.fileformat)
# print(metainfo.filters_)
# print(metainfo.contig)
# print(metainfo.infos_)
# print(metainfo.is_gvcf)
samples = metainfo.sample_names

records = vcf_object.parse_records()


# now lets go through individual record and extract the required fields and print records
for record in records:

    print(record)
    chrom = record.CHROM
    pos = record.POS
    id = record.ID
    ref = record.REF
    alt = record.QUAL
    filter = record.FILTER
    info = record.INFO
    print(info)
    format_ = record.FORMAT
    sample_val = []
    for i, sample in enumerate(samples, start= 9):
        sample_val.append(record[i])

    

