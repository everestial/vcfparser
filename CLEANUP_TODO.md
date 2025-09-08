# Project Cleanup & Organization TODO

## 🧹 File Cleanup Tasks

### 🔴 **Remove Unnecessary Files**
```bash
# Temporary/Personal files
rm testing_self.md
rm after_type_hints.csv  
rm baseline_results.csv
rm pre_commit_final.csv
rm PRE_COMMIT_TEST_REPORT.md

# System files  
rm .DS_Store

# Legacy CI (Travis CI is deprecated)
rm .travis.yml

# Outdated build files
rm make.bat

# Empty requirements file 
rm requirements.txt
```

### 🟡 **Consider Removing**
- **`tox.ini`** - Multi-environment testing config (not currently used)

---

## 📂 **File Organization Tasks**

### **Testing Files Consolidation**
Current scattered testing files:
```
├── tests/                    # Legacy integration tests
├── tests_new/               # New comprehensive unit tests  
├── benchmarks/              # Performance benchmarks
├── run_tests.py            # Python test runner
├── run_tests.sh            # Bash test runner
├── pytest.ini             # Pytest configuration
├── mypy.ini               # Type checking config
├── TESTING.md             # Testing documentation
└── input_test.vcf         # Test data file
└── write_test.vcf         # Test output file
```

### **Proposed Reorganization**:
```
├── tests/
│   ├── integration/        # Legacy integration tests (from tests/)
│   ├── unit/              # New unit tests (from tests_new/unit/)
│   ├── benchmarks/        # Performance tests (from benchmarks/)  
│   ├── data/              # Test data files
│   │   ├── input_test.vcf
│   │   ├── full_vcf43.vcf.gz
│   │   └── outputs/       # Test output files (write_test.vcf, etc.)
│   ├── config/            # Test configuration
│   │   ├── pytest.ini
│   │   └── mypy.ini
│   ├── runners/           # Test execution scripts
│   │   ├── run_tests.py
│   │   └── run_tests.sh
│   ├── reports/           # Test reports and docs
│   │   ├── TEST_FAILURES.md
│   │   ├── TODO_TEST_FIXES.md
│   │   └── TESTING.md
│   └── conftest.py        # Shared test configuration
```

---

## 📋 **Documentation Organization**

### **Current Documentation Files**:
```
├── README.md              # Main project README
├── WARP.md               # Development guide  
├── TESTING.md            # Testing documentation
├── MODERNIZATION_PLAN.md # Development strategy
├── PROGRESS_LOG.md       # Progress tracking
├── DEVELOPMENT_STRATEGY.md # Integration roadmap
├── docs/                 # Sphinx documentation
└── LICENSE               # License file
```

### **Proposed Documentation Structure**:
```
├── README.md              # Main project README (keep at root)
├── LICENSE               # License (keep at root)
├── docs/
│   ├── development/      # Development guides
│   │   ├── WARP.md
│   │   ├── MODERNIZATION_PLAN.md
│   │   ├── PROGRESS_LOG.md
│   │   └── DEVELOPMENT_STRATEGY.md
│   ├── testing/          # Testing documentation
│   │   └── TESTING.md
│   └── api/              # API documentation (current sphinx docs)
│       ├── AUTHORS.rst
│       ├── conf.py
│       ├── index.rst
│       └── ...
```

---

## 🔧 **Build & Config Organization**

### **Current Config Files**:
```
├── setup.py              # Legacy setup
├── pyproject.toml        # Modern Python packaging
├── uv.lock              # UV dependency lock
├── .gitignore           # Git ignore rules
```

### **Proposed Structure**:
```
├── pyproject.toml        # Main build config (keep at root)
├── uv.lock              # Dependency lock (keep at root)  
├── .gitignore           # Git config (keep at root)
├── config/              # Additional configurations
│   └── (future config files as needed)
```

---

## 🎯 **Implementation Priority**

### **Phase 1: Immediate Cleanup** (Low Risk)
1. Remove unnecessary files (`.DS_Store`, temp CSVs, etc.)
2. Update `.gitignore` to prevent future clutter

### **Phase 2: Testing Reorganization** (Medium Risk)  
1. Move test files to unified structure
2. Update import paths in test files
3. Update test runner paths
4. Update CI/CD configurations

### **Phase 3: Address the TODO items** (Medium Risk)  
1. Address the TODO items that are open in the codebases for several functions, scripts

### **Phase 4: Documentation Reorganization** (Low Risk)
1. Move documentation to `docs/` subdirectories
2. Update internal documentation links
3. Update main README.md references

### **Phase 5: Advanced Organization** (Future)
1. Consider package structure improvements
2. Evaluate build system optimizations
3. Review and optimize development workflows

---

## 📋 **Benefits of Reorganization**

### **Developer Experience**:
- ✅ Cleaner project root directory
- ✅ Logical grouping of related files  
- ✅ Easier navigation and maintenance
- ✅ Better separation of concerns

### **Project Maintenance**:
- ✅ Reduced clutter and confusion
- ✅ Easier onboarding for new contributors
- ✅ Clearer project structure
- ✅ Better alignment with Python packaging standards

### **CI/CD Benefits**:
- ✅ Cleaner test execution
- ✅ Better test organization
- ✅ Easier maintenance of test suites

---

**Note**: This is a future task list. Current project structure works well and all tests are passing. Reorganization should be done incrementally to avoid breaking existing workflows.

**Created**: 2025-01-07  
**Status**: Planning phase - ready for future implementation
