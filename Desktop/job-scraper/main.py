# import imapclient
# import imaplib
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# # Keywords to filter job emails
# JOB_PLATFORMS = ["Glassdoor", "LinkedIn", "Indeed"]

# # Connect to IMAP and Fetch Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("INBOX")
#         messages = client.search(["UNSEEN"])  # Fetch unread emails

#         if not messages:
#             print("No new job emails found.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             # Extract Email Content
#             subject = email_message["Subject"]
#             if not any(platform in subject for platform in JOB_PLATFORMS):
#                 continue  # Skip non-job emails

#             if email_message.is_multipart():
#                 body = email_message.get_payload(0).get_payload(decode=True).decode("utf-8")
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8")

#             soup = BeautifulSoup(body, "html.parser")  # Parse email content

#             # Extract job details
#             job = {
#                 "title": soup.find("h1").text.strip() if soup.find("h1") else "",
#                 "company": soup.find("strong").text.strip() if soup.find("strong") else "",
#                 "location": soup.find("p", class_="location").text.strip() if soup.find("p", class_="location") else "",
#                 "description": soup.find("p").text if soup.find("p") else "",
#                 "salary": "",
#                 "job_type": "",
#                 "posted_date": datetime.now(timezone.utc).isoformat(),
#                 "apply_url": soup.find("a")["href"] if soup.find("a") else "",
#                 "job_id": f"linkedin_{hash(soup.find('h1').text + soup.find('strong').text)}",
#                 "source": "LinkedIn",
#                 "scraped_at": datetime.now(timezone.utc).isoformat(),
#                 "keywords": []
#             }
#             job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)



# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# # Job platforms to filter
# JOB_PLATFORMS = ["Glassdoor Jobs", "LinkedIn Job Alerts", "Phil @ ZipRecruiter", "Careerbuilder", "LinkedIn"]

# # Connect to IMAP and Fetch Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("INBOX")
#         messages = client.search(["UNSEEN"])  # Fetch unread emails

#         if not messages:
#             print("No new job emails found.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             # Extract Subject to Filter Job Emails
#             subject = email_message["Subject"]
#             if not any(platform in subject for platform in JOB_PLATFORMS):
#                 continue  # Skip non-job emails

#             # Extract Email Body
#             if email_message.is_multipart():
#                 body = email_message.get_payload(0).get_payload(decode=True).decode("utf-8")
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8")

#             soup = BeautifulSoup(body, "html.parser")  # Parse email content

#             # Extract job details
#             job = {
#                 "title": soup.find("h2").text.strip() if soup.find("h2") else "",
#                 "company": soup.find("strong").text.strip() if soup.find("strong") else "",
#                 "location": soup.find("p", class_="location").text.strip() if soup.find("p", class_="location") else "",
#                 "description": soup.find("p").text if soup.find("p") else "",
#                 "apply_url": soup.find("a")["href"] if soup.find("a") else "",
#                 "source": subject,  # Use email subject as source
#                 "scraped_at": datetime.now(timezone.utc).isoformat(),
#             }
#             job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)

# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone,timedelta

# from email import message_from_bytes
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")
# thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")
# messages = client.search([f'SINCE {thirty_days_ago}'])


# # Job platforms to filter
# JOB_PLATFORMS = ["Glassdoor Jobs", "LinkedIn Job Alerts", "Phil @ ZipRecruiter", "Careerbuilder", "LinkedIn"]

# # Connect to IMAP and Fetch Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("INBOX")
#         messages = client.search(["UNSEEN"])  # Fetch unread emails

#         if not messages:
#             print("No new job emails found.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             # Extract Subject to Filter Job Emails
#             subject = email_message["Subject"]
#             if not any(platform in subject for platform in JOB_PLATFORMS):
#                 continue  # Skip non-job emails

#             # Extract Email Body (Fixing NoneType error)
#             body = ""
#             if email_message.is_multipart():
#                 payload = email_message.get_payload(0)
#                 if payload:
#                     body = payload.get_payload(decode=True).decode("utf-8") if payload else ""
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8") if email_message.get_payload() else ""

#             # Debugging - Print email structure if parsing fails
#             if not body:
#                 print("Failed to extract body from email:", subject)

#             soup = BeautifulSoup(body, "html.parser")  # Parse email content

#             # Extract job details safely
#             title = soup.find("h2") or soup.find("h1")  # Alternative selectors
#             company = soup.find("strong") or soup.find("span", class_="company-name")

#             job = {
#                 "title": title.text.strip() if title else "Unknown Title",
#                 "company": company.text.strip() if company else "Unknown Company",
#                 "location": soup.find("p", class_="location").text.strip() if soup.find("p", class_="location") else "",
#                 "description": soup.find("p").text if soup.find("p") else "",
#                 "apply_url": soup.find("a")["href"] if soup.find("a") else "",
#                 "source": subject,  # Use email subject as source
#                 "scraped_at": datetime.now(timezone.utc).isoformat(),
#             }
#             job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)
# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone, timedelta
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os
# from lxml import etree

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# # XPath selectors for different platforms
# XPATH_SELECTORS = {
#     "Glassdoor Jobs": "//*[@id='m_-4583445198408703372GDEmailWrapper']/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody",
#     "LinkedIn Job Alerts": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td",
#     "Phil @ ZipRecruiter": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td"
# }

# # Connect to IMAP and Fetch Job Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("[Gmail]/All Mail")


#         thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")
#         messages = client.search(["SINCE", thirty_days_ago])

#         if not messages:
#             print("No new job emails found within the last 30 days.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             subject = email_message["Subject"]
#             matched_platform = next((p for p in XPATH_SELECTORS if p in subject), None)
#             if not matched_platform:
#                 continue  # Skip emails that don't match known platforms

#             # Extract Email Body
#             body = ""
#             if email_message.is_multipart():
#                 payload = email_message.get_payload(0)
#                 if payload:
#                     body = payload.get_payload(decode=True).decode("utf-8") if payload else ""
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8") if email_message.get_payload() else ""

#             if not body:
#                 print(f"Failed to extract body from email: {subject}")
#                 continue

#             soup = BeautifulSoup(body, "html.parser")
#             html_tree = etree.HTML(str(soup))

#             # Extract job details using the correct XPath selector
#             job_elements = html_tree.xpath(XPATH_SELECTORS[matched_platform])

#             for job_element in job_elements:
#                 title = job_element.xpath(".//a/text()")
#                 company = job_element.xpath(".//span/text()")  # Company name span
#                 location = job_element.xpath(".//p/text()")  # Location
#                 salary = job_element.xpath(".//span[contains(text(), '$')]/text()")  # Salary details
#                 apply_url = job_element.xpath(".//a/@href")

