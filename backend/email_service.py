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
    sender_email = os.getenv('SENDER_EMAIL', 'temarmalcolm27@gmail.com')
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
                    📞 (876) 490-7208 | 📧 icesolutions.mybusiness@gmail.com</p>
                    
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
        (876) 490-7208 | icesolutions.mybusiness@gmail.com
        
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
            # For Gmail, use email as username. For SendGrid, use "apikey"
            username = sender_email if "gmail" in smtp_server else "apikey"
            server.login(username, sender_password)
            server.sendmail(sender_email, customer_email, message.as_string())
        
        logger.info(f"Confirmation email sent successfully to {customer_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {customer_email}: {str(e)}")
        return False



def send_order_confirmation_email(
    customer_email: str,
    customer_name: str,
    order_id: str,
    quantity: int,
    subtotal: float,
    discount: float,
    total: float,
    delivery_address: str,
    tracking_url: str
):
    """
    Send order confirmation email to customer after successful payment
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's name
        order_id: Unique order ID
        quantity: Number of bags ordered
        subtotal: Subtotal before discount
        discount: Discount amount
        total: Total amount paid
        delivery_address: Delivery address
        tracking_url: URL to track the order
    """
    
    # Email configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.sendgrid.net')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL', 'temarmalcolm27@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    # If no email credentials configured, log and return
    if not sender_password:
        logger.warning("Email credentials not configured. Skipping order confirmation email.")
        logger.info(f"Would have sent order confirmation to {customer_email} for Order #{order_id}")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Order Confirmed! #{order_id} - Ice Solutions"
        message["From"] = f"Ice Solutions <{sender_email}>"
        message["To"] = customer_email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9fafb; }}
                .header {{ background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .order-box {{ background: #ecfeff; border: 2px solid #06b6d4; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .order-details {{ margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
                .detail-row.total {{ font-weight: bold; font-size: 18px; border-top: 2px solid #06b6d4; border-bottom: none; padding-top: 15px; }}
                .button {{ display: inline-block; background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 14px; color: #6b7280; }}
                .status-box {{ background: #dcfce7; border: 2px solid #16a34a; border-radius: 8px; padding: 15px; margin: 20px 0; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Order Confirmed!</h1>
                    <p style="margin: 0; font-size: 24px; font-weight: bold;">Order #{order_id}</p>
                    <p style="margin: 10px 0 0 0; font-size: 16px;">Thank you for choosing Ice Solutions!</p>
                </div>
                
                <div class="content">
                    <p style="font-size: 18px;"><strong>Hi {customer_name},</strong></p>
                    
                    <p>Your payment has been successfully processed and your ice order is confirmed! We're getting your order ready for delivery.</p>
                    
                    <div class="order-box">
                        <h2 style="margin-top: 0; color: #0e7490;">📦 Order Summary</h2>
                        <div class="order-details">
                            <div class="detail-row">
                                <span>Order ID:</span>
                                <span><strong>#{order_id}</strong></span>
                            </div>
                            <div class="detail-row">
                                <span>10lb Ice Bags:</span>
                                <span><strong>{quantity} bags</strong></span>
                            </div>
                            <div class="detail-row">
                                <span>Subtotal:</span>
                                <span>JMD ${subtotal:.2f}</span>
                            </div>
                            {f'<div class="detail-row"><span>Discount:</span><span style="color: #16a34a;">-JMD ${discount:.2f}</span></div>' if discount > 0 else ''}
                            <div class="detail-row total">
                                <span>Total Paid:</span>
                                <span style="color: #06b6d4;">JMD ${total:.2f}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="status-box">
                        <p style="margin: 0; font-size: 16px; color: #166534;"><strong>✅ Status: Planning</strong></p>
                        <p style="margin: 5px 0 0 0; font-size: 14px; color: #15803d;">Your order is being prepared for delivery</p>
                    </div>
                    
                    <p><strong>📍 Delivery Address:</strong><br>
                    {delivery_address}</p>
                    
                    <center>
                        <a href="{tracking_url}" class="button" style="color: white;">🔍 Track Your Order</a>
                    </center>
                    
                    <h3 style="color: #0e7490;">What Happens Next?</h3>
                    <ol>
                        <li><strong>Planning:</strong> We're preparing your order (Current stage)</li>
                        <li><strong>In Transit:</strong> Your ice is on the way!</li>
                        <li><strong>Delivered:</strong> Enjoy your crystal-clear ice!</li>
                    </ol>
                    
                    <p style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0;">
                        <strong>💡 Track your order anytime:</strong><br>
                        Visit <a href="{tracking_url}" style="color: #0e7490;">{tracking_url}</a> to see real-time updates on your delivery status.
                    </p>
                    
                    <h3 style="color: #0e7490;">Need Help?</h3>
                    <p>Questions about your order? We're here to help!</p>
                    <ul>
                        <li>📞 Call: (876) 490-7208</li>
                        <li>💬 Chat: Visit our website</li>
                        <li>📧 Email: temarmalcolm27@gmail.com</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p><strong>Ice Solutions</strong><br>
                    Washington Gardens, Kingston, Jamaica<br>
                    📞 (876) 490-7208 | More Ice = More Vibes! 🧊</p>
                    
                    <p style="font-size: 12px; margin-top: 15px;">
                        Order #{ order_id} | <a href="{tracking_url}" style="color: #06b6d4;">Track Order</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        ORDER CONFIRMED! #{order_id}
        
        Hi {customer_name},
        
        Thank you for choosing Ice Solutions! Your payment has been successfully processed.
        
        ORDER SUMMARY:
        Order ID: #{order_id}
        10lb Ice Bags: {quantity} bags
        Subtotal: JMD ${subtotal:.2f}
        {f'Discount: -JMD ${discount:.2f}' if discount > 0 else ''}
        Total Paid: JMD ${total:.2f}
        
        DELIVERY ADDRESS:
        {delivery_address}
        
        STATUS: Planning
        Your order is being prepared for delivery
        
        TRACK YOUR ORDER:
        {tracking_url}
        
        WHAT HAPPENS NEXT:
        1. Planning: We're preparing your order (Current stage)
        2. In Transit: Your ice is on the way!
        3. Delivered: Enjoy your crystal-clear ice!
        
        NEED HELP?
        Call: (876) 490-7208
        Email: temarmalcolm27@gmail.com
        
        Ice Solutions
        Washington Gardens, Kingston, Jamaica
        More Ice = More Vibes! 🧊
        """
        
        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # For Gmail, use email as username. For SendGrid, use "apikey"
            username = sender_email if "gmail" in smtp_server else "apikey"
            server.login(username, sender_password)
            server.sendmail(sender_email, customer_email, message.as_string())
        
        logger.info(f"Order confirmation email sent successfully to {customer_email} for Order #{order_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email to {customer_email}: {str(e)}")
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
