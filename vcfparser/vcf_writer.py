class VCFWriter:
    """
    A vcf writer to write headerline and datalines into new file

    """

    def __init__(self, filename):
        self.w_file = open(filename, "a")

    def add_normal_metadata(self, key : str, value : str):
        """
        This is used to add normal key value metadata like: fileformat, filedate, refrence

        Parameters
        ----------
        key :
            string value, could be file format, reference etc.
        value :
            string  value for the corresponding key

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> key = "fileformat"
        >>> value = "VCFv4.2"
        >>> writer.add_normal_metadata(key, value)
        ##fileformat= VCFv4.2\n
        """
        print(f"##{key}= {value}\n", file=self.w_file)

    def add_info(self, id, num=".", type=".", desc="", key="INFO"):
        """
        This is used to add INFO to the file

        Parameters
        ----------
        id :
            string value i.e. identifier for this info. line
        num :
            string value for the corresponding id
        type :
            type of the value
        desc :
            description of the id

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> id = "AF"
        >>> num = "A"
        >>> type = "Float"
        >>> desc = "Allele Frequency, for each ALT allele, in the same order as listed"
        >>> writer.add_info(id, num, type, desc)
        ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency, for each ALT allele, in the same order as listed">\n
        
        """
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n',
            file=self.w_file,
        )

    def add_format(self, id, num=".", type=".", desc="", key="FORMAT"):
        """
        This is used to add FORMAT to the file

        Parameters
        ----------
        id :
            string value i.e. identifier for this info. line
        num :
            string value for the corresponding id
        type :
            type of the value
        desc :
            description of the id

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> id = "GT"
        >>> num = "1"
        >>> type = "String"
        >>> desc = "Genotype"
        >>> writer.add_info(id, num, type, desc)
        ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
        
        """
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n',
            file=self.w_file,
        )

    def add_filter(self, id, desc="", key="FILTER"):
        """
        This is used to add FILTER to the file

        Parameters
        ----------
        id :
            string value i.e. identifier for the filter
        desc :
            description of the id

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> id = "LowQual"
        >>> desc = "Low quality"
        >>> writer.add_filter(id, desc)
        ##FILTER=<ID=LowQual,Description="Low quality">

        """
        print(f'##{key}=<ID={id},Description="{desc}">\n', file=self.w_file)

    def add_filter_long(self, id, num=".", type=".", desc="", key="FILTER"):
        """
        This is used to add FILTER to the file

        Parameters
        ----------
        id :
            string value i.e. identifier for the filter
        num :
            string value for the corresponding id
        type :
            type of the value
        desc :
            description of the id

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> id = "LowQual"
        >>> num = "1"
        >>> type = "String"
        >>> desc = "Low quality"
        >>> writer.add_filter(id, desc)
        ##FILTER=<ID=LowQual,Number=1,Type=String,Description="Low quality">

        """
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">\n',
            file=self.w_file,
        )

    def add_contig(self, id, length, key="contig"):
        """
        This is used to add contig header to the file

        Parameters
        ----------
        id :
            string value i.e. identifier for the filter
        length :
            value of the length tag

        Returns
        -------
        None

        Examples
        --------
        >>> writer = VCFWriter("new_file.vcf")
        >>> id = "scaffold_861"
        >>> length = "4139"
        >>> writer.add_filter(id, desc)
        ##contig=<ID=scaffold_861,length=4139>

        """
        print(f"##{key}=<ID={id}, length={length}>\n", file=self.w_file)

    def add_header_line(self, record_keys):
        ## TODO: include docstring and example -> confused over the type of record_keys
        print(f"{record_keys}", sep="\t", file=self.w_file)

    def add_record_value(self, preheader, info, format_, sample_str):
        """
            confused just like add_header_line
        """
        print(f"{preheader}", sep="\t", end="\t", file=self.w_file)
        print(f"{info}", sep="\t", end="\t", file=self.w_file)
        print(f"{format_}", sep="\t", end="\t", file=self.w_file)
        print(f"{sample_str}", sep="\t", end="\t", file=self.w_file)