#                 job = {
#                     "title": title[0].strip() if title else "Unknown Title",
#                     "company": company[0].strip() if company else "Unknown Company",
#                     "location": location[0].strip() if location else "",
#                     "salary": salary[0].strip() if salary else "Not Provided",
#                     "apply_url": apply_url[0] if apply_url else "",
#                     "source": matched_platform,
#                     "scraped_at": datetime.now(timezone.utc).isoformat(),
#                 }
#                 job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)







# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone, timedelta
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os
# from lxml import etree

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# # XPath selectors for different platforms
# XPATH_SELECTORS = {
#     "Glassdoor Jobs": "//*[@id='m_-4583445198408703372GDEmailWrapper']/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody",
#     "LinkedIn Job Alerts": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td",
#     "Phil @ ZipRecruiter": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td",
#     "Careerbuilder": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[3]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td[2]/table[4]/tbody/tr/td/table/tbody/tr/td"
# }

# # Connect to IMAP and Fetch Job Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("[Gmail]/All Mail")  # Ensure search includes all emails, not just Inbox

#         # Search emails by subject instead of restrictive date-based filters
#         messages_glassdoor = client.search(['SUBJECT', "Glassdoor Jobs"])
#         messages_linkedin = client.search(['SUBJECT', "LinkedIn Job Alerts"])
#         messages_ziprecruiter = client.search(['SUBJECT', "Phil @ ZipRecruiter"])
#         messages_careerbuilder = client.search(['SUBJECT', "Careerbuilder"])

#         # Combine all message results
#         messages = messages_glassdoor + messages_linkedin + messages_ziprecruiter + messages_careerbuilder
#         print(f"Found {len(messages)} job emails.")

#         if not messages:
#             print("No new job emails found.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             subject = email_message["Subject"]
#             matched_platform = next((p for p in XPATH_SELECTORS if p in subject), None)
#             if not matched_platform:
#                 continue  # Skip emails that don't match known platforms

#             # Extract Email Body
#             body = ""
#             if email_message.is_multipart():
#                 payload = email_message.get_payload(0)
#                 if payload:
#                     body = payload.get_payload(decode=True).decode("utf-8") if payload else ""
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8") if email_message.get_payload() else ""

#             if not body:
#                 print(f"Failed to extract body from email: {subject}")
#                 continue

#             soup = BeautifulSoup(body, "html.parser")
#             html_tree = etree.HTML(str(soup))

#             # Extract job details using the correct XPath selector
#             job_elements = html_tree.xpath(XPATH_SELECTORS[matched_platform])

#             for job_element in job_elements:
#                 title = job_element.xpath(".//a/text()")
#                 company = job_element.xpath(".//span/text()")
#                 location = job_element.xpath(".//p/text()")
#                 salary = job_element.xpath(".//span[contains(text(), '$')]/text()")
#                 apply_url = job_element.xpath(".//a/@href")

#                 job = {
#                     "title": title[0].strip() if title else "Unknown Title",
#                     "company": company[0].strip() if company else "Unknown Company",
#                     "location": location[0].strip() if location else "",
#                     "salary": salary[0].strip() if salary else "Not Provided",
#                     "apply_url": apply_url[0] if apply_url else "",
#                     "source": matched_platform,
#                     "scraped_at": datetime.now(timezone.utc).isoformat(),
#                 }
#                 job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)







# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone, timedelta
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os
# from lxml import etree

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# # XPath selectors for different platforms
# XPATH_SELECTORS = {
#     "Glassdoor Jobs": "//*[@id='m_-4583445198408703372GDEmailWrapper']/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody",
#     "LinkedIn Job Alerts": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td",
#     "Phil @ ZipRecruiter": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td",
#     "Careerbuilder": "/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[3]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td[2]/table[4]/tbody/tr/td/table/tbody/tr/td"
# }

# # Connect to IMAP and Fetch Job Emails
# def fetch_job_emails():
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("[Gmail]/All Mail")  # Ensure search includes all emails, not just Inbox

#         # Search emails by subject instead of restrictive date-based filters
#         messages_glassdoor = client.search(['SUBJECT', "Glassdoor Jobs"])
#         messages_linkedin = client.search(['SUBJECT', "LinkedIn Job Alerts"])
#         messages_ziprecruiter = client.search(['SUBJECT', "Phil @ ZipRecruiter"])
#         messages_careerbuilder = client.search(['SUBJECT', "Careerbuilder"])

#         # Combine all message results
#         messages = messages_glassdoor + messages_linkedin + messages_ziprecruiter + messages_careerbuilder
#         print(f"Found {len(messages)} job emails.")

#         if not messages:
#             print("No new job emails found.")
#             return []

#         job_listings = []
#         for msg_id in messages:
#             raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#             email_message = message_from_bytes(raw_email)

#             subject = email_message["Subject"]
#             matched_platform = next((p for p in XPATH_SELECTORS if p in subject), None)
#             if not matched_platform:
#                 continue  # Skip emails that don't match known platforms

#             # Extract Email Body
#             body = ""
#             if email_message.is_multipart():
#                 payload = email_message.get_payload(0)
#                 if payload:
#                     body = payload.get_payload(decode=True).decode("utf-8") if payload else ""
#             else:
#                 body = email_message.get_payload(decode=True).decode("utf-8") if email_message.get_payload() else ""

#             if not body:
#                 print(f"Failed to extract body from email: {subject}")
#                 continue

#             print("Raw Email Content Preview:", body[:1000])  # Debugging: Print email content

#             soup = BeautifulSoup(body, "html.parser")
#             html_tree = etree.HTML(str(soup))

#             # Extract job details using the correct XPath selector
#             job_elements = html_tree.xpath(XPATH_SELECTORS[matched_platform])

#             for job_element in job_elements:
#                 title = job_element.xpath(".//a[@class='job-title']/text()") or job_element.xpath(".//h2/text()")
#                 company = job_element.xpath(".//span[@class='company-name']/text()") or job_element.xpath(".//strong/text()")
#                 location = job_element.xpath(".//p[@class='location']/text()") or job_element.xpath(".//td[contains(@class,'job-location')]/text()")
#                 salary = job_element.xpath(".//span[contains(text(), '$')]/text()")
#                 apply_url = job_element.xpath(".//a[@class='apply-link']/@href") or job_element.xpath(".//a/@href")

#                 job = {
#                     "title": title[0].strip() if title else "No Title Found",
#                     "company": company[0].strip() if company else "No Company Found",
#                     "location": location[0].strip() if location else "No Location Found",
#                     "salary": salary[0].strip() if salary else "Salary Not Provided",
#                     "apply_url": apply_url[0] if apply_url else "No Apply URL",
#                     "source": matched_platform,
#                     "scraped_at": datetime.now(timezone.utc).isoformat(),
#                 }
#                 print(f"Extracted Job: {job}")  # Debugging: Print extracted job details
#                 job_listings.append(job)

