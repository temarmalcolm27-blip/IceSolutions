"""
Simple Email Service for IceSolutions
Sends confirmation emails to customers
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

def send_notification_confirmation_email(customer_email: str, product_name: str, product_size: str):
    """
    Send confirmation email to customer who subscribed to product notifications
    
    Args:
        customer_email: Customer's email address
        product_name: Name of the product
        product_size: Size of the product (e.g., "50 lbs", "100 lbs")
    """
    
    # Email configuration (using environment variables)
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL', 'orders@icesolutions.com')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    # If no email credentials configured, log and return
    if not sender_password:
        logger.warning("Email credentials not configured. Skipping email notification.")
        logger.info(f"Would have sent notification confirmation to {customer_email} for {product_size} {product_name}")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"You're on the list! {product_size} Ice Bags Notification"
        message["From"] = f"Ice Solutions <{sender_email}>"
        message["To"] = customer_email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 14px; color: #6b7280; }}
                .button {{ display: inline-block; background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .highlight {{ background: #ecfeff; border-left: 4px solid #06b6d4; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 You're on the List!</h1>
                    <p style="margin: 0; font-size: 18px;">More Ice = More Vibes</p>
                </div>
                
                <div class="content">
                    <h2>Thank you for your interest!</h2>
                    
                    <p>We've successfully added you to our notification list for:</p>
                    
                    <div class="highlight">
                        <strong style="font-size: 18px; color: #0e7490;">{product_size} {product_name}</strong>
                    </div>
                    
                    <p>As soon as these bags become available, you'll be the first to know! We'll send you an email with:</p>
                    
                    <ul>
                        <li>✅ Product availability confirmation</li>
                        <li>✅ Pricing information</li>
                        <li>✅ Direct link to order</li>
                        <li>✅ Any special launch offers</li>
                    </ul>
                    
                    <p><strong>What makes our ice special?</strong></p>
                    <ul>
                        <li>🧊 Crystal-clear, restaurant-quality ice</li>
                        <li>🚚 Same-day delivery (order 2 hours ahead)</li>
                        <li>💰 FREE delivery in Washington Gardens</li>
                        <li>🎯 Bulk discounts available (5%, 10%, 15%)</li>
                    </ul>
                    
                    <p>Need ice now? Our <strong>10lb bags</strong> are available for immediate order!</p>
                    
                    <center>
                        <a href="https://icesolutions.com/products" class="button" style="color: white;">View Available Products</a>
                    </center>
                </div>
                
                <div class="footer">
                    <p><strong>Ice Solutions</strong><br>
                    Washington Gardens, Kingston, Jamaica<br>
                    📞 (876) 490-7208 | 📧 orders@icesolutions.com</p>
                    
                    <p style="font-size: 12px; margin-top: 15px;">
                        You're receiving this email because you subscribed to product notifications on our website.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        You're on the List!
        
        Thank you for your interest in Ice Solutions!
        
        We've successfully added you to our notification list for:
        {product_size} {product_name}
        
        As soon as these bags become available, you'll be the first to know!
        
        What makes our ice special?
        - Crystal-clear, restaurant-quality ice
        - Same-day delivery (order 2 hours ahead)
        - FREE delivery in Washington Gardens
        - Bulk discounts available (5%, 10%, 15%)
        
        Need ice now? Our 10lb bags are available for immediate order!
        Visit: https://icesolutions.com/products
        
        Ice Solutions
        Washington Gardens, Kingston, Jamaica
        (876) 490-7208 | orders@icesolutions.com
        
        More Ice = More Vibes!
        """
        
        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, customer_email, message.as_string())
        
        logger.info(f"Confirmation email sent successfully to {customer_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {customer_email}: {str(e)}")
        return False


# Email configuration instructions
EMAIL_SETUP_INSTRUCTIONS = """
EMAIL SERVICE SETUP INSTRUCTIONS:

To enable email notifications, add these to your backend/.env file:

1. For Gmail (most common):
   SMTP_SERVER="smtp.gmail.com"
   SMTP_PORT="587"
   SENDER_EMAIL="your-email@gmail.com"
   SENDER_PASSWORD="your-app-password"
   
   Note: For Gmail, you need to use an "App Password" not your regular password:
   - Go to Google Account settings
   - Security > 2-Step Verification
   - App passwords > Generate new app password
   - Use that password in SENDER_PASSWORD

2. For SendGrid:
   SMTP_SERVER="smtp.sendgrid.net"
   SMTP_PORT="587"
   SENDER_EMAIL="apikey"
   SENDER_PASSWORD="your-sendgrid-api-key"

3. For other providers:
   Update SMTP_SERVER and SMTP_PORT accordingly
   SENDER_EMAIL should be your verified sender email
   SENDER_PASSWORD is your SMTP password or API key

If email credentials are not configured, the system will still work but no confirmation 
emails will be sent (notification will be logged instead).
"""

if __name__ == "__main__":
    print(EMAIL_SETUP_INSTRUCTIONS)
