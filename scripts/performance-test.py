#!/usr/bin/env python3
"""
Performance Testing Script for Password Cracking Tools
Benchmarks Hashcat and John the Ripper performance across different hash types and configurations.
"""

import subprocess
import time
import json
import csv
import argparse
import sys
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class PasswordCrackingBenchmark:
    def __init__(self):
        self.results = {}
        self.system_info = self.gather_system_info()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def gather_system_info(self) -> Dict:
        """Collect system information for benchmark context."""
        system_info = {
            'timestamp': datetime.now().isoformat(),
            'platform': sys.platform
        }
        
        try:
            # CPU information
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo', 'r') as f:
                    cpu_info = f.read()
                    cpu_model = re.search(r'model name\s*:\s*(.+)', cpu_info)
                    if cpu_model:
                        system_info['cpu'] = cpu_model.group(1).strip()
                        
            # Memory information
            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r') as f:
                    mem_info = f.read()
                    mem_total = re.search(r'MemTotal:\s*(\d+)', mem_info)
                    if mem_total:
                        system_info['memory_gb'] = int(mem_total.group(1)) // 1024 // 1024
                        
            # GPU information (if available)
            try:
                gpu_result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                          capture_output=True, text=True, timeout=5)
                if gpu_result.returncode == 0:
                    system_info['gpu'] = gpu_result.stdout.strip().split('\n')[0]
            except:
                system_info['gpu'] = 'Not available'
                
        except Exception as e:
            print(f"Warning: Could not gather complete system information: {e}")
            
        return system_info
    
    def check_tool_availability(self) -> Tuple[bool, bool]:
        """Check if Hashcat and John the Ripper are available."""
        hashcat_available = False
        john_available = False
        
        try:
            subprocess.run(['hashcat', '--version'], capture_output=True, timeout=5)
            hashcat_available = True
        except:
            print("Warning: Hashcat not found or not accessible")
            
        try:
            subprocess.run(['john', '--version'], capture_output=True, timeout=5)
            john_available = True
        except:
            print("Warning: John the Ripper not found or not accessible")
            
        return hashcat_available, john_available
    
    def benchmark_hashcat(self) -> Dict:
        """Run Hashcat benchmark and parse results."""
        print("Running Hashcat benchmark...")
        
        try:
            result = subprocess.run(['hashcat', '-b', '-m', '0,100,1400,3200,1800'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"Hashcat benchmark failed: {result.stderr}")
                return {}
                
            return self.parse_hashcat_benchmark(result.stdout)
            
        except subprocess.TimeoutExpired:
            print("Hashcat benchmark timed out")
            return {}
        except Exception as e:
            print(f"Hashcat benchmark error: {e}")
            return {}
    
    def parse_hashcat_benchmark(self, output: str) -> Dict:
        """Parse Hashcat benchmark output."""
        results = {}
        hash_types = {
            '0': 'MD5',
            '100': 'SHA1', 
            '1400': 'SHA256',
            '3200': 'bcrypt',
            '1800': 'SHA512'
        }
        
        lines = output.split('\n')
        for line in lines:
            if 'H/s' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part in hash_types:
                        try:
                            # Find the H/s value
                            for j in range(i+1, len(parts)):
                                if 'H/s' in parts[j]:
                                    speed_str = parts[j-1]
                                    speed = self.parse_hashcat_speed(speed_str)
                                    results[hash_types[part]] = {
                                        'speed_hs': speed,
                                        'speed_formatted': parts[j-1] + ' ' + parts[j]
                                    }
                                    break
                        except:
                            continue
                            
        return results
    
    def parse_hashcat_speed(self, speed_str: str) -> float:
        """Parse Hashcat speed string to numeric value."""
        multipliers = {'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}
        
        try:
            if speed_str[-1] in multipliers:
                return float(speed_str[:-1]) * multipliers[speed_str[-1]]
            else:
                return float(speed_str)
        except:
            return 0.0
    
    def benchmark_john(self) -> Dict:
        """Run John the Ripper benchmark."""
        print("Running John the Ripper benchmark...")
        
        try:
            result = subprocess.run(['john', '--test=10'], 
                                  capture_output=True, text=True, timeout=60)
            
            return self.parse_john_benchmark(result.stdout + result.stderr)
            
        except subprocess.TimeoutExpired:
            print("John the Ripper benchmark timed out")
            return {}
        except Exception as e:
            print(f"John the Ripper benchmark error: {e}")
            return {}
    
    def parse_john_benchmark(self, output: str) -> Dict:
        """Parse John the Ripper benchmark output."""
        results = {}
        
        lines = output.split('\n')
        for line in lines:
            if 'c/s' in line.lower():
                # Extract hash type and speed
                if ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        hash_type = parts[0].strip()
                        speed_part = parts[1].strip()
                        
                        # Extract speed value
                        speed_match = re.search(r'(\d+(?:\.\d+)?[KMG]?)\s*c/s', speed_part, re.IGNORECASE)
                        if speed_match:
                            speed_str = speed_match.group(1)
                            speed = self.parse_john_speed(speed_str)
                            results[hash_type] = {
                                'speed_cs': speed,
                                'speed_formatted': speed_match.group(0)
                            }
                            
        return results
    
    def parse_john_speed(self, speed_str: str) -> float:
        """Parse John the Ripper speed string to numeric value."""
        multipliers = {'K': 1e3, 'M': 1e6, 'G': 1e9}
        
        try:
            if speed_str[-1] in multipliers:
                return float(speed_str[:-1]) * multipliers[speed_str[-1]]
            else:
                return float(speed_str)
        except:
            return 0.0
    
    def run_attack_performance_test(self) -> Dict:
        """Run actual attack performance tests with sample data."""
        print("Running attack performance tests...")
        
        # Create test hash file
        test_hashes = [
            "5f4dcc3b5aa765d61d8327deb882cf99",  # password
            "e10adc3949ba59abbe56e057f20f883e",  # 123456
            "21232f297a57a5a743894a0e4a801fc3"   # admin
        ]
        
        hash_file = f"test_hashes_{self.timestamp}.txt"
        with open(hash_file, 'w') as f:
            for hash_val in test_hashes:
                f.write(f"{hash_val}\n")
        
        # Create small wordlist
        wordlist_file = f"test_wordlist_{self.timestamp}.txt"
        wordlist = ["password", "123456", "admin", "test", "hello", "world", "secret"]
        with open(wordlist_file, 'w') as f:
            for word in wordlist:
                f.write(f"{word}\n")
        
        results = {}
        
        # Test Hashcat dictionary attack
        try:
            start_time = time.time()
            result = subprocess.run([
                'hashcat', '-m', '0', hash_file, wordlist_file, 
                '--potfile-disable', '--quiet'
            ], capture_output=True, text=True, timeout=30)
            
            elapsed_time = time.time() - start_time
            results['hashcat_dictionary'] = {
                'time_seconds': elapsed_time,
                'success': result.returncode == 0
            }
        except:
            results['hashcat_dictionary'] = {'time_seconds': 0, 'success': False}
        
        # Test John dictionary attack
        try:
            start_time = time.time()
            result = subprocess.run([
                'john', '--wordlist=' + wordlist_file, hash_file, '--format=Raw-MD5'
            ], capture_output=True, text=True, timeout=30)
            
            elapsed_time = time.time() - start_time
            results['john_dictionary'] = {
                'time_seconds': elapsed_time,
                'success': result.returncode == 0
            }
        except:
            results['john_dictionary'] = {'time_seconds': 0, 'success': False}
        
        # Cleanup
        try:
            os.remove(hash_file)
            os.remove(wordlist_file)
        except:
            pass
        
        return results
    
    def generate_report(self) -> Dict:
        """Generate comprehensive performance report."""
        hashcat_available, john_available = self.check_tool_availability()
        
        report = {
            'metadata': {
                'timestamp': self.timestamp,
                'system_info': self.system_info,
                'tools_available': {
                    'hashcat': hashcat_available,
                    'john_the_ripper': john_available
                }
            },
            'benchmarks': {},
            'performance_tests': {}
        }
        
        if hashcat_available:
            report['benchmarks']['hashcat'] = self.benchmark_hashcat()
            
        if john_available:
            report['benchmarks']['john_the_ripper'] = self.benchmark_john()
        
        if hashcat_available or john_available:
            report['performance_tests'] = self.run_attack_performance_test()
        
        return report
    
    def save_results(self, report: Dict, output_dir: str = "."):
        """Save benchmark results to files."""
        # Save JSON report
        json_file = os.path.join(output_dir, f"performance_report_{self.timestamp}.json")
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save CSV summary
        csv_file = os.path.join(output_dir, f"performance_summary_{self.timestamp}.csv")
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tool', 'Hash Type', 'Speed (H/s)', 'Speed Formatted'])
            
            # Hashcat results
            hashcat_data = report.get('benchmarks', {}).get('hashcat', {})
            for hash_type, data in hashcat_data.items():
                writer.writerow(['Hashcat', hash_type, data.get('speed_hs', 0), 
                               data.get('speed_formatted', '')])
            
            # John the Ripper results  
            john_data = report.get('benchmarks', {}).get('john_the_ripper', {})
            for hash_type, data in john_data.items():
                writer.writerow(['John the Ripper', hash_type, data.get('speed_cs', 0), 
                               data.get('speed_formatted', '')])
        
        print(f"Results saved to:")
        print(f"  JSON Report: {json_file}")
        print(f"  CSV Summary: {csv_file}")
    
    def print_summary(self, report: Dict):
        """Print benchmark summary to console."""
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("="*60)
        
        print(f"\nSystem Information:")
        sys_info = report['metadata']['system_info']
        print(f"  Timestamp: {sys_info.get('timestamp', 'Unknown')}")
        print(f"  CPU: {sys_info.get('cpu', 'Unknown')}")
        print(f"  Memory: {sys_info.get('memory_gb', 'Unknown')} GB")
        print(f"  GPU: {sys_info.get('gpu', 'Unknown')}")
        
        print(f"\nTool Availability:")
        tools = report['metadata']['tools_available']
        print(f"  Hashcat: {'Available' if tools['hashcat'] else 'Not Available'}")
        print(f"  John the Ripper: {'Available' if tools['john_the_ripper'] else 'Not Available'}")
        
        # Hashcat results
        hashcat_results = report.get('benchmarks', {}).get('hashcat', {})
        if hashcat_results:
            print(f"\nHashcat Benchmark Results:")
            for hash_type, data in hashcat_results.items():
                print(f"  {hash_type}: {data.get('speed_formatted', 'N/A')}")
        
        # John the Ripper results
        john_results = report.get('benchmarks', {}).get('john_the_ripper', {})
        if john_results:
            print(f"\nJohn the Ripper Benchmark Results:")
            for hash_type, data in john_results.items():
                print(f"  {hash_type}: {data.get('speed_formatted', 'N/A')}")
        
        # Performance test results
        perf_tests = report.get('performance_tests', {})
        if perf_tests:
            print(f"\nAttack Performance Tests:")
            for test_name, data in perf_tests.items():
                status = "Success" if data.get('success', False) else "Failed"
                time_str = f"{data.get('time_seconds', 0):.2f}s"
                print(f"  {test_name}: {status} ({time_str})")

def main():
    parser = argparse.ArgumentParser(description="Password cracking performance benchmark tool")
    parser.add_argument('--output-dir', default='.', help='Output directory for results')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    parser.add_argument('--json-only', action='store_true', help='Only output JSON report')
    
    args = parser.parse_args()
    
    # Initialize benchmark
    benchmark = PasswordCrackingBenchmark()
    
    if not args.quiet:
        print("Starting Password Cracking Performance Benchmark...")
        print(f"System: {benchmark.system_info.get('cpu', 'Unknown CPU')}")
        print(f"Memory: {benchmark.system_info.get('memory_gb', 'Unknown')} GB")
        print(f"GPU: {benchmark.system_info.get('gpu', 'Unknown')}")
        print("-" * 60)
    
    # Run benchmark
    try:
        report = benchmark.generate_report()
        benchmark.save_results(report, args.output_dir)
        
        if not args.json_only:
            benchmark.print_summary(report)
            
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError running benchmark: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()