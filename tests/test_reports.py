"""
Tests for report generator
"""
import json
import tempfile
from pathlib import Path
import pytest
from src.reports import ReportGenerator


SAMPLE_RESULTS = {
    "target": "https://example.com",
    "vulnerabilities": [
        {"type": "Missing Security Header", "severity": "Medium", "description": "No CSP", "recommendation": "Add CSP"},
        {"type": "SQL Injection", "severity": "Critical", "url": "/login", "description": "SQLi in login", "recommendation": "Use parameterized queries"},
    ],
    "xss": [
        {"type": "XSS", "severity": "High", "url": "/search", "description": "Reflected XSS", "recommendation": "Encode output"},
    ],
    "csrf": [],
}


def test_collects_all_vulns():
    gen = ReportGenerator(SAMPLE_RESULTS)
    assert len(gen._all_vulns) == 3


def test_sorted_by_severity():
    gen = ReportGenerator(SAMPLE_RESULTS)
    severities = [v["severity"] for v in gen._all_vulns]
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
    assert severities == sorted(severities, key=lambda s: order.get(s, 99))


def test_summary_counts():
    gen = ReportGenerator(SAMPLE_RESULTS)
    s = gen._build_summary()
    assert s["total"] == 3
    assert s["by_severity"]["Critical"] == 1
    assert s["by_severity"]["High"] == 1
    assert s["by_severity"]["Medium"] == 1


def test_to_json():
    gen = ReportGenerator(SAMPLE_RESULTS, target="https://example.com")
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    gen.to_json(path)
    data = json.loads(Path(path).read_text())
    assert data["meta"]["target"] == "https://example.com"
    assert data["summary"]["total"] == 3
    assert len(data["findings"]) == 3


def test_to_markdown_contains_findings():
    gen = ReportGenerator(SAMPLE_RESULTS)
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        path = f.name
    gen.to_markdown(path)
    content = Path(path).read_text()
    assert "SQL Injection" in content
    assert "Critical" in content
    assert "https://example.com" in content


def test_to_html_contains_table():
    gen = ReportGenerator(SAMPLE_RESULTS)
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        path = f.name
    gen.to_html(path)
    content = Path(path).read_text()
    assert "<table>" in content
    assert "SQL Injection" in content
    assert "#d62728" in content  # Critical severity color


def test_empty_results():
    gen = ReportGenerator({})
    assert gen._all_vulns == []
    s = gen._build_summary()
    assert s["total"] == 0
