# 📚 Claude-BugHunter Resources Index

This directory contains all resources from the [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) project, integrated into Bug Hunter Toolkit.

---

## 📁 Directory Structure

```
claude-bughunter/
├── skills/              # 51 bug hunting skills
├── commands/            # 14 slash commands
├── scripts/             # Automation scripts
├── docs/                # Documentation and guides
├── CLAUDE_BUGHUNTER_README.md
├── USAGE.md
├── INSTALL.md
└── INDEX.md (this file)
```

---

## 🎯 Skills (51 Total)

### Web Application Hunting (28 skills)

#### Injection Vulnerabilities
- `hunt-xss/` - Cross-Site Scripting (174 disclosed reports)
- `hunt-sqli/` - SQL Injection (8 disclosed reports)
- `hunt-ssti/` - Server-Side Template Injection
- `hunt-rce/` - Remote Code Execution (67 disclosed reports)
- `hunt-xxe/` - XML External Entity (4 disclosed reports)

#### Authorization & Access Control
- `hunt-idor/` - Insecure Direct Object Reference (26 disclosed reports)
- `hunt-auth-bypass/` - Authentication Bypass (4 disclosed reports)
- `hunt-csrf/` - Cross-Site Request Forgery (10 disclosed reports)

#### Server-Side Attacks
- `hunt-ssrf/` - Server-Side Request Forgery (9 disclosed reports)
- `hunt-http-smuggling/` - HTTP Request Smuggling
- `hunt-cache-poison/` - Web Cache Poisoning (4 disclosed reports)

#### Identity & Authentication
- `hunt-ato/` - Account Takeover (9 paths)
- `hunt-mfa-bypass/` - MFA/2FA Bypass (7 patterns)
- `hunt-oauth/` - OAuth 2.0 Vulnerabilities (10 disclosed reports)
- `hunt-saml/` - SAML/SSO Attacks

#### API & Modern Web
- `hunt-api-misconfig/` - API Misconfigurations
- `hunt-graphql/` - GraphQL Vulnerabilities (3 disclosed reports)
- `hunt-file-upload/` - File Upload Bypass (10 techniques)

#### Business Logic & Concurrency
- `hunt-business-logic/` - Business Logic Flaws (7 disclosed reports)
- `hunt-race-condition/` - Race Conditions (3 disclosed reports)
- `hunt-llm-ai/` - LLM/AI Vulnerabilities

#### Platform-Specific
- `hunt-aspnet/` - ASP.NET Vulnerabilities
- `hunt-sharepoint/` - SharePoint Attacks
- `hunt-ntlm-info/` - NTLM Information Disclosure
- `hunt-subdomain/` - Subdomain Takeover (11 disclosed reports)
- `hunt-cloud-misconfig/` - Cloud Misconfigurations

#### Miscellaneous
- `hunt-misc/` - Catch-all (225 disclosed reports)
- `hunt-dispatch/` - Hunt mode router

### Enterprise Platform Attack (7 skills)

#### Identity Fabric
- `m365-entra-attack/` - Microsoft 365 / Entra ID
- `okta-attack/` - Okta Identity Provider

#### Cloud & Infrastructure
- `cloud-iam-deep/` - AWS/Azure/GCP IAM Privilege Escalation
- `vmware-vcenter-attack/` - VMware vCenter/vSphere
- `enterprise-vpn-attack/` - Enterprise SSL VPN Appliances

#### Mobile & Supply Chain
- `apk-redteam-pipeline/` - Android APK Red Team
- `supply-chain-attack-recon/` - Supply Chain Reconnaissance

### Red Team Tradecraft (2 skills)

- `redteam-mindset/` - Operator Discipline & DO NOT STOP Directive
- `mid-engagement-ir-detection/` - SOC Patch Detection

### Recon & OSINT (4 skills)

- `offensive-osint/` - 15-Reference Probe Arsenal
- `web2-recon/` - Subdomain Enumeration & Host Discovery
- `osint-methodology/` - 5-Stage Recon Pipeline
- `bb-local-toolkit/` - Local Bug Bounty Toolkit Router

### Workflow & Validation (5 skills)

