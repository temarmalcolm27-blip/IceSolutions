"""
Test email sending with SendGrid
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv('.env')

def test_sendgrid_smtp():
    print("Testing SendGrid SMTP connection...\n")
    
    # Get credentials
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.sendgrid.net')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    api_key = os.getenv('SENDER_PASSWORD')
    
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Sender Email: {sender_email}")
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: Not found")
    print()
    
    if not api_key or not sender_email:
        print("❌ ERROR: Missing SENDER_EMAIL or SENDER_PASSWORD in .env file")
        return False
    
    try:
        # Create test message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Email from Ice Solutions"
        message["From"] = f"Ice Solutions <{sender_email}>"
        message["To"] = sender_email
        
        text = "This is a test email from Ice Solutions. If you receive this, email is working!"
        html = """
        <html>
            <body>
                <h2>Test Email from Ice Solutions</h2>
                <p>This is a test email. If you receive this, email is working! ✅</p>
            </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        print("Connecting to SendGrid SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Show detailed debug info
        
        print("\nStarting TLS...")
        server.starttls()
        
        print("\nLogging in...")
        # For SendGrid, username is always "apikey"
        server.login("apikey", api_key)
        
        print("\nSending email...")
        server.sendmail(sender_email, sender_email, message.as_string())
        
        print("\nClosing connection...")
        server.quit()
        
        print("\n✅ SUCCESS! Email sent successfully!")
        print(f"Check inbox: {sender_email}")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify your SendGrid API key is correct")
        print("2. Ensure sender email is verified in SendGrid")
        print("3. Check SendGrid API key has 'Mail Send' permissions")
        print("4. Try regenerating the API key in SendGrid dashboard")
        return False

if __name__ == "__main__":
    test_sendgrid_smtp()
