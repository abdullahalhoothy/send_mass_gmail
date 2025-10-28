#!/usr/bin/env python3
"""
Quick Start Example for Gmail Mass Sender

This example shows how to use the GmailMassSender class.
"""

# from send_mass_gmail_selenium import GmailMassSender
from send_mass_email_smtp import send_bulk_emails


def main():
    # Create an instance with default file paths
    # sender = GmailMassSender(
    #     emails_file="emails.txt",
    #     content_file="email_content.txt",
    #     attachments_dir="attachments",
    # )

    # Run the mass email sender
    # sender.run()

    send_bulk_emails(
        contacts_file="canada_licensed_customs_brokers.csv",
    )


if __name__ == "__main__":
    main()
