# Troubleshooting Guide

## Common Issues and Solutions

### 1. "No module named 'selenium'" Error

**Problem**: When running the script, you get an error that selenium is not installed.

**Solution**: Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. ChromeDriver Issues

**Problem**: Error related to ChromeDriver or browser compatibility.

**Solution**: The script uses `webdriver-manager` which automatically downloads the correct ChromeDriver version. Make sure you have:
- Google Chrome installed on your system
- Internet connection for the first run (to download ChromeDriver)

### 3. Cannot Find Gmail Elements

**Problem**: Script fails with errors like "Could not find element" or timeout errors.

**Solution**: 
- Make sure you're fully logged into Gmail before pressing Enter
- Navigate to your inbox after logging in
- Gmail's interface may have changed - the XPath selectors might need updating
- Try increasing timeout values in the code (currently 10 seconds)

### 4. Emails Not Sending

**Problem**: The compose window opens but emails don't send.

**Solution**:
- Check that your email content file has the correct format
- Ensure Gmail isn't showing any warning messages
- You might have hit Gmail's sending limit (500 emails/day for regular accounts)
- Check your internet connection

### 5. Attachments Not Working

**Problem**: Attachments aren't being added to emails.

**Solution**:
- Verify files exist in the `attachments` directory
- Check file permissions (files must be readable)
- Try with smaller files first (Gmail has a 25MB attachment limit per email)
- Ensure file paths don't contain special characters

### 6. "detach" Option Not Working

**Problem**: Browser closes immediately after script completes.

**Solution**:
- This is expected behavior in some environments
- Comment out the `options.add_experimental_option("detach", True)` line if needed
- The script is designed to keep the browser open for review

### 7. Gmail Security Warnings

**Problem**: Gmail shows security warnings or blocks the login.

**Solution**:
- This is normal for automated browser access
- Use your regular Gmail account and complete any security challenges
- Enable 2FA and use App Passwords if needed (though manual login should work)
- Make sure you're not using VPN or proxy that Gmail might flag

### 8. Slow Performance

**Problem**: Script runs very slowly.

**Solution**:
- The delays between emails are intentional to avoid spam filters
- Do not reduce `time.sleep()` values as this may trigger Gmail's spam detection
- If you need to send many emails, consider breaking into smaller batches

### 9. Special Characters in Email Body

**Problem**: Special characters appear incorrectly in sent emails.

**Solution**:
- Save `email_content.txt` with UTF-8 encoding
- Use a text editor that supports UTF-8

### 10. Script Hangs During Login

**Problem**: Script waits indefinitely after opening Gmail.

**Solution**:
- The script is waiting for you to press Enter - this is normal behavior
- Make sure you complete the login process in the browser
- Navigate to your Gmail inbox
- Return to the terminal and press Enter

## Testing Tips

1. **Start Small**: Test with just 1-2 email addresses first
2. **Test Email**: Send to your own email addresses first to verify formatting
3. **Monitor**: Watch the browser window during the first few sends
4. **Check Sent**: Verify emails appear in your Gmail "Sent" folder
5. **Recipient Check**: Have a test recipient verify they received the email correctly

## Performance Optimization

- Keep email list under 500 addresses (Gmail daily limit)
- Use smaller attachments when possible
- Run during off-peak hours if sending many emails
- Don't run multiple instances simultaneously

## Getting Help

If you continue to experience issues:

1. Check the console output for specific error messages
2. Review the Gmail web interface for any warnings or errors
3. Try with a fresh Gmail account to rule out account-specific issues
4. Update to the latest version of Chrome and Python packages

## Updating XPath Selectors

If Gmail's interface changes, you may need to update the XPath selectors in `send_mass_gmail.py`. Here's where they are:

- Compose button: `//div[contains(@class, 'T-I') and contains(text(), 'Compose')]`
- To field: `//textarea[@name='to']`
- Subject field: `//input[@name='subjectbox']`
- Body field: `//div[@aria-label='Message Body']`
- Attach button: `//input[@type='file' and @name='Filedata']`
- Send button: `//div[@aria-label='Send ‪(Ctrl-Enter)‬']`

To find updated selectors:
1. Open Gmail in Chrome
2. Press F12 to open Developer Tools
3. Use the element inspector to find the new selectors
4. Update the corresponding lines in the script
