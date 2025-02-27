import asyncio
import argparse
import os
from src.ci_integration import CIRunner
from .utils import load_config
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scan', methods=['POST'])
def scan():
    config = request.json
    # Run your existing scanning logic here
    results = run_security_scan(config)
    return jsonify(results)

async def main():
    parser = argparse.ArgumentParser(description='API Security Analyzer')
    parser.add_argument('--config', type=str, default='config/ci_config.yml',
                       help='Path to configuration file')
    parser.add_argument('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', type=str,
                       help='OpenAI API key (optional if set in environment)')
    
    args = parser.parse_args()
    
    # Set OpenAI API key if provided
    if args.api_key:
        os.environ['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'] = args.api_key
    
    # Initialize and run the security scanner
    runner = CIRunner(args.config)
    try:
        analysis = await runner.run_security_scan()
        print("\n=== Security Analysis Results ===")
        print(f"Risk Score: {analysis['risk_score']:.2f}/10.0")
        print(f"Total Vulnerabilities: {len(analysis['vulnerabilities'])}")
        print("\nDetailed Analysis:")
        print(analysis['ai_analysis'])
        
    except Exception as e:
        print(f"Error during security scan: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True) 