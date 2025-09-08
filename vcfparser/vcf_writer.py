from typing import TextIO, Optional, Union, List, Any
import os


class VCFWriter:
    """
    A VCF writer to write header lines and data lines into a new file.
    
    This class provides methods to write various VCF metadata sections
    and record data to an output file. It supports context manager
    protocol for proper file handling.
    
    Parameters
    ----------
    filename : str
        Path to the output VCF file
    mode : str, optional
        File open mode (default: "w" for write, "a" for append)
        
    Examples
    --------
    >>> with VCFWriter("output.vcf") as writer:
    ...     writer.add_normal_metadata("fileformat", "VCFv4.3")
    ...     writer.add_info("DP", "1", "Integer", "Total read depth")
    """
    
    # Instance attributes
    filename: str
    w_file: Optional[Any]  # Using Any to handle file objects
    _is_closed: bool

    def __init__(self, filename: str, mode: str = "w") -> None:
        """
        Initialize VCFWriter with output filename.
        
        Parameters
        ----------
        filename : str
            Path to the output VCF file
        mode : str, optional
            File open mode (default: "w")
        """
        self.filename = filename
        self.w_file = None
        self._is_closed = False
        
        try:
            self.w_file = open(filename, mode, encoding="utf-8")
        except (IOError, FileNotFoundError, PermissionError) as e:
            # Re-raise the original exception type for better error handling
            raise e

    def __enter__(self) -> 'VCFWriter':
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """Exit context manager and close file."""
        self.close()
    
    def close(self) -> None:
        """Close the output file if it's open."""
        if self.w_file and not self._is_closed:
            self.w_file.close()
            self._is_closed = True
    
    def _ensure_open(self) -> None:
        """Ensure the file is open for writing."""
        if self.w_file is None or self._is_closed:
            raise ValueError("File is not open for writing")

    def add_normal_metadata(self, key: str, value: str) -> None:
        """
        Add normal key-value metadata like fileformat, filedate, reference.
        
        Parameters
        ----------
        key : str
            Metadata key (e.g., "fileformat", "fileDate")
        value : str
            Metadata value
            
        Examples
        --------
        >>> writer.add_normal_metadata("fileformat", "VCFv4.3")
        >>> writer.add_normal_metadata("fileDate", "20231201")
        """
        self._ensure_open()
        print(f"##{key}={value}", file=self.w_file)

    def add_info(self, id: str, num: str = ".", type: str = ".", desc: str = "", key: str = "INFO") -> None:
        """
        Add INFO metadata line to VCF header.
        
        Parameters
        ----------
        id : str
            INFO field ID
        num : str, optional
            Number of values (default: ".")
        type : str, optional
            Data type (Integer, Float, String, etc.) (default: ".")
        desc : str, optional
            Description of the INFO field (default: "")
        key : str, optional
            Metadata key (default: "INFO")
            
        Examples
        --------
        >>> writer.add_info("DP", "1", "Integer", "Total read depth")
        >>> writer.add_info("AF", "A", "Float", "Allele frequency")
        """
        self._ensure_open()
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">',
            file=self.w_file,
        )

    def add_format(self, id: str, num: str = ".", type: str = ".", desc: str = "", key: str = "FORMAT") -> None:
        """
        Add FORMAT metadata line to VCF header.
        
        Parameters
        ----------
        id : str
            FORMAT field ID
        num : str, optional
            Number of values (default: ".")
        type : str, optional
            Data type (Integer, Float, String, etc.) (default: ".")
        desc : str, optional
            Description of the FORMAT field (default: "")
        key : str, optional
            Metadata key (default: "FORMAT")
            
        Examples
        --------
        >>> writer.add_format("GT", "1", "String", "Genotype")
        >>> writer.add_format("DP", "1", "Integer", "Read depth")
        """
        self._ensure_open()
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">',
            file=self.w_file,
        )

    def add_filter(self, id: str, desc: str = "", key: str = "FILTER") -> None:
        """
        Add FILTER metadata line to VCF header.
        
        Parameters
        ----------
        id : str
            FILTER field ID
        desc : str, optional
            Description of the filter (default: "")
        key : str, optional
            Metadata key (default: "FILTER")
            
        Examples
        --------
        >>> writer.add_filter("LowQual", "Low quality variants")
        >>> writer.add_filter("PASS", "All filters passed")
        """
        self._ensure_open()
        print(f'##{key}=<ID={id},Description="{desc}">', file=self.w_file)

    def add_filter_long(self, id: str, num: str = ".", type: str = ".", desc: str = "", key: str = "FILTER") -> None:
        """
        Add extended FILTER metadata line with Number and Type fields.
        
        Parameters
        ----------
        id : str
            FILTER field ID
        num : str, optional
            Number of values (default: ".")
        type : str, optional
            Data type (default: ".")
        desc : str, optional
            Description of the filter (default: "")
        key : str, optional
            Metadata key (default: "FILTER")
            
        Examples
        --------
        >>> writer.add_filter_long("CustomFilter", "1", "String", "Custom filtering")
        """
        self._ensure_open()
        print(
            f'##{key}=<ID={id},Number={num},Type={type},Description="{desc}">',
            file=self.w_file,
        )

    def add_contig(self, id: str, length: Union[int, str], key: str = "contig") -> None:
        """
        Add contig metadata line to VCF header.
        
        Parameters
        ----------
        id : str
            Contig ID/name
        length : Union[int, str]
            Contig length in base pairs
        key : str, optional
            Metadata key (default: "contig")
            
        Examples
        --------
        >>> writer.add_contig("chr1", 249250621)
        >>> writer.add_contig("scaffold_591", 5806)
        """
        self._ensure_open()
        print(f"##{key}=<ID={id},length={length}>", file=self.w_file)

    def add_header_line(self, record_keys: Union[str, List[str]]) -> None:
        """
        Add the header line with column names to VCF file.
        
        Parameters
        ----------
        record_keys : Union[str, List[str]]
            Column header line (e.g., "#CHROM\tPOS\tID..." or list of column names)
            
        Examples
        --------
        >>> writer.add_header_line("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1")
        >>> writer.add_header_line(["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "Sample1"])
        """
        self._ensure_open()
        if isinstance(record_keys, list):
            header_line = "\t".join(record_keys)
        else:
            header_line = record_keys
        print(header_line, file=self.w_file)

    def add_record_value(self, preheader: str, info: str, format_: str, sample_str: str) -> None:
        """
        Add a data record line to VCF file.
        
        Parameters
        ----------
        preheader : str
            Pre-INFO columns (CHROM, POS, ID, REF, ALT, QUAL, FILTER)
        info : str
            INFO column value
        format_ : str
            FORMAT column value  
        sample_str : str
            Sample columns values
            
        Examples
        --------
        >>> writer.add_record_value(
        ...     "chr1\t123\t.\tA\tT\t60\tPASS",
        ...     "DP=20;AF=0.5", 
        ...     "GT:DP", 
        ...     "1/1:20"
        ... )
        """
        self._ensure_open()
        record_parts = [preheader, info, format_, sample_str]
        record_line = "\t".join(record_parts)
        print(record_line, file=self.w_file)
        
    def add_record_from_parts(self, chrom: str, pos: Union[int, str], id: str = ".", 
                             ref: str = ".", alt: str = ".", qual: str = ".", 
                             filter_val: str = ".", info: str = ".", 
                             format_val: str = "", *sample_values: str) -> None:
        """
        Add a VCF record from individual field components.
        
        Parameters
        ----------
        chrom : str
            Chromosome/contig name
        pos : Union[int, str]
            Position
        id : str, optional
            Variant ID (default: ".")
        ref : str, optional
            Reference allele (default: ".")
        alt : str, optional
            Alternate allele(s) (default: ".")
        qual : str, optional
            Quality score (default: ".")
        filter_val : str, optional
            Filter status (default: ".")
        info : str, optional
            INFO field (default: ".")
        format_val : str, optional
            FORMAT field (default: "")
        *sample_values : str
            Sample column values
            
        Examples
        --------
        >>> writer.add_record_from_parts(
        ...     "chr1", 123, "rs123", "A", "T", "60", "PASS", 
        ...     "DP=20;AF=0.5", "GT:DP", "1/1:20", "0/1:15"
        ... )
        """
        self._ensure_open()
        record_parts = [str(chrom), str(pos), id, ref, alt, qual, filter_val, info]
        
        if format_val:
            record_parts.append(format_val)
            record_parts.extend(sample_values)
        elif sample_values:
            # If samples provided but no format, add empty format field
            record_parts.append("")
            record_parts.extend(sample_values)
            
        record_line = "\t".join(record_parts)
        print(record_line, file=self.w_file)
    
    def __del__(self) -> None:
        """Destructor to ensure file is closed."""
        self.close()
