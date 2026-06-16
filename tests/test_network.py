"""
Tests for port scanner
"""
import pytest
from unittest.mock import patch, MagicMock
from src.network import PortScanner


def test_init_defaults():
    s = PortScanner("192.168.1.1")
    assert s.target == "192.168.1.1"
    assert s.timeout == 1.0
    assert s.threads == 100


def test_parse_range_dash():
    s = PortScanner("localhost", port_range="80-82")
    assert s.ports == [80, 81, 82]


def test_parse_range_csv():
    s = PortScanner("localhost", port_range="22,80,443")
    assert s.ports == [22, 80, 443]


def test_parse_range_mixed():
    s = PortScanner("localhost", port_range="22,80-82,443")
    assert 22 in s.ports
    assert 80 in s.ports
    assert 81 in s.ports
    assert 443 in s.ports


def test_parse_range_out_of_bounds():
    s = PortScanner("localhost", port_range="0,65536,80")
    # 0 and 65536 are out of valid range
    assert 80 in s.ports
    assert 0 not in s.ports
    assert 65536 not in s.ports


@patch("socket.gethostbyname", side_effect=Exception("resolve error"))
def test_scan_unresolvable_host(mock_resolve):
    s = PortScanner("notexist.invalid", port_range="80")
    result = s.scan()
    assert "error" in result


@patch("socket.gethostbyname", return_value="127.0.0.1")
def test_check_port_open(mock_gethostbyname):
    s = PortScanner("localhost", port_range="80")
    s._resolved_ip = "127.0.0.1"
    with patch("socket.socket") as MockSocket:
        instance = MockSocket.return_value.__enter__.return_value
        instance.connect_ex.return_value = 0
        instance.recv.return_value = b"HTTP/1.1 200 OK"
        result = s._check_port(80)
    assert result is not None
    assert result["port"] == 80
    assert result["state"] == "open"
    assert result["service"] == "HTTP"


@patch("socket.gethostbyname", return_value="127.0.0.1")
def test_check_port_closed(mock_gethostbyname):
    s = PortScanner("localhost", port_range="9999")
    s._resolved_ip = "127.0.0.1"
    with patch("socket.socket") as MockSocket:
        instance = MockSocket.return_value.__enter__.return_value
        instance.connect_ex.return_value = 111  # connection refused
        result = s._check_port(9999)
    assert result is None


def test_build_summary_high_risk():
    open_ports = [{"port": 21}, {"port": 23}, {"port": 80}]
    summary = PortScanner._build_summary(open_ports)
    assert summary["risk_level"] == "High"
    assert 21 in summary["risky_ports"]
    assert 23 in summary["risky_ports"]


def test_build_summary_low_risk():
    open_ports = [{"port": 80}, {"port": 443}]
    summary = PortScanner._build_summary(open_ports)
    assert summary["risk_level"] == "Low"
    assert summary["risky_ports"] == []
