#!/usr/bin/env python3
"""
Comprehensive Hunt Example
Demonstrates the full workflow: Scan → CVE Search → Exploit Search → Report
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scanner.vulnerability_scanner import VulnerabilityScanner
from src.web_tester.web_app_tester import WebAppTester
from src.exploit_finder.cve_searcher import CVESearcher
from src.exploit_finder.exploitdb_searcher import ExploitAggregator
from loguru import logger


def comprehensive_hunt(target: str, technology: str = None):
    """
    Perform comprehensive security hunt
    
    Args:
        target: Target URL to scan
        technology: Technology stack (e.g., 'apache', 'wordpress')
    """
    print("=" * 70)
    print("🎯 COMPREHENSIVE SECURITY HUNT")
    print("=" * 70)
    print(f"\nTarget: {target}")
    if technology:
        print(f"Technology: {technology}")
    print("\n")
    
    results = {
        'target': target,
        'technology': technology,
        'scan_results': {},
        'web_test_results': {},
        'cve_results': [],
        'exploit_results': {}
    }
    
    # Phase 1: Vulnerability Scanning
    print("📡 Phase 1: Vulnerability Scanning")
    print("-" * 70)
    try:
        scanner = VulnerabilityScanner(target, timeout=10, threads=5)
        scan_results = scanner.scan()
        results['scan_results'] = scan_results
        
        print(f"✓ Found {scan_results.get('total_vulnerabilities', 0)} vulnerabilities")
        print(f"  Duration: {scan_results.get('duration', 'N/A')}")
    except Exception as e:
        print(f"✗ Scanning error: {str(e)}")
        logger.error(f"Scan error: {str(e)}")
    
    print("\n")
    
    # Phase 2: Web Application Testing
    print("🌐 Phase 2: Web Application Testing")
    print("-" * 70)
    try:
        tester = WebAppTester(target, timeout=10)
        web_results = tester.test_all()
        results['web_test_results'] = web_results
        
        print(f"✓ XSS vulnerabilities: {len(web_results.get('xss', []))}")
        print(f"✓ SQLi vulnerabilities: {len(web_results.get('sqli', []))}")
        print(f"✓ CSRF vulnerabilities: {len(web_results.get('csrf', []))}")
        print(f"  Total: {web_results.get('total_vulnerabilities', 0)}")
    except Exception as e:
        print(f"✗ Web testing error: {str(e)}")
        logger.error(f"Web test error: {str(e)}")
    
    print("\n")
    
    # Phase 3: CVE Intelligence
    if technology:
        print(f"🔍 Phase 3: CVE Intelligence for {technology}")
        print("-" * 70)
        try:
            cve_searcher = CVESearcher()
            
            # Search for CVEs
            cves = cve_searcher.search_by_keyword(technology, limit=15)
            results['cve_results'] = cves
            
            print(f"✓ Found {len(cves)} CVEs")
            
            # Show top critical CVEs
            critical_cves = [c for c in cves if c.get('cvss', 0) != 'N/A' and float(c.get('cvss', 0)) >= 7.0]
            if critical_cves:
                print(f"\n  Critical CVEs (CVSS >= 7.0):")
                for cve in critical_cves[:5]:
                    print(f"    • {cve.get('cve_id')} (CVSS: {cve.get('cvss')})")
            
            # Search for exploitable CVEs
            exploitable = cve_searcher.search_exploitable_cves(technology)
            print(f"\n✓ Found {len(exploitable)} exploitable CVEs")
            
        except Exception as e:
            print(f"✗ CVE search error: {str(e)}")
            logger.error(f"CVE search error: {str(e)}")
    
    print("\n")
    
    # Phase 4: Exploit Intelligence
    if technology:
        print(f"💣 Phase 4: Exploit Intelligence for {technology}")
        print("-" * 70)
        try:
            aggregator = ExploitAggregator()
            exploit_results = aggregator.search_all_sources(technology)
            results['exploit_results'] = exploit_results
            
            print(f"✓ Exploit sources aggregated")
            print(f"\n  Recommended commands:")
            print(f"    {exploit_results.get('searchsploit_command', 'N/A')}")
            
            if exploit_results.get('recommendations'):
                print(f"\n  Additional resources:")
                for rec in exploit_results.get('recommendations', [])[:3]:
                    print(f"    • {rec}")
            
        except Exception as e:
            print(f"✗ Exploit search error: {str(e)}")
            logger.error(f"Exploit search error: {str(e)}")
    
    print("\n")
    
    # Phase 5: Summary & Recommendations
    print("📊 Phase 5: Hunt Summary")
    print("=" * 70)
    
    total_issues = (
        results['scan_results'].get('total_vulnerabilities', 0) +
        results['web_test_results'].get('total_vulnerabilities', 0)
    )
    
    print(f"\n  Total Issues Found: {total_issues}")
    print(f"  CVEs Identified: {len(results.get('cve_results', []))}")
    print(f"  Exploit Sources: Multiple databases")
    
    print(f"\n  Priority Actions:")
    print(f"    1. Review and validate all {total_issues} vulnerabilities")
    print(f"    2. Check CVE references for patch availability")
    print(f"    3. Search for working exploits using provided commands")
    print(f"    4. Generate detailed security report")
    print(f"    5. Implement remediation measures")
    
    # Save results
    output_file = f"hunt_results_{technology or 'target'}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Results saved to: {output_file}")
    print("\n" + "=" * 70)
    
    return results


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Comprehensive Security Hunt Example"
    )
    parser.add_argument(
        'target',
        help='Target URL (e.g., https://example.com)'
    )
    parser.add_argument(
        '--tech',
        help='Technology stack (e.g., apache, wordpress, nginx)'
    )
    
    args = parser.parse_args()
    
    try:
        comprehensive_hunt(args.target, args.tech)
    except KeyboardInterrupt:
        print("\n\n⚠️  Hunt interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {str(e)}")
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
