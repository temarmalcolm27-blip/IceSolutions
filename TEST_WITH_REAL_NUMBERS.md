# 🧪 Testing the Sales Agent System with Real Numbers

## What Marcus (Your AI Sales Agent) Says

When Marcus calls a lead, he delivers this message:

### The Call Script (TwiML)

```
Hello, this is Marcus from Ice Solutions. We provide party ice deliveries 
for businesses in the corporate area and Kingston at a reasonable price.

[pause]

We provide crystal-clear, restaurant-quality ice delivered fresh to your door. 
Our 10-pound bags start at just 350 Jamaican dollars, with great bulk discounts available.

[pause]

Whether you're planning a party, running a bar, or need ice for an event, we can help.
We offer same-day delivery, and it's FREE in Washington Gardens!

[pause]

For more information or to place an order, please call us at 8 7 6, 4 9 0, 7 2 0 8.
That's 8 7 6, 4 9 0, 7 2 0 8.

[pause]

You can also order online at our website. Remember, More Ice equals More Vibes!
Thank you and have a great day!
```

### Key Points Marcus Mentions:
- ✅ Ice Solutions introduction
- ✅ Service description (party ice deliveries)
- ✅ Price: JMD $350 per 10lb bag
- ✅ Bulk discounts available
- ✅ Same-day delivery
- ✅ FREE delivery in Washington Gardens
- ✅ Contact number: (876) 490-7208
- ✅ Tagline: "More Ice = More Vibes"

---

## How to Add Real Jamaican Numbers for Testing

### Method 1: Add Leads Directly to Your Database

Create a file with your test numbers:

```bash
# Add a single test lead
curl -X POST "http://localhost:8001/api/leads/scrape?count=0"

# Then manually add to database using the dashboard
# Or use the command below
```

### Method 2: Add Leads via API (Recommended)

Create a script to add your test numbers:

```bash
#!/bin/bash

# Test Lead 1 - Your own number (for testing)
curl -X POST "http://localhost:8001/api/leads/scrape?count=1"

# After generating, you can view all leads
curl "http://localhost:8001/api/leads" | python3 -m json.tool

# Pick a lead and update with your real number
# This updates the lead in the database
```

### Method 3: Add Manually to Google Sheets (Easiest!)

1. Open your Google Sheet:
   https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit

2. Add your test numbers in Row 2, 3, 4, etc:

   | Business Name | Phone | Address | Type | Area | Status | Call Date | Call Notes | Result |
   |--------------|-------|---------|------|------|--------|-----------|------------|--------|
   | Your Test Business | 876-XXX-XXXX | Your Address | restaurant | Washington Gardens | New | | | |
   | Friend's Business | 876-YYY-YYYY | Their Address | bar | Half Way Tree | New | | | |

3. Then sync to your backend:
   ```bash
   curl "http://localhost:8001/api/leads/sync"
   ```

---

## Making Test Calls

### Step 1: View Your Leads

```bash
# Get all leads
curl "http://localhost:8001/api/leads" | python3 -m json.tool > my_leads.json

# Or just view the first few
curl "http://localhost:8001/api/leads" | python3 -m json.tool | head -50
```

### Step 2: Pick a Number and Make a Call

**Important**: Replace with an actual number from your leads!

```bash
# Example call command
curl -X POST "http://localhost:8001/api/leads/call/876-XXX-XXXX?lead_name=Your%20Business%20Name"
```

**Full Example:**
```bash
# If your lead is "Joe's Bar" with phone 876-555-1234
curl -X POST "http://localhost:8001/api/leads/call/876-555-1234?lead_name=Joe%27s%20Bar"
```

### Expected Response:
```json
{
  "status": "success",
  "message": "Call initiated to Joe's Bar",
  "call_sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "phone": "+1876555xxxx"
}
```

### Step 3: What Happens Next

1. **Twilio initiates the call** from your Twilio number: **(229) 600-5631**
2. **The phone rings** at the number you specified
3. **When answered**, Marcus's voice message plays
4. **The call lasts** approximately 45-60 seconds
5. **Call details** are logged in your database

---

## Monitoring Calls

### Check Call Status in Database

```bash
# View updated lead with call info
curl "http://localhost:8001/api/leads" | python3 -m json.tool | grep -A 20 "876-555-1234"
```

### Update Call Results

After the call, update the status:

```bash
curl -X POST "http://localhost:8001/api/leads/update/876-555-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Contacted",
    "call_notes": "Left voicemail with Marcus message",
    "result": "Awaiting callback"
  }'
```

---

## Testing Best Practices

### 1. Test with Your Own Number First ✅

**Add your own number as a test lead:**

