<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:8b0000,100:0d1117&height=200&section=header&text=Bug%20Hunter%20Toolkit&fontSize=45&fontColor=ff6b6b&fontAlignY=38&desc=Professional%20Security%20Research%20%7C%20Bug%20Bounty%20%7C%20Recon%20%7C%20AI-Powered&descSize=17&descAlignY=58&descColor=8b949e&animation=fadeIn" />

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/Version-3.0.0-red?style=flat-square)](https://github.com/codebytaki/bug-hunter-toolkit/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Stars](https://img.shields.io/github/stars/codebytaki/bug-hunter-toolkit?style=flat-square&color=yellow)](https://github.com/codebytaki/bug-hunter-toolkit/stargazers)
[![Issues](https://img.shields.io/github/issues/codebytaki/bug-hunter-toolkit?style=flat-square)](https://github.com/codebytaki/bug-hunter-toolkit/issues)
[![Security](https://img.shields.io/badge/ethical-use%20only-critical?style=flat-square)](SECURITY.md)

**Production-ready security testing and bug bounty toolkit with AI-powered vulnerability intelligence, CVE search, exploit discovery, and automated reporting.**

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [🗺️ Methodology](#️-hunt-methodology) · [📖 Modules](#-modules) · [🤝 Contributing](#-contributing)

</div>

> ⚠️ **For authorized security testing only.** Always get written permission before testing any system.

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🔍 Recon & Discovery**
- Subdomain enumeration
- Port scanning & service detection
- Directory & parameter discovery
- JavaScript file analysis
- Wayback Machine mining

</td>
<td width="50%">

**🧪 Vulnerability Testing**
- XSS, SQLi, CSRF, SSRF detection
- CORS misconfiguration checks
- Open redirect testing
- Auth bypass techniques
- Business logic fuzzing

</td>
</tr>
<tr>
<td width="50%">

**🧠 AI-Powered Intelligence**
- CVE database search (NVD, CIRCL)
- Exploit-DB integration
- AI severity prediction
- Smart target prioritization
- Automated report generation

</td>
<td width="50%">

**📊 Reporting**
- HTML dashboard with charts
- Executive summary
- POC + CVSS scoring
- JSON / Markdown export
- Evidence screenshot capture

</td>
</tr>
</table>

---

## 🗺️ Hunt Methodology

```
Target
  │
  ▼
🔭 Recon
  ├── Subdomain Enumeration (subfinder, amass)
  ├── Port Scan (nmap)
  └── Tech Fingerprinting
  │
  ▼
📡 Enumeration
  ├── Directory Discovery (ffuf)
  ├── JS File Analysis
  └── Parameter Discovery (gau, katana)
  │
  ▼
🧪 Discovery & Testing
  ├── XSS / SQLi / SSRF / CORS
  ├── Auth Bypass
  └── Business Logic
  │
  ▼
🔍 CVE & Exploit Intelligence
  ├── CVE Search (NVD, CIRCL)
  ├── Exploit-DB Lookup
  └── CVSS Scoring
  │
  ▼
📝 Validation & Reporting
  ├── POC Creation
  ├── Impact Assessment
  └── HTML/JSON/Markdown Report
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/codebytaki/bug-hunter-toolkit.git
cd bug-hunter-toolkit

# Setup
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run full hunt
python bug_hunter.py hunt target.com --output results.json
```

### Or with Docker

```bash
docker build -t bug-hunter .
docker run -it bug-hunter hunt target.com
```

---

## 💡 Usage

### Full Automated Hunt (one command)

```bash
python bug_hunter.py hunt target.com --output report.html
```

Generates: `report.html` · `report.json` · `findings.md` · screenshots

### CVE Intelligence

```bash
# Search CVEs by keyword
python bug_hunter.py cve apache --limit 20

# Get specific CVE details
python bug_hunter.py cveinfo CVE-2021-44228

# Save results
python bug_hunter.py cve wordpress --output cves.json
```

### Exploit Discovery

```bash
# Find exploits
python bug_hunter.py exploit wordpress

# Combined CVE + Exploit hunt
python bug_hunter.py hunt apache --output hunt.json
```

### Python API

```python
from bug_hunter import SecurityAssessment

assessment = SecurityAssessment(
    target="https://target.com",
    scope=["web", "network", "config"]
)
results = assessment.run()
assessment.export_report("report.html")
```

---

## 📦 Tool Coverage

| Tool | Included | Purpose |
|------|----------|---------|
| subfinder | ✅ | Subdomain enumeration |
| httpx | ✅ | HTTP probing |
| katana | ✅ | JS crawling |
| gau | ✅ | URL discovery |
| ffuf | ✅ | Directory fuzzing |
| nuclei | ✅ | Vulnerability templates |
| NVD / CIRCL | ✅ | CVE databases |
| Exploit-DB | ✅ | Exploit search |

---

## 🛡️ OWASP / CVE Coverage

| Category | Covered |
|----------|---------|
| OWASP Top 10 (2021) | ✅ Full |
| MITRE ATT&CK | ✅ Mapped |
| CWE Classification | ✅ |
| CVSS v3 Scoring | ✅ |
| CVE Cross-reference | ✅ |

---

## 📁 Project Structure

```
bug-hunter-toolkit/
├── src/
│   ├── scanner/               # Core vulnerability scanners
│   ├── web_tester/            # XSS, SQLi, CSRF, CORS
│   ├── network/               # Port scan, service detection
│   ├── exploit_finder/        # CVE + Exploit search
│   │   ├── cve_searcher.py
│   │   └── exploitdb_searcher.py
│   ├── reports/               # Report generation
│   └── utils/                 # Helpers & utilities
├── claude-bughunter/          # Advanced methodology framework
│   ├── commands/              # Hunt commands
│   ├── skills/                # Specialized hunt skills (50+)
│   └── docs/                  # Architecture & guides
├── wordlists/                 # Security wordlists
├── examples/                  # Usage examples
├── tests/                     # Test suite
├── docs/                      # Documentation
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── bug_hunter.py              # Main CLI entry
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── CODE_OF_CONDUCT.md
```

---

## 🗺️ Roadmap

- [x] Core vulnerability scanner
- [x] CVE & Exploit-DB integration
- [x] Claude-BugHunter methodology
- [x] Docker support
- [ ] 🧠 AI Executive Report Generator (v3.1)
- [ ] 📊 HTML Dashboard with charts (v3.1)
- [ ] 🔐 JWT / OAuth attack module (v3.2)
- [ ] 🌐 Web3 / Smart Contract auditing (v3.2)
- [ ] 🤖 LLM-powered recon suggestions (v4.0)
- [ ] 🏆 HackerOne / Bugcrowd API integration (v4.0)

---

## 🧪 Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

---

## 📚 Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackerOne Hacktivity](https://hackerone.com/hacktivity)
- [Bug Bounty Platforms](https://github.com/codebytaki/bug-hunter-toolkit/wiki)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome — bug fixes, new modules, wordlists, or docs.

---

## 🛡️ Responsible Disclosure

1. Get **written authorization** before testing
2. Document findings carefully
3. Report to the organization first
4. Follow responsible disclosure — see [SECURITY.md](SECURITY.md)

---

## 📄 License

MIT © [Taki](https://github.com/codebytaki) — see [LICENSE](LICENSE)

---

<div align="center">

**Built with ❤️ by [codebytaki](https://github.com/codebytaki)**

⭐ Star this repo if it helped your bug bounty journey!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:8b0000,100:0d1117&height=80&section=footer" />

</div>
