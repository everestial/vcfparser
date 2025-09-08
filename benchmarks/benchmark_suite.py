#!/usr/bin/env python3
"""
vcfparser Benchmarking Suite

This script measures the performance of vcfparser operations to establish
baselines and track improvements during the modernization process.

Usage:
    python benchmarks/benchmark_suite.py
    python benchmarks/benchmark_suite.py --detailed
    python benchmarks/benchmark_suite.py --memory
"""

import argparse
import time
import tracemalloc
import psutil
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add vcfparser to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from vcfparser import VcfParser
except ImportError:
    print("Error: vcfparser not found. Make sure it's installed or in PYTHONPATH")
    sys.exit(1)


@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    operation: str
    time_seconds: float
    memory_peak_mb: float
    records_processed: int = 0
    records_per_second: float = 0.0
    
    def __post_init__(self):
        if self.records_processed > 0 and self.time_seconds > 0:
            self.records_per_second = self.records_processed / self.time_seconds


class VCFBenchmarker:
    """Benchmark suite for vcfparser operations."""
    
    def __init__(self, vcf_file: str = "input_test.vcf"):
        """
        Initialize benchmarker with VCF file.
        
        Args:
            vcf_file: Path to VCF file for testing
        """
        self.vcf_file = Path(vcf_file)
        if not self.vcf_file.exists():
            raise FileNotFoundError(f"VCF file not found: {vcf_file}")
        
        self.results: List[BenchmarkResult] = []
        
    def _measure_memory_and_time(self, func, *args, **kwargs) -> Tuple[float, float, any]:
        """
        Measure execution time and peak memory usage of a function.
        
        Returns:
            Tuple of (time_seconds, peak_memory_mb, return_value)
        """
        # Start memory tracking
        tracemalloc.start()
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Measure execution time
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        # Get peak memory
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        peak_memory = max(peak / 1024 / 1024, final_memory - initial_memory)
        
        execution_time = end_time - start_time
        
        return execution_time, peak_memory, result
    
    def benchmark_parse_metadata(self) -> BenchmarkResult:
        """Benchmark metadata parsing."""
        def parse_metadata():
            vcf = VcfParser(str(self.vcf_file))
            return vcf.parse_metadata()
        
        time_taken, memory_used, metadata = self._measure_memory_and_time(parse_metadata)
        
        result = BenchmarkResult(
            operation="parse_metadata",
            time_seconds=time_taken,
            memory_peak_mb=memory_used
        )
        self.results.append(result)
        return result
    
    def benchmark_parse_records(self, limit: Optional[int] = None) -> BenchmarkResult:
        """Benchmark record parsing."""
        def parse_records():
            vcf = VcfParser(str(self.vcf_file))
            records = vcf.parse_records()
            count = 0
            for record in records:
                count += 1
                if limit and count >= limit:
                    break
            return count
        
        time_taken, memory_used, record_count = self._measure_memory_and_time(parse_records)
        
        result = BenchmarkResult(
            operation=f"parse_records{'_' + str(limit) if limit else ''}",
            time_seconds=time_taken,
            memory_peak_mb=memory_used,
            records_processed=record_count
        )
        self.results.append(result)
        return result
    
    def benchmark_genotype_analysis(self, limit: int = 1000) -> BenchmarkResult:
        """Benchmark genotype analysis methods."""
        def analyze_genotypes():
            vcf = VcfParser(str(self.vcf_file))
            records = vcf.parse_records()
            count = 0
            
            for record in records:
                # Test common genotype operations
                record.genotype_property.isHOMREF()
                record.genotype_property.isHOMVAR()
                record.genotype_property.isHETVAR()
                record.genotype_property.isMissing()
                
                count += 1
                if count >= limit:
                    break
            return count
        
        time_taken, memory_used, record_count = self._measure_memory_and_time(analyze_genotypes)
        
        result = BenchmarkResult(
            operation="genotype_analysis",
            time_seconds=time_taken,
            memory_peak_mb=memory_used,
            records_processed=record_count
        )
        self.results.append(result)
        return result
    
    def benchmark_info_parsing(self, limit: int = 1000) -> BenchmarkResult:
        """Benchmark INFO field parsing."""
        def parse_info():
            vcf = VcfParser(str(self.vcf_file))
            records = vcf.parse_records()
            count = 0
            
            for record in records:
                record.get_info_as_dict()
                count += 1
                if count >= limit:
                    break
            return count
        
        time_taken, memory_used, record_count = self._measure_memory_and_time(parse_info)
        
        result = BenchmarkResult(
            operation="info_parsing",
            time_seconds=time_taken,
            memory_peak_mb=memory_used,
            records_processed=record_count
        )
        self.results.append(result)
        return result
    
    def benchmark_format_mapping(self, limit: int = 1000) -> BenchmarkResult:
        """Benchmark FORMAT to sample mapping."""
        def map_formats():
            vcf = VcfParser(str(self.vcf_file))
            records = vcf.parse_records()
            count = 0
            
            for record in records:
                record.get_format_to_sample_map()
                count += 1
                if count >= limit:
                    break
            return count
        
        time_taken, memory_used, record_count = self._measure_memory_and_time(map_formats)
        
        result = BenchmarkResult(
            operation="format_mapping",
            time_seconds=time_taken,
            memory_peak_mb=memory_used,
            records_processed=record_count
        )
        self.results.append(result)
        return result
    
    def run_full_suite(self, detailed: bool = False) -> List[BenchmarkResult]:
        """Run the complete benchmark suite."""
        print(f"Starting benchmark suite with {self.vcf_file.name}...")
        print(f"File size: {self.vcf_file.stat().st_size / 1024 / 1024:.2f} MB")
        print("-" * 60)
        
        # Core benchmarks
        self.benchmark_parse_metadata()
        
        if detailed:
            # Run detailed benchmarks with different limits
            for limit in [100, 1000, 5000]:
                self.benchmark_parse_records(limit)
                self.benchmark_genotype_analysis(limit)
                self.benchmark_info_parsing(limit)
                self.benchmark_format_mapping(limit)
        else:
            # Quick benchmarks
            self.benchmark_parse_records(1000)
            self.benchmark_genotype_analysis(500)
            self.benchmark_info_parsing(500)
            self.benchmark_format_mapping(500)
        
        return self.results
    
    def print_results(self):
        """Print benchmark results in a formatted table."""
        print("\n" + "="*80)
        print("BENCHMARK RESULTS")
        print("="*80)
        
        print(f"{'Operation':<20} {'Time (s)':<10} {'Memory (MB)':<12} {'Records':<8} {'Rec/s':<10}")
        print("-" * 80)
        
        for result in self.results:
            records_str = str(result.records_processed) if result.records_processed > 0 else "N/A"
            rps_str = f"{result.records_per_second:.0f}" if result.records_per_second > 0 else "N/A"
            
            print(f"{result.operation:<20} {result.time_seconds:<10.4f} "
                  f"{result.memory_peak_mb:<12.2f} {records_str:<8} {rps_str:<10}")
    
    def save_results(self, filename: str = "benchmark_results.csv"):
        """Save results to CSV file."""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Operation', 'Time_Seconds', 'Memory_MB', 'Records_Processed', 'Records_Per_Second'])
            
            for result in self.results:
                writer.writerow([
                    result.operation,
                    result.time_seconds,
                    result.memory_peak_mb,
                    result.records_processed,
                    result.records_per_second
                ])
        
        print(f"\nResults saved to {filename}")


def main():
    """Main benchmarking script."""
    parser = argparse.ArgumentParser(description="vcfparser Performance Benchmarking")
    parser.add_argument("--vcf", default="input_test.vcf", 
                       help="VCF file to use for benchmarking")
    parser.add_argument("--detailed", action="store_true",
                       help="Run detailed benchmarks with multiple limits")
    parser.add_argument("--save", type=str, 
                       help="Save results to CSV file")
    parser.add_argument("--memory", action="store_true",
                       help="Focus on memory usage benchmarks")
    
    args = parser.parse_args()
    
    try:
        benchmarker = VCFBenchmarker(args.vcf)
        
        # Run benchmarks
        results = benchmarker.run_full_suite(detailed=args.detailed)
        
        # Display results
        benchmarker.print_results()
        
        # Save results if requested
        if args.save:
            benchmarker.save_results(args.save)
        
        # Summary
        total_time = sum(r.time_seconds for r in results)
        peak_memory = max(r.memory_peak_mb for r in results)
        
        print(f"\nSUMMARY:")
        print(f"Total benchmark time: {total_time:.2f} seconds")
        print(f"Peak memory usage: {peak_memory:.2f} MB")
        print(f"vcfparser version: Available (no version info yet)")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Benchmark failed: {e}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())