```bash
# Manually add to Google Sheets with YOUR number
# Then sync
curl "http://localhost:8001/api/leads/sync"

# Make a call to yourself
curl -X POST "http://localhost:8001/api/leads/call/YOUR-876-NUMBER?lead_name=Test%20Call"
```

**You should receive a call from (229) 600-5631** and hear Marcus's message!

### 2. Test with Friends/Family Who Know You're Testing ✅

Get permission from a few friends or family members:
- Tell them they'll receive a call from (229) 600-5631
- It's a test of your ice delivery sales system
- The call will be about 45-60 seconds
- They can hang up anytime

### 3. Only Call Real Businesses After Testing ✅

Once you've confirmed the system works:
- Generate real business leads
- Call during business hours (9 AM - 5 PM)
- Respect do-not-call preferences
- Keep track of responses

---

## Sample Test Plan

### Test 1: Self Test (Your Number)
```bash
# Add your number to sheet, then:
curl "http://localhost:8001/api/leads/sync"
curl -X POST "http://localhost:8001/api/leads/call/876-YOUR-NUMBER?lead_name=Self%20Test"
```
✅ Verify: You receive call from (229) 600-5631 and hear Marcus

### Test 2: Friendly Test (Friend's Number - With Permission!)
```bash
# Add friend's number to sheet, then:
curl "http://localhost:8001/api/leads/sync"
curl -X POST "http://localhost:8001/api/leads/call/876-FRIEND-NUMBER?lead_name=Friend%20Test"
```
✅ Verify: Friend receives call and reports message quality

### Test 3: Update Results
```bash
curl -X POST "http://localhost:8001/api/leads/update/876-YOUR-NUMBER" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Contacted",
    "call_notes": "Test successful - message clear",
    "result": "System working perfectly"
  }'
```
✅ Verify: Check Google Sheet - should show updated status

---

## Viewing Call Logs

### Check Twilio Call Logs

1. Go to: https://console.twilio.com/
2. Login with your account
3. Navigate to: **Phone Numbers** → **Manage** → **Active Numbers**
4. Click your number: **(229) 600-5631**
5. View **Call Logs** to see:
   - Call duration
   - Call status (completed, busy, no-answer)
   - Recording (if enabled)

### Check Your Database

```bash
# View all leads with call attempts
curl "http://localhost:8001/api/leads" | python3 -m json.tool | grep -A 15 "call_attempts"
```

---

## Important Notes

### Phone Number Format

Jamaican phone numbers should be in format:
- ✅ `876-XXX-XXXX`
- ✅ `876XXXXXXX`
- ✅ `+1876XXXXXXX`

The system will automatically format them for Twilio.

### Call Costs

Check your Twilio account for:
- Outbound call rates to Jamaica
- Your account balance
- Usage alerts

### Legal Considerations

⚠️ **Important**:
- Only call businesses (not personal numbers)
- Respect business hours
- Honor do-not-call requests
- Keep records of who you've called
- Provide opt-out option

---

## Quick Reference Commands

```bash
# Add your test numbers to Google Sheet, then:

# 1. Sync leads from sheet
curl "http://localhost:8001/api/leads/sync"

# 2. View all leads
curl "http://localhost:8001/api/leads"

# 3. Make a test call (replace with real number)
curl -X POST "http://localhost:8001/api/leads/call/876-XXX-XXXX?lead_name=Business%20Name"

# 4. Update call result
curl -X POST "http://localhost:8001/api/leads/update/876-XXX-XXXX" \
  -H "Content-Type: application/json" \
  -d '{"status":"Contacted","call_notes":"Test call","result":"Success"}'

# 5. Check stats
curl "http://localhost:8001/api/leads/stats"

# 6. Open dashboard
# file:///app/lead_management_dashboard.html
```

---

## Troubleshooting

### "Call failed" or error
- Check Twilio account has credit
- Verify phone number format
- Check Twilio console for error details

### "No leads found"
- Run: `curl "http://localhost:8001/api/leads/sync"`
- Verify Google Sheet has leads
- Check service account has Editor access

### Call quality issues
- Check your internet connection
- Verify PUBLIC_URL in .env is accessible
- Test TwiML directly: `curl "http://localhost:8001/api/sales-agent/twiml"`

---

## Next Steps

1. **Add 2-3 test numbers** (your own, friends with permission)
2. **Make test calls** and verify message quality
3. **Update results** in the system
4. **Check Google Sheet** to see logged data
5. **Generate real leads** when ready
6. **Start calling businesses** during appropriate hours

🎉 **Your Marcus AI sales agent is ready to start calling! More Ice = More Vibes!**
