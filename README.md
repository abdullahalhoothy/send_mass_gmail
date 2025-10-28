# 📧 Mass Email Sender

A Python script for sending personalized bulk emails with HTML templates, attachments, and Jinja2 templating support.

## ✨ Features

- **📝 Jinja2 Templates**: Create dynamic email templates with variables and logic
- **📎 Bulk Attachments**: Automatically attach all files from a directory
- **🎨 HTML & Plain Text**: Support for both HTML and plain text emails
- **🔐 Secure Authentication**: Environment-based credentials management
- **📊 Progress Tracking**: Real-time sending progress with summaries
- **⏱️ Rate Limiting**: Configurable delays to avoid spam filters

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/abdullahalhoothy/send_mass_gmail.git
cd send_mass_gmail

# Create python env & active it
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### Create your .env file:

```txt
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

#### Gmail Setup:

1. Enable 2-Factor Authentication in your Google Account

2. Generate an App Password:

    - Go to Google Account → Security → 2-Step Verification
    - Scroll to "App passwords"
    - Generate for "Mail"
    - Use the 16-character password in .env

## 🎯 Usage

### Basic Usage:

```bash
python send_mass_gmail_smtp.py
```

## 🛠️ Technical Details

### Dependencies

- `jinja2` - Template engine
- `python-dotenv` - Environment management
- Built-in: `smtplib`, `email`, `csv`, `ssl`

### Email Limits

- **Gmail**: ~500 emails/day
- **Attachment** size: 25MB total per email
- **Rate limiting**: Built-in delays to avoid spam filters

## 🐛 Troubleshooting

### Common Issues:

1. Authentication Failed
    - Verify 2FA is enabled
    - Use App Password (not regular password)
    - Check .env file formatting

2. Attachments Not Sending
    - Verify file paths
    - Check supported file types
    - Ensure files are not too large

3. Templates Not Rendering
    - Check Jinja2 syntax
    - Verify CSV column names match template variables
    - Ensure template file encoding is UTF-8

4. Emails Going to Spam
    - Reduce sending rate (increase delays)
    - Check email content