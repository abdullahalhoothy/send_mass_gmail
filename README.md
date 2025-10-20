# Send Mass Gmail

A Python script that uses Selenium to automate sending mass emails through Gmail's web interface. The script opens Gmail, waits for you to log in manually, then sends the same email with attachments to multiple recipients.

## Features

- 🌐 Opens Gmail in a browser window
- 👤 Waits for manual login (no need to store credentials)
- 📧 Sends the same email to multiple recipients
- 📎 Supports file attachments
- ⏱️ Built-in delays to avoid spam filters
- 📊 Progress tracking and success/failure reporting

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- Gmail account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abdullahalhoothy/send_mass_gmail.git
cd send_mass_gmail
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Email List (`emails.txt`)

Create or edit `emails.txt` and add recipient email addresses, one per line:

```
recipient1@example.com
recipient2@example.com
recipient3@example.com
```

Lines starting with `#` are treated as comments and ignored.

### 2. Email Content (`email_content.txt`)

Create or edit `email_content.txt` with your email subject and body:

```
Subject: Your Email Subject Here

Body: 
Your email message goes here.
You can write multiple lines.

Best regards,
Your Name
```

### 3. Attachments (Optional)

Create an `attachments` directory and place any files you want to attach:

```bash
mkdir attachments
# Place your files in this directory
```

All files in the `attachments` directory will be attached to every email.

## Usage

1. Run the script:
```bash
python send_mass_gmail.py
```

2. The script will:
   - Open Gmail in a Chrome browser window
   - Prompt you to log in manually
   - Wait for you to press ENTER after logging in

3. After you press ENTER:
   - The script will automatically compose and send emails to all recipients
   - You'll see progress updates in the terminal
   - Each email will have the same subject, body, and attachments

## Example Output

```
============================================================
Gmail Mass Email Sender
============================================================
Loaded 3 email addresses
Subject: Meeting Invitation
Body preview: Dear Team,

This is to invite you to our upcomin...
Found 2 attachment(s)

Opening Gmail...

============================================================
Please log in to Gmail manually in the browser window.
After logging in and reaching your inbox, come back here
and press ENTER to continue...
============================================================

Press ENTER when you're logged in and ready to send emails: 

Proceeding with email sending...

============================================================
Starting to send 3 emails...
============================================================

[1/3] Sending email to: recipient1@example.com
  Attaching: document.pdf
  Attaching: image.png
✓ Email sent successfully to recipient1@example.com

[2/3] Sending email to: recipient2@example.com
  Attaching: document.pdf
  Attaching: image.png
✓ Email sent successfully to recipient2@example.com

[3/3] Sending email to: recipient3@example.com
  Attaching: document.pdf
  Attaching: image.png
✓ Email sent successfully to recipient3@example.com

============================================================
Sending complete!
Successfully sent: 3
Failed: 0
============================================================

All done! You can close the browser window when ready.
```

## Important Notes

⚠️ **Gmail Sending Limits**: Gmail has daily sending limits. For regular accounts, this is typically 500 emails per day. Exceeding this may result in your account being temporarily restricted.

⚠️ **Spam Prevention**: The script includes delays between emails to avoid triggering spam filters. Do not reduce these delays.

⚠️ **Browser Control**: Keep the browser window open and do not interact with it while the script is running.

⚠️ **Manual Login**: This approach requires manual login, which is more secure than storing credentials but means you need to be present to start the process.

## Troubleshooting

### Script can't find Gmail elements

Gmail's interface occasionally changes. If the script fails to find elements, the XPath selectors may need updating. Check for Gmail UI updates.

### Attachments not uploading

Ensure file paths are correct and files exist in the `attachments` directory. The script uses absolute paths.

### Browser closes immediately

The script is configured to keep the browser open. If it closes, check for errors in the console output.

## License

MIT License - feel free to use and modify as needed.

## Disclaimer

This tool is for legitimate use only. Always comply with Gmail's Terms of Service and applicable laws regarding email communication. Do not use for spam or unsolicited emails.