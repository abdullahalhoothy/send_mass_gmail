"""
Mass Gmail Sender using Selenium
This script opens Gmail, waits for manual login, then sends emails to a list of recipients.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class GmailMassSender:
    def __init__(self, emails_file='emails.txt', content_file='email_content.txt', attachments_dir='attachments'):
        """
        Initialize the Gmail Mass Sender.
        
        Args:
            emails_file: Path to file containing email addresses (one per line)
            content_file: Path to file containing email subject and body
            attachments_dir: Directory containing files to attach
        """
        self.emails_file = emails_file
        self.content_file = content_file
        self.attachments_dir = attachments_dir
        self.driver = None
        self.email_list = []
        self.subject = ""
        self.body = ""
        self.attachments = []
        
    def setup_driver(self):
        """Setup Firefox WebDriver with appropriate options."""
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager
        
        options = webdriver.FirefoxOptions()
        # Keep browser open after script ends (optional)
        options.set_preference("detach", True)
        
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        
    def load_email_list(self):
        """Load email addresses from file."""
        if not os.path.exists(self.emails_file):
            print(f"Warning: {self.emails_file} not found. Please create it with email addresses.")
            return False
            
        with open(self.emails_file, 'r') as f:
            self.email_list = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            
        if not self.email_list:
            print(f"No email addresses found in {self.emails_file}")
            return False
            
        print(f"Loaded {len(self.email_list)} email addresses")
        return True
        
    def load_email_content(self):
        """Load email subject and body from file."""
        if not os.path.exists(self.content_file):
            print(f"Warning: {self.content_file} not found. Using default content.")
            self.subject = "Default Subject"
            self.body = "Default email body"
            return True
            
        with open(self.content_file, 'r') as f:
            content = f.read()
            
        # Parse subject and body
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('Subject:'):
                self.subject = line.replace('Subject:', '').strip()
            elif line.startswith('Body:'):
                self.body = '\n'.join(lines[i+1:]).strip()
                break
                
        print(f"Subject: {self.subject}")
        print(f"Body preview: {self.body[:50]}...")
        return True
        
    def load_attachments(self):
        """Load list of attachments from directory."""
        if os.path.exists(self.attachments_dir) and os.path.isdir(self.attachments_dir):
            self.attachments = [
                os.path.abspath(os.path.join(self.attachments_dir, f))
                for f in os.listdir(self.attachments_dir)
                if os.path.isfile(os.path.join(self.attachments_dir, f))
            ]
            print(f"Found {len(self.attachments)} attachment(s)")
        else:
            print(f"No attachments directory found at {self.attachments_dir}")
            self.attachments = []
        return True
        
    def open_gmail(self):
        """Open Gmail and wait for manual login."""
        print("\nOpening Gmail...")
        self.driver.get("https://mail.google.com")
        
        print("\n" + "="*60)
        print("Please log in to Gmail manually in the browser window.")
        print("After logging in and reaching your inbox, come back here")
        print("and press ENTER to continue...")
        print("="*60 + "\n")
        
        input("Press ENTER when you're logged in and ready to send emails: ")
        
        # Wait a moment for the page to settle
        time.sleep(2)
        print("\nProceeding with email sending...")
        
    def compose_email(self, recipient):
        """
        Compose and send an email to a single recipient.
        
        Args:
            recipient: Email address of the recipient
        """
        try:
            print(f"\nSending email to: {recipient}")
            
            # Click compose button
            compose_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'T-I') and contains(text(), 'Compose')]"))
            )
            compose_button.click()
            time.sleep(2)
            
            # Fill in recipient
            to_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@name='to']"))
            )
            to_field.send_keys(recipient)
            time.sleep(1)
            
            # Fill in subject
            subject_field = self.driver.find_element(By.XPATH, "//input[@name='subjectbox']")
            subject_field.send_keys(self.subject)
            time.sleep(1)
            
            # Fill in body
            body_field = self.driver.find_element(By.XPATH, "//div[@aria-label='Message Body']")
            body_field.send_keys(self.body)
            time.sleep(1)
            
            # Attach files if any
            if self.attachments:
                for attachment in self.attachments:
                    try:
                        print(f"  Attaching: {os.path.basename(attachment)}")
                        attach_button = self.driver.find_element(By.XPATH, "//input[@type='file' and @name='Filedata']")
                        attach_button.send_keys(attachment)
                        time.sleep(2)  # Wait for upload
                    except Exception as e:
                        print(f"  Warning: Could not attach {attachment}: {e}")
            
            # Send email
            send_button = self.driver.find_element(By.XPATH, "//div[@aria-label='Send ‪(Ctrl-Enter)‬']")
            send_button.click()
            
            print(f"✓ Email sent successfully to {recipient}")
            time.sleep(3)  # Wait between emails to avoid triggering spam filters
            
            return True
            
        except TimeoutException:
            print(f"✗ Timeout while sending to {recipient}")
            return False
        except NoSuchElementException as e:
            print(f"✗ Could not find element while sending to {recipient}: {e}")
            return False
        except Exception as e:
            print(f"✗ Error sending to {recipient}: {e}")
            return False
            
    def send_all_emails(self):
        """Send emails to all recipients in the list."""
        if not self.email_list:
            print("No emails to send!")
            return
            
        print(f"\n{'='*60}")
        print(f"Starting to send {len(self.email_list)} emails...")
        print(f"{'='*60}\n")
        
        success_count = 0
        failed_count = 0
        
        for i, email in enumerate(self.email_list, 1):
            print(f"\n[{i}/{len(self.email_list)}]", end=" ")
            if self.compose_email(email):
                success_count += 1
            else:
                failed_count += 1
                
        print(f"\n{'='*60}")
        print(f"Sending complete!")
        print(f"Successfully sent: {success_count}")
        print(f"Failed: {failed_count}")
        print(f"{'='*60}\n")
        
    def run(self):
        """Main execution method."""
        try:
            # Load configuration
            if not self.load_email_list():
                return
            self.load_email_content()
            self.load_attachments()
            
            # Setup browser
            self.setup_driver()
            
            # Open Gmail and wait for login
            self.open_gmail()
            
            # Send emails
            self.send_all_emails()
            
            print("\nAll done! You can close the browser window when ready.")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            # Optionally close the driver (commented out to let user review)
            # if self.driver:
            #     self.driver.quit()
            pass


def main():
    """Main entry point."""
    print("="*60)
    print("Gmail Mass Email Sender")
    print("="*60)
    
    sender = GmailMassSender()
    sender.run()


if __name__ == "__main__":
    main()
