# 🔐 IceSolutions - Complete API & Credentials Reference

## SAVE THIS FILE SECURELY ON YOUR COMPUTER
Location: Create folder `IceSolutions_Credentials` and save this as `MASTER_CREDENTIALS.txt`

---

## 1️⃣ STRIPE (Payment Processing)

**Purpose**: Handle all online payments via credit/debit cards
**Website**: https://stripe.com
**Dashboard**: https://dashboard.stripe.com

### Credentials:
```
Test API Key (for testing): sk_test_XXXXXXXXXXXXX
Live API Key (for production): sk_live_XXXXXXXXXXXXX
```

### Current Status:
✅ Configured in backend
Location: `/app/backend/.env` → `STRIPE_API_KEY`

### Where to Find Your Keys:
1. Log into Stripe Dashboard
2. Go to: Developers → API Keys
3. Copy "Secret key" (starts with sk_test_ or sk_live_)

### What It Does:
- Processes customer payments
- Handles checkout sessions
- Manages webhooks for payment confirmation
- Stores payment sessions

---

## 2️⃣ SENDGRID (Email Service)

**Purpose**: Send order confirmation and notification emails
**Website**: https://sendgrid.com
**Dashboard**: https://app.sendgrid.com

### Credentials:
```
API Key: SG.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Sender Email: orders@icesolutions.com
Sender Name: Ice Solutions
```

### Current Status:
✅ API Key configured
⚠️ Need to verify sender email is authenticated

### Where to Find Your Key:
1. Log into SendGrid
2. Go to: Settings → API Keys
3. Create new key or use existing
4. Copy the full key (starts with SG.)

### Important Setup Steps:
1. Go to: Settings → Sender Authentication
2. Verify domain: icesolutions.com
3. Or verify single sender: orders@icesolutions.com
4. Must be verified before emails can be sent

### What It Does:
- Sends order confirmation emails
- Includes order ID and tracking link
- Sends product availability notifications

---

## 3️⃣ GOOGLE SHEETS API (Order & Lead Management)

**Purpose**: Store and track orders and leads
**Website**: https://console.cloud.google.com
**Project**: temarvoiceagent

### Service Account:
```
Email: icesolutions-agent@temarvoiceagent.iam.gserviceaccount.com
Credentials File: google_sheets_credentials.json
```

### Current Sheets:

**Leads Sheet:**
```
URL: https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit
Sheet ID: 1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8
Purpose: Chat leads and bulk order inquiries
```

**Orders Sheet (TO BE CREATED):**
```
URL: [ADD AFTER CREATING]
Sheet ID: [EXTRACT FROM URL]
Purpose: Paid orders from Stripe
```

### Headers Required for Orders Sheet:
```
Order ID | Customer Name | Phone | Email | Business Name | Quantity | Subtotal | Discount | Total | Delivery Address | Status | Order Date | Payment Session | Notes
```

### Status Options:
- Planning
- In Transit
- Delivered

### Service Account Credentials (JSON):
Located at: `/app/backend/google_sheets_credentials.json`
**COPY THIS FILE TO YOUR COMPUTER**

### What It Does:
- Stores all orders after successful payment
- Tracks order status for customer tracking
- Stores chat leads and bulk inquiries
- Allows manual status updates

---

## 4️⃣ EMERGENT LLM KEY (Chat AI)

**Purpose**: Powers Temar Malcolm chat widget
**Platform**: Emergent (emergent.sh)

### Credentials:
```
Universal Key: sk-emergent-f62468b2cCeCfD4E15
```

### Current Status:
✅ Configured and working

### What It Provides:
- Access to OpenAI GPT-4o-mini
- Access to Anthropic Claude
- Access to Google Gemini
- Single key for all LLM providers

### What It Does:
- Powers AI chat responses
- Answers customer questions
- Takes orders via chat
- Uses knowledge base for accurate info

---

## 5️⃣ TWILIO (Voice/SMS) - OPTIONAL

**Purpose**: Phone calls and SMS (currently not in active use)
**Website**: https://twilio.com
**Dashboard**: https://console.twilio.com

### Credentials:
```
Account SID: [In .env if configured]
Auth Token: [In .env if configured]
Phone Number: (876) 490-7208
```

