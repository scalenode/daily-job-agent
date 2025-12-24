import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]

KEYWORDS = [
    "entry level digital marketing",
    "junior digital marketing",
    "digital marketing executive"
]

def search_jobs(keyword):
    url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l="
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    for job in soup.select(".job_seen_beacon")[:5]:
        title = job.select_one("h2").text.strip()
        company = job.select_one(".companyName").text.strip()
        link = "https://www.indeed.com" + job.find("a")["href"]
        jobs.append(f"{title} — {company}\n{link}")
    return jobs

def send_email(results):
    body = "\n\n".join(results) if results else "No jobs found today."
    msg = MIMEText(body)
    msg["Subject"] = "Daily Entry-Level Digital Marketing Jobs"
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()

def main():
    all_jobs = []
    for kw in KEYWORDS:
        all_jobs.extend(search_jobs(kw))
    send_email(all_jobs)

if __name__ == "__main__":
    main()
