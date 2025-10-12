# Google Apps Script Webhook Setup

This guide will help you set up a Google Apps Script webhook for your Ice Solutions lead management system.

## What This Does

The webhook allows:
1. **Reading leads** from your Google Sheet (for the sales agent to call)
2. **Writing call results** back to the sheet (logging outcomes)
3. **Adding new leads** programmatically from your backend

## Setup Instructions

### Step 1: Open Script Editor

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit
2. Click **Extensions** → **Apps Script**
3. Delete any existing code in the editor

### Step 2: Copy and Paste This Code

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

### Step 3: Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click the gear icon (⚙️) next to "Select type"
3. Choose **Web app**
4. Configure:
   - **Description**: "Ice Solutions Lead Webhook"
   - **Execute as**: Me (your email)
   - **Who has access**: Anyone
5. Click **Deploy**
6. **Authorize** the script (you may see a security warning - click "Advanced" → "Go to [project name]")
7. **Copy the Web App URL** - this is your webhook URL

### Step 4: Update Your Backend

The webhook URL you just copied is already in your `.env` file:
```
GOOGLE_SHEETS_WEBHOOK_URL="https://script.google.com/macros/s/AKfycbwVCylN-6Yk1_IqbowpiR_Gmpipm7_c8OWicTuT91CMNIdES_Lk6hG3YjY8oeUoQuVw/exec"
```

If it's different, update this URL in `/app/backend/.env`

### Step 5: Set Up Sheet Headers

Make sure your Google Sheet has these exact column headers in the first row:

| Business Name | Phone | Address | Type | Area | Status | Call Date | Call Notes | Result |
|---------------|-------|---------|------|------|--------|-----------|------------|--------|

## Testing the Webhook

### Test 1: Health Check
```bash
curl "YOUR_WEBHOOK_URL?action=health"
```

Expected response:
```json
{
  "status": "ok",
  "message": "Ice Solutions Lead Webhook is running",
  "timestamp": "2025-01-..."
}
```

### Test 2: Get Leads
```bash
curl "YOUR_WEBHOOK_URL?action=getLeads"
```

Expected response:
```json
{
  "success": true,
  "count": 0,
  "leads": []
}
```

### Test 3: Add a Test Lead (POST request)
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

Expected response:
```json
{
  "success": true,
  "message": "Lead added successfully"
}
```

### Test 4: Update a Lead
```bash
curl -X POST "YOUR_WEBHOOK_URL?action=updateLead" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "876-555-1234",
    "status": "Contacted",
    "call_date": "2025-01-12",
    "call_notes": "Interested in 10 bags weekly",
    "result": "Follow up needed"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Lead updated successfully"
}
```

## API Endpoints Summary

### GET Requests
- `?action=health` - Check if webhook is running
- `?action=getLeads` - Get all uncalled leads
- `?action=getLead&phone=876-555-1234` - Get specific lead

### POST Requests
- `?action=addLead` - Add a new lead (body: JSON with lead data)
- `?action=updateLead` - Update existing lead (body: JSON with phone + updates)

## Troubleshooting

**Problem**: "Script not authorized"
- **Solution**: Reauthorize the script in the deployment settings

**Problem**: "Permission denied"
- **Solution**: Make sure "Who has access" is set to "Anyone" in deployment settings

**Problem**: "Lead not found" when updating
- **Solution**: Ensure phone numbers match exactly (including formatting)

**Problem**: Empty leads returned
- **Solution**: Check that your sheet has the correct headers and data in the right columns

## Security Notes

- This webhook is publicly accessible (required for Twilio integration)
- It only reads/writes to your specific Google Sheet
- No sensitive data should be stored in the sheet
- Consider adding API key authentication for production use

## Next Steps

Once the webhook is working:
1. Test it using the curl commands above
2. Your backend can now sync leads automatically
3. The Twilio AI agent can read leads to call
4. Call results will be written back to the sheet
