#!/bin/bash
# Password Cracking Lab Automation Script
# Automates the setup and execution of password cracking exercises

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SAMPLES_DIR="$PROJECT_ROOT/samples"
RESULTS_DIR="$PROJECT_ROOT/results"
LOG_FILE="$RESULTS_DIR/lab_session_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'  
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

print_banner() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "    Password Cracking Laboratory Automation"
    echo "    Hashcat & John the Ripper Training Suite"
    echo "=================================================="
    echo -e "${NC}"
}

check_dependencies() {
    log "Checking dependencies..."
    
    local deps=("hashcat" "john" "python3")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Missing dependencies: ${missing[*]}${NC}"
        echo "Please install missing tools and try again."
        exit 1
    fi
    
    log "All dependencies satisfied"
}

setup_directories() {
    log "Setting up directory structure..."
    
    mkdir -p "$SAMPLES_DIR"/{hashes,wordlists,results}
    mkdir -p "$RESULTS_DIR"
    mkdir -p "$PROJECT_ROOT"/{configs,analysis}
    
    log "Directory structure created"
}

generate_sample_hashes() {
    log "Generating sample hash files..."
    
    # Generate comprehensive hash samples
    python3 "$SCRIPT_DIR/hash-generator.py" --samples > "$SAMPLES_DIR/hashes/comprehensive_hashes.txt"
    
    # Extract different hash types for specific exercises
    grep "^[a-f0-9]\{32\}$" "$SAMPLES_DIR/hashes/comprehensive_hashes.txt" | head -20 > "$SAMPLES_DIR/hashes/md5_samples.txt"
    grep "^[a-f0-9]\{40\}$" "$SAMPLES_DIR/hashes/comprehensive_hashes.txt" | head -10 > "$SAMPLES_DIR/hashes/sha1_samples.txt"
    
    log "Sample hash files generated"
}

prepare_wordlists() {
    log "Preparing wordlists..."
    
    # Check for rockyou.txt
    if [[ -f "/usr/share/wordlists/rockyou.txt" ]]; then
        ln -sf "/usr/share/wordlists/rockyou.txt" "$SAMPLES_DIR/wordlists/rockyou.txt"
    elif [[ -f "/usr/share/wordlists/rockyou.txt.gz" ]]; then
        log "Extracting rockyou.txt.gz..."
        gunzip -c "/usr/share/wordlists/rockyou.txt.gz" > "$SAMPLES_DIR/wordlists/rockyou.txt"
    else
        echo -e "${YELLOW}Warning: rockyou.txt not found. Download manually.${NC}"
    fi
    
    # Create small test wordlist
    head -1000 "$SAMPLES_DIR/wordlists/rockyou.txt" > "$SAMPLES_DIR/wordlists/small_test.txt" 2>/dev/null || true
    
    log "Wordlist preparation completed"
}

run_exercise_1() {
    local exercise="Exercise 1: Basic Dictionary Attack"
    log "Starting $exercise"
    
    local hash_file="$SAMPLES_DIR/hashes/md5_samples.txt"
    local wordlist="$SAMPLES_DIR/wordlists/small_test.txt"
    local output_file="$RESULTS_DIR/exercise1_results.txt"
    
    echo -e "${GREEN}$exercise${NC}"
    echo "Target: MD5 hashes with small wordlist"
    
    # Hashcat dictionary attack
    if hashcat -m 0 "$hash_file" "$wordlist" --potfile-disable -o "$output_file" --quiet; then
        local cracked=$(wc -l < "$output_file" 2>/dev/null || echo "0")
        log "Hashcat cracked $cracked passwords"
    else
        log "Hashcat attack completed (check for results manually)"
    fi
    
    # John the Ripper attack
    local john_output="$RESULTS_DIR/exercise1_john.txt"
    john --wordlist="$wordlist" "$hash_file" --pot="$john_output.pot" 2>/dev/null || true
    john --show "$hash_file" --pot="$john_output.pot" > "$john_output" 2>/dev/null || true
    
    log "Exercise 1 completed. Results in $RESULTS_DIR"
}

