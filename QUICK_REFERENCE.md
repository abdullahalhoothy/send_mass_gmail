# Quick Reference

## Files Overview

| File | Purpose |
|------|---------|
| `send_mass_gmail.py` | Main script - run this to send emails |
| `example.py` | Example usage (alternative entry point) |
| `emails.txt` | List of recipient email addresses (one per line) |
| `email_content.txt` | Email subject and body content |
| `attachments/` | Directory for files to attach to emails |
| `requirements.txt` | Python dependencies |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit your email list
nano emails.txt

# 3. Edit your email content
nano email_content.txt

# 4. (Optional) Add attachments
cp myfile.pdf attachments/

# 5. Run the script
python send_mass_gmail.py
```

## Configuration Files Format

### emails.txt
```
# Comments start with #
recipient1@example.com
recipient2@example.com
recipient3@example.com
```

### email_content.txt
```
Subject: Your Subject Here

Body: 
Your email message.
Multiple lines supported.
```

## Common Commands

```bash
# Run the main script
python send_mass_gmail.py

# Run the example
python example.py

# Check Python syntax
python -m py_compile send_mass_gmail.py

# Install/upgrade dependencies
pip install -r requirements.txt --upgrade
```

## Important Notes

✅ **DO:**
- Test with 1-2 emails first
- Keep browser window visible
- Wait for login before pressing Enter
- Check Gmail's "Sent" folder to verify

❌ **DON'T:**
- Close browser during sending
- Reduce sleep timers (spam protection)
- Send to more than 500 emails/day
- Use for spam or unsolicited emails

## Keyboard Shortcuts During Login

- After the script opens Gmail, you can:
  - Log in manually in the browser
  - Complete 2FA if prompted
  - Navigate to inbox
  - Return to terminal and press **Enter**

## Expected Flow

1. Script opens Chrome with Gmail
2. You see: "Please log in to Gmail manually..."
3. You log in to Gmail in the browser
4. You press Enter in the terminal
5. Script automatically sends all emails
6. You see progress for each email
7. Final summary shows success/failure count

## Gmail Limits

| Account Type | Daily Limit |
|--------------|-------------|
| Free Gmail | 500 emails/day |
| Google Workspace | 2,000 emails/day |

## File Size Limits

- Maximum attachment size: 25 MB per email
- For larger files, use Google Drive links instead

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -r requirements.txt` |
| ChromeDriver error | Update Chrome browser |
| Can't find elements | Update Gmail interface selectors |
| Emails not sending | Check Gmail sending limits |
| Attachments failing | Verify files exist and are <25MB |

For detailed troubleshooting, see `TROUBLESHOOTING.md`.
