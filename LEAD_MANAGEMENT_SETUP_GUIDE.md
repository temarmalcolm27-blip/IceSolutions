# Ice Solutions Lead Management & Sales Agent Setup Guide

Welcome! This guide will walk you through setting up your complete lead generation and automated sales calling system.

## 🎯 System Overview

Your Ice Solutions platform now includes:
1. **Lead Scraper**: Generates business leads in target Kingston areas
2. **Google Sheets Integration**: Stores and manages leads
3. **Twilio AI Sales Agent** (Marcus): Automatically calls leads to sell ice
4. **Call Result Tracking**: Logs outcomes back to Google Sheets
5. **Admin Dashboard**: Monitor lead stats and performance

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ Twilio Account (SID, Auth Token, Phone Number) - Already configured!
- ✅ Google Sheets API credentials - Already configured!
- ✅ Google Sheet created - Already exists!
- ⏳ Google Apps Script webhook - Needs setup (10 minutes)

## 🚀 Quick Start Guide

### Step 1: Set Up Google Sheets Structure

1. **Open your Google Sheet**: https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit

2. **Add these exact column headers in Row 1**:
   ```
   Business Name | Phone | Address | Type | Area | Status | Call Date | Call Notes | Result
   ```

3. **Share with service account**:
   - Click "Share" button
   - Add this email: `icesolutions-agent@temarvoiceagent.iam.gserviceaccount.com`
   - Give it "Editor" permissions
   - Click "Send"

### Step 2: Deploy Google Apps Script Webhook

📖 **Follow the detailed instructions in**: `/app/GOOGLE_APPS_SCRIPT_WEBHOOK.md`

**Quick summary**:
1. Open your Google Sheet → Extensions → Apps Script
2. Copy the webhook code from the guide
3. Deploy as Web App (Anyone can access)
4. Copy the webhook URL
5. Update `.env` file if URL is different

**Test the webhook**:
```bash
curl "YOUR_WEBHOOK_URL?action=health"
```

Expected: `{"status":"ok","message":"Ice Solutions Lead Webhook is running"}`

### Step 3: Generate Your First Leads

Now that everything is set up, let's generate some leads!

**Option A: Generate Sample Leads (Quick Test)**
```bash
curl -X POST "http://localhost:8001/api/leads/scrape?count=10"
```

This will:
- Generate 10 sample businesses
- Add them to your Google Sheet
- Store them in your database
- Ready to be called!

**Option B: Generate Leads for Specific Areas**
```bash
curl -X POST "http://localhost:8001/api/leads/scrape?count=20" \
  -H "Content-Type: application/json"
```

Target specific areas:
- Washington Gardens
- Duhaney Park
- Patrick City
- Pembrook Hall

**Option C: Manual Lead Entry**
Add leads directly to your Google Sheet with these columns filled in:
- Business Name: "Sunset Bar & Grill"
- Phone: "876-555-1234"
- Address: "123 Main Road, Washington Gardens, Kingston"
- Type: "bar" or "restaurant" or "shop" etc.
- Area: "Washington Gardens"
- Status: "New"
- Leave other columns blank

### Step 4: Sync Leads from Google Sheets

After adding leads manually or via scraping, sync them to your backend:

```bash
curl "http://localhost:8001/api/leads/sync"
```

This will:
- Read all "New" leads from your Google Sheet
- Add them to your database
- Make them available for calling

### Step 5: Make Your First Sales Call!

**Call a single lead**:
```bash
curl -X POST "http://localhost:8001/api/leads/call/876-555-1234?lead_name=Sunset%20Bar"
```

What happens:
1. Marcus (AI agent) calls the number
2. Delivers the sales pitch about ice delivery
3. Updates lead status in database
4. You can log results manually

**View all your leads**:
```bash
curl "http://localhost:8001/api/leads"
```

**Check lead statistics**:
```bash
curl "http://localhost:8001/api/leads/stats"
```

### Step 6: Update Lead Results After Calls

After Marcus calls a lead, update the result:

```bash
curl -X POST "http://localhost:8001/api/leads/update/876-555-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Interested",
    "call_notes": "Owner interested in weekly delivery of 10 bags",
    "result": "Follow up next week"
  }'
```

This updates both the database AND your Google Sheet!

## 📊 Monitoring & Management

### View Lead Stats

```bash
curl "http://localhost:8001/api/leads/stats"
```

Returns:
- Total leads
- Breakdown by status (New, Contacted, Interested, Sold, Not Interested)
- Leads by area
- Leads by business type

### Check All Leads

```bash
curl "http://localhost:8001/api/leads"
```

Returns all leads in your database with full details.

### Sync Latest from Google Sheets

```bash
curl "http://localhost:8001/api/leads/sync"
```

Pulls any new leads you've added manually to the sheet.

## 🎙️ Sales Agent Script

Marcus (your AI sales agent) follows this script:

**Opening**:
> "Hello, this is Marcus from Ice Solutions. We provide party ice deliveries for businesses in the corporate area and Kingston at a reasonable price."

**Key Points**:
- Premium restaurant-quality ice
- JMD $350 per 10lb bag
- Bulk discounts: 5%, 10%, 15%
- FREE delivery in Washington Gardens
- Same-day delivery available
- Order online or cash on delivery

