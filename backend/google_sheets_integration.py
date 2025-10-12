"""
Google Sheets Integration for Lead Management
Reads lead data from Google Sheets for sales agent outbound calls
"""

import gspread
from google.oauth2.service_account import Credentials
import logging
import os
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class GoogleSheetsLeadManager:
    """Manages leads from Google Sheets"""
    
    def __init__(self, credentials_json_path: Optional[str] = None):
        """
        Initialize Google Sheets client
        
        Args:
            credentials_json_path: Path to service account credentials JSON file
                                  If None, will try to get from environment variable
        """
        self.credentials_json_path = credentials_json_path or os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        self.client = None
        self.sheet = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if not self.credentials_json_path or not os.path.exists(self.credentials_json_path):
                logger.warning("Google Sheets credentials not found. Please set GOOGLE_SHEETS_CREDENTIALS_PATH")
                return False
                
            # Define the scope
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Authenticate using service account
            creds = Credentials.from_service_account_file(
                self.credentials_json_path, 
                scopes=scope
            )
            self.client = gspread.authorize(creds)
            logger.info("Successfully authenticated with Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {str(e)}")
            return False
    
    def connect_to_sheet(self, sheet_url: str, worksheet_name: str = "Sheet1"):
        """
        Connect to a specific Google Sheet
        
        Args:
            sheet_url: URL of the Google Sheet
            worksheet_name: Name of the worksheet (default: "Sheet1")
        """
        try:
            if not self.client:
                if not self.authenticate():
                    return False
            
            # Open the spreadsheet by URL
            spreadsheet = self.client.open_by_url(sheet_url)
            self.sheet = spreadsheet.worksheet(worksheet_name)
            logger.info(f"Connected to sheet: {spreadsheet.title}, worksheet: {worksheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to sheet: {str(e)}")
            return False
    
    def get_leads(self, sheet_url: str = None, worksheet_name: str = "Sheet1") -> List[Dict]:
        """
        Get all leads from the Google Sheet
        
        Expected columns: Business Name, Phone, Address, Type, Area, Status, Call Date, Call Notes, Result
        
        Args:
            sheet_url: URL of the Google Sheet (optional if already connected)
            worksheet_name: Name of the worksheet
            
        Returns:
            List of lead dictionaries
        """
        try:
            if sheet_url:
                if not self.connect_to_sheet(sheet_url, worksheet_name):
                    return []
            
            if not self.sheet:
                logger.error("Not connected to any sheet")
                return []
            
            # Get all records as list of dictionaries
            # Assumes first row is headers: Business Name, Phone, Address, Type, Area, Status, Call Date, Call Notes, Result
            records = self.sheet.get_all_records()
            
            leads = []
            for record in records:
                # Only include leads that have a phone number and are not marked as "Contacted" or "Sold"
                status = record.get('Status', '').lower()
                if record.get('Phone') and status not in ['contacted', 'sold', 'not interested']:
                    leads.append({
                        'business_name': record.get('Business Name', ''),
                        'phone': str(record.get('Phone', '')),
                        'address': record.get('Address', ''),
                        'type': record.get('Type', ''),
                        'area': record.get('Area', ''),
                        'status': record.get('Status', 'New'),
                        'call_date': record.get('Call Date', ''),
                        'call_notes': record.get('Call Notes', ''),
                        'result': record.get('Result', '')
                    })
            
            logger.info(f"Retrieved {len(leads)} leads from sheet")
            return leads
            
        except Exception as e:
            logger.error(f"Failed to get leads: {str(e)}")
            return []
    
    def update_lead_status(self, phone: str, status: str, call_date: str = "", call_notes: str = "", result: str = ""):
        """
        Update the status and call details of a lead in the sheet
        
        Args:
            phone: Phone number of the lead
            status: New status (e.g., "Contacted", "Interested", "Not Interested", "Sold")
            call_date: Date of the call
            call_notes: Notes from the call
            result: Result of the call (e.g., "Order placed", "Follow up needed", "Not interested")
        """
        try:
            if not self.sheet:
                logger.error("Not connected to any sheet")
                return False
            
            # Find the row with this phone number
            cell = self.sheet.find(phone)
            if cell:
                row_number = cell.row
                
                # Column indices (1-based): Business Name=1, Phone=2, Address=3, Type=4, Area=5, Status=6, Call Date=7, Call Notes=8, Result=9
                
                # Update status column (column 6)
                if status:
                    self.sheet.update_cell(row_number, 6, status)
                
                # Update call date column (column 7)
                if call_date:
                    self.sheet.update_cell(row_number, 7, call_date)
                
                # Update call notes column (column 8)
                if call_notes:
                    existing_notes = self.sheet.cell(row_number, 8).value or ""
                    updated_notes = f"{existing_notes}\n{call_notes}" if existing_notes else call_notes
                    self.sheet.update_cell(row_number, 8, updated_notes)
                
                # Update result column (column 9)
                if result:
                    self.sheet.update_cell(row_number, 9, result)
                
                logger.info(f"Updated lead status for {phone} to {status}")
                return True
            else:
                logger.warning(f"Phone number {phone} not found in sheet")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update lead status: {str(e)}")
            return False
    
    def add_lead(self, name: str, phone: str, email: str = "", status: str = "New", notes: str = ""):
        """
        Add a new lead to the sheet
        
        Args:
            name: Lead's name
            phone: Lead's phone number
            email: Lead's email (optional)
            status: Initial status (default: "New")
            notes: Any notes about the lead
        """
        try:
            if not self.sheet:
                logger.error("Not connected to any sheet")
                return False
            
            # Append new row
            row = [name, phone, email, status, notes]
            self.sheet.append_row(row)
            
            logger.info(f"Added new lead: {name} ({phone})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add lead: {str(e)}")
            return False


# Example usage and setup instructions
SETUP_INSTRUCTIONS = """
GOOGLE SHEETS INTEGRATION SETUP:

1. Create a Google Cloud Project:
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing one

2. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and enable it
   - Also enable "Google Drive API"

3. Create Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in service account details
   - Click "Done"

4. Create and Download Key:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Select "JSON" format
   - Download the JSON file

5. Save Credentials:
   - Save the downloaded JSON file to /app/backend/google_sheets_credentials.json
   - Add to .env file: GOOGLE_SHEETS_CREDENTIALS_PATH="/app/backend/google_sheets_credentials.json"

6. Share Your Google Sheet:
   - Open your Google Sheet with leads
   - Click "Share"
   - Add the service account email (found in the JSON file as "client_email")
   - Give it "Editor" permissions

7. Sheet Format:
   Your Google Sheet should have these columns (first row as headers):
   - Name (Lead's full name)
   - Phone (Phone number in any format)
   - Email (Email address)
   - Status (New, Contacted, Interested, Not Interested, Sold)
   - Notes (Any additional information)

8. Test the Integration:
   Use the /api/leads/sync endpoint to test fetching leads
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
