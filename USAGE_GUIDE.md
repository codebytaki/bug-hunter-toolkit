# 🛡️ Bug Hunter Toolkit - Complete Usage Guide

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [CLI Commands](#cli-commands)
4. [Python API](#python-api)
5. [Docker Usage](#docker-usage)
6. [Examples](#examples)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/codebytaki/bug-hunter-toolkit.git
cd bug-hunter-toolkit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### First Scan

```bash
# Run vulnerability scan
python bug_hunter.py scan https://example.com

# Run web application tests
python bug_hunter.py webtest https://example.com --test all
```

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Method 1: Standard Installation

```bash
git clone https://github.com/codebytaki/bug-hunter-toolkit.git
cd bug-hunter-toolkit
pip install -r requirements.txt
```

### Method 2: Docker Installation

```bash
# Build Docker image
docker build -t bug-hunter-toolkit .

# Run container
docker run bug-hunter-toolkit scan https://example.com
```

### Method 3: Development Installation

```bash
git clone https://github.com/codebytaki/bug-hunter-toolkit.git
cd bug-hunter-toolkit
pip install -e .
pip install -r requirements-dev.txt
```

---

## CLI Commands

### 1. Vulnerability Scan

```bash
# Basic scan
python bug_hunter.py scan https://example.com

# Custom timeout and threads
python bug_hunter.py scan https://example.com --timeout 20 --threads 10

# Save report to custom file
python bug_hunter.py scan https://example.com --output my_report.md
```

**Options:**
- `--timeout`: Request timeout in seconds (default: 10)
- `--threads`: Number of concurrent threads (default: 5)
- `--output, -o`: Output report file (default: report.md)

### 2. Web Application Testing

```bash
# Test all vulnerabilities
python bug_hunter.py webtest https://example.com --test all

# Test only XSS
python bug_hunter.py webtest https://example.com --test xss

# Test only SQL Injection
python bug_hunter.py webtest https://example.com --test sqli

# Test only CSRF
python bug_hunter.py webtest https://example.com --test csrf
```

**Options:**
- `--test`: Type of test (xss, sqli, csrf, all)
- `--output, -o`: Output report file

### 3. Subdomain Enumeration

```bash
# Basic subdomain enumeration
python bug_hunter.py subdomain example.com

# With custom wordlist
python bug_hunter.py subdomain example.com --wordlist custom.txt

# Save results
python bug_hunter.py subdomain example.com --output subdomains.txt
```

### 4. Port Scanning

```bash
# Scan common ports
python bug_hunter.py portscan 192.168.1.1

# Scan specific port range
python bug_hunter.py portscan 192.168.1.1 --ports 1-1000

# Scan specific ports
python bug_hunter.py portscan 192.168.1.1 --ports 80,443,8080
```

---

## Python API

### Vulnerability Scanner

```python
from src.scanner.vulnerability_scanner import VulnerabilityScanner

# Initialize scanner
scanner = VulnerabilityScanner(
    target="https://example.com",
    timeout=10,
    threads=5
)

# Run scan
results = scanner.scan()

# Access results
print(f"Found {results['total_vulnerabilities']} vulnerabilities")

for vuln in results['vulnerabilities']:
    print(f"[{vuln['severity']}] {vuln['type']}: {vuln['description']}")
```

### Web Application Tester

```python
from src.web_tester.web_app_tester import WebAppTester

# Initialize tester
tester = WebAppTester("https://example.com")

# Test for XSS
xss_results = tester.test_xss()
print(f"Found {len(xss_results)} XSS vulnerabilities")

# Test for SQL Injection
sqli_results = tester.test_sqli()
print(f"Found {len(sqli_results)} SQLi vulnerabilities")

# Test for CSRF
csrf_results = tester.test_csrf()
print(f"Found {len(csrf_results)} CSRF vulnerabilities")

# Run all tests
all_results = tester.test_all()
print(f"Total vulnerabilities: {all_results['total_vulnerabilities']}")
```

### Custom Scanning

```python
from src.scanner.vulnerability_scanner import VulnerabilityScanner
import json

# Create scanner
scanner = VulnerabilityScanner("https://example.com")

# Run specific checks
security_headers = scanner._check_security_headers()
ssl_issues = scanner._check_ssl_tls()
exposed_files = scanner._check_common_files()

# Combine results
all_issues = security_headers + ssl_issues + exposed_files

# Export to JSON
with open('results.json', 'w') as f:
    json.dump(all_issues, f, indent=2)
```

---

## Docker Usage

### Build Image

```bash
docker build -t bug-hunter-toolkit .
```

### Run Scans

```bash
# Vulnerability scan
docker run bug-hunter-toolkit scan https://example.com

# Web application test
docker run bug-hunter-toolkit webtest https://example.com --test all

# Mount volume for reports
docker run -v $(pwd)/reports:/app/reports bug-hunter-toolkit scan https://example.com -o /app/reports/scan.md
```

### Interactive Mode

```bash
# Start interactive shell
docker run -it bug-hunter-toolkit /bin/bash

# Run commands inside container
python bug_hunter.py scan https://example.com
```

---

## Examples

### Example 1: Complete Security Assessment

```python
from src.scanner.vulnerability_scanner import VulnerabilityScanner
from src.web_tester.web_app_tester import WebAppTester

target = "https://example.com"

# Run vulnerability scan
print("Running vulnerability scan...")
scanner = VulnerabilityScanner(target)
vuln_results = scanner.scan()

# Run web application tests
print("Running web application tests...")
tester = WebAppTester(target)
web_results = tester.test_all()

# Combine results
total_issues = vuln_results['total_vulnerabilities'] + web_results['total_vulnerabilities']

print(f"\n=== Security Assessment Complete ===")
print(f"Target: {target}")
print(f"Total Issues Found: {total_issues}")
print(f"  - Infrastructure: {vuln_results['total_vulnerabilities']}")
print(f"  - Web Application: {web_results['total_vulnerabilities']}")
```

### Example 2: Automated Bug Bounty Workflow

```bash
#!/bin/bash

TARGET="example.com"
OUTPUT_DIR="reports/$TARGET"

mkdir -p $OUTPUT_DIR

# 1. Subdomain enumeration
echo "[+] Enumerating subdomains..."
python bug_hunter.py subdomain $TARGET -o $OUTPUT_DIR/subdomains.txt

# 2. Scan each subdomain
while read subdomain; do
    echo "[+] Scanning $subdomain..."
    python bug_hunter.py scan https://$subdomain -o $OUTPUT_DIR/${subdomain}_scan.md
    python bug_hunter.py webtest https://$subdomain -o $OUTPUT_DIR/${subdomain}_web.md
done < $OUTPUT_DIR/subdomains.txt

echo "[+] Assessment complete! Reports saved to $OUTPUT_DIR"
```

### Example 3: Continuous Monitoring

```python
import schedule
import time
from src.scanner.vulnerability_scanner import VulnerabilityScanner

def monitor_target():
    """Monitor target for new vulnerabilities"""
    target = "https://example.com"
    scanner = VulnerabilityScanner(target)
    results = scanner.scan()
    
    if results['total_vulnerabilities'] > 0:
        # Send alert
        print(f"⚠️ Found {results['total_vulnerabilities']} vulnerabilities!")
        # Add notification logic here
    else:
        print("✓ No new vulnerabilities found")

# Schedule daily scans
schedule.every().day.at("09:00").do(monitor_target)

print("Starting continuous monitoring...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Best Practices

### 1. Authorization

✅ **Always get written permission** before testing any system
✅ **Stay within scope** defined by the target
✅ **Follow responsible disclosure** practices

### 2. Rate Limiting

```python
# Use appropriate delays
scanner = VulnerabilityScanner(
    target="https://example.com",
    timeout=10,
    threads=3  # Lower threads for rate limiting
)
```

### 3. Logging

```python
from loguru import logger

# Configure detailed logging
logger.add("security_scan_{time}.log", rotation="10 MB")

# Log all activities
logger.info("Starting security assessment")
```

### 4. Report Management

```bash
# Organize reports by date and target
mkdir -p reports/$(date +%Y-%m-%d)/example.com
python bug_hunter.py scan https://example.com -o reports/$(date +%Y-%m-%d)/example.com/scan.md
```

### 5. Error Handling

```python
try:
    scanner = VulnerabilityScanner(target)
    results = scanner.scan()
except Exception as e:
    logger.error(f"Scan failed: {str(e)}")
    # Handle error appropriately
```

---

## Troubleshooting

### Common Issues

#### 1. Connection Timeout

```bash
# Increase timeout
python bug_hunter.py scan https://example.com --timeout 30
```

#### 2. SSL Certificate Errors

```python
# Disable SSL verification (use with caution)
import requests
requests.packages.urllib3.disable_warnings()
```

#### 3. Rate Limiting

```bash
# Reduce threads
python bug_hunter.py scan https://example.com --threads 2
```

#### 4. Permission Denied

```bash
# Make script executable
chmod +x bug_hunter.py
```

### Debug Mode

```python
from loguru import logger
import sys

# Enable debug logging
logger.remove()
logger.add(sys.stderr, level="DEBUG")
```

---

## Legal & Ethical Guidelines

### ⚖️ Legal Notice

This tool is for **authorized security testing only**. Always:

- ✅ Obtain written permission
- ✅ Follow scope limitations
- ✅ Respect privacy laws
- ✅ Practice responsible disclosure
- ✅ Document all findings

### 🎯 Bug Bounty Programs

When using for bug bounties:

1. Read program rules carefully
2. Stay within defined scope
3. Report findings promptly
4. Don't exploit vulnerabilities
5. Follow disclosure timeline

---

## Additional Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bug Bounty Platforms](https://www.hackerone.com/)
- [Security Testing Methodology](https://portswigger.net/web-security)

---

## Support

- **Issues**: https://github.com/codebytaki/bug-hunter-toolkit/issues
- **Discussions**: https://github.com/codebytaki/bug-hunter-toolkit/discussions

---

**Happy (Ethical) Hacking! 🛡️**
