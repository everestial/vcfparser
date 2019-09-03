"""
Some utility function to convert format tags to sample values
"""

def map_format_tags_to_sample_values(record_dict, sample_names, iupac):
    """map format tags to sample values in VCF file"""

    len_format_tags = len(record_dict['FORMAT'])
    split_format_tags = record_dict['FORMAT'].split(":")
    ref_and_alts = [record_dict['REF']] + record_dict['ALT'].split(',')

    for name in sample_names:
        sample_value_string = record_dict[name]
        sample_values = sample_value_string.split(":")

        # number of items in each sample should equal to number of format tags
        if len(sample_values) == 1:
            sample_values = sample_values + ["."] * (len_format_tags - 1)
        elif len(sample_values) == 0:
            sample_values = sample_values + ["."] * (len_format_tags)

        # map the format tags to the sample values
        mapped_format_sample = dict(zip(split_format_tags, sample_values))


        if iupac:
            for tag in iupac:
                numeric_tag = mapped_format_sample[tag]
                iupac_tag = convert_genotypes(ref_and_alts, numeric_tag)

                # update the genotype values 
                mapped_format_sample[tag] = iupac_tag

        # update the sample record (tags, values) in the record_dict
        record_dict[name] = mapped_format_sample

    # after the for loop is complete all the the sample record should be updated
    # then return the record dict
    return record_dict

def convert_genotypes(ref_and_alt, numeric_genotype):
    iupac_genotype = []  # default value 
    
    for its in numeric_genotype:
        try:
            if type(int(its)) is int:
                iupac_genotype.append(ref_and_alt[int(its)])
        except ValueError:
            iupac_genotype.append(its)
                
    iupac_genotype = ''.join(iupac_genotype)       
    
    return iupac_genotype  