#         return job_listings

# # Save to CSV
# def save_to_csv(job_listings, filename="job_listings.csv"):
#     df = pd.DataFrame(job_listings)
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(job_listings)} job listings to {filename}")

# # Run Extraction Process
# if __name__ == "__main__":
#     jobs = fetch_job_emails()
#     if jobs:
#         save_to_csv(jobs)

# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os
# from email.header import decode_header
# import re

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# def extract_linkedin_jobs_from_html(html_content):
#     """
#     Extract job listings from LinkedIn job alert emails using BeautifulSoup
#     """
#     soup = BeautifulSoup(html_content, 'html.parser')
#     jobs = []
    
#     # Look for job containers - LinkedIn typically uses table-based layouts
#     # Try multiple selectors to catch different email formats
#     job_containers = []
    
#     # Method 1: Look for tables with job information
#     tables = soup.find_all('table')
#     for table in tables:
#         # Look for job titles (usually in links or bold text)
#         job_links = table.find_all('a', href=True)
#         for link in job_links:
#             if 'linkedin.com/jobs' in link.get('href', ''):
#                 job_containers.append(table)
#                 break
    
#     # Method 2: Look for divs with job-related classes or content
#     divs = soup.find_all('div')
#     for div in divs:
#         if div.find('a', href=lambda x: x and 'linkedin.com/jobs' in x):
#             job_containers.append(div)
    
#     # Method 3: Search for job patterns in the HTML
#     # Look for elements containing job-related text patterns
#     all_elements = soup.find_all(['td', 'div', 'span', 'p'])
    
#     processed_jobs = set()  # To avoid duplicates
    
#     for container in job_containers:
#         job_data = extract_job_from_container(container)
#         if job_data and job_data['title'] != 'No Title Found':
#             job_key = (job_data['title'], job_data['company'])
#             if job_key not in processed_jobs:
#                 jobs.append(job_data)
#                 processed_jobs.add(job_key)
    
#     # If no structured containers found, try text-based extraction
#     if not jobs:
#         jobs = extract_jobs_from_text(html_content)
    
#     return jobs

# def extract_job_from_container(container):
#     """
#     Extract job information from a container element
#     """
#     job_data = {
#         "title": "No Title Found",
#         "company": "No Company Found", 
#         "location": "No Location Found",
#         "salary": "Salary Not Provided",
#         "apply_url": "No Apply URL",
#         "source": "LinkedIn Job Alerts",
#         "scraped_at": datetime.now(timezone.utc).isoformat(),
#     }
    
#     # Find job title and URL
#     job_link = container.find('a', href=lambda x: x and 'linkedin.com/jobs' in x)
#     if job_link:
#         job_data['title'] = job_link.get_text(strip=True)
#         job_data['apply_url'] = job_link.get('href')
    
#     # Find company name - usually near the job title
#     company_patterns = [
#         container.find('strong'),
#         container.find('b'),
#         container.find(text=re.compile(r'^[A-Z][a-zA-Z\s&,.-]+$'))  # Company name pattern
#     ]
    
#     for pattern in company_patterns:
#         if pattern and isinstance(pattern, str):
#             if len(pattern.strip()) > 2 and not any(x in pattern.lower() for x in ['apply', 'view', 'job', 'click']):
#                 job_data['company'] = pattern.strip()
#                 break
#         elif pattern:
#             text = pattern.get_text(strip=True)
#             if len(text) > 2 and not any(x in text.lower() for x in ['apply', 'view', 'job', 'click']):
#                 job_data['company'] = text
#                 break
    
#     # Find location - look for city/state patterns
#     all_text = container.get_text()
#     location_match = re.search(r'([A-Z][a-zA-Z\s]+,\s*[A-Z]{2})|([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)', all_text)
#     if location_match:
#         job_data['location'] = location_match.group().strip()
    
#     # Find salary - look for dollar amounts
#     salary_match = re.search(r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*per\s*year|\s*annually|\s*/year)?', all_text, re.IGNORECASE)
#     if salary_match:
#         job_data['salary'] = salary_match.group().strip()
    
#     return job_data

# def extract_jobs_from_text(html_content):
#     """
#     Fallback method: extract jobs from raw text patterns
#     """
#     jobs = []
    
#     # Find all LinkedIn job URLs
#     job_urls = re.findall(r'https?://[^\s]*linkedin\.com/jobs/view/\d+[^\s]*', html_content)
    
#     soup = BeautifulSoup(html_content, 'html.parser')
#     text_content = soup.get_text()
    
#     for url in job_urls:
#         # Try to find job title near the URL
#         url_index = html_content.find(url)
#         if url_index != -1:
#             # Look for text before and after the URL
#             context_start = max(0, url_index - 200)
#             context_end = min(len(html_content), url_index + len(url) + 200)
#             context = html_content[context_start:context_end]
            
#             # Extract job info from context
#             context_soup = BeautifulSoup(context, 'html.parser')
#             job_data = {
#                 "title": "Job Title Not Found",
#                 "company": "Company Not Found",
#                 "location": "Location Not Found", 
#                 "salary": "Salary Not Provided",
#                 "apply_url": url,
#                 "source": "LinkedIn Job Alerts",
#                 "scraped_at": datetime.now(timezone.utc).isoformat(),
#             }
            
#             # Try to extract title from link text or nearby text
#             link_elem = context_soup.find('a', href=url)
#             if link_elem:
#                 job_data['title'] = link_elem.get_text(strip=True)
            
#             jobs.append(job_data)
    
#     return jobs

# def fetch_linkedin_job_emails():
#     """
#     Fetch and parse LinkedIn job alert emails
#     """
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("[Gmail]/All Mail")
        
#         # Search for LinkedIn job alerts specifically
#         # Use both subject and sender criteria
#         messages = client.search([
#             'OR',
#             ['SUBJECT', 'LinkedIn Job Alerts'],
#             ['FROM', 'jobalerts-noreply@linkedin.com']
#         ])
        
#         print(f"Found {len(messages)} LinkedIn job alert emails.")
        
#         if not messages:
#             print("No LinkedIn job emails found.")
#             return []
        
#         all_jobs = []
#         processed_jobs = set()  # To avoid duplicates across emails
        
#         for msg_id in messages:
#             try:
#                 raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#                 email_message = message_from_bytes(raw_email)
                
#                 # Decode subject
#                 subject_decoded = decode_header(email_message["Subject"])[0][0]
#                 if isinstance(subject_decoded, bytes):
#                     subject_decoded = subject_decoded.decode("utf-8")
                
#                 print(f"Processing email: {subject_decoded}")
                
#                 # Extract email body
#                 body = get_email_body(email_message)
#                 if not body:
#                     print(f"Could not extract body from email: {subject_decoded}")
#                     continue
                
#                 # Extract jobs from this email
#                 jobs = extract_linkedin_jobs_from_html(body)
                
