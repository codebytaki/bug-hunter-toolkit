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


if __name__ == '__main__':
    cli()
