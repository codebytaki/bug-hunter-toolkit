# Architecture

## Hunt Methodology Flow

```
Target Domain / URL
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                     RECON                           │
│                                                     │
│  SubdomainEnumerator                                │
│  ├── DNS bruteforce (concurrent, 30 workers)        │
│  └── crt.sh CT log lookup                          │
│                                                     │
│  PortScanner                                        │
│  ├── TCP connect (100 concurrent workers)           │
│  ├── Banner grabbing                                │
│  └── Risk assessment                               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                  ENUMERATION                        │
│                                                     │
│  WebAppTester                                       │
│  ├── Form discovery (BeautifulSoup)                 │
│  ├── XSS: reflected payload injection               │
│  ├── SQLi: error-based detection                    │
│  └── CSRF: token absence check                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│             VULNERABILITY SCANNING                  │
│                                                     │
│  VulnerabilityScanner                               │
│  ├── Security headers check (7 headers)             │
│  ├── SSL/TLS validation                             │
│  ├── Exposed sensitive files (.env, config.php...)  │
│  ├── Directory listing detection                    │
│  ├── Information disclosure (Server header)         │
│  └── Dangerous HTTP methods (PUT, DELETE, TRACE)    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│            CVE & EXPLOIT INTELLIGENCE               │
│                                                     │
│  CVESearcher                                        │
│  ├── CIRCL API (cve.circl.lu)                       │
│  ├── Keyword & product search                       │
│  ├── Recent CVE feed                                │
│  └── Exploitable CVE detection (PoC references)    │
│                                                     │
│  ExploitAggregator                                  │
│  ├── Exploit-DB query                               │
│  ├── Metasploit module suggestions                  │
│  └── searchsploit command generation               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                   REPORTING                         │
│                                                     │
│  ReportGenerator                                    │
│  ├── JSON  (machine-readable, API-compatible)       │
│  ├── Markdown (GitHub/Jira-friendly)                │
│  └── HTML  (self-contained, dark theme dashboard)  │
└─────────────────────────────────────────────────────┘
```

## Module Structure

```
src/
├── scanner/
│   └── vulnerability_scanner.py   # Header, SSL, file, method checks
├── web_tester/
│   └── web_app_tester.py          # XSS, SQLi, CSRF form testing
├── subdomain/
│   └── __init__.py                # DNS bruteforce + crt.sh CT logs
├── network/
│   └── __init__.py                # TCP port scanner + banner grabbing
├── exploit_finder/
│   ├── cve_searcher.py            # CIRCL/NVD CVE API wrapper
│   └── exploitdb_searcher.py      # Exploit-DB + Metasploit advisor
└── reports/
    └── __init__.py                # JSON / Markdown / HTML report generator
```

## CLI Command Map

```
bug_hunter.py
├── scan      <target>          Full vulnerability scan
├── webtest   <target>          XSS / SQLi / CSRF tests
├── subdomain <domain>          DNS bruteforce + CT log
├── portscan  <target>          TCP port scan + banners
├── cve       <keyword>         CVE database search
├── cveinfo   <CVE-ID>          Specific CVE details
├── exploit   <keyword>         Exploit-DB search
├── hunt      <keyword>         CVE + Exploit combined
└── report    <json_file>       Generate HTML/MD from scan JSON
```

## Data Flow: Full Hunt

```
bug_hunter.py hunt target.com --output results.json
        │
        ├── CVESearcher.search_exploitable_cves("target.com")
        │         └── GET cve.circl.lu/api/search/target.com
        │
        ├── ExploitAggregator.search_all_sources("target.com")
        │         └── Exploit-DB query + searchsploit command
        │
        └── JSON output: { keyword, cves[], exploits{}, timestamp }
```

## Rate Limiting & Ethics

- All HTTP requests use a session with `User-Agent: BugHunterToolkit/3.0`
- DNS resolution timeout: 3s per subdomain
- Port scan timeout: 1s per port (configurable)
- Web tester uses non-destructive payloads only (no writes/deletes)
- No automatic exploitation — toolkit is detection + reporting only
- **Always obtain written authorization before testing any system**
