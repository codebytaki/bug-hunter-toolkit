#!/usr/bin/env python3
"""
Practical Bug Hunting Demo
Demonstrates using Bug Hunter Toolkit with Claude-BugHunter methodologies
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

console = Console()

def show_banner():
    """Display demo banner"""
    console.print(Panel.fit(
        "[bold cyan]🎯 Bug Hunter Toolkit - Practical Demo[/bold cyan]\n"
        "[yellow]Using Claude-BugHunter Methodologies[/yellow]",
        border_style="cyan"
    ))

def show_skills_overview():
    """Show available Claude-BugHunter skills"""
    console.print("\n[bold cyan]📚 Available Claude-BugHunter Skills[/bold cyan]\n")
    
    skills_dir = Path("claude-bughunter/skills")
    if not skills_dir.exists():
        console.print("[red]Claude-BugHunter skills not found![/red]")
        return
    
    # Count skills by category
    categories = {
        "Web Hunting": ["hunt-xss", "hunt-sqli", "hunt-idor", "hunt-ssrf", "hunt-rce"],
        "Authentication": ["hunt-ato", "hunt-auth-bypass", "hunt-mfa-bypass", "hunt-oauth"],
        "API & Modern": ["hunt-api-misconfig", "hunt-graphql", "hunt-file-upload"],
        "Enterprise": ["m365-entra-attack", "okta-attack", "vmware-vcenter-attack"],
        "Methodology": ["bb-methodology", "triage-validation", "evidence-hygiene"]
    }
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Skills", style="yellow", width=50)
    table.add_column("Count", style="green", width=10)
    
    for category, skills in categories.items():
        available = [s for s in skills if (skills_dir / s).exists()]
        table.add_row(
            category,
            ", ".join(available[:3]) + ("..." if len(available) > 3 else ""),
            str(len(available))
        )
    
    console.print(table)
    
    total_skills = len(list(skills_dir.glob("*/")))
    console.print(f"\n[green]✓[/green] Total Skills Available: [bold]{total_skills}[/bold]")

def show_methodology():
    """Show the 5-phase bug hunting methodology"""
    console.print("\n[bold cyan]🎯 5-Phase Bug Hunting Methodology[/bold cyan]\n")
    
    phases = [
        ("1. SCOPE", "Define engagement boundaries, read program rules"),
        ("2. RECON", "Asset discovery, subdomain enum, endpoint mapping"),
        ("3. HUNT", "Active vulnerability testing using hunt-* skills"),
        ("4. VALIDATE", "Apply 7-Question Gate before reporting"),
        ("5. REPORT", "Professional documentation with evidence")
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Phase", style="cyan", width=15)
    table.add_column("Description", style="white", width=60)
    
    for phase, desc in phases:
        table.add_row(phase, desc)
    
    console.print(table)

def show_7_question_gate():
    """Show the 7-Question Validation Gate"""
    console.print("\n[bold cyan]✅ 7-Question Validation Gate[/bold cyan]\n")
    console.print("[yellow]Apply this before reporting any finding:[/yellow]\n")
    
    questions = [
        "Q1: Can attacker use this RIGHT NOW with a real HTTP request?",
        "Q2: Is the impact on the program's accepted-impact list?",
        "Q3: Is the asset in scope?",
        "Q4: Does it work without privileged access attacker can't get?",
        "Q5: Is this not already known or documented behavior?",
        "Q6: Can impact be proved beyond 'technically possible'?",
        "Q7: Is this not on the never-submit list?"
    ]
    
    for q in questions:
        console.print(f"  [green]✓[/green] {q}")
    
    console.print("\n[yellow]All 7 must be YES to proceed with reporting![/yellow]")

def show_xss_hunting_guide():
    """Show XSS hunting methodology"""
    console.print("\n[bold cyan]🔍 XSS Hunting Guide (hunt-xss skill)[/bold cyan]\n")
    
    xss_skill = Path("claude-bughunter/skills/hunt-xss/SKILL.md")
    if xss_skill.exists():
        console.print("[green]✓[/green] XSS skill found with 174+ disclosed report patterns\n")
        
        console.print("[bold]Key Testing Points:[/bold]")
        console.print("  • Reflected XSS in URL parameters")
        console.print("  • Stored XSS in user inputs")
        console.print("  • DOM-based XSS in JavaScript")
        console.print("  • Blind XSS in admin panels")
        
        console.print("\n[bold]Common Payloads:[/bold]")
        payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert(1)>',
            '<svg/onload=alert(1)>',
            'javascript:alert(1)',
            '"><script>alert(String.fromCharCode(88,83,83))</script>'
        ]
        for payload in payloads:
            console.print(f"  • [yellow]{payload}[/yellow]")
        
        console.print(f"\n[cyan]Full methodology:[/cyan] {xss_skill}")
    else:
        console.print("[red]XSS skill not found![/red]")

def show_idor_hunting_guide():
    """Show IDOR hunting methodology"""
    console.print("\n[bold cyan]🔍 IDOR Hunting Guide (hunt-idor skill)[/bold cyan]\n")
    
    idor_skill = Path("claude-bughunter/skills/hunt-idor/SKILL.md")
    if idor_skill.exists():
        console.print("[green]✓[/green] IDOR skill found with 26+ disclosed report patterns\n")
        
        console.print("[bold]What to Look For:[/bold]")
        console.print("  • Numeric IDs in URLs (/users/42, /orders/123)")
        console.print("  • UUID/GUID parameters")
        console.print("  • API endpoints with object references")
        console.print("  • GraphQL node() queries")
        
        console.print("\n[bold]Testing Approach:[/bold]")
        console.print("  1. Create two test accounts (User A and User B)")
        console.print("  2. Access User A's resource with User B's session")
        console.print("  3. Try HTTP method changes (GET → POST, PUT, DELETE)")
        console.print("  4. Test array wrapping: id=123 → id[]=123")
        console.print("  5. Check for wildcard access: id=* or id=all")
        
        console.print(f"\n[cyan]Full methodology:[/cyan] {idor_skill}")
    else:
        console.print("[red]IDOR skill not found![/red]")

def show_practical_example():
    """Show a practical hunting example"""
    console.print("\n[bold cyan]💡 Practical Example: Testing a Web Application[/bold cyan]\n")
    
    console.print("[bold]Scenario:[/bold] Testing https://example.com/api/users/42\n")
    
    console.print("[bold yellow]Step 1: Classify the URL[/bold yellow]")
    console.print("  Pattern detected: Numeric ID in API endpoint")
    console.print("  Relevant skills: hunt-idor, hunt-api-misconfig")
    console.print("  Command: [cyan]python claude-bughunter/scripts/cbh.py classify 'https://example.com/api/users/42'[/cyan]\n")
    
    console.print("[bold yellow]Step 2: Study the Methodology[/bold yellow]")
    console.print("  Read: [cyan]claude-bughunter/skills/hunt-idor/SKILL.md[/cyan]")
    console.print("  Review: [cyan]claude-bughunter/docs/disclosed-reports/hunt-idor.md[/cyan]\n")
    
    console.print("[bold yellow]Step 3: Test for IDOR[/bold yellow]")
    console.print("  1. Login as User A (ID: 42)")
    console.print("  2. Access: GET /api/users/42 → 200 OK (own data)")
    console.print("  3. Try: GET /api/users/43 → 200 OK (other user's data) ⚠️")
    console.print("  4. Verify: Can see email, phone, address of user 43\n")
    
    console.print("[bold yellow]Step 4: Validate with 7-Question Gate[/bold yellow]")
    console.print("  Q1: Real HTTP request? ✓ YES (curl command works)")
    console.print("  Q2: Accepted impact? ✓ YES (PII disclosure)")
    console.print("  Q3: In scope? ✓ YES (api.example.com in scope)")
    console.print("  Q4: No admin needed? ✓ YES (any user can exploit)")
    console.print("  Q5: Not known? ✓ YES (not in disclosed reports)")
    console.print("  Q6: Concrete impact? ✓ YES (actual PII leaked)")
    console.print("  Q7: Not never-submit? ✓ YES (valid finding)")
    console.print("  [green]VERDICT: PASS - Proceed to report![/green]\n")
    
    console.print("[bold yellow]Step 5: Capture Evidence[/bold yellow]")
    console.print("  Apply evidence hygiene: [cyan]claude-bughunter/skills/evidence-hygiene/SKILL.md[/cyan]")
    console.print("  • Redact cookies and session tokens")
    console.print("  • Black-bar PII in screenshots")
    console.print("  • Sanitize HAR files\n")
    
    console.print("[bold yellow]Step 6: Generate Report[/bold yellow]")
    console.print("  Command: [cyan]python claude-bughunter/scripts/cbh.py report finding.md --platform h1[/cyan]")
    console.print("  Include: CVE references, CVSS score, remediation steps")

def show_resources():
    """Show available resources"""
    console.print("\n[bold cyan]📚 Available Resources[/bold cyan]\n")
    
    resources = [
        ("Skills", "claude-bughunter/skills/", "51 bug hunting methodologies"),
        ("Commands", "claude-bughunter/commands/", "14 slash commands"),
        ("Scripts", "claude-bughunter/scripts/", "Automation tools (cbh.py)"),
        ("Disclosed Reports", "claude-bughunter/docs/disclosed-reports/", "681+ report patterns"),
        ("Verification Labs", "claude-bughunter/docs/verification/", "Practice environments"),
        ("Documentation", "claude-bughunter/docs/", "Guides and references")
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Resource", style="cyan", width=20)
    table.add_column("Location", style="yellow", width=40)
    table.add_column("Description", style="white", width=30)
    
    for name, location, desc in resources:
        exists = "✓" if Path(location).exists() else "✗"
        table.add_row(f"{exists} {name}", location, desc)
    
    console.print(table)

def show_next_steps():
    """Show recommended next steps"""
    console.print("\n[bold cyan]🚀 Next Steps[/bold cyan]\n")
    
    steps = [
        ("1. Study Methodology", "cat claude-bughunter/skills/bb-methodology/SKILL.md"),
        ("2. Learn Validation", "cat claude-bughunter/skills/triage-validation/SKILL.md"),
        ("3. Pick a Skill", "cat claude-bughunter/skills/hunt-xss/SKILL.md"),
        ("4. Review Patterns", "cat claude-bughunter/docs/disclosed-reports/hunt-xss.md"),
        ("5. Practice Lab", "cat claude-bughunter/docs/verification/juice-shop-2026-05-15.md"),
        ("6. Start Hunting", "python bug_hunter.py scan https://target.com")
    ]
    
    for step, command in steps:
        console.print(f"  [green]✓[/green] [bold]{step}[/bold]")
        console.print(f"    [cyan]{command}[/cyan]\n")

def main():
    """Main demo function"""
    show_banner()
    
    console.print("\n[bold]This demo shows how to use Bug Hunter Toolkit with Claude-BugHunter methodologies[/bold]\n")
    
    # Show all sections
    show_skills_overview()
    show_methodology()
    show_7_question_gate()
    show_xss_hunting_guide()
    show_idor_hunting_guide()
    show_practical_example()
    show_resources()
    show_next_steps()
    
    console.print("\n" + "=" * 80)
    console.print(Panel.fit(
        "[bold green]✅ Demo Complete![/bold green]\n"
        "[yellow]You now understand how to use the toolkit with Claude-BugHunter skills[/yellow]\n\n"
        "[cyan]Start hunting: python bug_hunter.py --help[/cyan]",
        border_style="green"
    ))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n\n[red]Error: {str(e)}[/red]")
        sys.exit(1)
