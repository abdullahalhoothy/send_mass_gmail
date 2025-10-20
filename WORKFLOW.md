# Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    GMAIL MASS SENDER WORKFLOW                    │
└─────────────────────────────────────────────────────────────────┘

  START
    │
    ▼
┌─────────────────────┐
│ Load Configuration  │
│  • emails.txt       │
│  • email_content.txt│
│  • attachments/     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Setup Chrome Driver │
│  • Auto-install     │
│  • Open browser     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Open Gmail Website  │
│ (mail.google.com)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   WAIT FOR USER     │
│  Manual Login       │
│  Press ENTER ⏎      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  For Each Email in  │
│  emails.txt:        │
└──────────┬──────────┘
           │
           ├──────────────────┐
           ▼                  │
   ┌───────────────┐          │
   │ Click Compose │          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │ Fill Recipient│          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │ Fill Subject  │          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │  Fill Body    │          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │Attach Files   │          │
   │  (if any)     │          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │  Click Send   │          │
   └───────┬───────┘          │
           ▼                  │
   ┌───────────────┐          │
   │  Wait 3 sec   │          │
   └───────┬───────┘          │
           │                  │
           └──────────────────┘
           │
           ▼
┌─────────────────────┐
│  Show Summary       │
│  • Success count    │
│  • Failed count     │
└──────────┬──────────┘
           │
           ▼
         END
```

## Detailed Steps

### Phase 1: Initialization
1. **Load Email List**: Read `emails.txt`, skip comments and empty lines
2. **Load Content**: Parse `email_content.txt` for subject and body
3. **Load Attachments**: Scan `attachments/` directory for files

### Phase 2: Browser Setup
4. **Install ChromeDriver**: Auto-download using webdriver-manager
5. **Launch Browser**: Open Chrome in maximized window
6. **Navigate to Gmail**: Load https://mail.google.com

### Phase 3: Manual Login
7. **Display Instructions**: Show message in terminal
8. **Wait for Input**: Pause execution with `input()` function
9. **User Actions** (manual):
   - Enter email/password
   - Complete 2FA if enabled
   - Wait for inbox to load
   - Return to terminal
   - Press Enter

### Phase 4: Email Sending Loop
For each email address in the list:

10. **Open Compose**: Click "Compose" button
11. **Fill Form**: 
    - To: recipient email
    - Subject: from content file
    - Body: from content file
12. **Attach Files**: Upload each file from attachments folder
13. **Send**: Click send button
14. **Wait**: 3-second delay (anti-spam)
15. **Report**: Print success/failure message

### Phase 5: Completion
16. **Show Summary**: Display total success/failure counts
17. **Keep Browser Open**: Allow user to review sent emails

## Key Features

### ⏱️ Timing
- **Initial wait**: User-controlled (manual login)
- **Element waits**: 10 seconds timeout for each Gmail element
- **Between emails**: 3 seconds delay
- **Upload wait**: 2 seconds per attachment

### 🔒 Security
- No password storage
- Manual authentication
- Works with 2FA
- No API keys needed

### 📊 Progress Tracking
- Real-time console output
- Email counter (e.g., [3/10])
- Success/failure indicators (✓/✗)
- Final summary report

### 🛡️ Error Handling
- Timeout exceptions
- Missing elements
- File upload failures
- Continues on individual failures

## User Interaction Points

```
Point 1: Configuration
├─ Edit emails.txt
├─ Edit email_content.txt
└─ Add files to attachments/

Point 2: Script Launch
└─ Run: python send_mass_gmail.py

Point 3: Browser Login
├─ See Gmail login page
├─ Enter credentials
├─ Complete 2FA
└─ Wait for inbox

Point 4: Confirmation
└─ Press Enter in terminal

Point 5: Monitoring
└─ Watch progress in terminal

Point 6: Review
└─ Check sent emails in browser
```
