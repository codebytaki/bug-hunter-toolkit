"""
Web Application Security Tester
Tests for XSS, SQLi, CSRF, and other web vulnerabilities
"""

import requests
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from loguru import logger
import re


class WebAppTester:
    """Web application security testing class"""
    
    def __init__(self, target: str, timeout: int = 10):
        """
        Initialize web app tester
        
        Args:
            target: Target URL
            timeout: Request timeout
        """
        self.target = target
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BugHunterToolkit/2.0 (Security Tester)'
        })
        
        logger.info(f"Initialized web app tester for: {target}")
    
    def test_xss(self) -> List[Dict]:
        """
        Test for Cross-Site Scripting (XSS) vulnerabilities
        
        Returns:
            List of XSS vulnerabilities found
        """
        logger.info("Testing for XSS vulnerabilities...")
        vulnerabilities = []
        
        # XSS payloads
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert(String.fromCharCode(88,83,83))</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg/onload=alert("XSS")>',
            'javascript:alert("XSS")',
            '<iframe src="javascript:alert(\'XSS\')">',
        ]
        
        try:
            # Get all forms on the page
            response = self.session.get(self.target, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            for form in forms:
                action = form.get('action', '')
                method = form.get('method', 'get').lower()
                inputs = form.find_all('input')
                
                form_url = urljoin(self.target, action)
                
                for payload in xss_payloads:
                    # Build form data
                    data = {}
                    for input_field in inputs:
                        name = input_field.get('name')
                        if name:
                            data[name] = payload
                    
                    try:
                        if method == 'post':
                            test_response = self.session.post(form_url, data=data, timeout=self.timeout)
                        else:
                            test_response = self.session.get(form_url, params=data, timeout=self.timeout)
                        
                        # Check if payload is reflected in response
                        if payload in test_response.text:
                            vulnerabilities.append({
                                'type': 'Cross-Site Scripting (XSS)',
                                'severity': 'High',
                                'url': form_url,
                                'method': method.upper(),
                                'payload': payload,
                                'description': f'Reflected XSS found in form at {form_url}',
                                'recommendation': 'Implement proper input validation and output encoding'
                            })
                            break  # Found XSS, no need to test more payloads for this form
                    
                    except Exception as e:
                        logger.debug(f"Error testing XSS payload: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error in XSS testing: {str(e)}")
        
        logger.info(f"XSS testing completed. Found {len(vulnerabilities)} vulnerabilities")
        return vulnerabilities
    
    def test_sqli(self) -> List[Dict]:
        """
        Test for SQL Injection vulnerabilities
        
        Returns:
            List of SQLi vulnerabilities found
        """
        logger.info("Testing for SQL Injection vulnerabilities...")
        vulnerabilities = []
        
        # SQL injection payloads
        sqli_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "' UNION SELECT NULL--",
            "1' AND '1'='1",
        ]
        
        # SQL error patterns
        sql_errors = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"valid MySQL result",
            r"MySqlClient\.",
            r"PostgreSQL.*ERROR",
            r"Warning.*\Wpg_.*",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            r"Driver.* SQL[\-\_\ ]*Server",
            r"OLE DB.* SQL Server",
            r"SQLServer JDBC Driver",
            r"Microsoft SQL Native Client error",
        ]
        
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            for form in forms:
                action = form.get('action', '')
                method = form.get('method', 'get').lower()
                inputs = form.find_all('input')
                
                form_url = urljoin(self.target, action)
                
                for payload in sqli_payloads:
                    data = {}
                    for input_field in inputs:
                        name = input_field.get('name')
                        if name:
                            data[name] = payload
                    
                    try:
                        if method == 'post':
                            test_response = self.session.post(form_url, data=data, timeout=self.timeout)
                        else:
                            test_response = self.session.get(form_url, params=data, timeout=self.timeout)
                        
                        # Check for SQL errors in response
                        for error_pattern in sql_errors:
                            if re.search(error_pattern, test_response.text, re.IGNORECASE):
                                vulnerabilities.append({
                                    'type': 'SQL Injection',
                                    'severity': 'Critical',
                                    'url': form_url,
                                    'method': method.upper(),
                                    'payload': payload,
                                    'description': f'SQL Injection vulnerability found at {form_url}',
                                    'recommendation': 'Use parameterized queries and prepared statements'
                                })
                                break
                    
                    except Exception as e:
                        logger.debug(f"Error testing SQLi payload: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error in SQLi testing: {str(e)}")
        
        logger.info(f"SQLi testing completed. Found {len(vulnerabilities)} vulnerabilities")
        return vulnerabilities
    
    def test_csrf(self) -> List[Dict]:
        """
        Test for Cross-Site Request Forgery (CSRF) vulnerabilities
        
        Returns:
            List of CSRF vulnerabilities found
        """
        logger.info("Testing for CSRF vulnerabilities...")
        vulnerabilities = []
        
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            for form in forms:
                action = form.get('action', '')
                method = form.get('method', 'get').lower()
                
                # Check if form has CSRF token
                has_csrf_token = False
                inputs = form.find_all('input')
                
                for input_field in inputs:
                    name = input_field.get('name', '').lower()
                    if any(token in name for token in ['csrf', 'token', '_token', 'authenticity']):
                        has_csrf_token = True
                        break
                
                if not has_csrf_token and method == 'post':
                    form_url = urljoin(self.target, action)
                    vulnerabilities.append({
                        'type': 'Cross-Site Request Forgery (CSRF)',
                        'severity': 'High',
                        'url': form_url,
                        'description': f'Form at {form_url} lacks CSRF protection',
                        'recommendation': 'Implement CSRF tokens for all state-changing operations'
                    })
        
        except Exception as e:
            logger.error(f"Error in CSRF testing: {str(e)}")
        
        logger.info(f"CSRF testing completed. Found {len(vulnerabilities)} vulnerabilities")
        return vulnerabilities
    
    def test_all(self) -> Dict:
        """
        Run all web application tests
        
        Returns:
            Dictionary containing all test results
        """
        logger.info("Running comprehensive web application tests...")
        
        results = {
            'target': self.target,
            'xss': self.test_xss(),
            'sqli': self.test_sqli(),
            'csrf': self.test_csrf(),
        }
        
        total_vulns = len(results['xss']) + len(results['sqli']) + len(results['csrf'])
        results['total_vulnerabilities'] = total_vulns
        
        logger.info(f"Web app testing completed. Total vulnerabilities: {total_vulns}")
        
        return results
