
# File: backend/src/services/n8n_service.py
import asyncio
import datetime
import aiohttp
import json
from typing import Dict, List

from server.src.scraper.crawl4ai_scapper import Crawl4AIJobScraper


class N8NService:
    """Service to interact with n8n workflows"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def trigger_scraping_workflow(self, user_id: str, keywords: List[str]) -> bool:
        """Trigger n8n scraping workflow"""
        try:
            payload = {
                "user_id": user_id,
                "keywords": keywords,
                "action": "start_scraping",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    return response.status == 200
                    
        except Exception as e:
            print(f"Error triggering n8n workflow: {e}")
            return False
    
    async def send_notification(self, user_id: str, notification_data: Dict) -> bool:
        """Send notification through n8n"""
        try:
            payload = {
                "user_id": user_id,
                "action": "send_notification",
                "data": notification_data,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url + "/notify", json=payload) as response:
                    return response.status == 200
                    
        except Exception as e:
            print(f"Error sending n8n notification: {e}")
            return False

# Example usage
if __name__ == "__main__":
    async def main():
        scraper = Crawl4AIJobScraper()
        results = await scraper.run_full_scrape(
            keywords=["python developer", "react developer"]
        )
        print(json.dumps(results, indent=2))
    
    asyncio.run(main())