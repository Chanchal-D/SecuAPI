from typing import List, Dict
import json
from .scanner import APIScanner
from .models.vulnerability import Vulnerability
import openai

class SecurityAnalyzer:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        
    def analyze_vulnerabilities(self, vulnerabilities: List[Vulnerability]) -> Dict:
        if not vulnerabilities:
            return {"analysis": "No vulnerabilities found."}
            
        # Prepare vulnerability data for AI analysis
        vuln_data = [v.to_dict() for v in vulnerabilities]
        
        # Use OpenAI to analyze vulnerabilities
        prompt = self._create_analysis_prompt(vuln_data)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a security expert analyzing API vulnerabilities."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "vulnerabilities": vuln_data,
                "ai_analysis": analysis,
                "risk_score": self._calculate_risk_score(vulnerabilities)
            }
        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "vulnerabilities": vuln_data
            }
    
    def _create_analysis_prompt(self, vuln_data: List[Dict]) -> str:
        return f"""
        As a security expert, analyze these API vulnerabilities. For each vulnerability:
        
        1. Risk Assessment:
           - Severity level justification
           - Potential business impact
           - Likelihood of exploitation
        
        2. Technical Analysis:
           - Attack vectors and scenarios
           - Potential chain reactions with other vulnerabilities
           - False positive probability
        
        3. Remediation Strategy:
           - Immediate mitigation steps
           - Long-term security improvements
           - Recommended security controls
           - Code-level fix examples where applicable
        
        4. Compliance Impact:
           - Relevant security standards (OWASP, PCI-DSS, etc.)
           - Regulatory considerations
        
        Vulnerabilities to analyze:
        {json.dumps(vuln_data, indent=2)}
        
        Format your response in clear sections with actionable insights.
        """
    
    def _calculate_risk_score(self, vulnerabilities: List[Vulnerability]) -> float:
        severity_weights = {
            "CRITICAL": 1.0,
            "HIGH": 0.7,
            "MEDIUM": 0.4,
            "LOW": 0.1
        }
        
        if not vulnerabilities:
            return 0.0
            
        total_weight = sum(severity_weights[v.severity.value] for v in vulnerabilities)
        return min(10.0, (total_weight / len(vulnerabilities)) * 10) 