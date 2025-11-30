import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Google API details
API_KEY = "AIzaSyDApg__0GaRJU9qi_EyN85oCkvhj6QGf_w"
CSE_ID = "a0024250f56b24f21"

# Gmail credentials
SENDER_EMAIL = "sakshisherkar99@gmail.com"
SENDER_PASSWORD = "ktvi rqzv kqls mjej"

print("Welcome to Hackveda's Digital Assistant!\n")

# Ask user inputs
query = input("Enter the keyword to search: ")
receiver_email = input("Enter recipient email: ")

# Google Search Function
def google_search(query, num_results=10):
    results = []
    for start in range(1, num_results, 10):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}&start={start}"
        response = requests.get(url).json()
        for item in response.get("items", []):
            results.append({
                "Title": item.get("title", ""),
                "Link": item.get("link", ""),
                "Snippet": item.get("snippet", "")
            })
    return results

# Run search and save results
print("\nSearching, please wait...")
data = google_search(query, num_results=20)
df = pd.DataFrame(data)
filename = "google_results.csv"
df.to_csv(filename, index=False)
print(f"✅ Google search results saved to {filename}")

# Email setup
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = receiver_email
msg['Subject'] = "Hackveda Python Project - Google Crawler Results"

body = f"Hello,\n\nPlease find attached the Google crawler results for '{query}'.\n\nRegards,\nSakshi"
msg.attach(MIMEText(body, 'plain'))

# Attach the file
with open(filename, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filename)}")
msg.attach(part)

# Send email (no exception handling)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)
server.send_message(msg)
server.quit()

print("✅ Email sent successfully!")