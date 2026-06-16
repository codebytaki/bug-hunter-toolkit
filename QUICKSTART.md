# 🚀 Quick Start Guide

Get started with Bug Hunter Toolkit in 5 minutes!

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bug-hunter-toolkit.git
cd bug-hunter-toolkit

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Basic Usage

### 1. Vulnerability Scan

Scan a target for common vulnerabilities:

```bash
python bug_hunter.py scan https://example.com
```

Output:
```
🔍 Starting vulnerability scan...
Target: https://example.com
Timeout: 10s
Threads: 5

✓ Found 5 vulnerabilities
  Duration: 0:00:15
✓ Report saved to: report.md
```

### 2. Web Application Testing

Test for XSS, SQLi, and CSRF:

```bash
python bug_hunter.py webtest https://example.com --test all
```

### 3. CVE Search (NEW!)

Search for CVEs related to your target technology:

```bash
# Search CVEs
python bug_hunter.py cve apache --limit 10

# Get specific CVE details
python bug_hunter.py cveinfo CVE-2021-44228
```

### 4. Exploit Search (NEW!)

Find exploits for discovered vulnerabilities:

```bash
# Search exploits
python bug_hunter.py exploit wordpress

# Comprehensive hunt (CVEs + Exploits)
python bug_hunter.py hunt apache --output results.json
```

## 🔥 Advanced Example

Run a comprehensive security hunt:

```bash
python examples/comprehensive_hunt_example.py https://target.com --tech apache
```

This will:
1. ✅ Scan for vulnerabilities
2. ✅ Test web application security
3. ✅ Search related CVEs
4. ✅ Find available exploits
5. ✅ Generate comprehensive report

## 📊 Understanding Results

### Vulnerability Severity Levels

- 🔴 **Critical** - Immediate action required (CVSS 9.0-10.0)
- 🟠 **High** - High priority (CVSS 7.0-8.9)
- 🟡 **Medium** - Should be addressed (CVSS 4.0-6.9)
- 🟢 **Low** - Minor issues (CVSS 0.1-3.9)

### CVE Information

Each CVE result includes:
- **CVE ID**: Unique identifier (e.g., CVE-2021-44228)
- **CVSS Score**: Severity rating (0-10)
- **Published Date**: When the vulnerability was disclosed
- **Summary**: Brief description
- **References**: Links to more information

## 🛠️ Common Workflows

### Workflow 1: Quick Security Check

```bash
# 1. Scan target
python bug_hunter.py scan https://target.com

# 2. Test web vulnerabilities
python bug_hunter.py webtest https://target.com

# 3. Review report.md
```

### Workflow 2: CVE Research

```bash
# 1. Identify technology (e.g., Apache 2.4.49)
python bug_hunter.py cve "apache 2.4.49" --limit 20

# 2. Get details on critical CVEs
python bug_hunter.py cveinfo CVE-2021-41773

# 3. Search for exploits
python bug_hunter.py exploit CVE-2021-41773
```

### Workflow 3: Comprehensive Hunt

```bash
# All-in-one command
python bug_hunter.py hunt wordpress --output hunt_results.json

# Review results
cat hunt_results.json | jq '.cve_results[] | select(.cvss >= 7.0)'
```

## 🎓 Learning Path

### Beginner
1. Start with basic vulnerability scanning
2. Learn to interpret scan results
3. Practice on intentionally vulnerable apps (DVWA, WebGoat)

### Intermediate
4. Use CVE search to research vulnerabilities
5. Combine scanning with exploit research
6. Generate comprehensive reports

### Advanced
7. Customize scanning modules
8. Integrate with CI/CD pipelines
9. Develop custom exploit modules

## 🔐 Best Practices

### ✅ DO
- Always get written authorization before testing
- Test in isolated environments first
- Document all findings thoroughly
- Follow responsible disclosure practices
- Keep the toolkit updated

### ❌ DON'T
- Test systems without permission
- Use exploits on production systems
- Share vulnerabilities publicly before disclosure
- Ignore legal and ethical boundaries

## 🆘 Troubleshooting

### Issue: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: "Connection timeout"
```bash
# Solution: Increase timeout
python bug_hunter.py scan https://target.com --timeout 30
```

### Issue: "Rate limited by CVE API"
```bash
# Solution: Reduce request frequency or use local CVE database
# Wait a few minutes and try again
```

## 📚 Next Steps

1. Read [CLAUDE_BUGHUNTER_INTEGRATION.md](CLAUDE_BUGHUNTER_INTEGRATION.md) for advanced features
2. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed documentation
3. Explore [examples/](examples/) directory for more use cases
4. Join our community for support and updates

## 🤝 Getting Help

- 📖 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Join our Discord community
- 📧 Email: support@bughuntertoolkit.com

## ⚡ Quick Reference

```bash
# Scanning
python bug_hunter.py scan <target>
python bug_hunter.py webtest <target>
python bug_hunter.py portscan <target>

# CVE & Exploits
python bug_hunter.py cve <keyword>
python bug_hunter.py cveinfo <CVE-ID>
python bug_hunter.py exploit <keyword>
python bug_hunter.py hunt <keyword>

# Subdomain Enumeration
python bug_hunter.py subdomain <domain>

# Help
python bug_hunter.py --help
python bug_hunter.py <command> --help
```

---

**Happy Hunting! 🎯**

Remember: With great power comes great responsibility. Always use these tools ethically and legally.
