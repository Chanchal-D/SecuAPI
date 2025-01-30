import json
from typing import Dict, List
from .models.vulnerability import Vulnerability
import requests

def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        return json.load(f)

def save_report(vulnerabilities: List[Vulnerability], output_path: str):
    report = {
        "vulnerabilities": [v.to_dict() for v in vulnerabilities],
        "total_vulnerabilities": len(vulnerabilities),
        "timestamp": datetime.now().isoformat()
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

def discover_endpoints(base_url: str) -> List[str]:
    """
    Attempt to discover API endpoints through common paths and swagger/openapi docs
    """
    common_paths = [
        '/api',
        '/swagger/v1/swagger.json',
        '/openapi.json',
        '/docs',
        '/api/v1'
    ]
    
    discovered = []
    
    for path in common_paths:
        try:
            response = requests.get(f"{base_url.rstrip('/')}{path}")
            if response.status_code == 200:
                discovered.append(path)
                
                # If swagger/openapi docs found, parse them for endpoints
                if 'swagger' in path or 'openapi' in path:
                    try:
                        docs = response.json()
                        if 'paths' in docs:
                            discovered.extend(docs['paths'].keys())
                    except:
                        pass
                        
        except Exception:
            continue
            
    return discovered 