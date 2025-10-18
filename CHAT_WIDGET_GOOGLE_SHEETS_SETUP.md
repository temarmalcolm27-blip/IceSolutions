# Google Sheets Setup for Chat Widget Leads

## Required Headers for Lead Management

Your Google Sheet needs these exact column headers in **Row 1**:

```
Name | Phone | Email | Business Name | Product Interest | Quantity | Inquiry | Date | Source
```

### Column Descriptions:

1. **Name**: Customer's full name
2. **Phone**: Phone number (with country code if applicable)
3. **Email**: Customer's email address
4. **Business Name**: Business name (if applicable, can be empty for individuals)
5. **Product Interest**: Which product they're interested in
   - 10lb Party Ice Bags
   - 50lb Commercial Ice Bags
   - 100lb Industrial Ice Bags
   - Bulk Order
   - Event Planning
6. **Quantity**: Number of bags/units needed
7. **Inquiry**: Their message or question
8. **Date**: When the lead was captured (auto-filled)
9. **Source**: Where the lead came from (auto-filled as "Website Chat")

## Your Google Sheet URL:
https://docs.google.com/spreadsheets/d/1wK3hgflRMOvvdnKXG2aFcqKo3ytsIz7GcvaCM_1sId8/edit

## Setup Steps:

1. **Open your Google Sheet** using the URL above

2. **Add the headers** in Row 1:
   - Copy the header row exactly as shown above
   - Paste into Row 1 of your sheet

3. **Verify permissions**:
   - Click the "Share" button
   - Confirm that `icesolutions-agent@temarvoiceagent.iam.gserviceaccount.com` has **Editor** access
   - If not listed, add it with Editor permissions

4. **Test the integration**:
   - Use the chat widget on your website
   - Fill out the lead form
   - Check if the data appears in your Google Sheet

## What Happens:

When a customer chats with Temar Malcolm and provides their information:
1. Their details are instantly saved to this Google Sheet
2. You receive a new row with all their information
3. You can follow up with them by phone, email, or both
4. The data is also saved to MongoDB for backup

## Example Row:

| Name | Phone | Email | Business Name | Product Interest | Quantity | Inquiry | Date | Source |
|------|-------|-------|---------------|------------------|----------|---------|------|--------|
| John Smith | (876) 555-1234 | john@example.com | Smith Events | 10lb Party Ice Bags | 15 | Need ice for wedding | 2025-01-14 10:30:00 | Website Chat |

## Troubleshooting:

**Leads not appearing?**
- Check service account permissions
- Verify the Google Sheet URL in backend/.env
- Check backend logs for errors

**Wrong data format?**
- Ensure headers match exactly (including spaces and capitalization)
- Don't add extra columns before these ones
- Keep headers in Row 1

## Need Help?

If you encounter any issues:
1. Check the backend logs: `tail -f /var/log/supervisor/backend.err.log`
2. Verify Google Sheets credentials are correct
3. Test the API endpoint directly: `/api/leads/chat`
