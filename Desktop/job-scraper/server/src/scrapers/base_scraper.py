# File: backend/src/scrapers/base_scraper.py
class BaseScraper:
    """Base class for all job site scrapers"""
    
    def __init__(self, headless: bool = True):
        self.stealth_driver = StealthDriver(headless=headless)
        self.driver = None
        
    def setup_driver(self):
        """Initialize the stealth driver"""
        self.driver = self.stealth_driver.create_stealth_driver()
        return self.driver is not None
    
    def safe_navigate(self, url: str, max_retries: int = 3) -> bool:
        """Safely navigate to URL with retries"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url) # type: ignore
                
                # Handle Cloudflare if present
                if "cloudflare" in self.driver.page_source.lower(): # type: ignore
                    if not self.stealth_driver.bypass_cloudflare(self.driver):
                        continue
                
                # Random delay after page load
                time.sleep(random.uniform(2, 5))
                
                # Perform human-like actions
                self.stealth_driver.random_mouse_movement(self.driver)
                
                return True
                
            except WebDriverException as e:
                print(f"Navigation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(5, 10))
        
        return False
    
    def extract_job_data(self, job_element) -> Dict:
        """Extract job data from element - to be implemented by subclasses"""
        raise NotImplementedError
    
    def search_jobs(self, keywords: str, location: str = "") -> List[Dict]:
        """Search for jobs - to be implemented by subclasses"""
        raise NotImplementedError
    
    def cleanup(self):
        """Clean up resources"""
        if self.stealth_driver:
            self.stealth_driver.close()