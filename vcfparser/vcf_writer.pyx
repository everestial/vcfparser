class VCFWriter:
    """
    A vcf writer to write headerline and datalines into new file

    """

    def __init__(self, filename):
        self.w_file = open(filename, 'a')

    def add_normal_metadata(self, key, value):
        """
        This is used to add normal key value metadata like: fileformat, filedate, refrence
        """
        print(f'##{key}= {value}\n', file=self.w_file)

    def add_info(self, id, num='.', type='.', desc='', key='INFO'):
        print(f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n', file=self.w_file)

    def add_format(self, id, num='.', type='.', desc='', key='FORMAT'):
        print(f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n', file=self.w_file)

    def add_filter(self, id, desc='', key='FILTER'):
        print(f'##{key}=<ID={id},Description="{desc}">\n', file=self.w_file)

    def add_filter_long(self, id, num='.', type='.', desc='', key='FILTER'):
        print(f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n', file=self.w_file)

    def add_contig(self, id, length, key='contig'):
        # Example contig: ##contig=<ID=scaffold_591,length=5806>
        print(f'##{key}=<ID={id}, length={length}>\n', file=self.w_file)

    def add_header_line(self, record_keys):
        print(f'{record_keys}', sep='\t', file=self.w_file)

    def add_record_value(self, preheader, info, format_, sample_str):
        print(f'{preheader}', sep='\t', end='\t', file=self.w_file)
        print(f'{info}', sep='\t', end='\t', file=self.w_file)
        print(f'{format_}', sep='\t', end='\t', file=self.w_file)
        print(f'{sample_str}', sep='\t', end='\t', file=self.w_file)
