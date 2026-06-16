"""
Network Scanning Module
TCP port scanning, service banner grabbing, and basic OS fingerprinting
"""

import socket
import concurrent.futures
from typing import List, Dict, Optional, Tuple
from loguru import logger
import time


# Well-known service names
COMMON_SERVICES: Dict[int, str] = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8888: "HTTP-Dev",
    9200: "Elasticsearch", 27017: "MongoDB",
}


class PortScanner:
    """
    Fast TCP connect scanner with optional banner grabbing.

    Usage::

        scanner = PortScanner("192.168.1.1", port_range="1-1024")
        results = scanner.scan()
    """

    def __init__(
        self,
        target: str,
        port_range: str = "1-1024",
        threads: int = 100,
        timeout: float = 1.0,
        grab_banners: bool = True,
    ):
        """
        Args:
            target: IP address or hostname
            port_range: Range string like '1-1024' or '80,443,8080'
            threads: Concurrent workers
            timeout: Per-port connection timeout in seconds
            grab_banners: Attempt to read service banners
        """
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.grab_banners = grab_banners
        self.ports = self._parse_range(port_range)
        self._resolved_ip: Optional[str] = None
        logger.info(f"PortScanner ready: {target}, {len(self.ports)} ports")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(self) -> Dict:
        """
        Run the port scan.

        Returns:
            Dict with keys: target, ip, open_ports, scan_time, summary
        """
        try:
            self._resolved_ip = socket.gethostbyname(self.target)
        except socket.gaierror as e:
            logger.error(f"Cannot resolve {self.target}: {e}")
            return {"error": str(e), "target": self.target}

        logger.info(f"Scanning {self.target} ({self._resolved_ip}), {len(self.ports)} ports")
        start = time.time()

        open_ports: List[Dict] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._check_port, port): port for port in self.ports}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)

        elapsed = round(time.time() - start, 2)
        open_ports.sort(key=lambda x: x["port"])

        logger.info(f"Scan complete: {len(open_ports)} open ports in {elapsed}s")

        return {
            "target": self.target,
            "ip": self._resolved_ip,
            "open_ports": open_ports,
            "total_scanned": len(self.ports),
            "scan_time_seconds": elapsed,
            "summary": self._build_summary(open_ports),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_port(self, port: int) -> Optional[Dict]:
        """Attempt TCP connection; return port info dict or None."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self._resolved_ip, port))
                if result == 0:
                    service = COMMON_SERVICES.get(port, "unknown")
                    banner = self._grab_banner(port) if self.grab_banners else ""
                    logger.debug(f"Open: {port}/{service}")
                    return {
                        "port": port,
                        "service": service,
                        "state": "open",
                        "banner": banner,
                    }
        except Exception:
            pass
        return None

    def _grab_banner(self, port: int) -> str:
        """Try to read the first 256 bytes of a service banner."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2.0)
                sock.connect((self._resolved_ip, port))
                # Some services send banner immediately; others need a probe
                sock.sendall(b"\r\n")
                banner = sock.recv(256).decode("utf-8", errors="replace").strip()
                return banner[:120]  # truncate
        except Exception:
            return ""

    @staticmethod
    def _parse_range(port_range: str) -> List[int]:
        """Parse '1-1024' or '80,443,8080' into a list of ints."""
        ports: List[int] = []
        for part in port_range.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-", 1)
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
        return [p for p in ports if 1 <= p <= 65535]

    @staticmethod
    def _build_summary(open_ports: List[Dict]) -> Dict:
        """Build a quick risk summary from open ports."""
        risky = {21, 23, 445, 3389, 5900}
        risky_found = [p for p in open_ports if p["port"] in risky]
        return {
            "total_open": len(open_ports),
            "risky_ports": [p["port"] for p in risky_found],
            "risk_level": "High" if risky_found else ("Medium" if len(open_ports) > 10 else "Low"),
        }
