import requests
from typing import List, Dict
from datetime import datetime
from .models.vulnerability import Vulnerability, Severity
import json
import re

class APIScanner:
    def __init__(self, base_url: str, headers: Dict = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        
    def scan_endpoint(self, endpoint: str) -> List[Vulnerability]:
        vulnerabilities = []
        
        # Test for common vulnerabilities
        vulns = [
            self._check_authentication(endpoint),
            self._check_injection(endpoint),
            self._check_rate_limiting(endpoint),
            self._check_ssl_tls(endpoint),
            self._check_cors(endpoint),
            self._check_jwt_vulnerabilities(endpoint),
            self._check_sensitive_data(endpoint)
        ]
        
        return [v for v in vulns if v is not None]
    
    def _check_authentication(self, endpoint: str) -> Vulnerability:
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            if response.status_code != 401:
                return Vulnerability(
                    title="Missing Authentication",
                    description="Endpoint accessible without authentication",
                    severity=Severity.HIGH,
                    endpoint=endpoint,
                    discovered_at=datetime.now(),
                    recommendation="Implement proper authentication mechanisms"
                )
        except Exception as e:
            print(f"Error checking authentication: {str(e)}")
        return None

    def _check_injection(self, endpoint: str) -> Vulnerability:
        # Test for SQL injection vulnerabilities
        test_payloads = ["'", "1' OR '1'='1", "1; DROP TABLE users"]
        for payload in test_payloads:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", 
                                     params={"q": payload},
                                     headers=self.headers)
                if any(error_msg in response.text.lower() for error_msg in 
                      ["sql", "database", "error"]):
                    return Vulnerability(
                        title="Potential SQL Injection",
                        description="Endpoint might be vulnerable to SQL injection",
                        severity=Severity.CRITICAL,
                        endpoint=endpoint,
                        discovered_at=datetime.now(),
                        recommendation="Use parameterized queries and input validation"
                    )
            except Exception:
                continue
        return None

    def _check_rate_limiting(self, endpoint: str) -> Vulnerability:
        try:
            # Make multiple rapid requests
            for _ in range(10):
                response = requests.get(f"{self.base_url}{endpoint}", 
                                     headers=self.headers)
            
            if response.status_code != 429:
                return Vulnerability(
                    title="Missing Rate Limiting",
                    description="No rate limiting detected on endpoint",
                    severity=Severity.MEDIUM,
                    endpoint=endpoint,
                    discovered_at=datetime.now(),
                    recommendation="Implement rate limiting to prevent abuse"
                )
        except Exception as e:
            print(f"Error checking rate limiting: {str(e)}")
        return None

    def _check_ssl_tls(self, endpoint: str) -> Vulnerability:
        try:
            response = requests.get(f"{self.base_url}{endpoint}", 
                                 verify=True)
            if not response.url.startswith("https"):
                return Vulnerability(
                    title="Insecure Communication",
                    description="Endpoint not using HTTPS",
                    severity=Severity.HIGH,
                    endpoint=endpoint,
                    discovered_at=datetime.now(),
                    recommendation="Enable HTTPS and redirect all HTTP traffic"
                )
        except Exception as e:
            print(f"Error checking SSL/TLS: {str(e)}")
        return None

    def _check_cors(self, endpoint: str) -> Vulnerability:
        try:
            headers = {
                'Origin': 'https://malicious-site.com',
                'Access-Control-Request-Method': 'GET'
            }
            response = requests.options(f"{self.base_url}{endpoint}", headers=headers)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                if response.headers['Access-Control-Allow-Origin'] == '*':
                    return Vulnerability(
                        title="Insecure CORS Configuration",
                        description="Endpoint allows requests from any origin",
                        severity=Severity.HIGH,
                        endpoint=endpoint,
                        discovered_at=datetime.now(),
                        recommendation="Implement strict CORS policy with specific allowed origins"
                    )
        except Exception as e:
            print(f"Error checking CORS: {str(e)}")
        return None

    def _check_jwt_vulnerabilities(self, endpoint: str) -> Vulnerability:
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            auth_header = response.headers.get('Authorization', '')
            
            if 'jwt' in auth_header.lower() or 'bearer' in auth_header.lower():
                # Check for common JWT vulnerabilities
                weak_token = "eyJhbGciOiJub25lIn0.eyJzdWIiOiIxMjM0NTY3ODkwIn0."
                headers = {'Authorization': f'Bearer {weak_token}'}
                
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
                if response.status_code != 401:
                    return Vulnerability(
                        title="Weak JWT Validation",
                        description="Endpoint accepts unsigned/weakly signed JWTs",
                        severity=Severity.CRITICAL,
                        endpoint=endpoint,
                        discovered_at=datetime.now(),
                        recommendation="Implement proper JWT validation with strong algorithms"
                    )
        except Exception as e:
            print(f"Error checking JWT: {str(e)}")
        return None

    def _check_sensitive_data(self, endpoint: str) -> Vulnerability:
        sensitive_patterns = [
            r'\b[\w\.-]+@[\w\.-]+\.\w+\b',  # Email
            r'\b\d{16}\b',                   # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b'        # SSN
        ]
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            content = response.text.lower()
            
            for pattern in sensitive_patterns:
                if re.search(pattern, content):
                    return Vulnerability(
                        title="Sensitive Data Exposure",
                        description="Endpoint may be exposing sensitive information",
                        severity=Severity.HIGH,
                        endpoint=endpoint,
                        discovered_at=datetime.now(),
                        recommendation="Implement data masking and encryption"
                    )
        except Exception as e:
            print(f"Error checking sensitive data: {str(e)}")
        return None 