- `bug-bounty/` - Master Orchestrator
- `bb-methodology/` - 5-Phase Non-Linear Workflow
- `triage-validation/` - 7-Question Gate
- `hunt-dispatch/` - Two-Track Dispatcher
- `security-arsenal/` - Payloads & Bypass Tables

### Reporting & Hygiene (4 skills)

- `report-writing/` - H1/Bugcrowd/Intigriti Templates
- `bugcrowd-reporting/` - VRT Mapping & Severity Requests
- `evidence-hygiene/` - Cookie/PII Redaction
- `redteam-report-template/` - Client-Facing Deliverable

### Specialized (2 skills)

- `web3-audit/` - DeFi/Smart Contract Audit
- `meme-coin-audit/` - Token Rug-Pull Detection

---

## 🎮 Commands (14 Total)

Located in `commands/` directory:

1. **autopilot.md** - Autonomous hunting mode
2. **chain.md** - Build exploit chains
3. **hunt.md** - Start hunting engagement
4. **intel.md** - Intelligence gathering
5. **memory-gc.md** - Memory management
6. **pickup.md** - Resume engagement
7. **recon.md** - Reconnaissance phase
8. **remember.md** - Save engagement state
9. **report.md** - Generate reports
10. **surface.md** - Attack surface mapping
11. **token-scan.md** - Token/Secret scanning
12. **triage.md** - Validate findings
13. **validate.md** - Validation gate
14. **web3-audit.md** - Web3 audit mode

---

## 🛠️ Scripts (5 Total)

Located in `scripts/` directory:

1. **cbh.py** - Claude-BugHunter CLI
   - `cbh recon <target>` - Passive recon
   - `cbh classify <url>` - Pattern matching
   - `cbh triage <finding.md>` - 7-Question Gate
   - `cbh report <finding.md>` - Report generation

2. **hunt.sh** - Engagement folder scaffolder

3. **install.sh** - Single-step installer

4. **install-community-skills.sh** - Refresh vendored skills

5. **refresh-cve-index.py** - CISA KEV refresh

---

## 📖 Documentation

Located in `docs/` directory:

### Main Guides
- **architecture.md** - System architecture
- **cbh-cli.md** - CLI reference
- **credits.md** - Attribution
- **cve-coverage.md** - CVE coverage matrix

### Disclosed Reports (Pattern Libraries)
Located in `docs/disclosed-reports/`:

- hunt-business-logic.md (7 reports)
- hunt-cache-poison.md (4 reports)
- hunt-csrf.md (10 reports)
- hunt-file-upload.md
- hunt-graphql.md (3 reports)
- hunt-http-smuggling.md
- hunt-idor.md (26 reports)
- hunt-mfa-bypass.md
- hunt-oauth.md (10 reports)
- hunt-rce.md (67 reports)
- hunt-saml.md
- hunt-sqli.md (8 reports)
- hunt-ssrf.md (9 reports)
- hunt-ssti.md
- hunt-xss.md (174 reports)

**Total: 681+ disclosed reports curated**

### Verification Labs
Located in `docs/verification/`:

- apache-cve-2021-41773.md
- jenkins-cve-2024-23897.md
- juice-shop-2026-05-15.md
- spring-cve-2022-22963.md
- hardened-lab-discipline-rules.md
- recon-hackerone-vdp.md
- phase2e-jwt-graphql-race.md
- phase2f-ssti-oauth-fileupload.md
- phase2g-saml-mfa-xxe.md
- phase2h-smuggling-cachepoison.md
- phase2i-llm-ato.md
- phase2j-cloud-localstack.md
- phase3-playwright-browser-execution.md

Plus lab environments with Docker configurations.

---

## 🚀 Quick Start

### 1. Read the Main Documentation
```bash
# Start here
cat claude-bughunter/CLAUDE_BUGHUNTER_README.md

# Usage guide
cat claude-bughunter/USAGE.md

# Installation
cat claude-bughunter/INSTALL.md
```

### 2. Explore Skills
```bash
# List all skills
ls claude-bughunter/skills/

# Read a specific skill
cat claude-bughunter/skills/hunt-xss/SKILL.md
```

