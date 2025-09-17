# Attack Strategies and Methodologies

## Overview

This document provides comprehensive coverage of password cracking attack strategies, from basic dictionary attacks to advanced hybrid techniques, with practical implementation examples and performance analysis.

## Attack Classification

### Primary Attack Types

#### 1. Dictionary Attacks (-a 0)
**Concept**: Test passwords from precompiled wordlists against target hashes.

**Implementation**:
```bash
# Basic dictionary attack with Hashcat
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

# John the Ripper dictionary attack  
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

**Characteristics**:
- **Speed**: Very Fast (minutes to hours)
- **Success Rate**: 60-85% against weak passwords
- **Resource Usage**: Low CPU/Memory
- **Best For**: Initial attack phase, common passwords

**Optimization Techniques**:
```bash
# Use multiple wordlists
hashcat -m 0 hashes.txt wordlist1.txt wordlist2.txt wordlist3.txt

# Specify encoding
hashcat -m 0 hashes.txt rockyou.txt --encoding-from=utf8 --encoding-to=utf8
```

#### 2. Brute Force Attacks (-a 3)
**Concept**: Systematically test all possible character combinations within specified parameters.

**Implementation**:
```bash
# 6-character brute force (all printable ASCII)
hashcat -m 0 hashes.txt -a 3 ?a?a?a?a?a?a

# Numbers only, 4-8 characters
hashcat -m 0 hashes.txt -a 3 ?d?d?d?d --increment
hashcat -m 0 hashes.txt -a 3 ?d?d?d?d?d?d?d?d --increment

# Letters and numbers, case sensitive
hashcat -m 0 hashes.txt -a 3 ?h?h?h?h?h?h?h?h
```

**Mask Definitions**:
- `?l` = abcdefghijklmnopqrstuvwxyz
- `?u` = ABCDEFGHIJKLMNOPQRSTUVWXYZ  
- `?d` = 0123456789
- `?h` = 0123456789abcdef
- `?H` = 0123456789ABCDEF
- `?s` = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
- `?a` = ?l?u?d?s

**Time Complexity Analysis**:
```python
# Character set sizes
lowercase = 26
uppercase = 26  
digits = 10
symbols = 32
total_printable = 95

# 8-character password combinations
combinations_8char = 95**8  # 6,634,204,312,890,625
# At 31B H/s (RTX 3090 MD5): ~7 days maximum
```

#### 3. Combinator Attacks (-a 1)
**Concept**: Combine words from two wordlists to create password candidates.

**Implementation**:
```bash
# Combine two wordlists
hashcat -m 0 hashes.txt -a 1 wordlist1.txt wordlist2.txt

# Common combinations
hashcat -m 0 hashes.txt -a 1 names.txt years.txt
hashcat -m 0 hashes.txt -a 1 colors.txt animals.txt
```

**Use Cases**:
- First name + last name combinations
- Company name + year combinations
- Adjective + noun combinations

#### 4. Hybrid Attacks (-a 6 & -a 7)
**Concept**: Combine dictionary words with mask patterns.

**Mode 6 (Dictionary + Mask)**:
```bash
# Dictionary word + 3 digits
hashcat -m 0 hashes.txt -a 6 rockyou.txt ?d?d?d

# Dictionary word + year
hashcat -m 0 hashes.txt -a 6 rockyou.txt ?d?d?d?d

# Dictionary word + special character + digits
hashcat -m 0 hashes.txt -a 6 rockyou.txt ?s?d?d
```

**Mode 7 (Mask + Dictionary)**:
```bash
# 3 digits + dictionary word
hashcat -m 0 hashes.txt -a 7 ?d?d?d rockyou.txt

# Year + dictionary word
hashcat -m 0 hashes.txt -a 7 ?d?d?d?d rockyou.txt
```

#### 5. Rule-Based Attacks
**Concept**: Apply transformations to dictionary words using rule sets.

**Hashcat Rules**:
```bash
# Use built-in rules
hashcat -m 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Common transformation rules
hashcat -m 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/leetspeak.rule

# Custom rule file
hashcat -m 0 hashes.txt rockyou.txt -r custom.rule
```

**John the Ripper Rules**:
```bash
# Built-in rules
john --wordlist=rockyou.txt --rules hashes.txt

# Specific rule set
john --wordlist=rockyou.txt --rules=Jumbo hashes.txt
```

**Common Rule Transformations**:
```
c    # Capitalize first letter
u    # Uppercase all
l    # Lowercase all  
$1   # Append '1'
$!   # Append '!'
^1   # Prepend '1'
so0  # Replace 's' with '0'
sa@  # Replace 'a' with '@'
```

## Advanced Attack Techniques

### 1. Fingerprinting and Hash Identification

**Hash-Identifier**:
```bash
# Identify hash type
hash-identifier
# Paste hash when prompted

# Hashcat hash identification
hashcat --example-hashes | grep -A5 -B5 "your_hash_pattern"
```

**Common Hash Formats**:
```
MD5:     32 hex characters
SHA1:    40 hex characters  
SHA256:  64 hex characters
NTLM:    32 hex characters (like MD5)
bcrypt:  $2a$, $2b$, $2x$, $2y$ prefix
Argon2:  $argon2i$, $argon2d$, $argon2id$ prefix
```

### 2. Statistical Analysis and Intelligence

**Password Pattern Analysis**:
```python
# Analyze cracked passwords for patterns
import collections

def analyze_patterns(cracked_passwords):
    lengths = [len(pwd) for pwd in cracked_passwords]
    
    print(f"Average length: {sum(lengths)/len(lengths):.1f}")
    print(f"Length distribution: {collections.Counter(lengths)}")
    
    # Character class analysis
    has_upper = sum(1 for pwd in cracked_passwords if any(c.isupper() for c in pwd))
    has_lower = sum(1 for pwd in cracked_passwords if any(c.islower() for c in pwd))
    has_digit = sum(1 for pwd in cracked_passwords if any(c.isdigit() for c in pwd))
    has_special = sum(1 for pwd in cracked_passwords if any(not c.isalnum() for c in pwd))
    
    total = len(cracked_passwords)
    print(f"Uppercase: {has_upper/total*100:.1f}%")
    print(f"Lowercase: {has_lower/total*100:.1f}%")  
    print(f"Digits: {has_digit/total*100:.1f}%")
    print(f"Special: {has_special/total*100:.1f}%")
```

### 3. Custom Wordlist Generation

**CeWL (Custom Word List Generator)**:
```bash
# Generate wordlist from website
cewl -d 2 -m 5 -w custom_wordlist.txt https://target-company.com

# Include email addresses
cewl -d 2 -m 5 -e -w custom_wordlist.txt https://target-company.com
```

**Crunch (Pattern-Based Generation)**:
```bash
# Generate 4-6 character passwords with specific pattern
crunch 4 6 0123456789 -o digits.txt

# Pattern: 2 letters + 2 digits
crunch 4 4 -t @@%% -o pattern.txt
```

### 4. Distributed Cracking

**Hashcat Distributed Setup**:
```bash
# Server mode
hashcat --server-password=mypassword

# Client connection
hashcat --client-host=192.168.1.100 --client-password=mypassword -m 0 hashes.txt rockyou.txt
```

## Performance Optimization Strategies

### 1. Hardware Optimization

**GPU Selection and Configuration**:
```bash
# Check available devices
hashcat -I

# Use specific GPU
hashcat -d 1 -m 0 hashes.txt rockyou.txt

# Multiple GPU utilization
hashcat -d 1,2,3 -m 0 hashes.txt rockyou.txt
```

**Memory Management**:
```bash
# Adjust workload tuning
hashcat -w 3 -m 0 hashes.txt rockyou.txt  # High performance
hashcat -w 1 -m 0 hashes.txt rockyou.txt  # Low resource usage
```

### 2. Attack Ordering Strategy

**Optimal Attack Sequence**:
1. **Quick Dictionary** (5-30 minutes)
   - rockyou.txt top 100K passwords
   - Common passwords list
   
2. **Rule-Based Dictionary** (1-6 hours)  
   - rockyou.txt + best64.rule
   - Common transformation rules
   
3. **Hybrid Attacks** (6-24 hours)
   - Dictionary + 2-3 digit append
   - Dictionary + year append
   
4. **Targeted Brute Force** (24+ hours)
   - Based on pattern analysis
   - Incremental character sets

5. **Full Brute Force** (Extended time)
   - Last resort for critical targets
   - Limit to 8-10 characters maximum

### 3. Success Rate Optimization

**Progressive Attack Strategy**:
```bash
#!/bin/bash
# Automated attack progression

HASHES="target_hashes.txt"
WORDLIST="/usr/share/wordlists/rockyou.txt"

# Phase 1: Quick dictionary (top 1M passwords)
head -n 1000000 $WORDLIST > quick_dict.txt
hashcat -m 0 $HASHES quick_dict.txt --potfile-disable -o phase1_results.txt

# Phase 2: Rules-based  
hashcat -m 0 $HASHES $WORDLIST -r /usr/share/hashcat/rules/best64.rule --potfile-disable -o phase2_results.txt

# Phase 3: Hybrid dictionary + digits
hashcat -m 0 $HASHES -a 6 $WORDLIST ?d?d --potfile-disable -o phase3_results.txt

# Phase 4: Hybrid dictionary + years
hashcat -m 0 $HASHES -a 6 $WORDLIST ?d?d?d?d --potfile-disable -o phase4_results.txt

# Combine results
cat phase*_results.txt > final_results.txt
```

## Countermeasure Analysis

### Attack Mitigation Strategies

**Against Dictionary Attacks**:
- Prohibit common passwords from policy databases
- Implement password blacklists (HaveIBeenPwned API)
- Regular password strength auditing

**Against Brute Force Attacks**:
- Enforce minimum 12+ character lengths
- Use memory-hard hashing algorithms (bcrypt, Argon2)
- Implement account lockout mechanisms

**Against Hybrid Attacks**:
- Prohibit predictable patterns (word+digits, word+year)
- Encourage passphrase adoption over complex passwords
- Implement context-aware password policies

This comprehensive attack methodology framework provides the foundation for understanding password vulnerabilities while emphasizing the critical importance of robust defensive measures in modern security implementations.