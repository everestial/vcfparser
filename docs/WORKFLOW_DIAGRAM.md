# vcfparser Usage Workflow

## Quick Visual Guide

```
📁 VCF File
    │
    ▼
🔍 VcfParser("example.vcf")
    │
    ├─── parse_metadata() ──➤ 📊 MetaDataViewer ──➤ 📄 Export Files
    │                             │                      ├─ .json
    │                             │                      ├─ .table  
    │                             │                      └─ .dict
    │
    └─── parse_records() ───➤ 🧬 Record Objects ──➤ 🔬 Genotype Analysis
                                  │                      ├─ isHOMREF()
                                  │                      ├─ isHETVAR()
                                  │                      ├─ isHOMVAR()
                                  │                      ├─ hasSNP()
                                  │                      └─ hasINDEL()
                                  │
                                  └─── Sample Data ──➤ 📈 Statistics
```

## Three Main Use Cases

### 1. 📖 Reading & Analyzing VCF Files
```
VCF Input ──➤ VcfParser ──➤ Analysis ──➤ Results
```

### 2. 📊 Metadata Export & Visualization  
```
VCF Input ──➤ MetaDataViewer ──➤ Export ──➤ Reports
```

### 3. ✍️ Writing New VCF Files
```
Your Data ──➤ VCFWriter ──➤ VCF Output
```

## Component Interaction

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   VCF File  │───▶│  VcfParser   │───▶│   Records   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                     │
                           ▼                     ▼
                   ┌──────────────┐    ┌─────────────────┐
                   │   Metadata   │    │ GenotypeProperty│
                   └──────────────┘    └─────────────────┘
                           │                     │
                           ▼                     ▼
                   ┌──────────────┐    ┌─────────────────┐
                   │MetaDataViewer│    │   Analysis      │
                   └──────────────┘    └─────────────────┘
```

## Type Safety Flow

```
📝 Type Hints ──➤ 🔍 mypy ──➤ ✅ Static Analysis ──➤ 🚀 Reliable Code
```

All classes and methods include comprehensive type annotations for:
- IDE autocompletion
- Static type checking  
- Runtime error prevention
- Better code documentation
