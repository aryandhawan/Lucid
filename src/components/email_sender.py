import os
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.entity.email_config import EmailConfig


class EmailDigestSender:
    def __init__(self, config: EmailConfig):
        self.config = config
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587

        with open("email_template.html", "r", encoding="utf-8") as f:
            self.template = f.read()

    def _build_html(self, digest_papers: list[dict]) -> str:
        before_block, rest = self.template.split("<!-- PAPER_BLOCK_START -->")
        paper_block_template, after_block = rest.split("<!-- PAPER_BLOCK_END -->")

        all_paper_blocks = ""
        for paper in digest_papers:
            block = paper_block_template
            for key, value in paper.items():
                block = block.replace(f"{{{{{key}}}}}", str(value))
            all_paper_blocks += block

        before_block = before_block.replace("{{digest_date}}", date.today().strftime("%B %d, %Y"))

        return before_block + all_paper_blocks + after_block

    def send_digest(self, digest_papers: list[dict]):
        if not digest_papers:
            print("No relevant papers today — skipping email.")
            return

        final_html = self._build_html(digest_papers)
        sender_email = self.config.sender_email
        sender_password = os.getenv("EMAIL_PASSWORD")
        subject = self.config.subject_template.replace("{date}", date.today().strftime("%B %d, %Y"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            for recipient in self.config.recipient_emails:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = recipient
                msg.attach(MIMEText(final_html, "html"))
                server.sendmail(sender_email, recipient, msg.as_string())

        print(f"Digest email sent to {len(self.config.recipient_emails)} recipients with {len(digest_papers)} papers.")