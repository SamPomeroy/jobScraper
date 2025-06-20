# # Advanced Selenium Bot Detection Bypass System

# # File: backend/src/utils/selenium_utils.py
# import random
# import time
# import json
# import os
# from typing import Optional, Dict, List
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, WebDriverException
# import undetected_chromedriver as uc
# from fake_useragent import UserAgent

# class StealthDriver:
#     """Advanced Selenium driver with comprehensive bot detection bypass"""
    
#     def __init__(self, headless: bool = False, use_proxy: bool = False):
#         self.headless = headless
#         self.use_proxy = use_proxy
#         self.driver = None
#         self.ua = UserAgent()
        
#     def create_stealth_driver(self) -> webdriver.Chrome:
#         """Create an undetected Chrome driver with stealth features"""
        
#         # Chrome options for stealth
#         options = uc.ChromeOptions()
        
#         # Basic stealth settings
#         if self.headless:
#             options.add_argument('--headless=new')
        
#         # Disable automation indicators
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
        
#         # Disable images and CSS for faster loading (optional)
#         prefs = {
#             "profile.managed_default_content_settings.images": 2,
#             "profile.default_content_setting_values": {
#                 "notifications": 2
#             }
#         }
#         options.add_experimental_option("prefs", prefs)
        
#         # Window size randomization
#         window_sizes = [
#             (1920, 1080), (1366, 768), (1440, 900), 
#             (1536, 864), (1280, 720), (1600, 900)
#         ]
#         width, height = random.choice(window_sizes)
#         options.add_argument(f'--window-size={width},{height}')
        
#         # Additional stealth arguments
#         stealth_args = [
#             '--no-sandbox',
#             '--disable-dev-shm-usage',
#             '--disable-gpu',
#             '--disable-extensions',
#             '--disable-plugins',
#             '--disable-images',
#             '--disable-javascript',
#             '--disable-default-apps',
#             '--disable-background-timer-throttling',
#             '--disable-backgrounding-occluded-windows',
#             '--disable-renderer-backgrounding',
#             '--disable-features=TranslateUI',
#             '--disable-ipc-flooding-protection',
#             '--no-first-run',
#             '--no-default-browser-check',
#             '--disable-logging',
#             '--disable-log-file',
#             '--silent',
#             '--disable-background-networking',
#             '--disable-background-timer-throttling',
#             '--disable-client-side-phishing-detection',
#             '--disable-popup-blocking',
#             '--disable-prompt-on-repost',
#             '--disable-hang-monitor',
#             '--disable-sync',
#             '--metrics-recording-only',
#             '--no-first-run',
#             '--safebrowsing-disable-auto-update',
#             '--enable-automation',
#             '--password-store=basic',
#             '--use-mock-keychain'
#         ]
        
#         for arg in stealth_args:
#             options.add_argument(arg)
        
#         # Random user agent
#         user_agent = self.ua.random
#         options.add_argument(f'--user-agent={user_agent}')
        
#         # Create driver with undetected-chromedriver
#         try:
#             driver = uc.Chrome(options=options, version_main=None)
            
#             # Execute CDP commands to further hide automation
#             driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#                 'source': '''
#                     Object.defineProperty(navigator, 'webdriver', {
#                         get: () => undefined,
#                     });
                    
#                     Object.defineProperty(navigator, 'plugins', {
#                         get: () => [1, 2, 3, 4, 5],
#                     });
                    
#                     Object.defineProperty(navigator, 'languages', {
#                         get: () => ['en-US', 'en'],
#                     });
                    
#                     window.chrome = {
#                         runtime: {},
#                     };
                    
#                     Object.defineProperty(navigator, 'permissions', {
#                         get: () => ({
#                             query: () => Promise.resolve({ state: 'granted' }),
#                         }),
#                     });
#                 '''
#             })
            
#             self.driver = driver
#             return driver
            
#         except Exception as e:
#             print(f"Error creating stealth driver: {e}")
#             return None
    
#     def human_like_typing(self, element, text: str, typing_speed: float = 0.1):
#         """Type text with human-like delays and occasional typos"""
#         element.clear()
        
#         for char in text:
#             element.send_keys(char)
#             # Random typing speed
#             delay = random.uniform(typing_speed * 0.5, typing_speed * 1.5)
#             time.sleep(delay)
            
#             # Occasional pause (like thinking)
#             if random.random() < 0.1:
#                 time.sleep(random.uniform(0.5, 2.0))
    
#     def human_like_scroll(self, driver, scroll_pause_time: float = 2):
#         """Scroll like a human with random pauses"""
#         # Get scroll height
#         last_height = driver.execute_script("return document.body.scrollHeight")
        