### 3. Use Commands
```bash
# Read command documentation
cat claude-bughunter/commands/hunt.md
cat claude-bughunter/commands/recon.md
```

### 4. Run Scripts
```bash
# Use the CLI
python claude-bughunter/scripts/cbh.py recon target.com

# Scaffold engagement
bash claude-bughunter/scripts/hunt.sh target-name
```

---

## 🎓 Learning Path

### Beginner
1. Read `CLAUDE_BUGHUNTER_README.md`
2. Study `bb-methodology/SKILL.md`
3. Practice with `juice-shop-2026-05-15.md` lab
4. Learn the 7-Question Gate in `triage-validation/SKILL.md`

### Intermediate
5. Study specific `hunt-*/SKILL.md` for your target
6. Review disclosed reports in `docs/disclosed-reports/`
7. Practice with verification labs
8. Use `cbh.py` CLI for automation

### Advanced
9. Study enterprise platform attacks (M365, Okta, vCenter)
10. Learn red team tradecraft skills
11. Master exploit chaining
12. Contribute to the methodology

---

## 🔍 Finding What You Need

### By Vulnerability Type
```bash
# XSS
cat skills/hunt-xss/SKILL.md
cat docs/disclosed-reports/hunt-xss.md

# SQL Injection
cat skills/hunt-sqli/SKILL.md
cat docs/disclosed-reports/hunt-sqli.md

# IDOR
cat skills/hunt-idor/SKILL.md
cat docs/disclosed-reports/hunt-idor.md
```

### By Platform
```bash
# Microsoft 365
cat skills/m365-entra-attack/SKILL.md

# Okta
cat skills/okta-attack/SKILL.md

# SharePoint
cat skills/hunt-sharepoint/SKILL.md

# ASP.NET
cat skills/hunt-aspnet/SKILL.md
```

### By Phase
```bash
# Recon
cat skills/offensive-osint/SKILL.md
cat skills/web2-recon/SKILL.md

# Hunt
cat skills/hunt-dispatch/SKILL.md

# Validate
cat skills/triage-validation/SKILL.md

# Report
cat skills/report-writing/SKILL.md
```

---

## 📊 Statistics

- **Total Skills**: 51
- **Total Commands**: 14
- **Total Scripts**: 5
- **Disclosed Reports**: 681+
- **Verification Labs**: 13+
- **Documentation Files**: 45+

---

## 🤝 Integration with Bug Hunter Toolkit

These resources are now integrated with Bug Hunter Toolkit:

### Python Integration
```python
# Use skills in your Python code
from src.exploit_finder.cve_searcher import CVESearcher

# Reference Claude-BugHunter methodologies
# See: claude-bughunter/skills/bb-methodology/SKILL.md
```

### CLI Integration
```bash
# Bug Hunter Toolkit commands
python bug_hunter.py hunt apache

# Claude-BugHunter CLI
python claude-bughunter/scripts/cbh.py recon target.com
```

### Workflow Integration
1. Use Bug Hunter Toolkit for automated scanning
2. Reference Claude-BugHunter skills for manual testing
3. Follow disclosed report patterns
4. Apply 7-Question Gate validation
5. Generate reports using templates

---

## 📝 Notes

- All skills are in Markdown format
- Skills auto-load based on keywords (in Claude Code)
- Commands are slash commands for Claude Code
- Scripts can be run standalone
- Labs require Docker for some exercises

---

## 🔗 Original Project

**Claude-BugHunter** by Sachin Sharma
- GitHub: https://github.com/elementalsouls/Claude-BugHunter
- LinkedIn: https://www.linkedin.com/in/sachinsharma8080/

---

## 📄 License

These resources maintain their original licenses from Claude-BugHunter project.

---

**Last Updated**: 2026-05-26  
**Integration Version**: 3.0.0  
**Total Files Copied**: 133+

---

For questions about using these resources, see:
- [CLAUDE_BUGHUNTER_INTEGRATION.md](../CLAUDE_BUGHUNTER_INTEGRATION.md)
- [QUICKSTART.md](../QUICKSTART.md)
- [USAGE.md](USAGE.md)
