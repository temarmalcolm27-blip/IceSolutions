from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import json
import asyncio
from urllib.parse import quote, unquote
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Connect
from twilio.request_validator import RequestValidator
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
from google_sheets_integration import GoogleSheetsLeadManager
from sales_agent_script import SALES_AGENT_SCRIPT, SALES_FAQ, calculate_ice_recommendation, calculate_price


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
request_validator = RequestValidator(TWILIO_AUTH_TOKEN)

# Stripe configuration
STRIPE_API_KEY = os.environ['STRIPE_API_KEY']

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# IceSolutions Models
class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    weight: str
    inStock: bool = True
    comingSoon: bool = False
    features: List[str] = []
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CustomerInfo(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class EventDetails(BaseModel):
    eventDate: datetime
    eventType: str
    guestCount: int
    iceAmount: int
    deliveryTime: str

class QuoteCalculation(BaseModel):
    bags: int
    basePrice: float
    deliveryFee: float
    total: float
    savings: float = 0.0

class Quote(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customerInfo: CustomerInfo
    eventDetails: EventDetails
    quote: QuoteCalculation
    specialRequests: str = ""
    status: str = "pending"  # pending, contacted, confirmed, completed
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuoteCreate(BaseModel):
    customerInfo: CustomerInfo
    eventDetails: EventDetails
    specialRequests: str = ""

class Contact(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str = ""
    subject: str
    message: str
    inquiryType: str = "General Inquiry"
    status: str = "new"  # new, replied, resolved
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str = ""
    subject: str
    message: str
    inquiryType: str = "General Inquiry"

class DeliveryArea(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    area: str
    deliveryFee: float
    timeSlots: List[str] = []
    isActive: bool = True
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# AI Agent Models
class CallAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quoteId: str
    customerId: str
    callSid: Optional[str] = None
    phoneNumber: str
    status: str = "initiated"  # initiated, ringing, in_progress, completed, failed, no_answer, busy
    duration: Optional[int] = None
    conversationSummary: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ConversationMessage(BaseModel):
    speaker: str  # "customer" or "agent"
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActiveSession(BaseModel):
    sessionId: str
    quoteId: str
    customerId: str
    callSid: str
    conversationHistory: List[ConversationMessage] = []
    contextData: Dict[str, Any] = {}
    startTime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Payment Models
class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    amount: float
    currency: str = "jmd"
    payment_status: str = "pending"  # pending, completed, failed, expired
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CheckoutRequest(BaseModel):
    bags: int
    delivery_address: str
    delivery_fee: float = 0.0
    metadata: Optional[Dict[str, Any]] = {}

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    delivery_address: str
    bags: int
    delivery_fee: float
    total_amount: float
    payment_session_id: Optional[str] = None

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    customer_email: str
    customer_phone: str
    delivery_address: str
    bags: int
    price_per_bag: float = 350.00
    subtotal: float
    discount_percent: float = 0.0
    discount_amount: float = 0.0
    delivery_fee: float
    total_amount: float
    payment_status: str = "pending"
    payment_session_id: Optional[str] = None
    order_status: str = "pending"  # pending, confirmed, in_delivery, delivered, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Products API
@api_router.get("/products", response_model=List[Product])
async def get_products():
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for product in products:
        if isinstance(product.get('createdAt'), str):
            product['createdAt'] = datetime.fromisoformat(product['createdAt'])
        if isinstance(product.get('updatedAt'), str):
            product['updatedAt'] = datetime.fromisoformat(product['updatedAt'])
    
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(product.get('createdAt'), str):
        product['createdAt'] = datetime.fromisoformat(product['createdAt'])
    if isinstance(product.get('updatedAt'), str):
        product['updatedAt'] = datetime.fromisoformat(product['updatedAt'])
    
    return product

# Quotes API
@api_router.post("/quotes", response_model=Quote)
async def create_quote(quote_input: QuoteCreate, background_tasks: BackgroundTasks):
    # Calculate quote pricing
    guest_count = quote_input.eventDetails.guestCount or 0
    ice_amount = quote_input.eventDetails.iceAmount or 0
    
    # Calculate recommended bags (1 bag per 25 guests or based on ice amount)
    recommended_bags = max(1, guest_count // 25) if guest_count else max(1, ice_amount // 10)
    
    base_price = recommended_bags * 350.00  # JMD $350 per 10lb bag
    
    # Calculate delivery fee based on address
    customer_address = quote_input.customerInfo.address.lower()
    is_washington_gardens = any(area in customer_address for area in [
        'washington gardens', 'washington garden', 'wash gardens', 'wash garden'
    ])
    
    if is_washington_gardens:
        delivery_fee = 0.0  # Free delivery to Washington Gardens
    else:
        delivery_fee = 300.00  # JMD $300 for areas outside Washington Gardens
    
    # Calculate bulk discount
    savings = 0.0
    if recommended_bags >= 20:
        savings = base_price * 0.15  # 15% discount for 20+ bags
    elif recommended_bags >= 10:
        savings = base_price * 0.10  # 10% discount for 10+ bags
    elif recommended_bags >= 5:
        savings = base_price * 0.05  # 5% discount for 5+ bags
    
    total = base_price + delivery_fee - savings
    
    quote_calc = QuoteCalculation(
        bags=recommended_bags,
        basePrice=base_price,
        deliveryFee=delivery_fee,
        total=total,
        savings=savings
    )
    
    quote = Quote(
        customerInfo=quote_input.customerInfo,
        eventDetails=quote_input.eventDetails,
        quote=quote_calc,
        specialRequests=quote_input.specialRequests
    )
    
    # Convert to dict and serialize datetimes for MongoDB
    doc = quote.model_dump()
    doc['createdAt'] = doc['createdAt'].isoformat()
    doc['updatedAt'] = doc['updatedAt'].isoformat()
    doc['eventDetails']['eventDate'] = doc['eventDetails']['eventDate'].isoformat()
    
    await db.quotes.insert_one(doc)
    
    # Automatically trigger AI agent callback
    background_tasks.add_task(initiate_ai_callback, quote.id, quote.customerInfo.phone, quote.customerInfo.name)
    
    return quote

# Scheduled quotes (no immediate callback)
@api_router.post("/quotes-scheduled", response_model=Quote)
async def create_scheduled_quote(quote_input: QuoteCreate):
    # Same calculation as regular quotes but no background callback task
    guest_count = quote_input.eventDetails.guestCount or 0
    ice_amount = quote_input.eventDetails.iceAmount or 0
    
    recommended_bags = max(1, guest_count // 25) if guest_count else max(1, ice_amount // 10)
    base_price = recommended_bags * 350.00
    
    # Calculate delivery fee based on address
    customer_address = quote_input.customerInfo.address.lower()
    is_washington_gardens = any(area in customer_address for area in [
        'washington gardens', 'washington garden', 'wash gardens', 'wash garden'
    ])
    
    if is_washington_gardens:
        delivery_fee = 0.0  # Free delivery to Washington Gardens
    else:
        delivery_fee = 300.00  # JMD $300 for areas outside Washington Gardens
    
    # Calculate bulk discount
    savings = 0.0
    if recommended_bags >= 20:
        savings = base_price * 0.15  # 15% discount for 20+ bags
    elif recommended_bags >= 10:
        savings = base_price * 0.10  # 10% discount for 10+ bags
    elif recommended_bags >= 5:
        savings = base_price * 0.05  # 5% discount for 5+ bags
    
    total = base_price + delivery_fee - savings
    
    quote_calc = QuoteCalculation(
        bags=recommended_bags,
        basePrice=base_price,
        deliveryFee=delivery_fee,
        total=total,
        savings=savings
    )
    
    quote = Quote(
        customerInfo=quote_input.customerInfo,
        eventDetails=quote_input.eventDetails,
        quote=quote_calc,
        specialRequests=quote_input.specialRequests,
        status="scheduled"  # Mark as scheduled callback
    )
    
    # Store without triggering immediate callback
    doc = quote.model_dump()
    doc['createdAt'] = doc['createdAt'].isoformat()
    doc['updatedAt'] = doc['updatedAt'].isoformat()
    doc['eventDetails']['eventDate'] = doc['eventDetails']['eventDate'].isoformat()
    
    await db.quotes.insert_one(doc)
    logger.info(f"Scheduled callback quote created: {quote.id}")
    
    return quote

# No-callback quotes endpoint (for future use if needed)
@api_router.post("/quotes-no-callback", response_model=Quote)
async def create_quote_no_callback(quote_input: QuoteCreate):
    # Same as regular quotes but without background callback task
    guest_count = quote_input.eventDetails.guestCount or 0
    ice_amount = quote_input.eventDetails.iceAmount or 0
    
    recommended_bags = max(1, guest_count // 25) if guest_count else max(1, ice_amount // 10)
    base_price = recommended_bags * 350.00
    
    # Calculate delivery fee based on address
    customer_address = quote_input.customerInfo.address.lower()
    is_washington_gardens = any(area in customer_address for area in [
        'washington gardens', 'washington garden', 'wash gardens', 'wash garden'
    ])
    
    if is_washington_gardens:
        delivery_fee = 0.0
    else:
        delivery_fee = 300.00
    
    # Calculate bulk discount
    savings = 0.0
    if recommended_bags >= 5:
        savings = base_price * 0.05
    if recommended_bags >= 10:
        savings = base_price * 0.10
    
    total = base_price + delivery_fee - savings
    
    quote_calc = QuoteCalculation(
        bags=recommended_bags,
        basePrice=base_price,
        deliveryFee=delivery_fee,
        total=total,
        savings=savings
    )
    
    quote = Quote(
        customerInfo=quote_input.customerInfo,
        eventDetails=quote_input.eventDetails,
        quote=quote_calc,
        specialRequests=quote_input.specialRequests,
        status="no_callback"
    )
    
    # Store without triggering callback
    doc = quote.model_dump()
    doc['createdAt'] = doc['createdAt'].isoformat()
    doc['updatedAt'] = doc['updatedAt'].isoformat()
    doc['eventDetails']['eventDate'] = doc['eventDetails']['eventDate'].isoformat()
    
    await db.quotes.insert_one(doc)
    logger.info(f"No-callback quote created: {quote.id}")
    
    return quote

@api_router.get("/quotes/{quote_id}", response_model=Quote)
async def get_quote(quote_id: str):
    quote = await db.quotes.find_one({"id": quote_id}, {"_id": 0})
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(quote.get('createdAt'), str):
        quote['createdAt'] = datetime.fromisoformat(quote['createdAt'])
    if isinstance(quote.get('updatedAt'), str):
        quote['updatedAt'] = datetime.fromisoformat(quote['updatedAt'])
    if isinstance(quote['eventDetails'].get('eventDate'), str):
        quote['eventDetails']['eventDate'] = datetime.fromisoformat(quote['eventDetails']['eventDate'])
    
    return quote

# Contacts API
@api_router.post("/contacts", response_model=Contact)
async def create_contact(contact_input: ContactCreate):
    contact = Contact(**contact_input.model_dump())
    
    # Convert to dict and serialize datetimes for MongoDB
    doc = contact.model_dump()
    doc['createdAt'] = doc['createdAt'].isoformat()
    doc['updatedAt'] = doc['updatedAt'].isoformat()
    
    await db.contacts.insert_one(doc)
    return contact

@api_router.get("/contacts", response_model=List[Contact])
async def get_contacts():
    contacts = await db.contacts.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for contact in contacts:
        if isinstance(contact.get('createdAt'), str):
            contact['createdAt'] = datetime.fromisoformat(contact['createdAt'])
        if isinstance(contact.get('updatedAt'), str):
            contact['updatedAt'] = datetime.fromisoformat(contact['updatedAt'])
    
    return contacts

# Payment Endpoints
@api_router.post("/checkout/create-session")
async def create_checkout_session(checkout_req: CheckoutRequest, origin_url: str):
    """Create Stripe checkout session for ice order"""
    try:
        # Calculate pricing
        price_per_bag = 350.00
        bags = checkout_req.bags
        subtotal = bags * price_per_bag
        
        # Apply bulk discounts
        discount_percent = 0.0
        if bags >= 20:
            discount_percent = 0.15
        elif bags >= 10:
            discount_percent = 0.10
        elif bags >= 5:
            discount_percent = 0.05
        
        discount_amount = subtotal * discount_percent
        total_after_discount = subtotal - discount_amount
        total_amount = total_after_discount + checkout_req.delivery_fee
        
        # Initialize Stripe checkout
        webhook_url = f"{origin_url}/api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
        
        # Create checkout session request
        success_url = f"{origin_url}/order-confirmation?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{origin_url}/quote"
        
        metadata = {
            "bags": str(bags),
            "delivery_address": checkout_req.delivery_address,
            "delivery_fee": str(checkout_req.delivery_fee),
            "discount_percent": str(discount_percent),
            "discount_amount": str(discount_amount),
            **checkout_req.metadata
        }
        
        checkout_request = CheckoutSessionRequest(
            amount=total_amount,
            currency="jmd",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        
        # Create checkout session
        session = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Store payment transaction
        transaction = PaymentTransaction(
            session_id=session.session_id,
            amount=total_amount,
            currency="jmd",
            payment_status="pending",
            metadata=metadata
        )
        
        doc = transaction.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.payment_transactions.insert_one(doc)
        
        return {
            "url": session.url,
            "session_id": session.session_id
        }
        
    except Exception as e:
        logging.error(f"Error creating checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")

@api_router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str):
    """Get the status of a checkout session"""
    try:
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        
        # Get checkout status from Stripe
        status = await stripe_checkout.get_checkout_status(session_id)
        
        # Update payment transaction in database
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "payment_status": status.payment_status,
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        return status
        
    except Exception as e:
        logging.error(f"Error getting checkout status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get checkout status: {str(e)}")

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: dict):
    """Handle Stripe webhook events"""
    try:
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url="")
        
        # Process webhook
        # Note: In production, verify webhook signature
        session_id = request.get("session_id")
        payment_status = request.get("payment_status")
        
        if session_id and payment_status:
            # Update payment transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": payment_status,
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
        
        return {"status": "success"}
        
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

@api_router.post("/orders", response_model=Order)
async def create_order(order_input: OrderCreate):
    """Create an order after successful payment"""
    try:
        # Calculate pricing
        price_per_bag = 350.00
        bags = order_input.bags
        subtotal = bags * price_per_bag
        
        # Apply bulk discounts
        discount_percent = 0.0
        if bags >= 20:
            discount_percent = 0.15
        elif bags >= 10:
            discount_percent = 0.10
        elif bags >= 5:
            discount_percent = 0.05
        
        discount_amount = subtotal * discount_percent
        
        order = Order(
            customer_name=order_input.customer_name,
            customer_email=order_input.customer_email,
            customer_phone=order_input.customer_phone,
            delivery_address=order_input.delivery_address,
            bags=bags,
            subtotal=subtotal,
            discount_percent=discount_percent,
            discount_amount=discount_amount,
            delivery_fee=order_input.delivery_fee,
            total_amount=order_input.total_amount,
            payment_session_id=order_input.payment_session_id,
            payment_status="completed",
            order_status="confirmed"
        )
        
        # Convert to dict and serialize datetimes for MongoDB
        doc = order.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.orders.insert_one(doc)
        return order
        
    except Exception as e:
        logging.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order by ID"""
    order = await db.orders.find_one({"id": order_id}, {"_id": 0})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(order.get('created_at'), str):
        order['created_at'] = datetime.fromisoformat(order['created_at'])
    if isinstance(order.get('updated_at'), str):
        order['updated_at'] = datetime.fromisoformat(order['updated_at'])
    
    return order

# Lead Management Endpoints (for Sales Agent)
@api_router.get("/leads/sync")
async def sync_leads_from_sheets(sheet_url: str = None):
    """
    Sync leads from Google Sheets
    
    Query params:
        sheet_url: URL of the Google Sheet (optional, can be configured in env)
    """
    try:
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsLeadManager()
        
        # Get sheet URL from environment if not provided
        if not sheet_url:
            sheet_url = os.getenv('GOOGLE_SHEETS_URL')
            
        if not sheet_url:
            return {
                "status": "error",
                "message": "No Google Sheet URL provided. Please provide sheet_url parameter or set GOOGLE_SHEETS_URL environment variable.",
                "setup_required": True
            }
        
        # Get leads from sheet
        leads = sheets_manager.get_leads(sheet_url=sheet_url)
        
        if not leads:
            return {
                "status": "warning",
                "message": "No new leads found or unable to connect to Google Sheets",
                "leads_count": 0,
                "leads": []
            }
        
        # Store leads in database for tracking
        for lead in leads:
            # Check if lead already exists
            existing = await db.leads.find_one({"phone": lead['phone']})
            if not existing:
                lead['created_at'] = datetime.now(timezone.utc).isoformat()
                lead['last_updated'] = datetime.now(timezone.utc).isoformat()
                lead['call_attempts'] = 0
                lead['last_call_date'] = None
                await db.leads.insert_one(lead)
        
        return {
            "status": "success",
            "message": f"Successfully synced {len(leads)} leads",
            "leads_count": len(leads),
            "leads": leads
        }
        
    except Exception as e:
        logger.error(f"Error syncing leads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to sync leads: {str(e)}")

@api_router.get("/leads")
async def get_all_leads():
    """Get all leads from database"""
    try:
        leads = await db.leads.find({}, {"_id": 0}).to_list(1000)
        return {"leads": leads, "count": len(leads)}
    except Exception as e:
        logger.error(f"Error getting leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/leads/call/{phone}")
async def initiate_sales_call(phone: str, lead_name: str = "customer"):
    """
    Initiate an outbound sales call to a lead
    
    Args:
        phone: Phone number to call
        lead_name: Name of the lead
    """
    try:
        # Format phone number for Twilio (add +1 if not present)
        if not phone.startswith('+'):
            # Assuming Jamaican numbers, add +1876
            phone_formatted = f"+1876{phone.replace('-', '').replace(' ', '')[-7:]}"
        else:
            phone_formatted = phone
        
        # Create TwiML for sales call
        public_url = os.environ.get('PUBLIC_URL', 'https://your-domain.ngrok-free.app')
        twiml_url = f"{public_url}/api/sales-agent/twiml?lead_name={urllib.parse.quote(lead_name)}"
        
        # Make the call
        call = twilio_client.calls.create(
            to=phone_formatted,
            from_=TWILIO_PHONE_NUMBER,
            url=twiml_url,
            method='GET'
        )
        
        # Update lead in database
        await db.leads.update_one(
            {"phone": phone},
            {
                "$inc": {"call_attempts": 1},
                "$set": {
                    "last_call_date": datetime.now(timezone.utc).isoformat(),
                    "last_call_sid": call.sid
                }
            }
        )
        
        logger.info(f"Initiated sales call to {phone} (SID: {call.sid})")
        
        return {
            "status": "success",
            "message": f"Call initiated to {lead_name}",
            "call_sid": call.sid,
            "phone": phone_formatted
        }
        
    except Exception as e:
        logger.error(f"Error initiating sales call: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")

@api_router.get("/sales-agent/script")
async def get_sales_script():
    """Get the sales agent script and FAQ"""
    return {
        "script": SALES_AGENT_SCRIPT,
        "faq": SALES_FAQ
    }

@api_router.get("/sales-agent/twiml")
async def get_sales_agent_twiml(lead_name: str = "customer"):
    """Generate TwiML for sales agent call"""
    logger.info(f"Sales TwiML requested for lead: {lead_name}")
    
    # Create TwiML for sales call
    twiml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="man" language="en-JM">
        Hello {lead_name}, this is calling from Ice Solutions, Jamaica's premier ice delivery service.
    </Say>
    <Pause length="1"/>
    <Say voice="man" language="en-JM">
        We provide crystal-clear, restaurant-quality ice delivered fresh to your door. 
        Our 10-pound bags start at just 350 Jamaican dollars, with great bulk discounts available.
    </Say>
    <Pause length="1"/>
    <Say voice="man" language="en-JM">
        Whether you're planning a party, running a bar, or need ice for an event, we can help.
        We offer same-day delivery, and it's FREE in Washington Gardens!
    </Say>
    <Pause length="1"/>
    <Say voice="man" language="en-JM">
        For more information or to place an order, please call us at 8 7 6, 4 9 0, 7 2 0 8.
        That's 8 7 6, 4 9 0, 7 2 0 8.
    </Say>
    <Pause length="1"/>
    <Say voice="man" language="en-JM">
        You can also order online at our website. Remember, More Ice equals More Vibes!
        Thank you and have a great day!
    </Say>
</Response>'''
    
    return Response(content=twiml_content, media_type="text/xml")

# AI Agent admin endpoints
@api_router.get("/admin/call-attempts")
async def get_call_attempts():
    """Get all AI agent call attempts for business review"""
    attempts = await db.call_attempts.find({}, {"_id": 0}).sort([("createdAt", -1)]).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for attempt in attempts:
        if isinstance(attempt.get('createdAt'), str):
            attempt['createdAt'] = datetime.fromisoformat(attempt['createdAt'])
        if isinstance(attempt.get('updatedAt'), str):
            attempt['updatedAt'] = datetime.fromisoformat(attempt['updatedAt'])
    
    return attempts

# Test endpoint for AI agent without making real calls
@api_router.post("/ai-agent/test-callback")
async def test_ai_callback(quote_id: str, phone_number: str = "+18764907208"):
    """Test the AI callback system without making real Twilio calls"""
    try:
        # Create test call attempt record
        call_attempt = CallAttempt(
            quoteId=quote_id,
            customerId=f"customer_{quote_id}",
            phoneNumber=phone_number,
            status="test_mode",
            callSid="test_call_123"
        )
        
        # Store call attempt in database
        doc = call_attempt.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        doc['updatedAt'] = doc['updatedAt'].isoformat()
        await db.call_attempts.insert_one(doc)
        
        logger.info(f"Test AI callback created for quote {quote_id}")
        
        return {
            "status": "success",
            "message": "Test callback record created",
            "call_attempt_id": call_attempt.id,
            "quote_id": quote_id,
            "phone_number": phone_number,
            "instructions": [
                "1. Get ngrok URL: run 'ngrok http 8001' after getting ngrok authtoken",
                "2. Update PUBLIC_URL environment variable with your ngrok URL", 
                "3. Test TwiML endpoint: /api/ai-agent/twiml",
                "4. The system will automatically call customers when quotes are submitted"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to create test AI callback: {e}")
        return {"status": "error", "message": str(e)}

# AI Sales Agent Functions
async def initiate_ai_callback(quote_id: str, phone_number: str, customer_name: str):
    """Initiate an AI callback for a quote/order"""
    try:
        logger.info(f"Initiating AI callback for quote {quote_id} to {phone_number}")
        
        # Create call attempt record
        call_attempt = CallAttempt(
            quoteId=quote_id,
            customerId=f"customer_{quote_id}",
            phoneNumber=phone_number,
            status="initiated"
        )
        
        # Store call attempt in database
        doc = call_attempt.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        doc['updatedAt'] = doc['updatedAt'].isoformat()
        await db.call_attempts.insert_one(doc)
        
        # Get quote details for personalized callback
        quote = await db.quotes.find_one({"id": quote_id}, {"_id": 0})
        
        if quote:
            bags = quote.get("quote", {}).get("bags", 1)
            total = int(quote.get("quote", {}).get("total", 350))
            delivery_fee = quote.get("quote", {}).get("deliveryFee", 300)
            address = quote.get("customerInfo", {}).get("address", "")
            guest_count = quote.get("eventDetails", {}).get("guestCount", 0)
            event_type = quote.get("eventDetails", {}).get("eventType", "event")
            
            # Create personalized TwiML with actual details
            twiml_response = VoiceResponse()
            
            twiml_response.say(f"Hello {customer_name}, this is Ice Solutions calling about your recent quote.", voice="man", rate="slow")
            twiml_response.pause(length=1)
            
            if guest_count > 0:
                twiml_response.say(f"You requested {bags} bags of ice for your {event_type} with {guest_count} guests.", voice="man", rate="slow")
            else:
                twiml_response.say(f"You requested {bags} bags of ice for your event.", voice="man", rate="slow")
            
            twiml_response.pause(length=1)
            
            if delivery_fee == 0:
                twiml_response.say(f"Your total is {total} Jamaican dollars with free delivery to Washington Gardens.", voice="man", rate="slow")
            else:
                twiml_response.say(f"Your total is {total} Jamaican dollars including 300 dollar delivery fee.", voice="man", rate="slow")
            
            twiml_response.pause(length=1)
            twiml_response.say("Please call us back at 876-490-7208 to confirm your order and arrange delivery.", voice="man", rate="slow")
            twiml_response.pause(length=1)
            twiml_response.say("Thank you for choosing Ice Solutions, where More Ice equals More Vibes!", voice="man", rate="slow")
        else:
            # Fallback if quote not found
            twiml_response = VoiceResponse()
            twiml_response.say("Hello, this is Ice Solutions calling about your ice delivery quote.", voice="man", rate="slow")
            twiml_response.pause(length=1)
            twiml_response.say("Please call us back at 876-490-7208 to confirm your order.", voice="man", rate="slow")
        
        call = twilio_client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            twiml=str(twiml_response)
        )
        
        # Update call attempt with Twilio call SID
        await db.call_attempts.update_one(
            {"id": call_attempt.id},
            {"$set": {"callSid": call.sid, "status": "initiated", "updatedAt": datetime.now(timezone.utc).isoformat()}}
        )
        
        logger.info(f"AI callback initiated successfully. Call SID: {call.sid}")
        
    except Exception as e:
        logger.error(f"Failed to initiate AI callback: {e}")
        # Update call attempt status to failed
        await db.call_attempts.update_one(
            {"quoteId": quote_id, "phoneNumber": phone_number},
            {"$set": {"status": "failed", "updatedAt": datetime.now(timezone.utc).isoformat()}}
        )

# Store active sessions in memory
active_sessions: Dict[str, ActiveSession] = {}

# TwiML endpoint for AI agent
@api_router.get("/ai-agent/test")
async def test_endpoint():
    """Simple test endpoint to verify Twilio can reach us"""
    return {"status": "success", "message": "Twilio can reach this endpoint"}

@api_router.get("/ai-agent/twiml")
async def get_ai_twiml(quote_id: str = "test", customer_name: str = "customer"):
    """Generate TwiML for AI agent call"""
    logger.info(f"TwiML requested for quote {quote_id}, customer {customer_name}")
    
    # Return the most basic TwiML possible
    twiml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="man">Hello from Ice Solutions. Please call 876-490-7208. Thank you.</Say>
</Response>'''
    
    return Response(content=twiml_content, media_type="text/xml")

# Status callback endpoint
@api_router.post("/ai-agent/status-callback")
async def handle_status_callback():
    """Handle Twilio call status updates"""
    # In a real implementation, you would validate the webhook signature
    # and update the call attempt status in the database
    return {"status": "received"}

# WebSocket endpoint for AI conversation
@api_router.websocket("/ai-agent/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    logger.info(f"AI Agent WebSocket connected: {session_id}")
    
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            # Handle different message types from ConversationRelay
            if data.get("type") == "setup":
                await handle_setup_message(websocket, session_id, data)
            elif data.get("type") == "user_utterance":
                await handle_user_utterance(websocket, session_id, data)
            elif data.get("type") == "interrupt":
                await handle_interrupt(websocket, session_id, data)
                
    except WebSocketDisconnect:
        logger.info(f"AI Agent WebSocket disconnected: {session_id}")
        # Clean up session
        if session_id in active_sessions:
            del active_sessions[session_id]
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

async def handle_setup_message(websocket: WebSocket, session_id: str, data: Dict):
    """Handle ConversationRelay setup message"""
    try:
        # Extract custom parameters
        quote_id = data.get("parameters", {}).get("quote_id")
        customer_name = data.get("parameters", {}).get("customer_name")
        call_sid = data.get("call_sid")
        
        # Load quote data from database
        quote = await db.quotes.find_one({"id": quote_id}, {"_id": 0})
        
        if not quote:
            logger.error(f"Quote not found: {quote_id}")
            return
        
        # Create active session
        session = ActiveSession(
            sessionId=session_id,
            quoteId=quote_id,
            customerId=quote["customerInfo"]["name"],
            callSid=call_sid,
            contextData={
                "quote": quote,
                "customer_name": customer_name
            }
        )
        
        active_sessions[session_id] = session
        logger.info(f"AI Agent session initialized for quote {quote_id}")
        
    except Exception as e:
        logger.error(f"Error handling setup message: {e}")

async def handle_user_utterance(websocket: WebSocket, session_id: str, data: Dict):
    """Handle user speech input and generate AI response"""
    try:
        if session_id not in active_sessions:
            return
            
        session = active_sessions[session_id]
        utterance = data.get("utterance", "").lower()
        
        # Add customer message to conversation history
        session.conversationHistory.append(
            ConversationMessage(speaker="customer", message=utterance)
        )
        
        # Generate AI response based on utterance and context
        response_text = await generate_ai_response(utterance, session)
        
        # Add agent message to conversation history
        session.conversationHistory.append(
            ConversationMessage(speaker="agent", message=response_text)
        )
        
        # Send response back to ConversationRelay
        response_message = {
            "type": "response",
            "text": response_text
        }
        
        await websocket.send_text(json.dumps(response_message))
        
    except Exception as e:
        logger.error(f"Error handling user utterance: {e}")

async def handle_interrupt(websocket: WebSocket, session_id: str, data: Dict):
    """Handle customer interruption during agent response"""
    # Customer started speaking while agent was talking
    # Clear any pending responses
    logger.info(f"Customer interrupted agent in session {session_id}")

async def generate_ai_response(utterance: str, session: ActiveSession) -> str:
    """Generate appropriate AI response based on customer input"""
    quote_data = session.contextData.get("quote", {})
    customer_name = session.contextData.get("customer_name", "")
    
    # Extract key information from quote
    bags = quote_data.get("quote", {}).get("bags", 0)
    total = quote_data.get("quote", {}).get("total", 0)
    delivery_fee = quote_data.get("quote", {}).get("deliveryFee", 0)
    event_date = quote_data.get("eventDetails", {}).get("eventDate", "")
    guest_count = quote_data.get("eventDetails", {}).get("guestCount", 0)
    
    # Simple rule-based responses (can be enhanced with LLM integration)
    if any(word in utterance for word in ["hello", "hi", "hey"]):
        return f"Hello {customer_name}! I'm calling about your ice delivery quote for {bags} bags of ice totaling JMD ${total:.0f}. How can I help you today?"
    
    elif any(word in utterance for word in ["price", "cost", "how much", "total"]):
        return f"Your quote is for {bags} bags of 10lb ice at JMD $350 each, plus JMD ${delivery_fee:.0f} delivery fee, for a total of JMD ${total:.0f}. Would you like to confirm this order?"
    
    elif any(word in utterance for word in ["delivery", "deliver", "when"]):
        return f"We can deliver your ice on your requested date. Our delivery areas are Washington Gardens (free delivery) and anywhere outside Washington Gardens (JMD $300 delivery fee). What area are you in?"
    
    elif any(word in utterance for word in ["confirm", "order", "yes", "book"]):
        return f"Perfect! I'll confirm your order for {bags} bags of ice totaling JMD ${total:.0f}. Can you confirm your delivery address and preferred delivery time?"
    
    elif any(word in utterance for word in ["cancel", "no", "not interested"]):
        return "No problem at all! Your quote will remain available if you change your mind. Is there anything else I can help you with regarding our ice delivery services?"
    
    elif any(word in utterance for word in ["question", "ask", "tell me"]):
        return "I'm here to help! I can tell you about our ice products, delivery areas, pricing, or help you modify your order. What would you like to know?"
    
    else:
        return "I understand. Let me help you with your ice delivery needs. You can ask me about pricing, delivery options, or confirm your order. What would you like to know?"

# Admin endpoint to view all quotes (for business owner)
@api_router.get("/admin/quotes", response_model=List[Quote])
async def get_all_quotes():
    """Get all quotes for business review (admin endpoint)"""
    quotes = await db.quotes.find({}, {"_id": 0}).sort([("createdAt", -1)]).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for quote in quotes:
        if isinstance(quote.get('createdAt'), str):
            quote['createdAt'] = datetime.fromisoformat(quote['createdAt'])
        if isinstance(quote.get('updatedAt'), str):
            quote['updatedAt'] = datetime.fromisoformat(quote['updatedAt'])
        if isinstance(quote['eventDetails'].get('eventDate'), str):
            quote['eventDetails']['eventDate'] = datetime.fromisoformat(quote['eventDetails']['eventDate'])
    
    return quotes

# Admin endpoint to view all contacts (for business owner)
@api_router.get("/admin/contacts")
async def get_all_contacts_admin():
    """Get all contact submissions for business review (admin endpoint)"""
    contacts = await db.contacts.find({}, {"_id": 0}).sort([("createdAt", -1)]).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects  
    for contact in contacts:
        if isinstance(contact.get('createdAt'), str):
            contact['createdAt'] = datetime.fromisoformat(contact['createdAt'])
        if isinstance(contact.get('updatedAt'), str):
            contact['updatedAt'] = datetime.fromisoformat(contact['updatedAt'])
    
    return contacts

# Delivery Areas API
@api_router.get("/delivery-areas", response_model=List[DeliveryArea])
async def get_delivery_areas():
    areas = await db.delivery_areas.find({"isActive": True}, {"_id": 0}).to_list(100)
    
    # Convert ISO string timestamps back to datetime objects
    for area in areas:
        if isinstance(area.get('createdAt'), str):
            area['createdAt'] = datetime.fromisoformat(area['createdAt'])
        if isinstance(area.get('updatedAt'), str):
            area['updatedAt'] = datetime.fromisoformat(area['updatedAt'])
    
    return areas

# Database seeding function
async def seed_database():
    """Seed the database with initial data if collections are empty"""
    
    # Seed products if collection is empty
    product_count = await db.products.count_documents({})
    if product_count == 0:
        products_data = [
            {
                "id": "prod_10lb",
                "name": "10lb Party Ice Bags",
                "description": "Perfect for parties, events, and small gatherings. Crystal-clear, restaurant-quality ice.",
                "price": 350.00,
                "weight": "10 lbs",
                "inStock": True,
                "comingSoon": False,
                "features": ["Crystal Clear", "Restaurant Quality", "Fast Melting", "Perfect Cube Size"],
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "prod_50lb",
                "name": "50lb Commercial Ice Bags",
                "description": "Coming Soon! Perfect for larger events and commercial use.",
                "price": 1750.00,
                "weight": "50 lbs",
                "inStock": False,
                "comingSoon": True,
                "features": ["Bulk Quantity", "Cost Effective", "Commercial Grade", "Extended Freshness"],
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "prod_100lb",
                "name": "100lb Industrial Ice Bags",
                "description": "Coming Soon! Ideal for restaurants, bars, and large-scale events.",
                "price": 3200.00,
                "weight": "100 lbs",
                "inStock": False,
                "comingSoon": True,
                "features": ["Maximum Volume", "Professional Grade", "Bulk Pricing", "Commercial Delivery"],
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }
        ]
        await db.products.insert_many(products_data)
        logger.info("Seeded products collection")
    
    # Seed delivery areas if collection is empty
    area_count = await db.delivery_areas.count_documents({})
    if area_count == 0:
        areas_data = [
            {
                "id": "area_washington_gardens",
                "area": "Washington Gardens",
                "deliveryFee": 0.0,
                "timeSlots": ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"],
                "isActive": True,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "area_outside_washington_gardens",
                "area": "Anywhere outside of Washington Gardens",
                "deliveryFee": 300.00,
                "timeSlots": ["10 AM - 1 PM", "1 PM - 4 PM", "4 PM - 7 PM"],
                "isActive": True,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }
        ]
        await db.delivery_areas.insert_many(areas_data)
        logger.info("Seeded delivery areas collection")
    else:
        # Check if we need to update delivery areas to new format
        existing_areas = await db.delivery_areas.find({}, {"_id": 0}).to_list(10)
        has_old_format = any(area.get("area") in ["Downtown Core", "West Side", "East Side", "North Suburbs"] for area in existing_areas)
        
        if has_old_format:
            logger.info("Updating delivery areas to new Jamaica format...")
            # Clear old areas and insert new ones
            await db.delivery_areas.delete_many({})
            areas_data = [
                {
                    "id": "area_washington_gardens",
                    "area": "Washington Gardens",
                    "deliveryFee": 0.0,
                    "timeSlots": ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"],
                    "isActive": True,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                },
                {
                    "id": "area_outside_washington_gardens",
                    "area": "Anywhere outside of Washington Gardens",
                    "deliveryFee": 300.00,
                    "timeSlots": ["10 AM - 1 PM", "1 PM - 4 PM", "4 PM - 7 PM"],
                    "isActive": True,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }
            ]
            await db.delivery_areas.insert_many(areas_data)
            logger.info("Updated delivery areas to Jamaica format")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await seed_database()
    logger.info("Backend startup complete")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()