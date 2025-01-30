from typing import Dict, List
import os
import yaml
from datetime import datetime
from .scanner import APIScanner
from .analyzer import SecurityAnalyzer
from .utils import save_report
from .notifications import NotificationService

class CIRunner:
    def __init__(self, config_path: str):
        self.config = self._load_ci_config(config_path)
        self.notification_service = NotificationService(self.config.get('notifications', {}))
        
    def _load_ci_config(self, path: str) -> Dict:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    async def run_security_scan(self) -> Dict:
        scanner = APIScanner(
            base_url=self.config['api']['base_url'],
            headers=self.config['api'].get('headers', {})
        )
        
        analyzer = SecurityAnalyzer(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Scan all endpoints
        all_vulnerabilities = []
        for endpoint in self.config['api']['endpoints']:
            vulnerabilities = scanner.scan_endpoint(endpoint)
            all_vulnerabilities.extend(vulnerabilities)
        
        # Analyze results
        analysis = analyzer.analyze_vulnerabilities(all_vulnerabilities)
        
        # Generate report
        report_path = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_report(all_vulnerabilities, report_path)
        
        # Send notifications if threshold exceeded
        if analysis['risk_score'] > self.config['thresholds']['max_risk_score']:
            await self.notification_service.send_alert(analysis)
        
        return analysis 