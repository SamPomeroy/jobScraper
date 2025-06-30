import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

TECH_KEYWORDS = [
    "software engineer",
    "front-end developer", 
    # "back-end developer",
    # "full-stack developer",
    # "mobile app developer", 
    "web developer",
    # "wordpress developer", "shopify developer", "react developer",
    # "vue.js developer", "angular developer", "javascript developer",
    # "typescript developer", "html/css developer", "ui developer",
    # "ux/ui developer", "web designer", "interaction designer",
    # "accessibility specialist", "devops engineer", "qa engineer",
    # "data analyst", "data scientist", "data engineer",
    # "machine learning engineer", "ai developer", "python engineer",
    # "python developer", "python web developer", "python data scientist",
    # "python full stack developer", "cloud engineer", "cloud architect",
    # "systems administrator", "network engineer", "site reliability engineer",
    # "platform engineer", "product manager", "technical product manager",
    # "ux designer", "ui designer", "cybersecurity analyst", "security engineer",
    # "information security manager", "it support specialist", "help desk technician",
    # "soc analyst", "blockchain developer", "ar/vr developer", "robotics engineer",
    # "prompt engineer", "technical program manager", "database administrator",
    # "etl developer", "solutions architect", "scrum master", "technical writer",
    # "api integration specialist", "web performance engineer",
    # "web accessibility engineer", "seo specialist", "web content manager"
]

LOCATION = "remote"
PAGES_PER_KEYWORD = 2
MAX_DAYS = 5

def configure_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
    )

    driver = uc.Chrome(options=options, headless=False)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver