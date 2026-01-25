import os
import smtplib
from email.message import EmailMessage
from models.RagEmail import RagEmail


class EmailService:
    def send(self, email_model: RagEmail) -> None:
        email = EmailMessage()
        email["From"] = email_model.from_
        email["To"] = email_model.to
        email["Subject"] = email_model.subject
        email["Reply-To"] = email_model.sender
        email["Bcc"] = email_model.copy_to
        email.set_content(f"{email_model.message}")
        if email_model.html_message:
            email.add_alternative(email_model.html_message, subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            email_password: str = os.getenv("EMAIL_PASSWORD")
            smtp.login(email_model.sender, email_password)
            smtp.send_message(email)
