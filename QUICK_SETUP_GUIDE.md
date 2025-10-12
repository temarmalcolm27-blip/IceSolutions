# 🚀 Quick Setup Guide - Google Sheets & Webhook

## Step 1: Set Up Google Sheet Headers (2 minutes)

### Instructions:
1. **Open your Google Sheet**: 
   https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit

2. **In Row 1, add these EXACT headers** (copy and paste into cells A1-I1):

   ```
   Business Name	Phone	Address	Type	Area	Status	Call Date	Call Notes	Result
   ```

   **Or add them individually:**
   - **A1**: Business Name
   - **B1**: Phone
   - **C1**: Address
   - **D1**: Type
   - **E1**: Area
   - **F1**: Status
   - **G1**: Call Date
   - **H1**: Call Notes
   - **I1**: Result

3. **Format the headers** (optional but recommended):
   - Select Row 1
   - Make it bold
   - Add background color (light blue or gray)
   - Center align text

4. **Share with Service Account**:
   - Click the **"Share"** button (top right)
   - Add this email: `icesolutions-agent@temarvoiceagent.iam.gserviceaccount.com`
   - Set permission to **"Editor"**
   - Click **"Send"**
   - You should see a confirmation

✅ **Done!** Your sheet is now ready to receive leads.

---

## Step 2: Deploy Google Apps Script Webhook (10 minutes)

### Part A: Open Apps Script Editor

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. You'll see a new tab with the Apps Script editor
3. Delete any existing code in the editor (select all and delete)

### Part B: Copy the Webhook Code

Copy this entire code block and paste it into the Apps Script editor:

```javascript
// Ice Solutions Lead Management Webhook
// This script provides API endpoints for reading and writing lead data

function doGet(e) {
  try {
    const action = e.parameter.action;
    
    switch(action) {
      case 'getLeads':
        return getLeads();
      case 'getLead':
        return getLead(e.parameter.phone);
      case 'health':
        return ContentService.createTextOutput(JSON.stringify({
          status: 'ok',
          message: 'Ice Solutions Lead Webhook is running',
          timestamp: new Date().toISOString()
        })).setMimeType(ContentService.MimeType.JSON);
      default:
        return ContentService.createTextOutput(JSON.stringify({
          error: 'Invalid action. Use: getLeads, getLead, or health'
        })).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    const action = e.parameter.action;
    const data = JSON.parse(e.postData.contents);
    
    switch(action) {
      case 'addLead':
        return addLead(data);
      case 'updateLead':
        return updateLead(data);
      default:
        return ContentService.createTextOutput(JSON.stringify({
          error: 'Invalid action. Use: addLead or updateLead'
        })).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Get all leads from the sheet
function getLeads() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Skip header row
  const headers = data[0];
  const leads = [];
  
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    
    // Only include leads with phone numbers and not yet contacted
    const status = row[5] ? row[5].toString().toLowerCase() : 'new';
    if (row[1] && status !== 'contacted' && status !== 'sold' && status !== 'not interested') {
      leads.push({
        business_name: row[0] || '',
        phone: row[1] || '',
        address: row[2] || '',
        type: row[3] || '',
        area: row[4] || '',
        status: row[5] || 'New',
        call_date: row[6] || '',
        call_notes: row[7] || '',
        result: row[8] || ''
      });
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    count: leads.length,
    leads: leads
  })).setMimeType(ContentService.MimeType.JSON);
}

// Get a specific lead by phone number
function getLead(phone) {
  if (!phone) {
    return ContentService.createTextOutput(JSON.stringify({
      error: 'Phone number is required'
    })).setMimeType(ContentService.MimeType.JSON);
  }
  
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (row[1] && row[1].toString() === phone.toString()) {
      return ContentService.createTextOutput(JSON.stringify({
        success: true,
        lead: {
          business_name: row[0] || '',
          phone: row[1] || '',
          address: row[2] || '',
          type: row[3] || '',
          area: row[4] || '',
          status: row[5] || 'New',
          call_date: row[6] || '',
          call_notes: row[7] || '',
          result: row[8] || ''
        }
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    error: 'Lead not found'
  })).setMimeType(ContentService.MimeType.JSON);
}

// Add a new lead to the sheet
function addLead(data) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Check if lead already exists
  const existingData = sheet.getDataRange().getValues();
  for (let i = 1; i < existingData.length; i++) {
    if (existingData[i][1] === data.phone) {
      return ContentService.createTextOutput(JSON.stringify({
        error: 'Lead with this phone number already exists'
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  // Add new row
  sheet.appendRow([
    data.business_name || '',
    data.phone || '',
    data.address || '',
    data.type || '',
    data.area || '',
    data.status || 'New',
    data.call_date || '',
    data.call_notes || '',
    data.result || ''
  ]);
  
  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    message: 'Lead added successfully'
  })).setMimeType(ContentService.MimeType.JSON);
}

// Update an existing lead
function updateLead(data) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const phoneToUpdate = data.phone;
  
  if (!phoneToUpdate) {
    return ContentService.createTextOutput(JSON.stringify({
      error: 'Phone number is required to update lead'
    })).setMimeType(ContentService.MimeType.JSON);
  }
  
  const existingData = sheet.getDataRange().getValues();
  
  for (let i = 1; i < existingData.length; i++) {
    if (existingData[i][1] === phoneToUpdate) {
      const row = i + 1; // Sheet rows are 1-indexed
      
      // Update only provided fields
      if (data.status) sheet.getRange(row, 6).setValue(data.status);
      if (data.call_date) sheet.getRange(row, 7).setValue(data.call_date);
      if (data.call_notes) {
        // Append to existing notes
        const existingNotes = sheet.getRange(row, 8).getValue() || '';
        const newNotes = existingNotes ? existingNotes + '\n' + data.call_notes : data.call_notes;
        sheet.getRange(row, 8).setValue(newNotes);
      }
      if (data.result) sheet.getRange(row, 9).setValue(data.result);
      
      return ContentService.createTextOutput(JSON.stringify({
        success: true,
        message: 'Lead updated successfully'
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    error: 'Lead not found'
  })).setMimeType(ContentService.MimeType.JSON);
}
```

