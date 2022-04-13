from vcfparser import VcfParser

# ** new class to add; 
from vcfparser import VCFWriter
import itertools


# instantiate a vcf object by passing file name
vcf_object = VcfParser('input_test.vcf')

# ** (low priority) for future: add “nc” flag to read the number of records at once
vcf_object = VcfParser('input_test.vcf')


# read and parse metadata 

metainfo = vcf_object.parse_metadata()
# print(metainfo.fileformat)
# print(metainfo.filters_)
# print(metainfo.contig)
# print(metainfo.infos_)
# print(metainfo.is_gvcf)
samples = metainfo.sample_names

## ** to do:
# should add method to return the whole raw metadata as is 
  # e.g: raw_metadata = metainfo.rawdata
# this will provide capacity to read metadata line by line on a for loop


## add method so new metadata information can be written by the writer 

  # e.g 
vcf_write_object = VcfWriter('write_test.vcf')

vcf_write_object.add_metadata('some metadata')
   # ** Note: metadata can be added as .write/add(metadata_name (e.g FORMAT, INFO, contig), several keys:values)
   # these metadata will be written as:
    # ##metadata_name=<comma joined “keys=values”>

   # add method to add a string as desired by the user
  #  vcf_write_object.add_string(some string)

   # add method to write the #CHROM line 
  #  vcf_write_object.add_record_keys(“CHROM”, “POS” .....) 
   # **note: this should be able to keep the index position of each key in memory so records value can be placed at right position while writing records (which is used downstream) 


## now parese records level information 

records = vcf_object.parse_records()

records_100 = itertools.islice(records,1,1000)
records_1000 = itertools.islice(records,1000,100000)


# read about tabix files to implement the following features
# chrom = '2' pos_range = (10000, 100000),
# start_pos = 10, no_of_records = 10 , 
# nc = 10000
  # ** maybe this iupac method can be used down stream (at sample level)

# vcf.write('#CHROM', 'POS'...., samples_names)
# vcf.write(header_line)

# now lets go through individual record and extract the required fields and print records
for record in records:
    print(record)  # ** should return record as string (at it is in the VCF), but as object ??
    chrom = record.CHROM
    pos = record.POS
    id = record.ID
    ref = record.REF
    alt = record.ALT
    qual = record.QUAL
    filter = record.FILTER # ** may be return as list, coz there might be multiple filters. But check first?

    info = record.get_info() # ** return as dictionary 
           # add method to capture INFO keys that have no values. return empty values “.” in such cases
    format_ = record.FORMAT # ** return as list 

    ## ** add new objects/methods to return SAMPLE with FORMAT level information 
    hom_ref_samples = record.HOMREF(tag = 'GT(default)|PG', bases = 'numeric|iupac')  # return dict with sample name and it’s GT value. 
           # also add capacity to return GT as iupac bases
    """
              rec.homref will return at default state:
              ordereddict : 'mso1e' :0/0, 'ma605: '0/0'

              rec.homref(tag= 'GT', base = 'iupac')
              ordereddict : 'mso1e' :0/0, 'ma605: 'A/A'
    """

    hom_var_samples = record.HOMVAR  # same as above

    # out
    het_var_samples = record.HETVAR  # same as above 
    samples_with_snps = record.hasSNP   # as dict, return samples that have all the variant only as SNP
    sample_with_indels = record.hasINDEL # as dict, return samples that have at least one allele as INDEL
    sample_with_specific_nucleotide = record.hasAllele['some GT nucleotide'] # as dict, return samples that has at least one allele as the given nucleotide 
    record.hasVAR[('some GT bases')] # as dict, return samples that has this specific genotype 
    record.noVAR # # as dict, return samples that have no bases called
    


    ## now map all the FORMAT tags to sample values, and return as ordered dict
    sample_records = record.mapped_record(tag = 'GT(default)|PG', bases = 'numeric|iupac', samples = [], format_ = ['']) 
    # ** return as dict, with FORMAT keys mapped to sample values
    ## may give sample names to map as arguments

    if sample_records['ms01e']['GT'] == '0/0':
      # {'ms01e': {'GT':'./.', "pi": '1'}, 'ms02g':{'GT':'./.', "pi": '1'},, 'ms03g': {'GT':'./.', "pi": '1'},}

      string_val = record.dict_to_str(sample_records)
      # gt:pi   ./.:1   ./.:1   ./.:1
      # vcf.write()
    
    # so, record.mapped_record[‘sample_name’] would return dict only for that ‘sample_name’
    # ** should we have iupac=[‘GT’, ‘PG’] method here?? 
    # something like, sample_A_record = record.mapped_record[‘sampleA’][‘GT’] would return numeric bases
    # but, sample_A_record = record.mapped_record[‘sampleA’][‘GT’].iupac(‘GT’) would return iupac bases 

    # ** addressing the above “sample_records” problem should not affect the “for loop” process for each sample shown below

    # sample_val = []
    # for i, sample in enumerate(samples, start= 9):  # ** start = 9 should be removed 
    #     sample_val.append(record[i])


## ** for future - add method to be able to write records 
## but, this will use the same writable object created above. i.e # vcf_write_object = VcfWriter('write_test.vcf')
# and the record can be written as: 
  # vcf_write_object.add_record(“CHROM”:”some value”)
  # vcf_write_object.add_record(“POS”:”some value”) 

  # ** i think the “add record” would be helpful if it can handle multiple keys ??
    # and also pass a delimiter to join the record information 
    # this way all the pre-header (CHROM to FILTER), INFO, FORMAT and sample information can be added 
  # eg:
  # the pre-header can be written as 
  # vcf_write_object.add_record(“CHROM”:”some value”, “POS”:”some value”, delimiter = “\t”, write_keys = False)

  # INFO can be written as
  # vcf_write_object.add_record(“AF”:[”sv1”, “sv2”], “AN”:[”sv”], delimiter = “;”, write_keys = True)

  # FORMAT can be written as 
  # vcf_write_object.add_record(“FORMAT” : [“GT”, “PG”, “PI”, ....], delimiter = “:”, write_keys = False)

  # sample level information can now be added on a for-loop
  # for name in samples:

      # vcf_write_object.add_record(name : [“GTvalue”, “PGvalue”, “PIvalue”, ....], delimiter = “:”, write_keys = False)
  

    
# - Add following capabilities to mapped_record() function
# # Add “sample control” method in mapping
# # Add not now “preheader control” method in mapping
# # Add “INFO keys control” method in mapping
# # Add “FORMAT keys control” method in mapping
# # may be ADD “FILTER” control method in mapping - should we return FILTER values as list, because there might be multiple FILTER tags for a single record?
# filter = 'missing_sites,low_allele_depth'.split(',')

# # where is the best position to put
# CHROM, POS control which is similar to fetch(CHROM, POS range)

# has_phased('GT', bases) returns  dict of sample names with phased genotypes 
# has_unphased('GT', bases)
# iupac_to_numeric()
# deletion overlapping variant()
# fetch from chrom pos 

# class Filter:
# 
#   
