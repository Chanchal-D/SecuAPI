from typing import Dict
import aiohttp
import json

class NotificationService:
    def __init__(self, config: Dict):
        self.config = config
        
    async def send_alert(self, analysis: Dict):
        if 'slack' in self.config:
            await self._send_slack_notification(analysis)
        if 'discord' in self.config:
            await self._send_discord_notification(analysis)
    
    async def _send_slack_notification(self, analysis: Dict):
        webhook_url = self.config['slack']['webhook_url']
        
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 Security Alert: High Risk Score Detected"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Risk Score:* {analysis['risk_score']}\n"
                               f"*Total Vulnerabilities:* {len(analysis['vulnerabilities'])}"
                    }
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json=message)
    
    async def _send_discord_notification(self, analysis: Dict):
        webhook_url = self.config['discord']['webhook_url']
        
        embed = {
            "title": "🚨 Security Alert: High Risk Score Detected",
            "color": 16711680,  # Red
            "fields": [
                {
                    "name": "Risk Score",
                    "value": str(analysis['risk_score']),
                    "inline": True
                },
                {
                    "name": "Total Vulnerabilities",
                    "value": str(len(analysis['vulnerabilities'])),
                    "inline": True
                }
            ]
        }
        
        message = {
            "embeds": [embed]
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json=message) 