#         while True:
#             # Scroll down to bottom with random speed
#             scroll_amount = random.randint(300, 800)
#             driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
#             # Wait to load page
#             time.sleep(random.uniform(scroll_pause_time * 0.5, scroll_pause_time * 1.5))
            
#             # Calculate new scroll height
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height
    
#     def random_mouse_movement(self, driver):
#         """Perform random mouse movements to mimic human behavior"""
#         actions = ActionChains(driver)
        
#         # Get window size
#         window_size = driver.get_window_size()
#         width, height = window_size['width'], window_size['height']
        
#         # Random mouse movements
#         for _ in range(random.randint(2, 5)):
#             x = random.randint(0, width)
#             y = random.randint(0, height)
#             actions.move_by_offset(x, y)
#             time.sleep(random.uniform(0.1, 0.5))
        
#         actions.perform()
    
#     def wait_and_find_element(self, driver, by, value, timeout: int = 10):
#         """Wait for element with random delay"""
#         try:
#             # Add random delay before searching
#             time.sleep(random.uniform(0.5, 2.0))
            
#             element = WebDriverWait(driver, timeout).until(
#                 EC.presence_of_element_located((by, value))
#             )
#             return element
#         except TimeoutException:
#             return None
    
#     def bypass_cloudflare(self, driver, max_attempts: int = 3):
#         """Bypass Cloudflare protection"""
#         for attempt in range(max_attempts):
#             try:
#                 # Wait for Cloudflare check
#                 WebDriverWait(driver, 30).until(
#                     lambda d: "cloudflare" not in d.current_url.lower() or
#                     d.find_elements(By.TAG_NAME, "body")
#                 )
                
#                 # Check if we're past Cloudflare
#                 if "cloudflare" not in driver.current_url.lower():
#                     return True
                
#                 # Wait longer for automatic bypass
#                 time.sleep(random.uniform(10, 15))
                
#             except TimeoutException:
#                 if attempt == max_attempts - 1:
#                     return False
                
#                 # Refresh and try again
#                 driver.refresh()
#                 time.sleep(random.uniform(5, 10))
        
#         return False
    
#     def close(self):
#         """Clean up driver"""
#         if self.driver:
#             self.driver.quit()

# # File: backend/src/scrapers/base_scraper.py
# class BaseScraper:
#     """Base class for all job site scrapers"""
    
#     def __init__(self, headless: bool = True):
#         self.stealth_driver = StealthDriver(headless=headless)
#         self.driver = None
        
#     def setup_driver(self):
#         """Initialize the stealth driver"""
#         self.driver = self.stealth_driver.create_stealth_driver()
#         return self.driver is not None
    
#     def safe_navigate(self, url: str, max_retries: int = 3) -> bool:
#         """Safely navigate to URL with retries"""
#         for attempt in range(max_retries):
#             try:
#                 self.driver.get(url)
                
#                 # Handle Cloudflare if present
#                 if "cloudflare" in self.driver.page_source.lower():
#                     if not self.stealth_driver.bypass_cloudflare(self.driver):
#                         continue
                
#                 # Random delay after page load
#                 time.sleep(random.uniform(2, 5))
                
#                 # Perform human-like actions
#                 self.stealth_driver.random_mouse_movement(self.driver)
                
#                 return True
                
#             except WebDriverException as e:
#                 print(f"Navigation attempt {attempt + 1} failed: {e}")
#                 if attempt < max_retries - 1:
#                     time.sleep(random.uniform(5, 10))
        
#         return False
    
#     def extract_job_data(self, job_element) -> Dict:
#         """Extract job data from element - to be implemented by subclasses"""
#         raise NotImplementedError
    
#     def search_jobs(self, keywords: str, location: str = "") -> List[Dict]:
#         """Search for jobs - to be implemented by subclasses"""
#         raise NotImplementedError
    
#     def cleanup(self):
#         """Clean up resources"""
#         if self.stealth_driver:
#             self.stealth_driver.close()

# # File: backend/src/scrapers/indeed_scraper.py
# class IndeedScraper(BaseScraper):
#     """Indeed job scraper with advanced bot detection bypass"""
    
#     def __init__(self, headless: bool = True):
#         super().__init__(headless)
#         self.base_url = "https://www.indeed.com"
    
#     def search_jobs(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Search Indeed for jobs"""
#         if not self.setup_driver():
#             return []
        
#         jobs = []
        
