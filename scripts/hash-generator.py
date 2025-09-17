#!/usr/bin/env python3
"""
Password Cracking Hash Generator
Generates sample hashes for educational password cracking exercises.
"""

import hashlib
import sys
import argparse
from datetime import datetime

def generate_md5_hash(password):
    """Generate MD5 hash for given password."""
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def generate_sha1_hash(password):
    """Generate SHA1 hash for given password."""
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

def generate_sha256_hash(password):
    """Generate SHA256 hash for given password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_sample_hashes():
    """Generate a comprehensive set of sample hashes for testing."""
    
    # Common weak passwords for educational purposes
    weak_passwords = [
        "password", "123456", "admin", "letmein", "qwerty",
        "password123", "hello", "welcome", "test123", "secret",
        "dragon", "monkey", "1234567890", "football", "iloveyou",
        "master", "sunshine", "princess", "abc123", "computer"
    ]
    
    # Policy-compliant but still weak passwords
    policy_passwords = [
        "Password1!", "Summer2023!", "Welcome123", "Admin2023",
        "Test@123", "Hello2023!", "Secret99!", "Company2023"
    ]
    
    # Stronger passwords (for comparison)
    strong_passwords = [
        "MyDog$N4me1sRex", "C0ff33&Do9nu75!", "Tr@vel2Paris2024",
        "B@sketb@ll#Fan42", "M0rning$un$h1ne"
    ]
    
    all_passwords = weak_passwords + policy_passwords + strong_passwords
    
    print("# Password Cracking Sample Hashes")
    print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"# Total passwords: {len(all_passwords)}")
    print("#" + "="*60)
    
    # Generate MD5 hashes (most common for educational purposes)
    print("\n## MD5 Hashes (Mode: 0)")
    print("# Format: hash (for cracking)")
    for password in all_passwords:
        hash_value = generate_md5_hash(password)
        print(f"{hash_value}")
    
    print("\n## MD5 Hash:Password Pairs (for verification)")
    print("# Format: hash:password")
    for password in all_passwords:
        hash_value = generate_md5_hash(password)
        print(f"{hash_value}:{password}")
    
    # Generate other hash types
    print("\n## SHA1 Hashes (Mode: 100)")
    for password in weak_passwords[:10]:  # Subset for variety
        hash_value = generate_sha1_hash(password)
        print(f"{hash_value}")
    
    print("\n## SHA256 Hashes (Mode: 1400)")  
    for password in weak_passwords[:5]:  # Smaller subset
        hash_value = generate_sha256_hash(password)
        print(f"{hash_value}")

def generate_custom_hashes(passwords, hash_type="md5"):
    """Generate hashes for custom password list."""
    
    hash_functions = {
        "md5": generate_md5_hash,
        "sha1": generate_sha1_hash,
        "sha256": generate_sha256_hash
    }
    
    if hash_type not in hash_functions:
        print(f"Error: Unsupported hash type '{hash_type}'")
        return
    
    hash_func = hash_functions[hash_type]
    
    print(f"# Custom {hash_type.upper()} Hashes")
    print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for password in passwords:
        hash_value = hash_func(password.strip())
        print(f"{hash_value}")

def main():
    """Main function with command-line argument parsing."""
    
    parser = argparse.ArgumentParser(
        description="Generate sample password hashes for educational cracking exercises"
    )
    
    parser.add_argument(
        "--type", 
        choices=["md5", "sha1", "sha256"],
        default="md5",
        help="Hash algorithm to use (default: md5)"
    )
    
    parser.add_argument(
        "--custom",
        help="File containing custom passwords (one per line)"
    )
    
    parser.add_argument(
        "--samples",
        action="store_true", 
        help="Generate comprehensive sample hash collection"
    )
    
    args = parser.parse_args()
    
    if args.custom:
        try:
            with open(args.custom, 'r', encoding='utf-8') as f:
                passwords = f.readlines()
            generate_custom_hashes(passwords, args.type)
        except FileNotFoundError:
            print(f"Error: File '{args.custom}' not found")
            sys.exit(1)
    
    elif args.samples:
        generate_sample_hashes()
    
    else:
        # Interactive mode
        print("Password Hash Generator")
        print("Enter passwords (one per line, empty line to finish):")
        
        passwords = []
        while True:
            password = input("Password: ")
            if not password:
                break
            passwords.append(password)
        
        if passwords:
            generate_custom_hashes(passwords, args.type)
        else:
            print("No passwords entered. Use --samples for sample data.")

if __name__ == "__main__":
    main()