from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

def get_headless_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # ✅ Corrected path using forward slashes
    driver_path = "C:/Users/snoep_a5dedf8/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

    if not os.path.isfile(driver_path):
        raise FileNotFoundError(f"❌ ChromeDriver not found at: {driver_path}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver