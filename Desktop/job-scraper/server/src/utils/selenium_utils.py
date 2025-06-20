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
#             return None # type: ignore
    
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
        
#         # Move to a known starting position (0,0)
#         actions.move_by_offset(1, 1)
        
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




import random
import time
import json
import os
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import shutil

class StealthDriver:
    """Advanced Selenium driver with comprehensive bot detection bypass."""

    def __init__(self, headless: bool = False, use_proxy: bool = False):
        self.headless = headless
        self.use_proxy = use_proxy
        self.driver = None
        self.ua = UserAgent()
    def __del__(self):  # <-- Add this here
            """Prevent undetected_chromedriver from calling quit inside __del__"""
            if self.driver:
                try:
                    self.driver.quit()
                except OSError:
                    pass  # Suppress invalid handle error

    def create_stealth_driver(self) -> Optional[webdriver.Chrome]:
        """Create an undetected Chrome driver with stealth features."""
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        # Headless mode
        if self.headless:
            options.add_argument("--headless=new")  # Correct headless argument

        # Disable automation indicators
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("useAutomationExtension", False)

        # Disable images and notifications for faster browsing
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Random window size
        window_sizes = [
            (1920, 1080), (1366, 768), (1440, 900),
            (1536, 864), (1280, 720), (1600, 900)
        ]
        width, height = random.choice(window_sizes)
        options.add_argument(f"--window-size={width},{height}")

        # Additional stealth arguments
        stealth_args = [
            "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
            "--disable-extensions", "--disable-images", "--disable-popup-blocking",
            "--disable-sync", "--metrics-recording-only",   '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-javascript',
            '--disable-default-apps',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-logging',
            '--disable-log-file',
            '--silent',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-client-side-phishing-detection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-hang-monitor',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain'
            
        ]
        for arg in stealth_args:
            options.add_argument(arg)

        # Random user-agent
        user_agent = self.ua.random
        options.add_argument(f"--user-agent={user_agent}")

        # Create driver with updated settings
        try:
            driver = uc.Chrome(options=options, version_main=None, use_subprocess=False) 


            # Execute CDP commands for additional stealth
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({ query: () => Promise.resolve({ state: 'granted' }) }),
                });
                """
            })
            self.driver = driver
            return driver

        except Exception as e:
            print(f"Error creating stealth driver: {e}")
            return None

    def human_like_typing(self, element, text: str, typing_speed: float = 0.1):
        """Type text with human-like delays and occasional typos."""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.5))
        if random.random() < 0.1:
            time.sleep(random.uniform(0.5, 2.0))

    def human_like_scroll(self, driver, scroll_pause_time: float = 2):
        """Scroll like a human with random pauses."""
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            scroll_amount = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(scroll_pause_time * 0.5, scroll_pause_time * 1.5))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def random_mouse_movement(self, driver):
        """Perform random mouse movements to mimic human behavior."""
        actions = ActionChains(driver)
        window_size = driver.get_window_size()
        width, height = window_size["width"], window_size["height"]
        actions.move_by_offset(1, 1)
        for _ in range(random.randint(2, 5)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            actions.move_by_offset(x, y)
            time.sleep(random.uniform(0.1, 0.5))
        actions.perform()

    def wait_and_find_element(self, driver, by, value, timeout: int = 10):
        """Wait for element with random delay."""
        try:
            time.sleep(random.uniform(0.5, 2.0))
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None

    def bypass_cloudflare(self, driver, max_attempts: int = 3):
        """Bypass Cloudflare protection."""
        for attempt in range(max_attempts):
            try:
                WebDriverWait(driver, 30).until(
                    lambda d: "cloudflare" not in d.current_url.lower()
                    or d.find_elements(By.TAG_NAME, "body")
                )
                if "cloudflare" not in driver.current_url.lower():
                    return True
                time.sleep(random.uniform(10, 15))
            except TimeoutException:
                if attempt == max_attempts - 1:
                    return False
                driver.refresh()
                time.sleep(random.uniform(5, 10))
        return False

  
    def close(self):
        """Safe cleanup for Selenium driver"""
        if self.driver:
            try:
                self.driver.quit()
                shutil.rmtree(self.driver.profile_path, ignore_errors=True)  # Prevent locked directory errors
            except OSError:
                pass  # Suppresses invalid handle error

# TEST: Run script directly
if __name__ == "__main__":
    driver = StealthDriver(headless=True)
    stealth_driver = driver.create_stealth_driver()

    if stealth_driver:
        stealth_driver.get("https://www.google.com")
        print(stealth_driver.title)
        
        # Proper cleanup
        stealth_driver.quit()  # <-- Add this line