#                 # Add unique jobs to our collection
#                 for job in jobs:
#                     job_key = (job['title'], job['company'], job['apply_url'])
#                     if job_key not in processed_jobs:
#                         all_jobs.append(job)
#                         processed_jobs.add(job_key)
#                         print(f"Extracted: {job['title']} at {job['company']}")
                
#             except Exception as e:
#                 print(f"Error processing email {msg_id}: {str(e)}")
#                 continue
        
#         return all_jobs

# def get_email_body(email_message):
#     """
#     Extract HTML body from email message
#     """
#     body = ""
    
#     if email_message.is_multipart():
#         for part in email_message.walk():
#             content_type = part.get_content_type()
#             if content_type == "text/html":
#                 try:
#                     payload = part.get_payload(decode=True)
#                     if payload:
#                         body = payload.decode("utf-8", errors='ignore')
#                         break
#                 except:
#                     continue
#             elif content_type == "text/plain" and not body:
#                 try:
#                     payload = part.get_payload(decode=True)
#                     if payload:
#                         body = payload.decode("utf-8", errors='ignore')
#                 except:
#                     continue
#     else:
#         try:
#             payload = email_message.get_payload(decode=True)
#             if payload:
#                 body = payload.decode("utf-8", errors='ignore')
#         except:
#             pass
    
#     return body

# def save_jobs_to_csv(job_listings, filename="linkedin_jobs.csv"):
#     """
#     Save job listings to CSV file
#     """
#     if not job_listings:
#         print("No job listings to save.")
#         return
    
#     df = pd.DataFrame(job_listings)
    
#     # Remove duplicates based on title and company
#     df = df.drop_duplicates(subset=['title', 'company', 'apply_url'])
    
#     if df.empty:
#         print("No unique job listings found after removing duplicates.")
#         return
    
#     # Sort by scraped_at date
#     df = df.sort_values('scraped_at', ascending=False)
    
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(df)} unique LinkedIn job listings to {filename}")
    
#     # Print summary
#     print("\nJob Summary:")
#     print(f"Total jobs: {len(df)}")
#     if len(df) > 0:
#         print(f"Companies found: {df['company'].nunique()}")
#         print(f"Locations found: {df['location'].nunique()}")

# # Run the extraction process
# if __name__ == "__main__":
#     print("Starting LinkedIn job email extraction...")
#     jobs = fetch_linkedin_job_emails()
    
#     if jobs:
#         save_jobs_to_csv(jobs)
        
#         # Print first few jobs as preview
#         print(f"\nFirst 3 jobs found:")
#         for i, job in enumerate(jobs[:3]):
#             print(f"{i+1}. {job['title']} at {job['company']} - {job['location']}")
#             print(f"   URL: {job['apply_url'][:80]}...")
#             print()
#     else:
#         print("No jobs were extracted. Check your email search criteria and HTML parsing logic.")




# import imapclient
# import email
# import pandas as pd
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from email import message_from_bytes
# from dotenv import load_dotenv
# import os
# from email.header import decode_header
# import re

# # Load environment variables
# load_dotenv()

# # Access stored values
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
# EMAIL_HOST = os.getenv("EMAIL_HOST")

# if not EMAIL_USER or not EMAIL_PASS:
#     raise ValueError("Email credentials not found! Set them in your .env file.")

# print(f"Email User: {EMAIL_USER}")

# def extract_linkedin_jobs_from_html(html_content):
#     """
#     Extract job listings from LinkedIn job alert emails using BeautifulSoup
#     """
#     soup = BeautifulSoup(html_content, 'html.parser')
#     jobs = []
    
#     # First, try to find actual job links (not "See similar jobs" links)
#     job_links = soup.find_all('a', href=lambda x: x and 'linkedin.com/jobs/view/' in str(x))
    
#     processed_jobs = set()  # To avoid duplicates
    
#     for link in job_links:
#         job_url = link.get('href')
#         if not job_url or 'similar-jobs' in job_url:
#             continue  # Skip "See similar jobs" links
            
#         job_data = extract_job_from_link_context(link, job_url)
#         if job_data and is_valid_job(job_data):
#             job_key = (job_data['title'], job_data['company'], job_data['apply_url'])
#             if job_key not in processed_jobs:
#                 jobs.append(job_data)
#                 processed_jobs.add(job_key)
    
#     # If no direct job links found, try alternative extraction methods
#     if not jobs:
#         jobs = extract_jobs_alternative_methods(soup)
    
#     return jobs

# def extract_job_from_link_context(link_element, job_url):
#     """
#     Extract job information from the context around a job link
#     """
#     job_data = {
#         "title": "No Title Found",
#         "company": "No Company Found", 
#         "location": "No Location Found",
#         "salary": "Salary Not Provided",
#         "apply_url": clean_url(job_url),
#         "source": "LinkedIn Job Alerts",
#         "scraped_at": datetime.now(timezone.utc).isoformat(),
#     }
    
#     # Extract job title from link text
#     title_text = link_element.get_text(strip=True)
#     if title_text and len(title_text) > 2 and not is_generic_text(title_text):
#         job_data['title'] = clean_text(title_text)
    
#     # Look for job info in the surrounding context
#     # Check parent elements for job details
#     current_element = link_element
#     for _ in range(5):  # Look up to 5 levels up
#         current_element = current_element.parent
#         if not current_element:
#             break
            
#         # Look for company name in nearby elements
#         company_candidates = find_company_in_context(current_element)
#         if company_candidates:
#             job_data['company'] = company_candidates[0]
        
#         # Look for location in nearby elements  
#         location_candidates = find_location_in_context(current_element)
#         if location_candidates:
#             job_data['location'] = location_candidates[0]
        
#         # Look for salary in nearby elements
#         salary_candidates = find_salary_in_context(current_element)
#         if salary_candidates:
#             job_data['salary'] = salary_candidates[0]
    
#     return job_data

# def find_company_in_context(element):
#     """Find company names in the given element context"""
#     companies = []
    
#     # Look for common company indicators
#     text_content = element.get_text() if element else ""
    
#     # Look for text that looks like company names
#     # Companies often appear after job titles or in specific patterns
#     lines = text_content.split('\n')
#     for i, line in enumerate(lines):
#         line = line.strip()
#         if not line or len(line) < 2:
#             continue
            
#         # Skip lines that are clearly not company names
#         if is_generic_text(line) or is_job_title_pattern(line):
#             continue
            
#         # Look for company name patterns
#         if is_company_name_pattern(line):
#             companies.append(clean_text(line))
    
#     return companies[:3]  # Return top 3 candidates

# def find_location_in_context(element):
#     """Find locations in the given element context"""
#     locations = []
    
#     text_content = element.get_text() if element else ""
    
