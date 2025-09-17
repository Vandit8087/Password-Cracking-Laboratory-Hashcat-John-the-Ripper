# Password Cracking Laboratory: Hashcat & John the Ripper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Kali Linux](https://img.shields.io/badge/platform-Kali%20Linux-blue)](https://www.kali.org/)

A comprehensive educational repository for understanding password security through ethical hacking techniques using Hashcat and John the Ripper tools.

## 🎯 Objective

Learn how weak passwords are cracked and how to defend against such attacks through hands-on laboratory exercises covering dictionary attacks, brute force techniques, and hybrid methodologies.

## 🛠️ Tools & Technologies

- **Hashcat**: Advanced password recovery tool with GPU acceleration
- **John the Ripper**: Popular password cracking tool optimized for CPU
- **Kali Linux**: Primary penetration testing platform
- **rockyou.txt**: Standard wordlist for dictionary attacks
- **VirtualBox/VMware**: Virtualization for safe testing environment

## 📁 Repository Structure

```
password-cracking-lab/
├── README.md                    # Main documentation
├── docs/                        # Comprehensive documentation
│   ├── complete-report.md       # Full technical analysis
│   ├── lab-setup-guide.md       # Environment configuration
│   ├── attack-strategies.md     # Detailed attack methodologies
│   └── defense-guide.md         # Security countermeasures
├── scripts/                     # Automation and utility scripts
│   ├── hash-generator.py        # Generate sample hashes
│   ├── performance-test.py      # Benchmark tools
│   └── lab-automation.sh        # Lab setup automation
├── samples/                     # Sample files and datasets
│   ├── hashes/                  # Test hash collections
│   ├── wordlists/               # Custom wordlists
│   └── results/                 # Attack output examples
├── configs/                     # Configuration files
│   ├── hashcat-rules/           # Custom Hashcat rules
│   └── john-configs/            # John the Ripper configs
├── analysis/                    # Performance and security analysis
│   ├── performance-data.csv     # Benchmarking results
│   ├── attack-timeline.csv      # Attack progression data
│   └── defense-strategies.csv   # Countermeasure analysis
└── LICENSE                      # MIT License
```

## 🚀 Quick Start

### Prerequisites

```bash
# Kali Linux with tools installed
sudo apt update && sudo apt install hashcat john
```

### Basic Usage

1. **Clone Repository**
```bash
git clone https://github.com/your-username/password-cracking-lab.git
cd password-cracking-lab
```

2. **Generate Sample Hashes**
```bash
python3 scripts/hash-generator.py
```

3. **Dictionary Attack with Hashcat**
```bash
hashcat -m 0 samples/hashes/sample_hashes.txt /usr/share/wordlists/rockyou.txt
```

4. **Dictionary Attack with John the Ripper**
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt samples/hashes/sample_hashes.txt
```

## 📊 Key Findings

- **Dictionary attacks** crack 60-85% of weak passwords within minutes
- **GPU acceleration** provides 20x speed improvement over CPU-only attacks
- **Modern algorithms** like Argon2 resist cracking attempts effectively
- **Hybrid attacks** increase success rates by 10-20% over pure dictionary attacks

## 🔬 Laboratory Exercises

### Exercise 1: Basic Dictionary Attack
- **Objective**: Crack MD5 hashes using rockyou.txt
- **Tools**: Hashcat, John the Ripper
- **Duration**: 30 minutes
- **Success Rate**: 60-85%

### Exercise 2: Rule-Based Attacks
- **Objective**: Apply transformations to dictionary words
- **Tools**: Hashcat with custom rules
- **Duration**: 1-6 hours
- **Success Rate**: 80%

### Exercise 3: Hybrid Attacks
- **Objective**: Combine dictionary + mask attacks
- **Tools**: Hashcat modes 6 & 7
- **Duration**: 6-24 hours
- **Success Rate**: 90%

## 🛡️ Defense Strategies

| Strategy | Effectiveness | Cost | Implementation |
|----------|--------------|------|----------------|
| Strong Password Policies | High | Low | Immediate |
| Multi-Factor Authentication | Very High | Medium | 1-2 weeks |
| Modern Hashing (bcrypt/Argon2) | Very High | Low | 2-4 weeks |
| Account Lockout Mechanisms | Medium | Low | 1 week |
| Password Managers | Very High | Medium | 2-3 weeks |

## 📈 Performance Benchmarks

### Hardware Performance (Hashes/Second)

| Hash Type | RTX 3090 (GPU) | Ryzen 5800X (CPU) | Security Level |
|-----------|----------------|-------------------|----------------|
| MD5 | 31,038M H/s | 1,508M H/s | Very Low |
| SHA1 | 10,500M H/s | 980M H/s | Low |
| SHA256 | 3,850M H/s | 420M H/s | Medium |
| bcrypt | 0.3K H/s | 0.15K H/s | High |
| Argon2 | 1 H/s | 0.5 H/s | Very High |

## ⚖️ Ethical Guidelines

This repository is intended for **educational purposes only**. All techniques should be applied exclusively in:

- ✅ Authorized penetration testing environments
- ✅ Personal learning laboratories with isolated systems
- ✅ Security research with proper permissions
- ✅ Defensive security improvement initiatives

**Never use these techniques on systems without explicit written authorization.**

## 🤝 Contributing

We welcome contributions to improve this educational resource:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📚 Additional Resources

- [Hashcat Official Documentation](https://hashcat.net/wiki/)
- [John the Ripper Documentation](https://www.openwall.com/john/doc/)
- [OWASP Password Security Guidelines](https://owasp.org/www-project-top-ten/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This educational material is provided for legitimate cybersecurity learning purposes. Users are responsible for ensuring all activities comply with applicable laws and regulations. The authors assume no liability for misuse of this information.

---

**🔐 Remember: The best defense is understanding the attack.**