### Part C: Deploy as Web App

1. Click the **💾 Save** icon (or Ctrl+S / Cmd+S)
2. Give your project a name: `Ice Solutions Lead Webhook`
3. Click **Deploy** → **New deployment**
4. Click the **gear icon** (⚙️) next to "Select type"
5. Choose **"Web app"**
6. Configure the deployment:
   - **Description**: "Ice Solutions Lead Webhook v1"
   - **Execute as**: **Me** (your email)
   - **Who has access**: **Anyone**
7. Click **Deploy**
8. You may see an authorization screen:
   - Click **"Review permissions"**
   - Choose your Google account
   - Click **"Advanced"** (if you see a warning)
   - Click **"Go to Ice Solutions Lead Webhook (unsafe)"**
   - Click **"Allow"**
9. **Copy the Web App URL** that appears

   It will look like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```

10. **Important**: Keep this URL! You'll need it for testing.

✅ **Done!** Your webhook is now deployed and ready to use.

---

## Step 3: Update Backend Configuration (If URL Changed)

Only do this if your webhook URL is different from what's already in the .env file.

Current URL in .env:
```
https://script.google.com/macros/s/AKfycbwVCylN-6Yk1_IqbowpiR_Gmpipm7_c8OWicTuT91CMNIdES_Lk6hG3YjY8oeUoQuVw/exec
```

If your new URL is different:

1. Open `/app/backend/.env`
2. Replace the `GOOGLE_SHEETS_WEBHOOK_URL` value with your new URL
3. Restart the backend:
   ```bash
   sudo supervisorctl restart backend
   ```

---

## Step 4: Test the Webhook

Run these commands to test:

### Test 1: Health Check
```bash
curl "YOUR_WEBHOOK_URL?action=health"
```

**Expected response:**
```json
{
  "status": "ok",
  "message": "Ice Solutions Lead Webhook is running",
  "timestamp": "2025-01-12T..."
}
```

### Test 2: Get Leads (should be empty initially)
```bash
curl "YOUR_WEBHOOK_URL?action=getLeads"
```

**Expected response:**
```json
{
  "success": true,
  "count": 0,
  "leads": []
}
```

### Test 3: Add a Test Lead
```bash
curl -X POST "YOUR_WEBHOOK_URL?action=addLead" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Restaurant",
    "phone": "876-555-1234",
    "address": "123 Main St, Kingston",
    "type": "restaurant",
    "area": "Washington Gardens",
    "status": "New"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Lead added successfully"
}
```

**Check your Google Sheet** - you should now see the test lead in Row 2!

---

## Step 5: Test Backend Integration

Now test that your backend can communicate with Google Sheets:

### Generate Leads and Sync to Sheets
```bash
# Generate 5 leads
curl -X POST "http://localhost:8001/api/leads/scrape?count=5"

# Sync from sheets (if you added leads manually)
curl "http://localhost:8001/api/leads/sync"

# Check stats
curl "http://localhost:8001/api/leads/stats"
```

### Open the Lead Management Dashboard
Open this file in your browser:
```
file:///app/lead_management_dashboard.html
```

You should see:
- Total leads count
- Breakdown by status, area, and type
- Full leads table
- Ability to click "Call" and "Update" buttons

---

## Step 6: Make Your First Test Call (Optional)

Once everything is working, you can test calling a lead:

```bash
# Replace with an actual phone number from your leads
curl -X POST "http://localhost:8001/api/leads/call/876-555-1234?lead_name=Test%20Restaurant"
```

Marcus (AI agent) will call the number!

---

## Troubleshooting

### "Error: Permission denied"
- Redeploy the webhook
- Make sure "Who has access" is set to "Anyone"

### "No leads showing in dashboard"
- Check that leads exist: `curl "http://localhost:8001/api/leads"`
- Generate some: `curl -X POST "http://localhost:8001/api/leads/scrape?count=10"`

### "Webhook not responding"
- Test the health check endpoint first
- Make sure you authorized the script properly
- Check that the URL doesn't have any typos

### "Sheet headers not found"
- Make sure Row 1 has the exact headers listed in Step 1
- Make sure there are no extra spaces before or after header names

---

## 🎉 You're All Set!

Once all tests pass, your complete lead management system is ready!

**What you can do now:**
1. Generate leads automatically
2. View stats and manage leads in the dashboard
3. Have Marcus call leads automatically
4. Track all call results in Google Sheets

**Next Steps:**
- Set up real lead scraping (Google Places API or manual research)
- Configure call schedules
- Set up follow-up automation
- Track conversion metrics

**More Ice = More Vibes! 🧊**