#     # Look for location patterns (City, State or City, Country)
#     location_patterns = [
#         r'([A-Z][a-zA-Z\s]+,\s*[A-Z]{2})',  # City, ST
#         r'([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)',  # City, State/Country
#         r'(Remote)',  # Remote work
#         r'([A-Z][a-zA-Z\s]+ Area)',  # Metro Area
#     ]
    
#     for pattern in location_patterns:
#         matches = re.findall(pattern, text_content)
#         for match in matches:
#             if isinstance(match, tuple):
#                 match = match[0] if match else ""
#             if match and len(match.strip()) > 2:
#                 locations.append(clean_text(match.strip()))
    
#     return locations[:3]  # Return top 3 candidates

# def find_salary_in_context(element):
#     """Find salary information in the given element context"""
#     salaries = []
    
#     text_content = element.get_text() if element else ""
    
#     # Look for salary patterns
#     salary_patterns = [
#         r'\$\d{2,3}(?:,\d{3})*(?:\s*-\s*\$\d{2,3}(?:,\d{3})*)?(?:\s*(?:per\s*year|annually|/year|/yr))?',
#         r'\$\d{2,3}(?:,\d{3})*(?:\s*-\s*\$\d{2,3}(?:,\d{3})*)?(?:\s*(?:per\s*hour|/hour|/hr))?',
#         r'\d{2,3}(?:,\d{3})*(?:\s*-\s*\d{2,3}(?:,\d{3})*)?k(?:\s*(?:per\s*year|annually|/year))?'
#     ]
    
#     for pattern in salary_patterns:
#         matches = re.findall(pattern, text_content, re.IGNORECASE)
#         for match in matches:
#             if match and len(match.strip()) > 2:
#                 salaries.append(clean_text(match.strip()))
    
#     return salaries[:3]  # Return top 3 candidates

# def is_valid_job(job_data):
#     """Check if the extracted job data is valid"""
#     # Skip jobs with generic titles
#     if is_generic_text(job_data['title']):
#         return False
    
#     # Skip if title is too short or looks like a navigation element
#     if len(job_data['title']) < 3:
#         return False
        
#     # Skip if URL is a "similar jobs" link
#     if 'similar-jobs' in job_data['apply_url']:
#         return False
    
#     return True

# def is_generic_text(text):
#     """Check if text is generic/non-specific"""
#     if not text:
#         return True
        
#     text_lower = text.lower().strip()
    
#     generic_phrases = [
#         'see similar jobs', 'view job', 'apply now', 'easy apply',
#         'see jobs', 'other jobs', 'actively recruiting', 'click here',
#         'view all', 'more jobs', 'job alert', 'unsubscribe',
#         'email preferences', 'linkedin', 'see all jobs'
#     ]
    
#     return any(phrase in text_lower for phrase in generic_phrases)

# def is_job_title_pattern(text):
#     """Check if text looks like a job title (for filtering company names)"""
#     if not text:
#         return False
        
#     text_lower = text.lower().strip()
    
#     job_keywords = [
#         'developer', 'engineer', 'manager', 'analyst', 'specialist',
#         'coordinator', 'assistant', 'director', 'lead', 'senior',
#         'junior', 'intern', 'consultant', 'architect', 'designer'
#     ]
    
#     return any(keyword in text_lower for keyword in job_keywords)

# def is_company_name_pattern(text):
#     """Check if text looks like a company name"""
#     if not text or len(text.strip()) < 2:
#         return False
        
#     text_clean = text.strip()
    
#     # Skip if it's clearly not a company name
#     if is_generic_text(text_clean) or is_job_title_pattern(text_clean):
#         return False
    
#     # Skip if it's too long (likely not just a company name)
#     if len(text_clean) > 60:
#         return False
    
#     # Skip if it contains too many non-letter characters
#     letter_count = sum(1 for c in text_clean if c.isalpha())
#     if letter_count < len(text_clean) * 0.5:
#         return False
    
#     return True

# def clean_text(text):
#     """Clean and normalize text"""
#     if not text:
#         return ""
    
#     # Remove extra whitespace
#     text = ' '.join(text.split())
    
#     # Remove common email artifacts
#     text = re.sub(r'\s*\|\s*', ' | ', text)  # Clean up pipe separators
#     text = re.sub(r'\s*-\s*', ' - ', text)   # Clean up dashes
    
#     # Trim to reasonable length
#     if len(text) > 100:
#         text = text[:100].strip()
    
#     return text.strip()

# def clean_url(url):
#     """Clean and normalize URLs"""
#     if not url:
#         return ""
    
#     # Remove tracking parameters but keep essential ones
#     if '?' in url:
#         base_url, params = url.split('?', 1)
#         # Keep only essential parameters
#         essential_params = []
#         for param in params.split('&'):
#             if param.startswith(('jobId=', 'referenceJobId=')):
#                 essential_params.append(param)
        
#         if essential_params:
#             url = base_url + '?' + '&'.join(essential_params)
#         else:
#             url = base_url
    
#     return url

# def extract_jobs_alternative_methods(soup):
#     """Alternative extraction methods when primary method fails"""
#     jobs = []
    
#     # Method 1: Look for job information in table cells
#     tables = soup.find_all('table')
#     for table in tables:
#         rows = table.find_all('tr')
#         for row in rows:
#             cells = row.find_all(['td', 'th'])
#             for cell in cells:
#                 job_links = cell.find_all('a', href=lambda x: x and 'linkedin.com/jobs/view/' in str(x))
#                 for link in job_links:
#                     job_url = link.get('href')
#                     if 'similar-jobs' not in job_url:
#                         job_data = extract_job_from_link_context(link, job_url)
#                         if job_data and is_valid_job(job_data):
#                             jobs.append(job_data)
    
#     return jobs

# def fetch_linkedin_job_emails():
#     """
#     Fetch and parse LinkedIn job alert emails
#     """
#     with imapclient.IMAPClient(EMAIL_HOST) as client:
#         client.login(EMAIL_USER, EMAIL_PASS)
#         client.select_folder("[Gmail]/All Mail")
        
#         # Search for LinkedIn job alerts specifically
#         # Use both subject and sender criteria
#         messages = client.search([
#             'OR',
#             ['SUBJECT', 'LinkedIn Job Alerts'],
#             ['FROM', 'jobalerts-noreply@linkedin.com']
#         ])
        
#         print(f"Found {len(messages)} LinkedIn job alert emails.")
        
#         if not messages:
#             print("No LinkedIn job emails found.")
#             return []
        
#         all_jobs = []
#         processed_jobs = set()  # To avoid duplicates across emails
        
#         for msg_id in messages:
#             try:
#                 raw_email = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
#                 email_message = message_from_bytes(raw_email)
                
#                 # Decode subject
#                 subject_decoded = decode_header(email_message["Subject"])[0][0]
#                 if isinstance(subject_decoded, bytes):
#                     subject_decoded = subject_decoded.decode("utf-8")
                