#         try:
#             # Build search URL
#             search_url = f"{self.base_url}/jobs?q={keywords.replace(' ', '+')}"
#             if location:
#                 search_url += f"&l={location.replace(' ', '+')}"
            
#             for page in range(pages):
#                 page_url = f"{search_url}&start={page * 10}"
                
#                 if not self.safe_navigate(page_url):
#                     continue
                
#                 # Wait for job listings to load
#                 job_cards = self.stealth_driver.wait_and_find_element(
#                     self.driver, By.CSS_SELECTOR, "[data-testid='job-title']"
#                 )
                
#                 if not job_cards:
#                     continue
                
#                 # Find all job cards
#                 job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
#                 for job_elem in job_elements:
#                     try:
#                         job_data = self.extract_job_data(job_elem)
#                         if job_data:
#                             jobs.append(job_data)
#                     except Exception as e:
#                         print(f"Error extracting job data: {e}")
#                         continue
                
#                 # Random delay between pages
#                 time.sleep(random.uniform(3, 7))
        
#         except Exception as e:
#             print(f"Error scraping Indeed: {e}")
        
#         finally:
#             self.cleanup()
        
#         return jobs
    
#     def extract_job_data(self, job_element) -> Dict:
#         """Extract job data from Indeed job card"""
#         try:
#             # Title
#             title_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] span")
#             title = title_elem.get_attribute("title") or title_elem.text
            
#             # Company
#             company_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='company-name'] span")
#             company = company_elem.get_attribute("title") or company_elem.text
            
#             # Location
#             location_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
#             location = location_elem.text
            
#             # Link
#             link_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] a")
#             job_link = link_elem.get_attribute("href")
            
#             # Job ID
#             job_id = job_element.get_attribute("data-jk")
            
#             return {
#                 "id": job_id,
#                 "title": title,
#                 "company": company,
#                 "location": location,
#                 "link": job_link,
#                 "source": "Indeed",
#                 "scraped_at": time.time()
#             }
            
#         except Exception as e:
#             print(f"Error extracting job data: {e}")
#             return None

# # Example usage
# if __name__ == "__main__":
#     scraper = IndeedScraper(headless=False)  # Set to True for production
#     jobs = scraper.search_jobs("software engineer", "San Francisco", pages=2)
    
#     for job in jobs:
#         print(f"Title: {job['title']}")
#         print(f"Company: {job['company']}")
#         print(f"Location: {job['location']}")
#         print(f"Link: {job['link']}")
#         print("-" * 50)
#         # File: backend/src/utils/proxy_manager.py
# import random
# import requests
# import time
# from typing import List, Dict, Optional
# from dataclasses import dataclass

# @dataclass
# class ProxyConfig:
#     host: str
#     port: int
#     username: Optional[str] = None
#     password: Optional[str] = None
#     protocol: str = "http"
    
#     def to_dict(self) -> Dict:
#         proxy_url = f"{self.protocol}://"
#         if self.username and self.password:
#             proxy_url += f"{self.username}:{self.password}@"
#         proxy_url += f"{self.host}:{self.port}"
        
#         return {
#             "http": proxy_url,
#             "https": proxy_url
#         }

# class ProxyManager:
#     """Manage rotating proxies for bot detection bypass"""
    
#     def __init__(self):
#         self.proxies: List[ProxyConfig] = []
#         self.current_proxy_index = 0
#         self.failed_proxies = set()
        
#     def add_proxy(self, host: str, port: int, username: str = None, password: str = None, protocol: str = "http"):
#         """Add a proxy to the rotation"""
#         proxy = ProxyConfig(host, port, username, password, protocol)
#         self.proxies.append(proxy)
    
#     def get_free_proxies(self) -> List[ProxyConfig]:
#         """Fetch free proxies from public sources (use with caution)"""
#         try:
#             # This is a basic example - in production, use paid proxy services
#             response = requests.get("https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
#             proxy_list = response.text.strip().split('\n')
            
#             proxies = []
#             for proxy in proxy_list[:10]:  # Limit to 10 proxies
#                 if ':' in proxy:
#                     host, port = proxy.split(':')
#                     proxies.append(ProxyConfig(host, int(port)))
            
#             return proxies
#         except Exception as e:
#             print(f"Error fetching free proxies: {e}")
#             return []
    
#     def test_proxy(self, proxy: ProxyConfig, timeout: int = 10) -> bool:
#         """Test if a proxy is working"""
#         try:
#             proxies = proxy.to_dict()
#             response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
#             return response.status_code == 200
#         except Exception:
#             return False
    
