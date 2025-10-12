# SendGrid Email Setup Guide for Ice Solutions

## Step-by-Step Setup Instructions

### Step 1: Create SendGrid Account (5 minutes)

1. **Go to SendGrid Website**
   - Visit: https://signup.sendgrid.com/
   
2. **Sign Up for Free Account**
   - Click "Start for Free" or "Sign Up"
   - Enter your email address (use: orders@icesolutions.com or your business email)
   - Create a strong password
   - Fill in company information:
     * Company Name: Ice Solutions
     * Company Website: icesolutions.com (or your actual domain)
     * Company Size: 1-10 employees
     * Role: Developer/Technical
   
3. **Verify Your Email**
   - Check your inbox for verification email from SendGrid
   - Click the verification link
   - Complete the account setup

### Step 2: Get Your SendGrid API Key (3 minutes)

1. **Log in to SendGrid Dashboard**
   - Go to: https://app.sendgrid.com/
   
2. **Navigate to API Keys**
   - Click "Settings" in the left sidebar
   - Click "API Keys"
   
3. **Create New API Key**
   - Click "Create API Key" button (top right)
   - Name: "IceSolutions-Production"
   - Permissions: Select "Full Access" (or "Restricted Access" with Mail Send enabled)
   - Click "Create & View"
   
4. **IMPORTANT: Copy Your API Key**
   - **You will only see this key once!**
   - Copy the entire key (starts with "SG.")
   - Save it somewhere safe temporarily
   - Example format: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Verify Sender Email (REQUIRED - 5 minutes)

SendGrid requires you to verify the email address you'll send from.

1. **Navigate to Sender Authentication**
   - In SendGrid dashboard, go to "Settings" → "Sender Authentication"
   
2. **Single Sender Verification (Quick Method)**
   - Click "Verify a Single Sender"
   - Click "Create New Sender"
   - Fill in the form:
     * From Name: Ice Solutions
     * From Email Address: orders@icesolutions.com (or your actual email)
     * Reply To: orders@icesolutions.com
     * Company Address: Washington Gardens, Kingston, Jamaica
     * City: Kingston
     * Country: Jamaica
   - Click "Create"
   
3. **Verify the Email**
   - Check inbox of the email you entered (orders@icesolutions.com)
   - Click the verification link from SendGrid
   - Email is now verified for sending!

**Alternative: Domain Authentication (More Professional)**
- If you own icesolutions.com domain, you can authenticate the entire domain
- This is optional but recommended for better deliverability
- Requires adding DNS records to your domain

### Step 4: Configure Backend .env File

1. **Open the backend .env file**
   ```bash
   nano /app/backend/.env
   ```
   
2. **Add these lines at the end of the file:**
   ```
   # SendGrid Email Configuration
   SMTP_SERVER="smtp.sendgrid.net"
   SMTP_PORT="587"
   SENDER_EMAIL="orders@icesolutions.com"
   SENDER_PASSWORD="YOUR_SENDGRID_API_KEY_HERE"
   ```

3. **Replace YOUR_SENDGRID_API_KEY_HERE with your actual API key**
   - Paste the full API key you copied (starts with SG.)
   - Make sure SENDER_EMAIL matches the verified email from Step 3
   - Example:
   ```
   SENDER_PASSWORD="SG.abc123xyz789..."
   ```

4. **Save the file**
   - Press Ctrl+X
   - Press Y to confirm
   - Press Enter to save

### Step 5: Restart Backend Server

```bash
sudo supervisorctl restart backend
```

Wait a few seconds for the server to restart.

### Step 6: Test Email Delivery

1. **Go to your website**
   - Navigate to: http://localhost:3000/products
   
2. **Test the Notify Feature**
   - Scroll to the 50lb or 100lb ice bags
   - Click "Notify When Available"
   - Enter your email address
   - Click "Notify Me"
   
3. **Check Your Email Inbox**
   - You should receive a confirmation email within seconds!
   - Subject: "You're on the list! [size] Ice Bags Notification"
   - Check spam folder if you don't see it

### Troubleshooting

**Email Not Received?**

1. **Check Backend Logs**
   ```bash
   tail -n 50 /var/log/supervisor/backend.err.log | grep -i email
   ```
   Look for:
   - "Confirmation email sent successfully" = Working! ✅
   - "Failed to send confirmation email" = Error ❌

2. **Verify SendGrid API Key**
   - Make sure you copied the entire key (starts with SG.)
   - No extra spaces or quotes in the .env file
   - Sender email matches verified email in SendGrid

3. **Check SendGrid Dashboard**
   - Go to: https://app.sendgrid.com/
   - Click "Activity" in left sidebar
   - You'll see all sent emails and their delivery status

4. **Common Issues**
   - **"Authentication failed"**: Wrong API key or not copied correctly
   - **"Sender not verified"**: Email in SENDER_EMAIL not verified in SendGrid
   - **Email in spam**: Add "noreply@sendgrid.net" to contacts

### SendGrid Free Tier Limits

- **100 emails per day** (plenty for notification confirmations)
- Unlimited contacts
- Email validation
- Marketing campaigns
- Upgrade anytime if you need more

### Best Practices

1. **Monitor Your Sending**
   - Check SendGrid dashboard regularly
   - Watch for bounced emails or spam reports

2. **Keep API Key Secure**
   - Never commit .env file to GitHub
   - Rotate API key if compromised

3. **Professional Domain (Optional)**
   - If you own icesolutions.com, set up domain authentication
   - Improves deliverability and looks more professional
   - Uses your own domain instead of sendgrid.net

### Need Help?

If you encounter any issues:
1. Check backend logs (command above)
2. Verify all steps were completed
3. Check SendGrid Activity dashboard
4. Ensure sender email is verified

## Quick Reference

**SendGrid Dashboard:** https://app.sendgrid.com/
**API Keys:** Settings → API Keys
**Sender Verification:** Settings → Sender Authentication
**Email Activity:** Activity (see all sent emails)

---

**Once configured, customers will automatically receive beautiful confirmation emails when they subscribe to product notifications!** 📧✅