run_exercise_2() {
    local exercise="Exercise 2: Rule-Based Attack"
    log "Starting $exercise"
    
    local hash_file="$SAMPLES_DIR/hashes/md5_samples.txt"
    local wordlist="$SAMPLES_DIR/wordlists/small_test.txt"
    local output_file="$RESULTS_DIR/exercise2_results.txt"
    
    echo -e "${GREEN}$exercise${NC}"
    echo "Target: MD5 hashes with rules transformation"
    
    # Use best64.rule if available
    local rule_file="/usr/share/hashcat/rules/best64.rule"
    if [[ -f "$rule_file" ]]; then
        hashcat -m 0 "$hash_file" "$wordlist" -r "$rule_file" --potfile-disable -o "$output_file" --quiet || true
        log "Rule-based attack completed with best64.rule"
    else
        log "Warning: best64.rule not found, skipping rule-based attack"
    fi
    
    log "Exercise 2 completed"
}

run_exercise_3() {
    local exercise="Exercise 3: Hybrid Attack"  
    log "Starting $exercise"
    
    local hash_file="$SAMPLES_DIR/hashes/md5_samples.txt"
    local wordlist="$SAMPLES_DIR/wordlists/small_test.txt"
    local output_file="$RESULTS_DIR/exercise3_results.txt"
    
    echo -e "${GREEN}$exercise${NC}"
    echo "Target: Dictionary + digit combinations"
    
    # Hybrid attack: dictionary + 2 digits
    hashcat -m 0 "$hash_file" -a 6 "$wordlist" ?d?d --potfile-disable -o "$output_file" --quiet || true
    
    log "Exercise 3 completed"
}

run_performance_test() {
    log "Running performance benchmark..."
    
    echo -e "${GREEN}Performance Benchmark${NC}"
    
    # Hashcat benchmark
    local bench_file="$RESULTS_DIR/hashcat_benchmark.txt"
    hashcat -b | tee "$bench_file"
    
    # System information
    local sysinfo_file="$RESULTS_DIR/system_info.txt"
    {
        echo "=== System Information ==="
        echo "Date: $(date)"
        echo "CPU: $(lscpu | grep 'Model name' | cut -d: -f2 | xargs)"
        echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
        echo "GPU: $(lspci | grep VGA | head -1)"
        echo ""
        echo "=== Hashcat Version ==="
        hashcat --version
        echo ""
        echo "=== John Version ==="
        john --version 2>&1 | head -3
    } > "$sysinfo_file"
    
    log "Performance benchmark completed"
}

generate_report() {
    log "Generating session report..."
    
    local report_file="$RESULTS_DIR/session_report.md"
    
    {
        echo "# Password Cracking Lab Session Report"
        echo ""
        echo "**Date:** $(date)"
        echo "**Duration:** $(( ($(date +%s) - session_start) / 60 )) minutes"
        echo ""
        echo "## System Configuration"
        echo "\`\`\`"
        cat "$RESULTS_DIR/system_info.txt" 2>/dev/null || echo "System info not available"
        echo "\`\`\`"
        echo ""
        echo "## Exercise Results"
        echo ""
        
        for i in {1..3}; do
            local result_file="$RESULTS_DIR/exercise${i}_results.txt"
            if [[ -f "$result_file" ]]; then
                local count=$(wc -l < "$result_file" 2>/dev/null || echo "0")
                echo "- **Exercise $i:** $count passwords cracked"
            fi
        done
        
        echo ""
        echo "## Files Generated"
        echo ""
        find "$RESULTS_DIR" -name "*.txt" -exec basename {} \; | sort | sed 's/^/- /'
        echo ""
        echo "---"
        echo "*Generated by Password Cracking Lab Automation*"
        
    } > "$report_file"
    
    log "Session report generated: $report_file"
}

cleanup() {
    log "Cleaning up temporary files..."
    
    # Remove hashcat potfiles to prevent interference
    rm -f hashcat.potfile
    rm -f ~/.hashcat/hashcat.potfile
    
    log "Cleanup completed"
}

main() {
    local session_start=$(date +%s)
    
    print_banner
    
    # Setup
    check_dependencies
    setup_directories
    
    # Preparation
    generate_sample_hashes  
    prepare_wordlists
    
    # Exercises
    run_exercise_1
    run_exercise_2
    run_exercise_3
    
    # Analysis
    run_performance_test
    
    # Reporting
    generate_report
    cleanup
    
    echo -e "${GREEN}Lab automation completed successfully!${NC}"
    echo -e "${BLUE}Results available in: $RESULTS_DIR${NC}"
    echo -e "${BLUE}Session log: $LOG_FILE${NC}"
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi