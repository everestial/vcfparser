
## Tests  

cd /Volumes/D/Project_VcfSimplify/vcfparser && source .venv/bin/activate && python -m pytest tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors::test_missing_fileformat_value -v


# Run a specific test method
python -m pytest tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors::test_missing_fileformat_value -v

# Run a specific test class
python -m pytest tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors -v

# Run all tests in a file
python -m pytest tests_new/unit/test_meta_header_parser.py -v

# Run with more detailed output
python -m pytest tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors::test_missing_fileformat_value -v -s

