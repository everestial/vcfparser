# Testing Guide for vcfparser

This document provides comprehensive information about running tests in the vcfparser project. We provide both bash and Python test runners for maximum compatibility across different platforms.

## Test Runners

### 1. Python Test Runner (Recommended - Cross-platform)

The `run_tests.py` script is the recommended way to run tests as it works on all platforms (Windows, macOS, Linux).

#### Usage Options:

```bash
# Run all tests (comprehensive test suite)
python run_tests.py

# Run only critical tests (fast feedback for development)  
python run_tests.py --quick

# Type checking only (mypy validation)
python run_tests.py --type-only

# Performance benchmarks only
python run_tests.py --benchmark

# Full pre-commit suite (includes all tests + benchmarks)
python run_tests.py --commit-ready
```

#### Key Features:

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux without shell dependencies
- **Colored terminal output**: Uses ANSI color codes for better visual feedback
- **Automatic virtual environment detection**: Checks for and reports on virtual environment status
- **Comprehensive test tracking**: Tracks pass/fail statistics across all test suites
- **Smart error handling**: Captures and displays command output appropriately
- **Detailed summary reports**: Shows overall statistics and component status

### 2. Bash Test Runner (Unix/Linux/macOS only)

The `run_tests.sh` script provides the same functionality but only works on Unix-like systems.

```bash
# Make executable (first time only)
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Quick tests only
./run_tests.sh --quick

# Type checking only  
./run_tests.sh --type-only

# Benchmarks only
./run_tests.sh --benchmark

# Full pre-commit suite
./run_tests.sh --commit-ready
```

## What the Test Runners Do

Both test runners execute the following test suites:

### 1. **Integration Tests** (Critical - 12 tests)
- Location: `tests/test_parser.py`
- Tests core VCF parsing functionality
- Validates metadata and record parsing
- **Must pass** for code to be commit-ready

### 2. **Legacy Unit Tests** (Critical - 36 tests)
- Location: `tests/testvcfparser/`
- Comprehensive unit tests for all modules:
  - `test_meta_header_parser.py`: 4 tests
  - `test_record_parser.py`: 22 tests
  - `test_vcf_parser.py`: 2 tests
  - `test_vcf_writer.py`: 8 tests
- **Must pass** for code to be commit-ready

### 3. **New Comprehensive Tests** (89/93 passing)
- Location: `tests_new/`
- Extended test coverage with modern testing practices
- 4 expected failures are documented in `TODO_TEST_FIXES.md`
- These failures are related to edge case error handling

### 4. **Type Checking** (mypy)
- Validates type hints in `vcf_parser.py`
- Uses configuration from `mypy.ini`
- **Must pass** for code to be commit-ready

### 5. **Core Integration Test** (Critical)
- Verifies the `iupac_to_numeric` bug fix
- Tests critical genotype analysis functionality
- Quick smoke test for core features
- **Must pass** for code to be commit-ready

### 6. **Performance Benchmarks** (Optional)
- Location: `benchmarks/benchmark_suite.py`
- Measures parsing performance and memory usage
- Provides baseline performance metrics
- Only run with `--benchmark` or `--commit-ready` flags

## Test Results Interpretation

### Success Indicators:
- **Integration Tests**: 12/12 passed ✅
- **Legacy Unit Tests**: 36/36 passed ✅  
- **Type Checking**: 0 errors found ✅
- **Core Integration**: All critical functionality working ✅

### Expected Failures:
- **New Comprehensive Tests**: 89/93 passed (4 expected failures)
  - These 4 failures are documented and relate to error handling edge cases
  - They do not affect core functionality

### Commit Readiness:
The code is **READY TO COMMIT** when:
- All critical tests pass (Integration + Legacy + Core Integration)
- Type checking passes with 0 errors
- Performance benchmarks complete successfully (if run)

## Development Workflow Integration

### Quick Development Feedback:
```bash
# Fast feedback during development (< 30 seconds)
python run_tests.py --quick
```

### Pre-commit Validation:
```bash
# Full validation before committing (2-3 minutes)
python run_tests.py --commit-ready
```

### Type Safety Validation:
```bash
# Quick type checking (< 10 seconds)
python run_tests.py --type-only
```

### Performance Monitoring:
```bash
# Baseline performance measurement (30-60 seconds)
python run_tests.py --benchmark
```

## Virtual Environment Requirements

Both test runners work best with an activated virtual environment:

```bash
# Activate virtual environment
source .venv/bin/activate

# Then run tests
python run_tests.py
```

The Python test runner will detect and report virtual environment status automatically.

## Continuous Integration (CI)

For CI/CD pipelines, use the Python test runner with appropriate flags:

```yaml
# Example CI configuration
script:
  - python run_tests.py --commit-ready  # Full test suite
```

The script returns appropriate exit codes:
- `0`: All tests passed
- `1`: Critical tests failed

## Test Data Requirements

The test suites require these sample files:
- `input_test.vcf` - Main test VCF file
- `full_vcf43.vcf.gz` - Compressed VCF example
- `write_test.vcf` - Output file for write operations

These files are included in the repository and automatically used by the test suites.

## Troubleshooting

### Common Issues:

1. **Virtual Environment Not Found**
   - Ensure `.venv/` directory exists
   - Activate virtual environment manually: `source .venv/bin/activate`

2. **Import Errors**
   - Install vcfparser in development mode: `pip install -e .`
   - Ensure all dependencies are installed

3. **Permission Errors (bash script)**
   - Make script executable: `chmod +x run_tests.sh`
   - Use Python runner instead: `python run_tests.py`

4. **Type Checking Errors**
   - Check `mypy.ini` configuration
   - Ensure py.typed marker file exists
   - Run `python -m mypy --version` to verify mypy installation

### Getting Help:

For issues with the test runners or interpreting results:
1. Check the detailed output from the test runner
2. Review individual test failure messages
3. Check `TODO_TEST_FIXES.md` for known issues
4. Refer to the main project documentation

## Performance Expectations

- **Quick tests**: ~30 seconds
- **Full test suite**: ~2-3 minutes  
- **Type checking only**: ~10 seconds
- **Benchmarks only**: ~30-60 seconds
- **Commit-ready suite**: ~3-4 minutes

These times may vary based on system performance and test data size.
