# TODO: Test Fixes for vcfparser

## Status: 4 Failed Tests to Address

The following tests failed during the test run on 2025-09-07. These need to be analyzed and fixed - either by correcting the code logic (preferred) or adjusting the test expectations.

---

## 1. MetaDataParser Error Handling Tests (2 failures)

### FAILED: `test_missing_fileformat_value`
**Location**: `tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors`
**Error**: `Failed: DID NOT RAISE <class 'SyntaxError'>`

**Issue**: Test expects a `SyntaxError` with message "fileformat must have a value" when `##fileformat=` is empty, but the code doesn't raise this exception.

**Test Code**:
```python
def test_missing_fileformat_value(self):
    """Test handling of missing fileformat value."""
    bad_lines = [
        "##fileformat=\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
    ]

    parser = MetaDataParser(bad_lines)
    with pytest.raises(SyntaxError, match="fileformat must have a value"):
        parser.parse_fileformat()
```

**Action Needed**: 
- [ ] **PREFERRED**: Update `MetaDataParser.parse_fileformat()` to raise `SyntaxError` when fileformat value is missing
- [ ] Alternative: Update test to match actual behavior

---

### FAILED: `test_missing_reference_value`
**Location**: `tests_new/unit/test_meta_header_parser.py::TestMetaDataParserErrors`
**Error**: `Failed: DID NOT RAISE <class 'SyntaxError'>`

**Issue**: Test expects a `SyntaxError` with message "Refrence value is not provided" when `##reference=` is empty, but the code doesn't raise this exception.

**Test Code**:
```python
def test_missing_reference_value(self):
    """Test handling of missing reference value."""
    bad_lines = [
        "##fileformat=VCFv4.2\n",
        "##reference=\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\n"
    ]

    parser = MetaDataParser(bad_lines)
    with pytest.raises(SyntaxError, match="Refrence value is not provided"):
        parser.parse_reference()
```

**Action Needed**:
- [ ] **PREFERRED**: Update `MetaDataParser.parse_reference()` to raise `SyntaxError` when reference value is missing
- [ ] Alternative: Update test to match actual behavior
- [ ] **Bonus**: Fix typo in expected message: "Refrence" → "Reference"

---

## 2. Record Parser Edge Cases (2 failures)

### FAILED: `test_empty_samples`
**Location**: `tests_new/unit/test_record_parser.py::TestRecordEdgeCases`
**Error**: `TypeError: 'NoneType' object is not iterable`

**Issue**: Record parser doesn't handle VCF records without sample data. The `_map_format_tags_to_sample_values()` method tries to iterate over `self.sample_names` which is `None` when there are no samples.

**Stack Trace**:
```python
def _map_format_tags_to_sample_values(self):
    """Private method to map format tags to sample values"""
    mapped_data = {}
    for i, name in enumerate(self.sample_names):  # <-- self.sample_names is None
        # ...
```

**Test Code**:
```python
def test_empty_samples(self):
    """Test record with no samples."""
    record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
    record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1', 'GT']
    record = Record(record_values, record_keys)
```

**Action Needed**:
- [ ] **PREFERRED**: Update `Record._map_format_tags_to_sample_values()` to handle `None` sample_names gracefully
- [ ] Fix in `Record.__init__()` line 44: `self.sample_names = self.record_keys[9:] if len(self.record_keys) > 9 else None`
- [ ] Should return empty dict `{}` when no samples exist

---

### FAILED: `test_malformed_info_field`
**Location**: `tests_new/unit/test_record_parser.py::TestRecordEdgeCases`
**Error**: `IndexError: list index out of range`

**Issue**: Record parser assumes FORMAT field (index 8) always exists, but this test provides only 8 fields (0-7), causing an IndexError when trying to access `self.record_values[8]`.

**Stack Trace**:
```python
def __init__(self, record_values, record_keys):
    # ...
    self.format_ = self.record_values[8].split(":")  # <-- IndexError here
```

**Test Code**:
```python
def test_malformed_info_field(self):
    """Test handling of malformed INFO fields."""
    record_keys = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
    record_values = ['chr1', '1000', '.', 'A', 'G', '30', 'PASS', 'AC=1;MALFORMED;DP=20']
    record = Record(record_values, record_keys)
```

**Action Needed**:
- [ ] **PREFERRED**: Update `Record.__init__()` to handle missing FORMAT field gracefully
- [ ] Add bounds checking before accessing `self.record_values[8]`
- [ ] Set `self.format_ = []` or `None` when FORMAT field doesn't exist
- [ ] Also handle missing sample values (indices 9+)

---

## Implementation Priority

1. **High Priority**: Record parser edge cases (fixes #3 and #4)
   - These are core functionality issues that could affect real-world VCF parsing
   - VCF files without samples are valid and should be supported

2. **Medium Priority**: MetaDataParser error handling (fixes #1 and #2)  
   - These are validation/error-reporting features
   - Current behavior might be acceptable (silent handling vs. exceptions)

---

## Testing Notes

- **Main functionality works**: 89/93 tests pass (96% success rate)
- **Core `iupac_to_numeric` fix**: ✅ Successfully implemented and tested
- **Existing integration tests**: ✅ All 12 tests pass
- **Record parser unit tests**: ✅ All 22 legacy tests pass

---

## Files to Modify

### For Record Parser Fixes:
- `vcfparser/record_parser.py` - `Record.__init__()` and `_map_format_tags_to_sample_values()` methods

### For MetaDataParser Fixes:
- `vcfparser/meta_header_parser.py` - `parse_fileformat()` and `parse_reference()` methods

### Test Files:
- `tests_new/unit/test_meta_header_parser.py`
- `tests_new/unit/test_record_parser.py`

---

**Created**: 2025-09-07  
**Status**: Open - Ready for development