### Current Status:
⚠️ Credentials exist but outbound calling system was removed
✅ Can be reactivated if needed later

### What It Could Do (If Reactivated):
- Send SMS order confirmations
- Automated calling for leads
- Voice-based ordering system

---

## 6️⃣ MONGODB (Database)

**Purpose**: Store application data
**Type**: Built-in database (already configured)

### Current Status:
✅ Fully configured and running

### What It Stores:
- Products
- Orders (backup)
- Quotes
- Contacts
- Chat leads
- Bulk orders
- Order counter (for Order ID generation)

### Location:
Internal to your Emergent environment
No external credentials needed

---

## 7️⃣ DOMAIN & EMAIL

### Domain:
```
Primary Domain: icesolutions.com
```

### Email Addresses:
```
Orders: orders@icesolutions.com
General: [Add if different]
Support: [Add if needed]
```

### DNS Settings:
Needed for:
- SendGrid email authentication (SPF, DKIM records)
- Domain verification
- SSL certificate

---

## 8️⃣ WEBSITE URLS

### Production:
```
Main Site: https://icesolutions.com
```

### Development:
```
Preview URL: [Your Emergent preview URL]
Local: http://localhost:3000
Backend: http://localhost:8001
```

### Important Pages:
```
Homepage: /
Products: /products
About: /about
Contact: /contact
Bulk Orders: /bulk-orders
Bulk Order Form: /bulk-order-form
Instant Quote: /quote
Checkout: /checkout
Order Confirmation: /order-confirmation
Order Tracking: /track-order
FAQ: /faq
Terms: /terms
Privacy: /privacy-policy
Refund Policy: /refund-policy
```

---

## 🔒 SECURITY NOTES

### Keep These PRIVATE:
- ❌ NEVER share API keys publicly
- ❌ NEVER commit credentials to Git/GitHub
- ❌ NEVER include in screenshots or videos
- ❌ NEVER send in plain text email

### Secure Storage:
- ✅ Save in encrypted folder on your computer
- ✅ Use password manager (LastPass, 1Password, etc.)
- ✅ Create backup copy in secure cloud storage
- ✅ Restrict access to only necessary people

### If Compromised:
1. Immediately rotate/regenerate the key
2. Update in application .env file
3. Restart backend service
4. Monitor for unauthorized usage

---

## 📋 QUICK REFERENCE: WHERE CREDENTIALS ARE USED

| Credential | Location | Purpose |
|-----------|----------|---------|
| Stripe API Key | `/app/backend/.env` → `STRIPE_API_KEY` | Payment processing |
| SendGrid API Key | `/app/backend/.env` → `SENDGRID_API_KEY` | Email sending |
| SendGrid Sender Email | `/app/backend/.env` → `SENDGRID_SENDER_EMAIL` | From address |
| Google Sheets Credentials | `/app/backend/google_sheets_credentials.json` | Sheet access |
| Google Sheet URLs | `/app/backend/.env` → `GOOGLE_SHEETS_URL` | Which sheet to use |
| Emergent LLM Key | `/app/backend/.env` → `EMERGENT_LLM_KEY` | Chat AI |
| MongoDB URL | `/app/backend/.env` → `MONGO_URL` | Database |
| Backend URL | `/app/frontend/.env` → `REACT_APP_BACKEND_URL` | API calls |

---

## 🆘 EMERGENCY CONTACTS & SUPPORT

### Stripe Support:
- Email: support@stripe.com
- Docs: https://stripe.com/docs

### SendGrid Support:
- Email: support@sendgrid.com
- Docs: https://docs.sendgrid.com

### Google Cloud Support:
- Docs: https://cloud.google.com/docs

### Emergent Platform:
- Support: [Your Emergent support contact]
- Docs: [Emergent documentation]

---

## ✅ VERIFICATION CHECKLIST

Before going live, verify:
- [ ] Stripe keys are for LIVE mode (not test)
- [ ] SendGrid sender email is verified
- [ ] Google Sheets shared with service account
- [ ] All credentials saved securely
- [ ] Backup copy created
- [ ] Team members have access only to what they need
- [ ] Email delivery tested
- [ ] Payment processing tested
- [ ] Order tracking tested

---

**Last Updated**: [ADD DATE]
**Updated By**: [YOUR NAME]
**Version**: 1.0