#     def get_working_proxy(self) -> Optional[ProxyConfig]:
#         """Get a working proxy from the list"""
#         if not self.proxies:
#             return None
        
#         # Try proxies starting from current index
#         for i in range(len(self.proxies)):
#             proxy_index = (self.current_proxy_index + i) % len(self.proxies)
#             proxy = self.proxies[proxy_index]
            
#             # Skip failed proxies
#             if proxy_index in self.failed_proxies:
#                 continue
            
#             if self.test_proxy(proxy):
#                 self.current_proxy_index = proxy_index
#                 return proxy
#             else:
#                 self.failed_proxies.add(proxy_index)
        
#         return None
    
#     def rotate_proxy(self) -> Optional[ProxyConfig]:
#         """Rotate to the next working proxy"""
#         self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
#         return self.get_working_proxy()

# # File: backend/src/utils/user_agents.py
# import random
# from typing import List

# class UserAgentManager:
#     """Manage user agent rotation"""
    
#     def __init__(self):
#         self.user_agents = [
#             # Chrome on Windows
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
#             # Chrome on Mac
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
#             # Firefox on Windows
#             "Mozilla/5.0
#             # File: backend/src/utils/proxy_manager.py
# import random
# import requests
# import time
# from typing import List, Dict, Optional
# from dataclasses import dataclass

# @dataclass
# class ProxyConfig:
#     host: str
#     port: int
#     username: Optional[str] = None
#     password: Optional[str] = None
#     protocol: str = "http"
    
#     def to_dict(self) -> Dict:
#         proxy_url = f"{self.protocol}://"
#         if self.username and self.password:
#             proxy_url += f"{self.username}:{self.password}@"
#         proxy_url += f"{self.host}:{self.port}"
        
#         return {
#             "http": proxy_url,
#             "https": proxy_url
#         }

# class ProxyManager:
#     """Manage rotating proxies for bot detection bypass"""
    
#     def __init__(self):
#         self.proxies: List[ProxyConfig] = []
#         self.current_proxy_index = 0
#         self.failed_proxies = set()
        
#     def add_proxy(self, host: str, port: int, username: str = None, password: str = None, protocol: str = "http"):
#         """Add a proxy to the rotation"""
#         proxy = ProxyConfig(host, port, username, password, protocol)
#         self.proxies.append(proxy)
    
#     def get_free_proxies(self) -> List[ProxyConfig]:
#         """Fetch free proxies from public sources (use with caution)"""
#         try:
#             # This is a basic example - in production, use paid proxy services
#             response = requests.get("https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
#             proxy_list = response.text.strip().split('\n')
            
#             proxies = []
#             for proxy in proxy_list[:10]:  # Limit to 10 proxies
#                 if ':' in proxy:
#                     host, port = proxy.split(':')
#                     proxies.append(ProxyConfig(host, int(port)))
            
#             return proxies
#         except Exception as e:
#             print(f"Error fetching free proxies: {e}")
#             return []
    
#     def test_proxy(self, proxy: ProxyConfig, timeout: int = 10) -> bool:
#         """Test if a proxy is working"""
#         try:
#             proxies = proxy.to_dict()
#             response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
#             return response.status_code == 200
#         except Exception:
#             return False
    
#     def get_working_proxy(self) -> Optional[ProxyConfig]:
#         """Get a working proxy from the list"""
#         if not self.proxies:
#             return None
        
#         # Try proxies starting from current index
#         for i in range(len(self.proxies)):
#             proxy_index = (self.current_proxy_index + i) % len(self.proxies)
#             proxy = self.proxies[proxy_index]
            
#             # Skip failed proxies
#             if proxy_index in self.failed_proxies:
#                 continue
            
#             if self.test_proxy(proxy):
#                 self.current_proxy_index = proxy_index
#                 return proxy
#             else:
#                 self.failed_proxies.add(proxy_index)
        
#         return None
    
#     def rotate_proxy(self) -> Optional[ProxyConfig]:
#         """Rotate to the next working proxy"""
#         self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
#         return self.get_working_proxy()

# # File: backend/src/utils/user_agents.py
# import random
# from typing import List

# class UserAgentManager:
#     """Manage user agent rotation"""
    
#     def __init__(self):
#         self.user_agents = [
#             # Chrome on Windows
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
#             # Chrome on Mac
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
#             # Firefox on Windows
#             "Mozilla/5.0
#             # Advanced Selenium Bot Detection Bypass System

# # File: backend/src/utils/selenium_utils.py
# import random
# import time
# import json
# import os
# from typing import Optional, Dict, List
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException, WebDriverException
# import undetected_chromedriver as uc
# from fake_useragent import UserAgent