#                 print(f"Processing email: {subject_decoded}")
                
#                 # Extract email body
#                 body = get_email_body(email_message)
#                 if not body:
#                     print(f"Could not extract body from email: {subject_decoded}")
#                     continue
                
#                 # Extract jobs from this email
#                 jobs = extract_linkedin_jobs_from_html(body)
                
#                 # Add unique jobs to our collection
#                 for job in jobs:
#                     job_key = (job['title'], job['company'], job['apply_url'])
#                     if job_key not in processed_jobs:
#                         all_jobs.append(job)
#                         processed_jobs.add(job_key)
#                         print(f"Extracted: {job['title']} at {job['company']}")
                
#             except Exception as e:
#                 print(f"Error processing email {msg_id}: {str(e)}")
#                 continue
        
#         return all_jobs

# def get_email_body(email_message):
#     """
#     Extract HTML body from email message
#     """
#     body = ""
    
#     if email_message.is_multipart():
#         for part in email_message.walk():
#             content_type = part.get_content_type()
#             if content_type == "text/html":
#                 try:
#                     payload = part.get_payload(decode=True)
#                     if payload:
#                         body = payload.decode("utf-8", errors='ignore')
#                         break
#                 except:
#                     continue
#             elif content_type == "text/plain" and not body:
#                 try:
#                     payload = part.get_payload(decode=True)
#                     if payload:
#                         body = payload.decode("utf-8", errors='ignore')
#                 except:
#                     continue
#     else:
#         try:
#             payload = email_message.get_payload(decode=True)
#             if payload:
#                 body = payload.decode("utf-8", errors='ignore')
#         except:
#             pass
    
#     return body

# def save_jobs_to_csv(job_listings, filename="linkedin_jobs_cleaned.csv"):
#     """
#     Save job listings to CSV file with data cleaning
#     """
#     if not job_listings:
#         print("No job listings to save.")
#         return
    
#     df = pd.DataFrame(job_listings)
    
#     # Clean the data
#     df = clean_dataframe(df)
    
#     # Remove duplicates based on title and company
#     df = df.drop_duplicates(subset=['title', 'company', 'apply_url'])
    
#     # Filter out invalid jobs
#     df = df[df['title'] != 'No Title Found']
#     df = df[~df['title'].str.contains('See similar jobs|View job|Apply now', case=False, na=False)]
    
#     if df.empty:
#         print("No valid job listings found after cleaning and removing duplicates.")
#         return
    
#     # Sort by scraped_at date
#     df = df.sort_values('scraped_at', ascending=False)
    
#     df.to_csv(filename, index=False)
#     print(f"Saved {len(df)} cleaned LinkedIn job listings to {filename}")
    
#     # Print summary
#     print("\nCleaned Job Summary:")
#     print(f"Total jobs: {len(df)}")
#     if len(df) > 0:
#         print(f"Companies found: {df['company'].nunique()}")
#         print(f"Locations found: {df['location'].nunique()}")
#         print(f"Jobs with salary info: {len(df[df['salary'] != 'Salary Not Provided'])}")
        
#         # Show sample of cleaned data
#         print(f"\nSample of cleaned jobs:")
#         for i, row in df.head(3).iterrows():
#             print(f"- {row['title']} at {row['company']} ({row['location']})")

# def clean_dataframe(df):
#     """
#     Clean the entire dataframe
#     """
#     # Clean title column
#     df['title'] = df['title'].apply(lambda x: clean_job_title(str(x)) if pd.notna(x) else 'No Title Found')
    
#     # Clean company column  
#     df['company'] = df['company'].apply(lambda x: clean_company_name(str(x)) if pd.notna(x) else 'No Company Found')
    
#     # Clean location column
#     df['location'] = df['location'].apply(lambda x: clean_location(str(x)) if pd.notna(x) else 'No Location Found')
    
#     # Clean salary column
#     df['salary'] = df['salary'].apply(lambda x: clean_salary(str(x)) if pd.notna(x) else 'Salary Not Provided')
    
#     # Clean URLs
#     df['apply_url'] = df['apply_url'].apply(lambda x: clean_url(str(x)) if pd.notna(x) else '')
    
#     return df

# def clean_job_title(title):
#     """Clean job title text"""
#     if not title or title == 'nan':
#         return 'No Title Found'
    
#     # Remove common artifacts
#     title = re.sub(r'\s*\|.*', '', title)  # Remove everything after |
#     title = re.sub(r'\s*-\s*.*Easy Apply.*', '', title, flags=re.IGNORECASE)
#     title = re.sub(r'\s*Easy Apply.*', '', title, flags=re.IGNORECASE)
#     title = re.sub(r'\s*Actively recruiting.*', '', title, flags=re.IGNORECASE)
    
#     # Clean up whitespace
#     title = ' '.join(title.split())
    
#     # Capitalize properly
#     if title and not title.isupper():
#         # Only capitalize if it's not already all caps (which might be intentional)
#         words = title.split()
#         if len(words) > 0 and words[0].islower():
#             title = title.title()
    
#     return title.strip() if title.strip() else 'No Title Found'

# def clean_company_name(company):
#     """Clean company name text"""
#     if not company or company == 'nan' or company == 'No Company Found':
#         return 'No Company Found'
    
#     # Remove job title artifacts that got mixed in
#     company = re.sub(r'entry level software developer|frontend developer|web developer|freelance', '', company, flags=re.IGNORECASE)
    
#     # Remove common artifacts
#     company = re.sub(r'\s*Easy Apply.*', '', company, flags=re.IGNORECASE)
#     company = re.sub(r'\s*Actively recruiting.*', '', company, flags=re.IGNORECASE)
#     company = re.sub(r'\s*See jobs.*', '', company, flags=re.IGNORECASE)
#     company = re.sub(r'\s*Other jobs.*', '', company, flags=re.IGNORECASE)
    
#     # Clean up whitespace and length
#     company = ' '.join(company.split())
    
#     # If too long, likely contains other text - try to extract just company name
#     if len(company) > 50:
#         # Look for company name patterns at the beginning
#         words = company.split()
#         if len(words) > 0:
#             # Take first few words that look like a company name
#             clean_words = []
#             for word in words[:4]:  # Max 4 words for company name
#                 if any(skip in word.lower() for skip in ['apply', 'recruiting', 'jobs', 'other']):
#                     break
#                 clean_words.append(word)
#             if clean_words:
#                 company = ' '.join(clean_words)
    
#     company = company.strip()
    
#     # Final validation
#     if not company or len(company) < 2 or is_generic_text(company):
#         return 'No Company Found'
    
#     return company

# def clean_location(location):
#     """Clean location text"""
#     if not location or location == 'nan' or location == 'No Location Found':
#         return 'No Location Found'
    
