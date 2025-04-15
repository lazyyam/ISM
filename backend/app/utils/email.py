import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

async def send_reset_email(to_email: str, token: str):
    reset_link = f"http://localhost:8080/reset-password?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(f"Click the link to reset your password:\n{reset_link}")

    #print("SMTP Config:", SMTP_HOST, SMTP_PORT, SMTP_USERNAME, FROM_EMAIL)


    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )
