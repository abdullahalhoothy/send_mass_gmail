#!/usr/bin/python3

import csv
import os
import smtplib
import ssl
import time
from email.message import EmailMessage
from logging import Logger
from pathlib import Path

import jinja2
from dotenv import load_dotenv

logger = Logger(__name__)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".rtf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".webp",
    ".xls",
    ".xlsx",
    ".csv",
    ".ppt",
    ".pptx",
    ".zip",
    ".rar",
}

# Load environment variables from .env file
load_dotenv()

# Email configuration
PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def load_jinja_template(template_file: str) -> str:
    """
    Load and parse Jinja2 template file
    Template should contain both subject and HTML/content
    """
    with open(template_file, "r", encoding="utf-8") as file:
        template_content = file.read()

    return template_content


def get_attachments_from_directory(attachments_dir: str) -> list[str]:
    """
    Get all files from attachments directory
    Returns list of file paths
    """
    if not os.path.exists(attachments_dir):
        # print(
        #     f"Attachments directory '{attachments_dir}' not found. No files will be attached."
        # )
        logger.warning(
            f"Attachments directory '{attachments_dir}' not found. No files will be attached."
        )
        return []

    attachment_files = []

    for file_path in Path(attachments_dir).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            attachment_files.append(str(file_path))

    logger.info(f"Found {len(attachment_files)} attachment(s) in '{attachments_dir}'")

    ## it's not necessary, just if you want to dispaly more info.
    # attachment_files.sort()
    # print(f"Found {len(attachment_files)} attachment(s) in '{attachments_dir}':")
    # for file_path in attachment_files:
    # file_size = os.path.getsize(file_path) / 1024
    # print(f"  - {os.path.basename(file_path)} ({file_size:.1f} KB)")
    # logger.info(f"  - {os.path.basename(file_path)} ({file_size:.1f} KB)")

    return attachment_files


def add_attachment_to_message(msg: EmailMessage, attachment_path: str):
    """Add attachment to email message"""
    try:
        file_name = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as f:
            file_data = f.read()

        import mimetypes

        mime_type, _ = mimetypes.guess_type(attachment_path)

        if mime_type is None:
            mime_type = "application/octet-stream"

        main_type, sub_type = mime_type.split("/", 1)

        msg.add_attachment(
            file_data, maintype=main_type, subtype=sub_type, filename=file_name
        )

        logger.info(f"\t✓ Attached: {file_name}")
        # print(f"\t✓ Attached: {file_name}")
        return True

    except Exception as e:
        err_msg: str = f"\t✗ Failed to attach {attachment_path}: {e}"
        logger.warning(err_msg)
        # print(err_msg)
        return False


def send_bulk_emails(
    contacts_file: str = "contacts.csv",
    template_file: str = "email_content.txt",
    attachments_dir: str | None = "attachments",
) -> None:
    """
    Send bulk emails using pure Jinja2 templates or Plain Text

    Args:
        contacts_file (str): Path to CSV file with contact information
        template_file (str): Path to Jinja2 template file (.html, .txt)
        attachments_dir (str): Path to directory containing attachment files (.pdf, .csv, ...etc)
    """

    # Load template
    template_content = load_jinja_template(template_file)

    # Create Jinja2 environment
    env = jinja2.Environment(loader=jinja2.BaseLoader())

    # Compile template
    template = env.from_string(template_content)

    # Get attachments from directory
    attachment_files = None
    if attachments_dir:
        attachment_files = get_attachments_from_directory(attachments_dir)

    # Create secure SSL context
    context = ssl.create_default_context()

    # Connect to SMTP server
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # print("Successfully logged into SMTP server")
        logger.info("Successfully logged into SMTP server")

        # Read contacts and send emails
        with open(contacts_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = list(reader)

            logger.info(f"Sending emails to {len(contacts)} recipients...")
            # print(f"\nSending emails to {len(contacts)} recipients...")

            delay_interval: int = 0

            start_time = time.time()
            for row_count, row in enumerate(contacts, 1):
                # Render template with contact data
                rendered_content = template.render(**row)

                # Split into subject and body (first line is subject, rest is body)
                lines = rendered_content.strip().split("\n")
                subject = lines[0].strip()
                body_content = "\n".join(lines[1:]).strip()

                # Create email message
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = SENDER_EMAIL
                msg["To"] = row["email"]

                # Determine content type and set accordingly
                if (
                    body_content.lower().strip().startswith("<!doctype html>")
                    or "<html>" in body_content.lower()
                ):
                    # HTML email
                    msg.set_content(
                        "Please view this email in an HTML-compatible email client."
                    )
                    msg.add_alternative(body_content, subtype="html")
                else:
                    # Plain text email
                    msg.set_content(body_content)

                # Add attachments if any
                if attachment_files:
                    # print(f"\nEmail {row_count} to {row['email']}:")
                    logger.info(f"Email {row_count} to {row['email']}:")
                    for attachment_path in attachment_files:
                        add_attachment_to_message(msg, attachment_path)

                # Send email
                server.send_message(msg)
                # print(f"✅ Sent email {row_count} to {row['email']}")
                logger.info(f"✅ Sent email {row_count} to {row['email']}")
                # print(f"   Subject: {subject}")
                logger.info(f"   Subject: {subject}")
                if attachment_files:
                    # print(f"   Attachments: {len(attachment_files)} file(s)")
                    logger.info(f"   Attachments: {len(attachment_files)} file(s)")

                # add small delay between each 10 sends to avoid google to tag your email as spam
                # (0.80 * 446) + (((446 - 1) // 5) * 3) # calculate the execution average time.
                # 0.80   = average processing time per email
                # 446-1  = total emails (excluding last email)
                # 5      = delay interval
                # 3      = delay time (time sleep)
                # result: 623.8s (10.39 min) per batch (446)

                if delay_interval < 5:
                    delay_interval += 1
                else:
                    delay_interval = 0
                    time.sleep(3)

            elapsed_time = time.time() - start_time
            logger.info(f"Execution time: {elapsed_time:.6f} seconds")


if __name__ == "__main__":
    # Create sample files
    # create_sample_files()

    # Configuration
    contacts_csv = "contacts.csv"
    email_template = "email_template.txt"  # or "email_template.txt" for plain text
    attachments_directory = "attachments"

    # print(f"\n{'='*50}")
    # print("READY TO SEND EMAILS")
    # print(f"{'='*50}")
    # print(f"Contacts: {contacts_csv}")
    # print(f"Template: {email_template}")
    # print(f"Attachments: {attachments_directory}")
    # print(f"{'='*50}")

    # Send bulk emails
    send_bulk_emails(contacts_csv, email_template, attachments_directory)