#     # Remove job title artifacts
#     location = re.sub(r'entry level software developer|frontend developer|web developer', '', location, flags=re.IGNORECASE)
    
#     # Remove common artifacts
#     location = re.sub(r'\s*Easy Apply.*', '', location, flags=re.IGNORECASE)
#     location = re.sub(r'\s*Actively recruiting.*', '', location, flags=re.IGNORECASE)
#     location = re.sub(r'.*Other jobs you might be interested in.*', '', location, flags=re.IGNORECASE)
    
#     # Extract location patterns
#     location_patterns = [
#         r'([A-Z][a-zA-Z\s]+,\s*[A-Z]{2})',  # City, ST
#         r'([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)',  # City, State/Country
#         r'(Remote)',  # Remote work
#         r'([A-Z][a-zA-Z\s]+ Area)',  # Metro Area
#     ]
    
#     for pattern in location_patterns:
#         matches = re.findall(pattern, location)
#         if matches:
#             clean_location = matches[0] if isinstance(matches[0], str) else matches[0][0] if matches[0] else ""
#             if clean_location and len(clean_location.strip()) > 2:
#                 return clean_location.strip()
    
#     # Clean up and validate
#     location = ' '.join(location.split())
#     location = location.strip()
    
#     if not location or len(location) < 2 or is_generic_text(location):
#         return 'No Location Found'
    
#     # If still too long, probably has other text mixed in
#     if len(location) > 40:
#         return 'No Location Found'
    
#     return location

# def clean_salary(salary):
#     """Clean salary text"""
#     if not salary or salary == 'nan' or salary == 'Salary Not Provided':
#         return 'Salary Not Provided'
    
#     # Look for salary patterns
#     salary_patterns = [
#         r'\$\d{2,3}(?:,\d{3})*(?:\s*-\s*\$\d{2,3}(?:,\d{3})*)?(?:\s*(?:per\s*year|annually|/year|/yr))?',
#         r'\$\d{2,3}(?:,\d{3})*(?:\s*-\s*\$\d{2,3}(?:,\d{3})*)?(?:\s*(?:per\s*hour|/hour|/hr))?',
#         r'\d{2,3}(?:,\d{3})*(?:\s*-\s*\d{2,3}(?:,\d{3})*)?k(?:\s*(?:per\s*year|annually|/year))?'
#     ]
    
#     for pattern in salary_patterns:
#         matches = re.findall(pattern, salary, re.IGNORECASE)
#         if matches:
#             return matches[0].strip()
    
#     # If it's just a number (like $83), might be hourly
#     if salary.strip().startswith('$') and salary.strip()[1:].isdigit():
#         return salary.strip()
    
#     return 'Salary Not Provided'

# # Run the extraction process
# if __name__ == "__main__":
#     print("Starting LinkedIn job email extraction...")
#     jobs = fetch_linkedin_job_emails()
    
#     if jobs:
#         save_jobs_to_csv(jobs)
        
#         # Print first few jobs as preview
#         print(f"\nFirst 3 jobs found:")
#         for i, job in enumerate(jobs[:3]):
#             print(f"{i+1}. {job['title']} at {job['company']} - {job['location']}")
#             print(f"   URL: {job['apply_url'][:80]}...")
#             print()
#     else:
#         print("No jobs were extracted. Check your email search criteria and HTML parsing logic.")






import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re

global total_jobs

# Define tech job keywords and titles
TECH_KEYWORDS = [
    'software engineer', 'frontend developer', 'backend developer', 'full stack developer',
    'web developer', 'mobile developer', 'ios developer', 'android developer',
    'react developer', 'angular developer', 'vue developer', 'javascript developer',
    'python developer', 'java developer', 'c# developer', '.net developer',
    'php developer', 'ruby developer', 'golang developer', 'scala developer',
    'devops engineer', 'cloud engineer', 'aws engineer', 'azure engineer',
    'data engineer', 'data scientist', 'machine learning engineer', 'ai engineer',
    'qa engineer', 'test engineer', 'automation engineer', 'site reliability engineer',
    'security engineer', 'cybersecurity', 'ui/ux designer', 'product manager',
    'technical lead', 'engineering manager', 'architect', 'systems engineer',
    'database administrator', 'network engineer', 'blockchain developer'
]

TECH_COMPANIES_KEYWORDS = [
    'tech', 'software', 'startup', 'saas', 'platform', 'digital', 'innovation',
    'technology', 'systems', 'solutions', 'development', 'engineering'
]

def configure_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

def search_tech_jobs(driver, country, job_location, date_posted, specific_role=None):
    """
    Search for tech jobs with multiple strategies
    """
    if specific_role:
        # Search for a specific tech role
        job_query = specific_role.replace(' ', '+')
    else:
        # Search for general tech terms
        job_query = "software+engineer+OR+developer+OR+programmer+OR+tech"
    
    # Add additional tech-related search terms
    full_url = f'{country}/jobs?q={job_query}&l={job_location}&fromage={date_posted}'
    print(f"Searching: {full_url}")
    driver.get(full_url)
    
    global total_jobs
    try:
        job_count_element = driver.find_element(By.XPATH,
                                                '//div[starts-with(@class, "jobsearch-JobCountAndSortPane-jobCount")]')
        total_jobs = job_count_element.find_element(By.XPATH, './span').text
        print(f"{total_jobs} found")
    except NoSuchElementException:
        print("No job count found")
        total_jobs = "Unknown"

    driver.save_screenshot('screenshot.png')
    return full_url

def is_tech_job(job_title, company_name):
    """
    Filter function to determine if a job is tech-related
    """
    if not job_title and not company_name:
        return False
    
    # Convert to lowercase for comparison
    title_lower = job_title.lower() if job_title else ""
    company_lower = company_name.lower() if company_name else ""
    
    # Check if job title contains tech keywords
    for keyword in TECH_KEYWORDS:
        if keyword in title_lower:
            return True
    
    # Check if company name suggests tech industry
    for keyword in TECH_COMPANIES_KEYWORDS:
        if keyword in company_lower:
            return True
    
    # Additional patterns for tech jobs
    tech_patterns = [
        r'\b(sr|senior|jr|junior)?\s*(software|web|mobile|frontend|backend|fullstack|full.stack)\b',
        r'\b(react|angular|vue|node|python|java|javascript|typescript)\b',
        r'\b(engineer|developer|programmer|architect)\b',
        r'\b(devops|sre|qa|test)\b',
        r'\b(ai|ml|machine.learning|data.science)\b'
    ]
    
    combined_text = f"{title_lower} {company_lower}"
    for pattern in tech_patterns:
        if re.search(pattern, combined_text):
            return True
    
    return False