# class StealthDriver:
#     """Advanced Selenium driver with comprehensive bot detection bypass"""
    
#     def __init__(self, headless: bool = False, use_proxy: bool = False):
#         self.headless = headless
#         self.use_proxy = use_proxy
#         self.driver = None
#         self.ua = UserAgent()
        
#     def create_stealth_driver(self) -> webdriver.Chrome:
#         """Create an undetected Chrome driver with stealth features"""
        
#         # Chrome options for stealth
#         options = uc.ChromeOptions()
        
#         # Basic stealth settings
#         if self.headless:
#             options.add_argument('--headless=new')
        
#         # Disable automation indicators
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
        
#         # Disable images and CSS for faster loading (optional)
#         prefs = {
#             "profile.managed_default_content_settings.images": 2,
#             "profile.default_content_setting_values": {
#                 "notifications": 2
#             }
#         }
#         options.add_experimental_option("prefs", prefs)
        
#         # Window size randomization
#         window_sizes = [
#             (1920, 1080), (1366, 768), (1440, 900), 
#             (1536, 864), (1280, 720), (1600, 900)
#         ]
#         width, height = random.choice(window_sizes)
#         options.add_argument(f'--window-size={width},{height}')
        
#         # Additional stealth arguments
#         stealth_args = [
#             '--no-sandbox',
#             '--disable-dev-shm-usage',
#             '--disable-gpu',
#             '--disable-extensions',
#             '--disable-plugins',
#             '--disable-images',
#             '--disable-javascript',
#             '--disable-default-apps',
#             '--disable-background-timer-throttling',
#             '--disable-backgrounding-occluded-windows',
#             '--disable-renderer-backgrounding',
#             '--disable-features=TranslateUI',
#             '--disable-ipc-flooding-protection',
#             '--no-first-run',
#             '--no-default-browser-check',
#             '--disable-logging',
#             '--disable-log-file',
#             '--silent',
#             '--disable-background-networking',
#             '--disable-background-timer-throttling',
#             '--disable-client-side-phishing-detection',
#             '--disable-popup-blocking',
#             '--disable-prompt-on-repost',
#             '--disable-hang-monitor',
#             '--disable-sync',
#             '--metrics-recording-only',
#             '--no-first-run',
#             '--safebrowsing-disable-auto-update',
#             '--enable-automation',
#             '--password-store=basic',
#             '--use-mock-keychain'
#         ]
        
#         for arg in stealth_args:
#             options.add_argument(arg)
        
#         # Random user agent
#         user_agent = self.ua.random
#         options.add_argument(f'--user-agent={user_agent}')
        
#         # Create driver with undetected-chromedriver
#         try:
#             driver = uc.Chrome(options=options, version_main=None)
            
#             # Execute CDP commands to further hide automation
#             driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#                 'source': '''
#                     Object.defineProperty(navigator, 'webdriver', {
#                         get: () => undefined,
#                     });
                    
#                     Object.defineProperty(navigator, 'plugins', {
#                         get: () => [1, 2, 3, 4, 5],
#                     });
                    
#                     Object.defineProperty(navigator, 'languages', {
#                         get: () => ['en-US', 'en'],
#                     });
                    
#                     window.chrome = {
#                         runtime: {},
#                     };
                    
#                     Object.defineProperty(navigator, 'permissions', {
#                         get: () => ({
#                             query: () => Promise.resolve({ state: 'granted' }),
#                         }),
#                     });
#                 '''
#             })
            
#             self.driver = driver
#             return driver
            
#         except Exception as e:
#             print(f"Error creating stealth driver: {e}")
#             return None
    
#     def human_like_typing(self, element, text: str, typing_speed: float = 0.1):
#         """Type text with human-like delays and occasional typos"""
#         element.clear()
        
#         for char in text:
#             element.send_keys(char)
#             # Random typing speed
#             delay = random.uniform(typing_speed * 0.5, typing_speed * 1.5)
#             time.sleep(delay)
            
#             # Occasional pause (like thinking)
#             if random.random() < 0.1:
#                 time.sleep(random.uniform(0.5, 2.0))
    
#     def human_like_scroll(self, driver, scroll_pause_time: float = 2):
#         """Scroll like a human with random pauses"""
#         # Get scroll height
#         last_height = driver.execute_script("return document.body.scrollHeight")
        
#         while True:
#             # Scroll down to bottom with random speed
#             scroll_amount = random.randint(300, 800)
#             driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
#             # Wait to load page
#             time.sleep(random.uniform(scroll_pause_time * 0.5, scroll_pause_time * 1.5))
            
#             # Calculate new scroll height
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height
    
#     def random_mouse_movement(self, driver):
#         """Perform random mouse movements to mimic human behavior"""
#         actions = ActionChains(driver)
        
#         # Get window size
#         window_size = driver.get_window_size()
#         width, height = window_size['width'], window_size['height']
        
#         # Random mouse movements
#         for _ in range(random.randint(2, 5)):
#             x = random.randint(0, width)
#             y = random.randint(0, height)
#             actions.move_by_offset(x, y)
#             time.sleep(random.uniform(0.1, 0.5))
        
#         actions.perform()
    
#     def wait_and_find_element(self, driver, by, value, timeout: int = 10):
#         """Wait for element with random delay"""
#         try:
#             # Add random delay before searching
#             time.sleep(random.uniform(0.5, 2.0))
            
#             element = WebDriverWait(driver, timeout).until(
#                 EC.presence_of_element_located((by, value))
#             )
#             return element
#         except TimeoutException:
#             return None
    
#     def bypass_cloudflare(self, driver, max_attempts: int = 3):
#         """Bypass Cloudflare protection"""
#         for attempt in range(max_attempts):
#             try:
#                 # Wait for Cloudflare check
#                 WebDriverWait(driver, 30).until(
#                     lambda d: "cloudflare" not in d.current_url.lower() or
#                     d.find_elements(By.TAG_NAME, "body")
#                 )
                
#                 # Check if we're past Cloudflare
#                 if "cloudflare" not in driver.current_url.lower():
#                     return True
                
#                 # Wait longer for automatic bypass
#                 time.sleep(random.uniform(10, 15))
                
#             except TimeoutException:
#                 if attempt == max_attempts - 1:
#                     return False
                
#                 # Refresh and try again
#                 driver.refresh()
#                 time.sleep(random.uniform(5, 10))
        
#         return False
    
#     def close(self):
#         """Clean up driver"""
#         if self.driver:
#             self.driver.quit()

# # File: backend/src/scrapers/base_scraper.py
# class BaseScraper:
#     """Base class for all job site scrapers"""
    
#     def __init__(self, headless: bool = True):
#         self.stealth_driver = StealthDriver(headless=headless)
#         self.driver = None
        
#     def setup_driver(self):
#         """Initialize the stealth driver"""
#         self.driver = self.stealth_driver.create_stealth_driver()
#         return self.driver is not None
    
#     def safe_navigate(self, url: str, max_retries: int = 3) -> bool:
#         """Safely navigate to URL with retries"""
#         for attempt in range(max_retries):
#             try:
#                 self.driver.get(url)
                
#                 # Handle Cloudflare if present
#                 if "cloudflare" in self.driver.page_source.lower():
#                     if not self.stealth_driver.bypass_cloudflare(self.driver):
#                         continue
                
#                 # Random delay after page load
#                 time.sleep(random.uniform(2, 5))
                
#                 # Perform human-like actions
#                 self.stealth_driver.random_mouse_movement(self.driver)
                
#                 return True
                
#             except WebDriverException as e:
#                 print(f"Navigation attempt {attempt + 1} failed: {e}")
#                 if attempt < max_retries - 1:
#                     time.sleep(random.uniform(5, 10))
        
#         return False
    
#     def extract_job_data(self, job_element) -> Dict:
#         """Extract job data from element - to be implemented by subclasses"""
#         raise NotImplementedError
    
#     def search_jobs(self, keywords: str, location: str = "") -> List[Dict]:
#         """Search for jobs - to be implemented by subclasses"""
#         raise NotImplementedError
    
#     def cleanup(self):
#         """Clean up resources"""
#         if self.stealth_driver:
#             self.stealth_driver.close()

# # File: backend/src/scrapers/indeed_scraper.py
# class IndeedScraper(BaseScraper):
#     """Indeed job scraper with advanced bot detection bypass"""
    
#     def __init__(self, headless: bool = True):
#         super().__init__(headless)
#         self.base_url = "https://www.indeed.com"
    
#     def search_jobs(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Search Indeed for jobs"""
#         if not self.setup_driver():
#             return []
        
#         jobs = []
        
#         try:
#             # Build search URL
#             search_url = f"{self.base_url}/jobs?q={keywords.replace(' ', '+')}"
#             if location:
#                 search_url += f"&l={location.replace(' ', '+')}"
            
#             for page in range(pages):
#                 page_url = f"{search_url}&start={page * 10}"
                
#                 if not self.safe_navigate(page_url):
#                     continue
                
