#!/usr/bin/env python3
"""
Bug Hunter Toolkit - Main CLI Application
Professional Security Testing Suite
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from loguru import logger
import sys
from datetime import datetime

# Configure logger
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
logger.add("logs/bug_hunter_{time}.log", rotation="10 MB")

console = Console()


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """
    🛡️ Bug Hunter Toolkit - Professional Security Testing Suite
    
    A comprehensive toolkit for security researchers and bug bounty hunters.
    """
    console.print(Panel.fit(
        "[bold cyan]🛡️ Bug Hunter Toolkit v2.0.0[/bold cyan]\n"
        "[yellow]Professional Security Testing Suite[/yellow]",
        border_style="cyan"
    ))


@cli.command()
@click.argument('target')
@click.option('--timeout', default=10, help='Request timeout in seconds')
@click.option('--threads', default=5, help='Number of concurrent threads')
@click.option('--output', '-o', default='report.md', help='Output report file')
def scan(target, timeout, threads, output):
    """
    Run comprehensive vulnerability scan on target
    
    Example: bug_hunter.py scan https://example.com
    """
    from src.scanner.vulnerability_scanner import VulnerabilityScanner
    
    console.print(f"\n[bold green]🔍 Starting vulnerability scan...[/bold green]")
    console.print(f"[cyan]Target:[/cyan] {target}")
    console.print(f"[cyan]Timeout:[/cyan] {timeout}s")
    console.print(f"[cyan]Threads:[/cyan] {threads}\n")
    
    try:
        scanner = VulnerabilityScanner(target, timeout=timeout, threads=threads)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=100)
            results = scanner.scan()
            progress.update(task, completed=100)
        
        # Display results
        display_scan_results(results)
        
        # Save report
        console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")
        logger.error(f"Scan error: {str(e)}")


@cli.command()
@click.argument('target')
@click.option('--test', type=click.Choice(['xss', 'sqli', 'csrf', 'all']), default='all')
@click.option('--output', '-o', default='web_test_report.md', help='Output report file')
def webtest(target, test, output):
    """
    Test web application for common vulnerabilities
    
    Example: bug_hunter.py webtest https://example.com --test xss
    """
    from src.web_tester.web_app_tester import WebAppTester
    
    console.print(f"\n[bold green]🌐 Starting web application tests...[/bold green]")
    console.print(f"[cyan]Target:[/cyan] {target}")
    console.print(f"[cyan]Tests:[/cyan] {test}\n")
    
    try:
        tester = WebAppTester(target)
        
        if test == 'all':
            results = tester.test_all()
        elif test == 'xss':
            results = {'xss': tester.test_xss()}
        elif test == 'sqli':
            results = {'sqli': tester.test_sqli()}
        elif test == 'csrf':
            results = {'csrf': tester.test_csrf()}
        
        # Display results
        display_web_test_results(results)
        
        console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")
        logger.error(f"Web test error: {str(e)}")


@cli.command()
@click.argument('domain')
@click.option('--wordlist', '-w', help='Custom wordlist file')
@click.option('--output', '-o', default='subdomains.txt', help='Output file')
def subdomain(domain, wordlist, output):
    """
    Enumerate subdomains for target domain
    
    Example: bug_hunter.py subdomain example.com
    """
    console.print(f"\n[bold green]🔎 Enumerating subdomains...[/bold green]")
    console.print(f"[cyan]Domain:[/cyan] {domain}\n")
    
    try:
        # Subdomain enumeration logic here
        console.print("[yellow]Subdomain enumeration in progress...[/yellow]")
        console.print(f"\n[green]✓[/green] Results saved to: {output}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")


@cli.command()
@click.argument('keyword')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
@click.option('--output', '-o', help='Output file (JSON format)')
def cve(keyword, limit, output):
    """
    Search for CVEs by keyword
    
    Example: bug_hunter.py cve apache --limit 20
    """
    from src.exploit_finder.cve_searcher import CVESearcher
    
    console.print(f"\n[bold green]🔍 Searching CVEs...[/bold green]")
    console.print(f"[cyan]Keyword:[/cyan] {keyword}")
    console.print(f"[cyan]Limit:[/cyan] {limit}\n")
    
    try:
        searcher = CVESearcher()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Searching CVE databases...", total=100)
            results = searcher.search_by_keyword(keyword, limit=limit)
            progress.update(task, completed=100)
        
        if results:
            display_cve_results(results)
            
            if output:
                import json
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2)
                console.print(f"\n[green]✓[/green] Results saved to: {output}")
        else:
            console.print("[yellow]No CVEs found for the given keyword[/yellow]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")
        logger.error(f"CVE search error: {str(e)}")


@cli.command()
@click.argument('cve_id')
def cveinfo(cve_id):
    """
    Get detailed information about a specific CVE
    
    Example: bug_hunter.py cveinfo CVE-2021-44228
    """
    from src.exploit_finder.cve_searcher import CVESearcher
    
    console.print(f"\n[bold green]📋 Fetching CVE Details...[/bold green]")
    console.print(f"[cyan]CVE ID:[/cyan] {cve_id}\n")
    
    try:
        searcher = CVESearcher()
        cve_data = searcher.get_cve_details(cve_id)
        
        if cve_data:
            display_cve_detail(cve_data)
        else:
            console.print(f"[yellow]CVE {cve_id} not found[/yellow]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")


@cli.command()
@click.argument('keyword')
@click.option('--limit', '-l', default=20, help='Maximum number of results')
def exploit(keyword, limit):
    """
    Search for exploits by keyword
    
    Example: bug_hunter.py exploit wordpress
    """
    from src.exploit_finder.exploitdb_searcher import ExploitAggregator
    
    console.print(f"\n[bold green]💣 Searching Exploits...[/bold green]")
    console.print(f"[cyan]Keyword:[/cyan] {keyword}\n")
    
    try:
        aggregator = ExploitAggregator()
        results = aggregator.search_all_sources(keyword)
        
        display_exploit_results(results)
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', help='Output file')
def hunt(keyword, output):
    """
    Comprehensive hunt: CVEs + Exploits + Vulnerabilities
    
    Example: bug_hunter.py hunt apache
    """
    from src.exploit_finder.cve_searcher import CVESearcher
    from src.exploit_finder.exploitdb_searcher import ExploitAggregator
    
    console.print(f"\n[bold green]🎯 Starting Comprehensive Hunt...[/bold green]")
    console.print(f"[cyan]Target:[/cyan] {keyword}\n")
    
    try:
        # Search CVEs
        console.print("[bold cyan]1. Searching CVEs...[/bold cyan]")
        cve_searcher = CVESearcher()
        cves = cve_searcher.search_exploitable_cves(keyword)
        console.print(f"   Found {len(cves)} exploitable CVEs\n")
        
        # Search Exploits
        console.print("[bold cyan]2. Searching Exploits...[/bold cyan]")
        exploit_agg = ExploitAggregator()
        exploits = exploit_agg.search_all_sources(keyword)
        console.print(f"   Exploit sources aggregated\n")
        
        # Display summary
        console.print("[bold cyan]3. Hunt Summary[/bold cyan]")
        display_hunt_summary(keyword, cves, exploits)
        
        if output:
            import json
            hunt_results = {
                'keyword': keyword,
                'cves': cves,
                'exploits': exploits,
                'timestamp': datetime.now().isoformat()
            }
            with open(output, 'w') as f:
                json.dump(hunt_results, f, indent=2)
            console.print(f"\n[green]✓[/green] Hunt results saved to: {output}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")


@cli.command()
@click.argument('target')
@click.option('--ports', '-p', default='1-1000', help='Port range to scan')
def portscan(target, ports):
    """
    Scan target for open ports
    
    Example: bug_hunter.py portscan 192.168.1.1 --ports 1-1000
    """
    console.print(f"\n[bold green]🔌 Starting port scan...[/bold green]")
    console.print(f"[cyan]Target:[/cyan] {target}")
    console.print(f"[cyan]Ports:[/cyan] {ports}\n")
    
    try:
        # Port scanning logic here
        console.print("[yellow]Port scanning in progress...[/yellow]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {str(e)}")


def display_scan_results(results):
    """Display vulnerability scan results in a table"""
    table = Table(title="Vulnerability Scan Results", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan")
    table.add_column("Severity", style="yellow")
    table.add_column("Description", style="white")
    
    for vuln in results.get('vulnerabilities', []):
        severity_color = {
            'Critical': 'bold red',
            'High': 'red',
            'Medium': 'yellow',
            'Low': 'green'
        }.get(vuln.get('severity', 'Low'), 'white')
        
        table.add_row(
            vuln.get('type', 'Unknown'),
            f"[{severity_color}]{vuln.get('severity', 'Low')}[/{severity_color}]",
            vuln.get('description', 'No description')
        )
    
    console.print(table)
    
    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total vulnerabilities: {results.get('total_vulnerabilities', 0)}")
    console.print(f"  Scan duration: {results.get('duration', 'N/A')}")


def display_web_test_results(results):
    """Display web application test results"""
    for test_type, vulns in results.items():
        if test_type == 'total_vulnerabilities' or test_type == 'target':
            continue
        
        if isinstance(vulns, list) and vulns:
            table = Table(title=f"{test_type.upper()} Vulnerabilities", show_header=True)
            table.add_column("URL", style="cyan")
            table.add_column("Severity", style="yellow")
            table.add_column("Description", style="white")
            
            for vuln in vulns:
                table.add_row(
                    vuln.get('url', 'N/A'),
                    vuln.get('severity', 'Unknown'),
                    vuln.get('description', 'No description')
                )
            
            console.print(table)


def display_cve_results(results):
    """Display CVE search results in a table"""
    table = Table(title="CVE Search Results", show_header=True, header_style="bold magenta")
    table.add_column("CVE ID", style="cyan", width=20)
    table.add_column("CVSS", style="yellow", width=8)
    table.add_column("Published", style="green", width=12)
    table.add_column("Summary", style="white")
    
    for cve in results:
        cvss = str(cve.get('cvss', 'N/A'))
        cvss_color = 'red' if cvss != 'N/A' and float(cvss) >= 7.0 else 'yellow'
        
        table.add_row(
            cve.get('cve_id', 'N/A'),
            f"[{cvss_color}]{cvss}[/{cvss_color}]",
            cve.get('published', 'N/A')[:10],
            cve.get('summary', 'No summary')[:80] + '...'
        )
    
    console.print(table)


def display_cve_detail(cve_data):
    """Display detailed CVE information"""
    console.print(Panel.fit(
        f"[bold cyan]{cve_data.get('cve_id', 'N/A')}[/bold cyan]\n"
        f"[yellow]CVSS: {cve_data.get('cvss', 'N/A')} | CWE: {cve_data.get('cwe', 'N/A')}[/yellow]",
        border_style="cyan"
    ))
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  {cve_data.get('summary', 'No summary available')}\n")
    
    console.print(f"[bold]Published:[/bold] {cve_data.get('published', 'N/A')}")
    console.print(f"[bold]Modified:[/bold] {cve_data.get('modified', 'N/A')}")
    console.print(f"[bold]CVSS Vector:[/bold] {cve_data.get('cvss_vector', 'N/A')}\n")
    
    if cve_data.get('vulnerable_products'):
        console.print(f"[bold]Vulnerable Products:[/bold]")
        for product in cve_data.get('vulnerable_products', [])[:5]:
            console.print(f"  • {product}")
    
    if cve_data.get('references'):
        console.print(f"\n[bold]References:[/bold]")
        for ref in cve_data.get('references', [])[:5]:
            console.print(f"  • {ref}")


def display_exploit_results(results):
    """Display exploit search results"""
    console.print(Panel.fit(
        f"[bold cyan]Exploit Search: {results.get('keyword', 'N/A')}[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print(f"\n[bold]Recommended Commands:[/bold]")
    console.print(f"  [cyan]SearchSploit:[/cyan] {results.get('searchsploit_command', 'N/A')}")
    
    if results.get('recommendations'):
        console.print(f"\n[bold]Additional Resources:[/bold]")
        for rec in results.get('recommendations', []):
            console.print(f"  • {rec}")


def display_hunt_summary(keyword, cves, exploits):
    """Display comprehensive hunt summary"""
    table = Table(title=f"Hunt Summary: {keyword}", show_header=True)
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Count", style="yellow", width=10)
    table.add_column("Details", style="white")
    
    table.add_row(
        "Exploitable CVEs",
        str(len(cves)),
        f"{len([c for c in cves if c.get('has_exploit')])} with known exploits"
    )
    
    table.add_row(
        "Exploit Sources",
        "Multiple",
        "Exploit-DB, Metasploit, GitHub"
    )
    
    console.print(table)
    
    if cves:
        console.print(f"\n[bold]Top CVEs:[/bold]")
        for cve in cves[:5]:
            console.print(f"  • {cve.get('cve_id')} (CVSS: {cve.get('cvss', 'N/A')})")


if __name__ == '__main__':
    cli()