def scrape_tech_job_data(driver, country, filter_tech=True):
    """
    Enhanced scraping with tech job filtering
    """
    df = pd.DataFrame({'Link': [''], 'Job Title': [''], 'Company': [''],
                       'Employer Active': [''], 'Location': [''], 'Tech Score': ['']})
    job_count = 0
    tech_job_count = 0
    
    while True:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        boxes = soup.find_all('div', class_='job_seen_beacon')

        for i in boxes:
            # Extract job data (same as original)
            try:
                link = i.find('a', {'data-jk': True}).get('href')
                link_full = country + link
            except (AttributeError, TypeError):
                try:
                    link = i.find('a', class_=lambda x: x and 'JobTitle' in x).get('href')
                    link_full = country + link
                except (AttributeError, TypeError):
                    link_full = None

            try:
                job_title = i.find('a', class_=lambda x: x and 'JobTitle' in x).text.strip()
            except AttributeError:
                try:
                    job_title = i.find('span', id=lambda x: x and 'jobTitle-' in str(x)).text.strip()
                except AttributeError:
                    job_title = None

            try:
                company = i.find('span', {'data-testid': 'company-name'}).text.strip()
            except AttributeError:
                try:
                    company = i.find('span', class_=lambda x: x and 'company' in str(x).lower()).text.strip()
                except AttributeError:
                    company = None

            try:
                employer_active = i.find('span', class_='date').text.strip()
            except AttributeError:
                try:
                    employer_active = i.find('span', {'data-testid': 'myJobsStateDate'}).text.strip()
                except AttributeError:
                    employer_active = None

            try:
                location_element = i.find('div', {'data-testid': 'text-location'})
                if location_element:
                    try:
                        location = location_element.find('span').text.strip()
                    except AttributeError:
                        location = location_element.text.strip()
                else:
                    raise AttributeError
            except AttributeError:
                try:
                    location_element = i.find('div', class_=lambda x: x and 'location' in str(x).lower())
                    if location_element:
                        try:
                            location = location_element.find('span').text.strip()
                        except AttributeError:
                            location = location_element.text.strip()
                    else:
                        location = ''
                except AttributeError:
                    location = ''

            # Apply tech filtering
            if filter_tech:
                if is_tech_job(job_title, company):
                    tech_score = "High"
                    tech_job_count += 1
                else:
                    continue  # Skip non-tech jobs
            else:
                tech_score = "N/A"

            new_data = pd.DataFrame({'Link': [link_full], 'Job Title': [job_title],
                                     'Company': [company],
                                     'Employer Active': [employer_active],
                                     'Location': [location],
                                     'Tech Score': [tech_score]})

            df = pd.concat([df, new_data], ignore_index=True)
            job_count += 1

        print(f"Scraped {job_count} jobs ({tech_job_count} tech jobs) of {total_jobs}")

        try:
            next_page = soup.find('a', {'aria-label': 'Next Page'}).get('href')
            next_page = country + next_page
            driver.get(next_page)
        except:
            break

    return df

def search_multiple_tech_roles(driver, country, job_location, date_posted, roles_list):
    """
    Search for multiple tech roles and combine results
    """
    all_jobs = pd.DataFrame()
    
    for role in roles_list:
        print(f"\n--- Searching for {role} ---")
        search_tech_jobs(driver, country, job_location, date_posted, role)
        role_jobs = scrape_tech_job_data(driver, country, filter_tech=True)
        
        if not role_jobs.empty:
            role_jobs['Search_Term'] = role
            all_jobs = pd.concat([all_jobs, role_jobs], ignore_index=True)
        
        # Small delay between searches
        import time
        time.sleep(2)
    
    # Remove duplicates based on job link
    all_jobs = all_jobs.drop_duplicates(subset=['Link'], keep='first')
    return all_jobs

def clean_data(df):
    def posted(x):
        try:
            x = x.replace('EmployerActive', '').strip()
            return x
        except AttributeError:
            pass
    df['Employer Active'] = df['Employer Active'].apply(posted)
    return df

def save_csv(df, job_position, job_location):
    def get_user_desktop_path():
        home_dir = os.path.expanduser("~")
        desktop_path = os.path.join(home_dir, "Desktop")
        return desktop_path

    file_path = os.path.join(get_user_desktop_path(), '{}_{}'.format(job_position, job_location))
    csv_file = '{}.csv'.format(file_path)
    df.to_csv('{}.csv'.format(file_path), index=False)
    return csv_file

def send_email(df, sender_email, receiver_email, job_position, job_location, password):
    sender = sender_email
    receiver = receiver_email
    password = password
    msg = MIMEMultipart()
    msg['Subject'] = f'Tech Jobs from Indeed - {job_position} in {job_location}'
    msg['From'] = sender
    msg['To'] = ','.join(receiver)

    # Add summary in email body
    tech_jobs_count = len(df[df['Tech Score'] == 'High']) if 'Tech Score' in df.columns else len(df)
    body = f"""
    Tech Job Search Results:
    - Total jobs found: {len(df)}
    - Tech jobs: {tech_jobs_count}
    - Search location: {job_location}
    - Search term: {job_position}
    
    Please find the detailed results in the attached CSV file.
    """
    
    msg.attach(MIMEText(body, 'plain'))

    attachment_filename = generate_attachment_filename(job_position, job_location)
    csv_content = df.to_csv(index=False).encode()

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
    msg.attach(part)

    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=sender, password=password)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

def send_email_empty(sender, receiver_email, subject, body, password):
    msg = MIMEMultipart()
    password = password
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(receiver_email)
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=sender, password=password)
    s.sendmail(sender, receiver_email, msg.as_string())
    s.quit()

def generate_attachment_filename(job_title, job_location):
    filename = f"tech_{job_title.replace(' ', '_')}_{job_location.replace(' ', '_')}.csv"
    return filename

# Example usage functions
def scrape_specific_tech_role(country, job_location, date_posted, role):
    """
    Scrape for a specific tech role
    """
    driver = configure_webdriver()
    try:
        search_tech_jobs(driver, country, job_location, date_posted, role)
        df = scrape_tech_job_data(driver, country, filter_tech=True)
        df = clean_data(df)
        return df
    finally:
        driver.quit()

def scrape_all_tech_jobs(country, job_location, date_posted):
    """
    Scrape for all tech jobs using broad search terms
    """
    driver = configure_webdriver()
    try:
        search_tech_jobs(driver, country, job_location, date_posted)
        df = scrape_tech_job_data(driver, country, filter_tech=True)
        df = clean_data(df)
        return df
    finally:
        driver.quit()

def scrape_multiple_tech_roles_main(country, job_location, date_posted, roles):
    """
    Scrape for multiple specific tech roles
    """
    driver = configure_webdriver()
    try:
        df = search_multiple_tech_roles(driver, country, job_location, date_posted, roles)
        df = clean_data(df)
        return df
    finally:
        driver.quit()