#                 # Wait for job listings to load
#                 job_cards = self.stealth_driver.wait_and_find_element(
#                     self.driver, By.CSS_SELECTOR, "[data-testid='job-title']"
#                 )
                
#                 if not job_cards:
#                     continue
                
#                 # Find all job cards
#                 job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
#                 for job_elem in job_elements:
#                     try:
#                         job_data = self.extract_job_data(job_elem)
#                         if job_data:
#                             jobs.append(job_data)
#                     except Exception as e:
#                         print(f"Error extracting job data: {e}")
#                         continue
                
#                 # Random delay between pages
#                 time.sleep(random.uniform(3, 7))
        
#         except Exception as e:
#             print(f"Error scraping Indeed: {e}")
        
#         finally:
#             self.cleanup()
        
#         return jobs
    
#     def extract_job_data(self, job_element) -> Dict:
#         """Extract job data from Indeed job card"""
#         try:
#             # Title
#             title_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] span")
#             title = title_elem.get_attribute("title") or title_elem.text
            
#             # Company
#             company_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='company-name'] span")
#             company = company_elem.get_attribute("title") or company_elem.text
            
#             # Location
#             location_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
#             location = location_elem.text
            
#             # Link
#             link_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] a")
#             job_link = link_elem.get_attribute("href")
            
#             # Job ID
#             job_id = job_element.get_attribute("data-jk")
            
#             return {
#                 "id": job_id,
#                 "title": title,
#                 "company": company,
#                 "location": location,
#                 "link": job_link,
#                 "source": "Indeed",
#                 "scraped_at": time.time()
#             }
            
#         except Exception as e:
#             print(f"Error extracting job data: {e}")
#             return None

# # Example usage
# if __name__ == "__main__":
#     scraper = IndeedScraper(headless=False)  # Set to True for production
#     jobs = scraper.search_jobs("software engineer", "San Francisco", pages=2)
    
#     for job in jobs:
#         print(f"Title: {job['title']}")
#         print(f"Company: {job['company']}")
#         print(f"Location: {job['location']}")
#         print(f"Link: {job['link']}")
#         print("-" * 50)
#         # Next.js Job Scraper Project Structure

# ## File Structure
# ```
# job-scraper/
# ├── frontend/                    # Next.js Frontend
# │   ├── src/
# │   │   ├── app/
# │   │   │   ├── layout.tsx
# │   │   │   ├── page.tsx
# │   │   │   ├── login/
# │   │   │   │   └── page.tsx
# │   │   │   ├── dashboard/
# │   │   │   │   └── page.tsx
# │   │   │   ├── resumes/
# │   │   │   │   └── page.tsx
# │   │   │   ├── api/
# │   │   │   │   ├── auth/
# │   │   │   │   ├── resumes/
# │   │   │   │   ├── jobs/
# │   │   │   │   └── scraper/
# │   │   │   └── globals.css
# │   │   ├── components/
# │   │   │   ├── ui/
# │   │   │   ├── auth/
# │   │   │   ├── dashboard/
# │   │   │   ├── resumes/
# │   │   │   └── layout/
# │   │   ├── lib/
# │   │   │   ├── supabase.ts
# │   │   │   ├── utils.ts
# │   │   │   └── types.ts
# │   │   └── hooks/
# │   ├── package.json
# │   ├── next.config.js
# │   ├── tailwind.config.js
# │   └── tsconfig.json
# ├── backend/                     # Python Backend
# │   ├── src/
# │   │   ├── scrapers/
# │   │   │   ├── __init__.py
# │   │   │   ├── base_scraper.py
# │   │   │   ├── indeed_scraper.py
# │   │   │   ├── linkedin_scraper.py
# │   │   │   └── glassdoor_scraper.py
# │   │   ├── models/
# │   │   │   ├── __init__.py
# │   │   │   ├── job.py
# │   │   │   └── user.py
# │   │   ├── services/
# │   │   │   ├── __init__.py
# │   │   │   ├── scraper_service.py
# │   │   │   ├── application_service.py
# │   │   │   └── notification_service.py
# │   │   ├── utils/
# │   │   │   ├── __init__.py
# │   │   │   ├── selenium_utils.py
# │   │   │   ├── proxy_manager.py
# │   │   │   └── user_agents.py
# │   │   ├── api/
# │   │   │   ├── __init__.py
# │   │   │   ├── main.py
# │   │   │   └── routes/
# │   │   └── config/
# │   │       ├── __init__.py
# │   │       └── settings.py
# │   ├── requirements.txt
# │   ├── Dockerfile
# │   └── docker-compose.yml
# ├── n8n/                        # n8n Workflows
# │   ├── workflows/
# │   │   ├── job-scraper.json
# │   │   └── notification.json
# │   └── docker-compose.n8n.yml
# └── README.md
# ```

# ## Package.json (Frontend)
# ```json
# {
#   "name": "job-scraper-frontend",
#   "version": "0.1.0",
#   "private": true,
#   "scripts": {
#     "dev": "next dev",
#     "build": "next build",
#     "start": "next start",
#     "lint": "next lint"
#   },
#   "dependencies": {
#     "next": "14.0.4",
#     "react": "^18",
#     "react-dom": "^18",
#     "@supabase/supabase-js": "^2.39.0",
#     "@supabase/auth-helpers-nextjs": "^0.8.7",
#     "lucide-react": "^0.263.1",
#     "clsx": "^2.0.0",
#     "tailwind-merge": "^2.2.0"
#   },
#   "devDependencies": {
#     "typescript": "^5",
#     "@types/node": "^20",
#     "@types/react": "^18",
#     "@types/react-dom": "^18",
#     "autoprefixer": "^10.0.1",
#     "postcss": "^8",
#     "tailwindcss": "^3.3.0",
#     "eslint": "^8",
#     "eslint-config-next": "14.0.4"
#   }
# }
# ```

# ## Requirements.txt (Backend)
# ```txt
# fastapi==0.104.1
# uvicorn[standard]==0.24.0
# selenium==4.15.2
# beautifulsoup4==4.12.2
# requests==2.31.0
# python-dotenv==1.0.0
# supabase==2.0.2
# crawl4ai==0.2.77
# undetected-chromedriver==3.5.4
# fake-useragent==1.4.0
# python-multipart==0.0.6
# aiofiles==23.2.1
# celery==5.3.4
# redis==5.0.1
# pandas==2.1.4
# numpy==1.25.2
# ```

# ## Next.js Config
# ```javascript
# /** @type {import('next').NextConfig} */
# const nextConfig = {
#   experimental: {
#     appDir: true,
#   },
#   images: {
#     domains: ['avatars.githubusercontent.com'],
#   },
# }

# module.exports = nextConfig
# ```

# ## Tailwind Config
# ```javascript
# /** @type {import('tailwindcss').Config} */
# module.exports = {
#   content: [
#     './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
#     './src/components/**/*.{js,ts,jsx,tsx,mdx}',
#     './src/app/**/*.{js,ts,jsx,tsx,mdx}',
#   ],
#   theme: {
#     extend: {
#       backgroundImage: {
#         'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
#         'gradient-conic':
#           'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
#       },
#     },
#   },
#   plugins: [],
# }
# ```

# ## TypeScript Config
# ```json
# {
#   "compilerOptions": {
#     "target": "es5",
#     "lib": ["dom", "dom.iterable", "esnext"],
#     "allowJs": true,
#     "skipLibCheck": true,
#     "strict": true,
#     "noEmit": true,
#     "esModuleInterop": true,
#     "module": "esnext",
#     "moduleResolution": "bundler",
#     "resolveJsonModule": true,
#     "isolatedModules": true,
#     "jsx": "preserve",
#     "incremental": true,
#     "plugins": [
#       {
#         "name": "next"
#       }
#     ],
#     "paths": {
#       "@/*": ["./src/*"]
#     }
#   },
#   "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
#   "exclude": ["node_modules"]
# }
# ```

# ## Environment Variables (.env.local)
# ```env
# # Supabase
# NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
# SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# # Python Backend
# PYTHON_API_URL=http://localhost:8000

# # n8n
# N8N_WEBHOOK_URL=your_n8n_webhook_url
# ```

# ## Setup Commands
# ```bash
# # Create project
# npx create-next-app@latest job-scraper --typescript --tailwind --eslint --app

# # Navigate to project
# cd job-scraper

# # Install additional dependencies
# npm install @supabase/supabase-js @supabase/auth-helpers-nextjs lucide-react clsx tailwind-merge

# # Create Python virtual environment
# python -m venv backend/venv

# # Activate virtual environment (Windows)
# backend\venv\Scripts\activate

# # Activate virtual environment (Mac/Linux)
# source backend/venv/bin/activate

# # Install Python dependencies
# pip install -r backend/requirements.txt

# # Create directories
# mkdir -p src/components/{ui,auth,dashboard,resumes,layout}
# mkdir -p src/lib src/hooks
# mkdir -p backend/src/{scrapers,models,services,utils,api,config}
# ```