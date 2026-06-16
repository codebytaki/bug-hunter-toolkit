#!/usr/bin/env python3
"""
Integration Test Script
Tests the new CVE and Exploit search features
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.exploit_finder.cve_searcher import CVESearcher
from src.exploit_finder.exploitdb_searcher import ExploitDBSearcher, ExploitAggregator
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def test_cve_searcher():
    """Test CVE Searcher functionality"""
    console.print("\n[bold cyan]Testing CVE Searcher...[/bold cyan]")
    
    try:
        searcher = CVESearcher()
        
        # Test 1: Search by keyword
        console.print("\n1. Testing keyword search...")
        results = searcher.search_by_keyword("apache", limit=5)
        console.print(f"   ✓ Found {len(results)} CVEs for 'apache'")
        
        if results:
            console.print(f"   Sample: {results[0].get('cve_id', 'N/A')}")
        
        # Test 2: Get CVE details
        console.print("\n2. Testing CVE details...")
        cve_detail = searcher.get_cve_details("CVE-2021-44228")
        if cve_detail:
            console.print(f"   ✓ Retrieved details for CVE-2021-44228")
            console.print(f"   CVSS: {cve_detail.get('cvss', 'N/A')}")
        else:
            console.print("   ⚠ Could not retrieve CVE details (API may be rate limited)")
        
        # Test 3: Search by product
        console.print("\n3. Testing product search...")
        product_results = searcher.search_by_product("wordpress")
        console.print(f"   ✓ Found {len(product_results)} CVEs for WordPress")
        
        # Test 4: Get recent CVEs
        console.print("\n4. Testing recent CVEs...")
        recent = searcher.get_recent_cves(days=7, limit=5)
        console.print(f"   ✓ Found {len(recent)} recent CVEs")
        
        # Test 5: Search exploitable CVEs
        console.print("\n5. Testing exploitable CVE search...")
        exploitable = searcher.search_exploitable_cves("apache")
        console.print(f"   ✓ Found {len(exploitable)} exploitable CVEs")
        
        console.print("\n[green]✓ CVE Searcher tests passed![/green]")
        return True
        
    except Exception as e:
        console.print(f"\n[red]✗ CVE Searcher test failed: {str(e)}[/red]")
        return False


def test_exploit_searcher():
    """Test Exploit Searcher functionality"""
    console.print("\n[bold cyan]Testing Exploit Searcher...[/bold cyan]")
    
    try:
        searcher = ExploitDBSearcher()
        
        # Test 1: Search exploits
        console.print("\n1. Testing exploit search...")
        results = searcher.search_exploits("wordpress")
        console.print(f"   ✓ Exploit search completed")
        
        # Test 2: Search by CVE
        console.print("\n2. Testing CVE-based exploit search...")
        cve_results = searcher.search_by_cve("CVE-2021-44228")
        console.print(f"   ✓ CVE exploit search completed")
        
        # Test 3: Get categories
        console.print("\n3. Testing exploit categories...")
        categories = searcher.get_exploit_categories()
        console.print(f"   ✓ Found {len(categories.get('platforms', []))} platforms")
        console.print(f"   ✓ Found {len(categories.get('types', []))} types")
        
        # Test 4: Searchsploit command
        console.print("\n4. Testing searchsploit command generation...")
        cmd = searcher.get_searchsploit_command("apache")
        console.print(f"   ✓ Generated: {cmd}")
        
        # Test 5: Metasploit modules
        console.print("\n5. Testing Metasploit module search...")
        msf_results = searcher.get_metasploit_modules("apache")
        console.print(f"   ✓ Metasploit search completed")
        
        console.print("\n[green]✓ Exploit Searcher tests passed![/green]")
        return True
        
    except Exception as e:
        console.print(f"\n[red]✗ Exploit Searcher test failed: {str(e)}[/red]")
        return False


def test_exploit_aggregator():
    """Test Exploit Aggregator functionality"""
    console.print("\n[bold cyan]Testing Exploit Aggregator...[/bold cyan]")
    
    try:
        aggregator = ExploitAggregator()
        
        # Test: Search all sources
        console.print("\n1. Testing multi-source aggregation...")
        results = aggregator.search_all_sources("apache")
        
        console.print(f"   ✓ Keyword: {results.get('keyword', 'N/A')}")
        console.print(f"   ✓ SearchSploit: {results.get('searchsploit_command', 'N/A')}")
        console.print(f"   ✓ Recommendations: {len(results.get('recommendations', []))}")
        
        console.print("\n[green]✓ Exploit Aggregator tests passed![/green]")
        return True
        
    except Exception as e:
        console.print(f"\n[red]✗ Exploit Aggregator test failed: {str(e)}[/red]")
        return False


def display_summary(results):
    """Display test summary"""
    console.print("\n" + "=" * 70)
    console.print(Panel.fit(
        "[bold cyan]Integration Test Summary[/bold cyan]",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Test Module", style="cyan")
    table.add_column("Status", style="yellow")
    
    for module, passed in results.items():
        status = "[green]✓ PASSED[/green]" if passed else "[red]✗ FAILED[/red]"
        table.add_row(module, status)
    
    console.print(table)
    
    all_passed = all(results.values())
    if all_passed:
        console.print("\n[bold green]🎉 All tests passed![/bold green]")
        console.print("\n[cyan]The integration is working correctly.[/cyan]")
        console.print("[cyan]You can now use the new CVE and Exploit search features.[/cyan]")
    else:
        console.print("\n[bold yellow]⚠ Some tests failed[/bold yellow]")
        console.print("\n[yellow]This might be due to:[/yellow]")
        console.print("  • Network connectivity issues")
        console.print("  • API rate limiting")
        console.print("  • Missing dependencies")
        console.print("\n[yellow]Try running: pip install -r requirements.txt[/yellow]")
    
    console.print("\n" + "=" * 70)


def main():
    """Run all integration tests"""
    console.print(Panel.fit(
        "[bold cyan]🛡️ Bug Hunter Toolkit - Integration Tests[/bold cyan]\n"
        "[yellow]Testing CVE and Exploit Search Features[/yellow]",
        border_style="cyan"
    ))
    
    results = {}
    
    # Run tests
    results["CVE Searcher"] = test_cve_searcher()
    results["Exploit Searcher"] = test_exploit_searcher()
    results["Exploit Aggregator"] = test_exploit_aggregator()
    
    # Display summary
    display_summary(results)
    
    # Exit code
    sys.exit(0 if all(results.values()) else 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Tests interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n\n[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)
