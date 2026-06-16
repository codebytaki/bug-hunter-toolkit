"""
Tests for subdomain enumerator
"""
import pytest
from unittest.mock import patch, MagicMock
from src.subdomain import SubdomainEnumerator


def test_init():
    e = SubdomainEnumerator("example.com")
    assert e.domain == "example.com"
    assert e.threads == 30


def test_domain_normalised():
    e = SubdomainEnumerator("  EXAMPLE.COM  ")
    assert e.domain == "example.com"


def test_parse_range_empty_by_default():
    e = SubdomainEnumerator("example.com")
    assert isinstance(e.DEFAULT_WORDLIST, list)
    assert len(e.DEFAULT_WORDLIST) > 10


@patch("src.subdomain.requests.get")
def test_crtsh_lookup_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"name_value": "api.example.com\nblog.example.com"},
        {"name_value": "*.example.com"},
    ]
    mock_get.return_value = mock_resp

    with patch("socket.gethostbyname", return_value="1.2.3.4"):
        e = SubdomainEnumerator("example.com")
        results = e._crtsh_lookup()

    assert any(r["subdomain"] == "api.example.com" for r in results)
    assert any(r["subdomain"] == "blog.example.com" for r in results)
    # Wildcard prefix should be stripped
    assert not any(r["subdomain"].startswith("*") for r in results)


@patch("src.subdomain.requests.get")
def test_crtsh_lookup_api_error(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp

    e = SubdomainEnumerator("example.com")
    results = e._crtsh_lookup()
    assert results == []


@patch("src.subdomain.requests.get", side_effect=Exception("network error"))
def test_crtsh_lookup_network_error(mock_get):
    e = SubdomainEnumerator("example.com")
    results = e._crtsh_lookup()
    assert results == []


def test_resolve_success():
    with patch("dns.resolver.Resolver.resolve") as mock_resolve:
        mock_ans = MagicMock()
        mock_ans.__str__ = lambda s: "1.2.3.4"
        mock_ans.__iter__ = lambda s: iter([mock_ans])
        mock_resolve.return_value = [mock_ans]
        e = SubdomainEnumerator("example.com")
        result = e._resolve("api.example.com")
    assert result is not None
    assert result["subdomain"] == "api.example.com"
    assert result["method"] == "bruteforce"


def test_resolve_nxdomain():
    import dns.exception
    with patch("dns.resolver.Resolver.resolve", side_effect=dns.exception.DNSException()):
        e = SubdomainEnumerator("example.com")
        result = e._resolve("notexist.example.com")
    assert result is None
