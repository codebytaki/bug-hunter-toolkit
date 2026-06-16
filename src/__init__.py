"""
Bug Hunter Toolkit - Professional Security Testing Suite
"""

__version__ = "3.0.0"
__author__ = "Taki"

from .scanner.vulnerability_scanner import VulnerabilityScanner
from .web_tester.web_app_tester import WebAppTester

# Optional imports - only if modules exist
try:
    from .network.network_scanner import NetworkScanner
except ImportError:
    NetworkScanner = None

try:
    from .subdomain.subdomain_finder import SubdomainFinder
except ImportError:
    SubdomainFinder = None

try:
    from .reports.report_generator import ReportGenerator
except ImportError:
    ReportGenerator = None

# New CVE and Exploit modules
try:
    from .exploit_finder.cve_searcher import CVESearcher
    from .exploit_finder.exploitdb_searcher import ExploitDBSearcher, ExploitAggregator
except ImportError:
    CVESearcher = None
    ExploitDBSearcher = None
    ExploitAggregator = None

__all__ = [
    "VulnerabilityScanner",
    "WebAppTester",
    "NetworkScanner",
    "SubdomainFinder",
    "ReportGenerator",
    "CVESearcher",
    "ExploitDBSearcher",
    "ExploitAggregator",
]