**Objection Handling**:
- Not interested? → Ask if they ever host events or need ice
- Price concern? → Highlight bulk discounts
- Bad timing? → Ask for callback time

**Closing**:
- Website: icesolutions.com
- Phone: (876) 490-7208
- Cash on delivery available

You can view/modify the script in: `/app/backend/sales_agent_script.py`

## 🔧 Advanced Configuration

### Customize Target Areas

Edit `/app/backend/lead_scraper.py`:
```python
TARGET_AREAS = [
    "Washington Gardens",
    "Duhaney Park",
    "Patrick City",
    "Pembrook Hall",
    "Your New Area Here"
]
```

### Customize Business Types

```python
BUSINESS_TYPES = [
    "bar",
    "restaurant",
    "shop",
    "event venue",
    "caterer",
    "hotel",
    "motel",
    "your_type_here"
]
```

### Modify Sales Script

Edit `/app/backend/sales_agent_script.py` to change:
- Opening greeting
- Pricing information
- Objection handling
- Closing statement

## 📱 Twilio Voice Configuration

Your Twilio settings (already configured):
- **Account SID**: ACc2dabec778b0c7958395bf060f535457
- **Phone Number**: (229) 600-5631
- **Auth Token**: Configured in .env

To change voice settings, edit the TwiML in `/app/backend/server.py`:
- Change `voice="man"` to `voice="woman"` or `voice="Polly.Amy"`
- Change `language="en-JM"` for different accent

## 🚨 Troubleshooting

### Issue: "No leads found"
**Solution**: 
1. Check Google Sheet has correct headers
2. Verify service account has Editor access
3. Run `/api/leads/scrape` to generate sample leads

### Issue: "Failed to sync leads"
**Solution**:
1. Check GOOGLE_SHEETS_URL in `.env` file
2. Verify credentials file exists: `/app/backend/google_sheets_credentials.json`
3. Check backend logs: `tail -f /var/log/supervisor/backend.err.log`

### Issue: "Call failed"
**Solution**:
1. Verify Twilio credentials in `.env`
2. Check phone number format (must be valid Jamaica number)
3. Ensure PUBLIC_URL in `.env` is accessible
4. Check Twilio account has credit

### Issue: "Webhook not responding"
**Solution**:
1. Redeploy Google Apps Script
2. Test with: `curl "WEBHOOK_URL?action=health"`
3. Check script has proper permissions

## 🎓 Workflow Example

Here's a complete workflow from start to finish:

```bash
# 1. Generate 20 leads
curl -X POST "http://localhost:8001/api/leads/scrape?count=20"

# 2. View lead stats
curl "http://localhost:8001/api/leads/stats"

# 3. Get all leads to call
curl "http://localhost:8001/api/leads"

# 4. Call the first lead
curl -X POST "http://localhost:8001/api/leads/call/876-400-1234?lead_name=Vibes%20Bar"

# 5. Update result after call
curl -X POST "http://localhost:8001/api/leads/update/876-400-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Interested",
    "call_notes": "Owner wants 15 bags for weekend party",
    "result": "Order placed - delivery Saturday 2PM"
  }'

# 6. Check updated stats
curl "http://localhost:8001/api/leads/stats"
```

## 🌐 Production Considerations

### For Real Lead Scraping (Not Sample Data)

The current system uses sample data generation. For production:

**Option 1: Google Places API** (Recommended)
- Most reliable and accurate
- Costs ~$17 per 1,000 queries
- Setup guide: https://developers.google.com/maps/documentation/places/web-service/overview

**Option 2: Web Scraping**
- Jamaica Yellow Pages
- Google Maps (via SerpAPI)
- Social media business pages
- Requires legal compliance and rate limiting

**Option 3: Purchase Business Lists**
- Jamaica Chamber of Commerce
- Business directories
- Verified and accurate data

**Option 4: Manual Research**
- Quality over quantity
- Personal verification
- Best for initial pilot

### Legal Considerations

- ✅ Only call businesses (not consumers)
- ✅ Respect do-not-call lists
- ✅ Provide opt-out option
- ✅ Store data securely
- ✅ Comply with Jamaica's telemarketing laws

### Scaling Up

When you're ready to scale:
1. Automate calling workflow (call all "New" leads daily)
2. Set up call scheduling (best times to reach businesses)
3. Implement follow-up system (callback reminders)
4. A/B test different scripts
5. Track conversion rates by area/type

## 📞 Support

Need help? Check:
- Backend logs: `/var/log/supervisor/backend.err.log`
- Google Sheets setup: `/app/GOOGLE_APPS_SCRIPT_WEBHOOK.md`
- Web scraping guide: View `/app/backend/lead_scraper.py`

## 🎉 You're All Set!

Your Ice Solutions lead management system is ready to go. Start by:
1. ✅ Setting up Google Sheet headers
2. ✅ Deploying the webhook
3. ✅ Generating your first batch of leads
4. ✅ Making your first sales calls

Remember: Marcus is friendly but not pushy. The goal is to educate and build relationships, not hard sell!

**More Ice = More Vibes! 🧊**
