# Laboratory Setup Guide

## Overview

This guide provides comprehensive instructions for setting up a secure password cracking laboratory environment using virtualization technology and ethical hacking tools.

## Hardware Requirements

### Minimum Requirements
- **CPU**: Modern quad-core processor with virtualization support (Intel VT-x/AMD-V)
- **RAM**: 8GB (16GB recommended for optimal performance)
- **Storage**: 50GB free space for VMs and wordlists
- **Network**: Stable internet connection for initial setup

### Recommended Configuration
- **CPU**: 8-core processor (Intel i7/AMD Ryzen 5 or higher)
- **RAM**: 16GB DDR4 or higher
- **Storage**: 100GB+ SSD for improved VM performance
- **GPU**: NVIDIA RTX series for GPU-accelerated cracking (optional but recommended)

## Software Requirements

### Host System
- **OS**: Windows 10/11, macOS, or Linux
- **Virtualization**: VirtualBox 7.0+ or VMware Workstation Pro
- **Browser**: Modern web browser for documentation access

### Virtual Machines
- **Attack Platform**: Kali Linux 2023.3+ (4GB RAM minimum)
- **Target Systems**: Windows 10/11 and Ubuntu Linux VMs
- **Network Configuration**: Host-only or NAT networks for isolation

## Installation Steps

### 1. Install Virtualization Software

#### VirtualBox Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install virtualbox virtualbox-ext-pack

# Windows/macOS
# Download from https://www.virtualbox.org/wiki/Downloads
```

#### VMware Workstation (Alternative)
```bash
# Professional environments may prefer VMware
# Download from VMware official website
# Follow installation wizard
```

### 2. Download Operating System Images

#### Kali Linux
```bash
# Download Kali Linux VM image
wget https://cdimage.kali.org/kali-2023.3/kali-linux-2023.3-virtualbox-amd64.7z

# Extract and import
7z x kali-linux-2023.3-virtualbox-amd64.7z
# Import .ova file into VirtualBox
```

#### Target Systems
- Windows 10/11 Developer VM from Microsoft
- Ubuntu Desktop 22.04 LTS ISO
- Configure with test user accounts

### 3. Network Configuration

#### Host-Only Network Setup
```bash
# VirtualBox Host-Only Network
VBoxManage hostonlyif create
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
```

#### Security Isolation
- Disable internet access for target VMs
- Enable communication between attack and target systems
- Document network topology for testing scenarios

### 4. Tool Installation and Validation

#### Hashcat Installation
```bash
# Kali Linux (pre-installed)
hashcat --version

# Ubuntu/Debian
sudo apt install hashcat

# Validate installation
hashcat --benchmark
```

#### John the Ripper Installation
```bash
# Kali Linux (pre-installed)
john --version

# Compile from source for latest features
git clone https://github.com/openwall/john.git
cd john/src
make -s clean && make -sj4
```

#### Wordlist Preparation
```bash
# Extract rockyou.txt
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Download additional wordlists
wget https://github.com/danielmiessler/SecLists/archive/master.zip
unzip master.zip -d /usr/share/wordlists/
```

## Performance Optimization

### GPU Acceleration Setup

#### NVIDIA Driver Installation
```bash
# Kali Linux
sudo apt update
sudo apt install nvidia-driver nvidia-cuda-toolkit

# Verify installation
nvidia-smi
hashcat -I  # List OpenCL devices
```

#### Memory Optimization
```bash
# Increase shared memory for large wordlists
echo 'kernel.shmmax = 268435456' >> /etc/sysctl.conf
sysctl -p
```

### VM Performance Tuning

#### VirtualBox Optimization
- Enable VT-x/AMD-V acceleration
- Allocate 4GB+ RAM to Kali VM
- Enable 3D acceleration for GPU access
- Configure adequate video memory (128MB+)

## Sample Test Environment

### Hash Generation Script
```python
#!/usr/bin/env python3
import hashlib
import sys

def generate_sample_hashes():
    passwords = [
        "password", "123456", "admin", "letmein", "qwerty",
        "password123", "hello", "welcome", "test123", "secret"
    ]
    
    print("# Sample MD5 Hashes for Testing")
    for pwd in passwords:
        md5_hash = hashlib.md5(pwd.encode()).hexdigest()
        print(f"{md5_hash}")  # Hash only for cracking
        
    print("\n# Hash:Password pairs for verification")
    for pwd in passwords:
        md5_hash = hashlib.md5(pwd.encode()).hexdigest()
        print(f"{md5_hash}:{pwd}")

if __name__ == "__main__":
    generate_sample_hashes()
```

### Basic Functionality Test
```bash
# Test Hashcat with sample hash
echo "5f4dcc3b5aa765d61d8327deb882cf99" > test_hash.txt
hashcat -m 0 test_hash.txt -a 3 password

# Test John the Ripper
echo "test:5f4dcc3b5aa765d61d8327deb882cf99" > test_john.txt
john --format=raw-md5 test_john.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

## Security Considerations

### Isolation Requirements
- **Network Isolation**: Prevent accidental external attacks
- **Data Protection**: Use dedicated VM storage
- **Access Control**: Limit lab access to authorized personnel
- **Documentation**: Maintain detailed test logs

### Legal Compliance
- **Authorization**: Only test on owned/authorized systems
- **Documentation**: Record all testing activities
- **Data Handling**: Secure storage of sensitive test data
- **Reporting**: Follow responsible disclosure practices

## Troubleshooting Guide

### Common Issues

#### GPU Not Detected
```bash
# Check OpenCL installation
clinfo

# Install OpenCL headers
sudo apt install opencl-headers

# Verify Hashcat GPU support
hashcat -I
```

#### Performance Issues
```bash
# Monitor system resources
htop
nvidia-smi  # GPU monitoring

# Check VM resource allocation
# Increase RAM/CPU allocation in VM settings
```

#### Wordlist Problems
```bash
# Check file permissions
ls -la /usr/share/wordlists/rockyou.txt

# Fix permissions if needed
sudo chmod +r /usr/share/wordlists/rockyou.txt
```

## Maintenance and Updates

### Regular Maintenance Tasks
- Update Kali Linux: `sudo apt update && sudo apt upgrade`
- Update wordlists: Download latest SecLists releases
- VM snapshots: Create clean state snapshots
- Performance monitoring: Regular benchmark tests

### Documentation Updates
- Test result documentation
- Configuration change logs  
- Performance baseline updates
- Security incident reports

This laboratory setup provides a secure, isolated environment for learning password security concepts while maintaining ethical boundaries and legal compliance.