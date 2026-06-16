"""
Subdomain Enumeration Module
DNS-based subdomain discovery with wordlist bruteforce and certificate transparency
"""

import socket
import concurrent.futures
import requests
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
import dns.resolver
import dns.exception


class SubdomainEnumerator:
    """Enumerate subdomains using DNS resolution, CT logs, and wordlist bruteforce"""

    DEFAULT_WORDLIST = [
        "www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "beta",
        "vpn", "remote", "portal", "app", "shop", "blog", "docs", "support",
        "help", "status", "cdn", "static", "assets", "media", "images",
        "login", "auth", "secure", "dashboard", "panel", "backend", "frontend",
        "internal", "intranet", "extranet", "smtp", "pop", "imap", "mx",
        "ns1", "ns2", "dns", "ldap", "ssh", "git", "gitlab", "jenkins",
        "jira", "confluence", "grafana", "prometheus", "kibana", "elastic",
    ]

    def __init__(self, domain: str, threads: int = 30, timeout: float = 3.0):
        """
        Initialize subdomain enumerator.

        Args:
            domain: Target root domain (e.g. 'example.com')
            threads: Concurrent DNS resolution workers
            timeout: DNS query timeout in seconds
        """
        self.domain = domain.lower().strip()
        self.threads = threads
        self.timeout = timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout
        self.resolver.timeout = timeout
        self.found: List[Dict] = []
        logger.info(f"SubdomainEnumerator initialised for: {self.domain}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def enumerate(self, wordlist: Optional[List[str]] = None) -> List[Dict]:
        """
        Run full enumeration: wordlist bruteforce + CT log lookup.

        Args:
            wordlist: Optional custom wordlist; falls back to built-in list

        Returns:
            List of dicts with keys: subdomain, ip, method
        """
        words = wordlist or self._load_wordlist() or self.DEFAULT_WORDLIST
        logger.info(f"Starting subdomain enumeration with {len(words)} words")

        bruteforce = self._bruteforce(words)
        ct_results = self._crtsh_lookup()

        # Merge and deduplicate
        seen: set = set()
        combined: List[Dict] = []
        for entry in bruteforce + ct_results:
            key = entry["subdomain"]
            if key not in seen:
                seen.add(key)
                combined.append(entry)

        self.found = sorted(combined, key=lambda x: x["subdomain"])
        logger.info(f"Enumeration complete. Found {len(self.found)} subdomains")
        return self.found

    def save(self, output_file: str = "subdomains.txt") -> str:
        """Save discovered subdomains to a text file."""
        path = Path(output_file)
        with path.open("w") as f:
            for entry in self.found:
                f.write(f"{entry['subdomain']}\t{entry.get('ip', 'N/A')}\t[{entry['method']}]\n")
        logger.info(f"Saved {len(self.found)} subdomains to {output_file}")
        return output_file

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve(self, subdomain: str) -> Optional[Dict]:
        """Attempt DNS A record resolution for a subdomain."""
        try:
            answers = self.resolver.resolve(subdomain, "A")
            ip = str(answers[0])
            logger.debug(f"Resolved: {subdomain} -> {ip}")
            return {"subdomain": subdomain, "ip": ip, "method": "bruteforce"}
        except (dns.exception.DNSException, Exception):
            return None

    def _bruteforce(self, words: List[str]) -> List[Dict]:
        """Concurrent DNS bruteforce."""
        candidates = [f"{w}.{self.domain}" for w in words]
        results: List[Dict] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._resolve, sub): sub for sub in candidates}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        logger.info(f"Bruteforce found {len(results)} subdomains")
        return results

    def _crtsh_lookup(self) -> List[Dict]:
        """
        Query crt.sh certificate transparency logs.
        Returns subdomains seen in public TLS certificates.
        """
        logger.info(f"Querying crt.sh for {self.domain}")
        results: List[Dict] = []

        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                logger.warning(f"crt.sh returned {resp.status_code}")
                return results

            entries = resp.json()
            seen: set = set()

            for entry in entries:
                raw = entry.get("name_value", "")
                for name in raw.splitlines():
                    name = name.strip().lower().lstrip("*.")
                    if name.endswith(f".{self.domain}") and name not in seen:
                        seen.add(name)
                        # Try to resolve
                        try:
                            ip = socket.gethostbyname(name)
                        except Exception:
                            ip = "N/A"
                        results.append({"subdomain": name, "ip": ip, "method": "crt.sh"})

            logger.info(f"crt.sh found {len(results)} subdomains")

        except Exception as e:
            logger.error(f"crt.sh lookup failed: {e}")

        return results

    def _load_wordlist(self) -> Optional[List[str]]:
        """Load wordlist from common locations."""
        candidates = [
            Path("wordlists/subdomains.txt"),
            Path("/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"),
        ]
        for path in candidates:
            if path.exists():
                words = [line.strip() for line in path.read_text().splitlines() if line.strip()]
                logger.info(f"Loaded {len(words)} words from {path}")
                return words
        return None
