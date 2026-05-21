"""
Tests for Web Application Tester
"""

import pytest
from src.web_tester.web_app_tester import WebAppTester


def test_web_tester_initialization():
    """Test web tester initialization"""
    tester = WebAppTester("https://example.com")
    assert tester.target == "https://example.com"
    assert tester.timeout == 10


def test_xss_test_returns_list():
    """Test XSS testing returns a list"""
    tester = WebAppTester("https://example.com", timeout=5)
    results = tester.test_xss()
    assert isinstance(results, list)


def test_sqli_test_returns_list():
    """Test SQLi testing returns a list"""
    tester = WebAppTester("https://example.com", timeout=5)
    results = tester.test_sqli()
    assert isinstance(results, list)


def test_csrf_test_returns_list():
    """Test CSRF testing returns a list"""
    tester = WebAppTester("https://example.com", timeout=5)
    results = tester.test_csrf()
    assert isinstance(results, list)


def test_all_tests():
    """Test running all tests"""
    tester = WebAppTester("https://example.com", timeout=5)
    results = tester.test_all()
    
    assert isinstance(results, dict)
    assert 'target' in results
    assert 'xss' in results
    assert 'sqli' in results
    assert 'csrf' in results
    assert 'total_vulnerabilities' in results


def test_web_tester_with_invalid_url():
    """Test web tester with invalid URL"""
    tester = WebAppTester("invalid-url")
    # Should handle gracefully
    assert tester.target == "invalid-url"
