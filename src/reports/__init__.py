"""
Report Generation Module
Produces Markdown, JSON, and HTML reports from scan results
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger


# Severity ordering for sorting
_SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}


def _severity_color(severity: str) -> str:
    return {
        "Critical": "#d62728",
        "High":     "#ff7f0e",
        "Medium":   "#e7ba52",
        "Low":      "#1f77b4",
        "Info":     "#aec7e8",
    }.get(severity, "#aec7e8")


class ReportGenerator:
    """Generate professional security reports in multiple formats."""

    def __init__(self, results: Dict[str, Any], target: str = ""):
        """
        Args:
            results: Combined scan results dict (from VulnerabilityScanner, WebAppTester, etc.)
            target:  Target URL/domain (used in headings)
        """
        self.results = results
        self.target = target or results.get("target", "Unknown")
        self.generated_at = datetime.utcnow().isoformat() + "Z"
        self._all_vulns: List[Dict] = self._collect_vulns()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def to_json(self, output_file: str = "report.json") -> str:
        """Export full results as JSON."""
        payload = {
            "meta": {
                "target": self.target,
                "generated_at": self.generated_at,
                "tool": "Bug Hunter Toolkit v3",
            },
            "summary": self._build_summary(),
            "findings": self._all_vulns,
            "raw": self.results,
        }
        Path(output_file).write_text(json.dumps(payload, indent=2, default=str))
        logger.info(f"JSON report written to {output_file}")
        return output_file

    def to_markdown(self, output_file: str = "report.md") -> str:
        """Generate a Markdown report."""
        summary = self._build_summary()
        lines: List[str] = [
            f"# 🛡️ Security Assessment Report",
            f"",
            f"**Target:** `{self.target}`  ",
            f"**Generated:** {self.generated_at}  ",
            f"**Tool:** Bug Hunter Toolkit v3",
            f"",
            f"---",
            f"",
            f"## Executive Summary",
            f"",
            f"| Severity | Count |",
            f"|----------|-------|",
        ]
        for sev in ["Critical", "High", "Medium", "Low", "Info"]:
            count = summary["by_severity"].get(sev, 0)
            if count:
                lines.append(f"| {sev} | {count} |")

        lines += [
            f"",
            f"**Total findings:** {summary['total']}",
            f"",
            f"---",
            f"",
            f"## Findings",
            f"",
        ]

        for i, vuln in enumerate(self._all_vulns, 1):
            sev = vuln.get("severity", "Info")
            lines += [
                f"### {i}. {vuln.get('type', 'Finding')} — {sev}",
                f"",
                f"- **URL/Location:** `{vuln.get('url', vuln.get('file', 'N/A'))}`",
                f"- **Description:** {vuln.get('description', 'N/A')}",
                f"- **Recommendation:** {vuln.get('recommendation', 'N/A')}",
                f"",
            ]
            if vuln.get("payload"):
                lines.append(f"```\nPayload: {vuln['payload']}\n```\n")

        Path(output_file).write_text("\n".join(lines))
        logger.info(f"Markdown report written to {output_file}")
        return output_file

    def to_html(self, output_file: str = "report.html") -> str:
        """Generate a self-contained HTML report."""
        summary = self._build_summary()
        rows = ""
        for vuln in self._all_vulns:
            sev = vuln.get("severity", "Info")
            color = _severity_color(sev)
            rows += (
                f"<tr>"
                f"<td>{vuln.get('type','N/A')}</td>"
                f"<td style='color:{color};font-weight:bold'>{sev}</td>"
                f"<td>{vuln.get('url', vuln.get('file','N/A'))}</td>"
                f"<td>{vuln.get('description','N/A')}</td>"
                f"<td>{vuln.get('recommendation','N/A')}</td>"
                f"</tr>"
            )

        sev_bars = ""
        total = max(summary["total"], 1)
        for sev, count in summary["by_severity"].items():
            pct = round(count / total * 100)
            color = _severity_color(sev)
            sev_bars += (
                f"<div style='margin:4px 0'>"
                f"<span style='display:inline-block;width:80px'>{sev}</span>"
                f"<span style='display:inline-block;background:{color};"
                f"width:{pct * 3}px;height:16px;vertical-align:middle'></span>"
                f" {count}"
                f"</div>"
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Security Report – {self.target}</title>
<style>
  body{{font-family:sans-serif;background:#0d1117;color:#c9d1d9;padding:2em}}
  h1{{color:#58a6ff}} h2{{color:#8b949e;border-bottom:1px solid #30363d;padding-bottom:.3em}}
  table{{width:100%;border-collapse:collapse;margin-top:1em}}
  th{{background:#161b22;color:#58a6ff;padding:8px;text-align:left}}
  td{{padding:8px;border-bottom:1px solid #21262d;font-size:.9em}}
  tr:hover td{{background:#161b22}}
  .meta{{color:#8b949e;font-size:.85em}}
</style>
</head>
<body>
<h1>🛡️ Security Assessment Report</h1>
<p class="meta">Target: <strong>{self.target}</strong> &nbsp;|&nbsp; Generated: {self.generated_at} &nbsp;|&nbsp; Tool: Bug Hunter Toolkit v3</p>

<h2>Summary</h2>
{sev_bars}
<p>Total findings: <strong>{summary['total']}</strong></p>

<h2>Findings</h2>
<table>
<thead><tr><th>Type</th><th>Severity</th><th>Location</th><th>Description</th><th>Recommendation</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>"""

        Path(output_file).write_text(html)
        logger.info(f"HTML report written to {output_file}")
        return output_file

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _collect_vulns(self) -> List[Dict]:
        """Flatten all vulnerability lists from the results dict."""
        vulns: List[Dict] = []

        # Direct list
        if isinstance(self.results, list):
            vulns = self.results
        else:
            # VulnerabilityScanner format
            vulns.extend(self.results.get("vulnerabilities", []))
            # WebAppTester format
            for key in ("xss", "sqli", "csrf"):
                vulns.extend(self.results.get(key, []))

        return sorted(vulns, key=lambda v: _SEVERITY_ORDER.get(v.get("severity", "Info"), 99))

    def _build_summary(self) -> Dict:
        counts: Dict[str, int] = {}
        for vuln in self._all_vulns:
            sev = vuln.get("severity", "Info")
            counts[sev] = counts.get(sev, 0) + 1
        return {"total": len(self._all_vulns), "by_severity": counts}
