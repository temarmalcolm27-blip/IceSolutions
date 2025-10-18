from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
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
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
from google_sheets_integration import GoogleSheetsLeadManager
from email_service import send_notification_confirmation_email


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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
        
        # Use HTTP-based conversational AI
        # More reliable than WebSocket approach
        public_url = os.environ.get('PUBLIC_URL', 'https://your-domain.ngrok-free.app')
        
        # Create TwiML that uses Gather for conversation
        from twilio.twiml.voice_response import VoiceResponse, Gather
        
        twiml_response = VoiceResponse()
        
        # Start conversation with initial greeting
        gather = Gather(
            input='speech',
            action=f'{public_url}/api/conversational-ai/handle?business_name={quote(lead_name)}',
            method='POST',
            speech_timeout='auto',
            language='en-US',
            timeout=5
        )
        
        # Initial greeting from Marcus
        gather.say(
            "Good day! This is Marcus from Ice Solutions. May I speak with the person who handles purchasing for your business?",
            voice='Polly.Matthew'
        )
        
        twiml_response.append(gather)
        
        # If no input, try again
        twiml_response.say(
            "I didn't hear a response. I'll call back another time. Have a great day!",
            voice='Polly.Matthew'
        )
        
        # Make the call with conversational AI
        call = twilio_client.calls.create(
            to=phone_formatted,
            from_=TWILIO_PHONE_NUMBER,
            twiml=str(twiml_response)
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

@api_router.post("/leads/scrape")
async def scrape_and_add_leads(count: int = 10, areas: Optional[List[str]] = None, types: Optional[List[str]] = None):
    """
    Generate sample leads and add them to Google Sheets and database
    
    Query params:
        count: Number of leads to generate (default: 10)
        areas: Target areas (optional, e.g., ["Washington Gardens", "Duhaney Park"])
        types: Business types (optional, e.g., ["bar", "restaurant"])
    
    Note: This uses sample data generation. For production, implement actual web scraping
    or integrate with Google Places API.
    """
    try:
        # Initialize lead scraper
        scraper = LeadScraper()
        
        # Generate leads
        leads = scraper.generate_sample_leads(count=count, areas=areas, business_types=types)
        
        if not leads:
            return {
                "status": "error",
                "message": "Failed to generate leads",
                "leads_added": 0
            }
        
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsLeadManager()
        sheet_url = os.getenv('GOOGLE_SHEETS_URL')
        
        leads_added = 0
        leads_added_to_sheets = 0
        errors = []
        
        # Add leads to Google Sheets and database
        for lead in leads:
            try:
                # Add to Google Sheets if configured
                if sheet_url:
                    try:
                        if sheets_manager.connect_to_sheet(sheet_url):
                            sheets_manager.add_lead(
                                business_name=lead['business_name'],
                                phone=lead['phone'],
                                address=lead['address'],
                                business_type=lead['type'],
                                area=lead['area'],
                                status='New'
                            )
                            leads_added_to_sheets += 1
                    except Exception as sheet_error:
                        logger.warning(f"Could not add to Google Sheets: {str(sheet_error)}")
                
                # Check if lead already exists in database
                existing = await db.leads.find_one({"phone": lead['phone']})
                if not existing:
                    # Create a clean copy without _id for insertion
                    lead_doc = {
                        'business_name': lead['business_name'],
                        'phone': lead['phone'],
                        'address': lead['address'],
                        'type': lead['type'],
                        'area': lead['area'],
                        'status': lead['status'],
                        'call_date': lead.get('call_date', ''),
                        'call_notes': lead.get('call_notes', ''),
                        'result': lead.get('result', ''),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'last_updated': datetime.now(timezone.utc).isoformat(),
                        'call_attempts': 0,
                        'last_call_date': None
                    }
                    await db.leads.insert_one(lead_doc)
                    leads_added += 1
                
            except Exception as lead_error:
                logger.error(f"Error adding lead {lead.get('phone', 'unknown')}: {str(lead_error)}")
                errors.append(f"{lead.get('business_name', 'unknown')}: {str(lead_error)}")
        
        # Return clean response without MongoDB ObjectIds
        return {
            "status": "success",
            "message": f"Successfully generated and added {leads_added} leads to database{f', {leads_added_to_sheets} to Google Sheets' if leads_added_to_sheets > 0 else ''}",
            "leads_added": leads_added,
            "leads_added_to_sheets": leads_added_to_sheets,
            "total_generated": len(leads),
            "errors": errors if errors else None,
            "sample_leads": [
                {
                    "business_name": l["business_name"],
                    "phone": l["phone"],
                    "area": l["area"],
                    "type": l["type"]
                } for l in leads[:5]
            ]
        }
        
    except Exception as e:
        logger.error(f"Error scraping leads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to scrape leads: {str(e)}")

@api_router.post("/leads/update/{phone}")
async def update_lead_call_result(phone: str, status: str, call_notes: str = "", result: str = ""):
    """
    Update lead status after a call attempt
    
    Args:
        phone: Phone number of the lead
        status: New status (Contacted, Interested, Not Interested, Sold)
        call_notes: Notes from the call
        result: Result of the call
    """
    try:
        # Update in database
        update_data = {
            "status": status,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
        if call_notes:
            update_data["call_notes"] = call_notes
        if result:
            update_data["result"] = result
        
        db_result = await db.leads.update_one(
            {"phone": phone},
            {"$set": update_data}
        )
        
        # Update in Google Sheets if configured
        sheets_manager = GoogleSheetsLeadManager()
        sheet_url = os.getenv('GOOGLE_SHEETS_URL')
        
        if sheet_url and sheets_manager.connect_to_sheet(sheet_url):
            call_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            sheets_manager.update_lead_status(
                phone=phone,
                status=status,
                call_date=call_date,
                call_notes=call_notes,
                result=result
            )
        
        if db_result.modified_count > 0:
            return {
                "status": "success",
                "message": f"Lead {phone} updated successfully"
            }
        else:
            return {
                "status": "warning",
                "message": f"No lead found with phone {phone} or no changes made"
            }
        
    except Exception as e:
        logger.error(f"Error updating lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update lead: {str(e)}")

@api_router.get("/leads/stats")
async def get_leads_stats():
    """Get statistics about leads"""
    try:
        total_leads = await db.leads.count_documents({})
        new_leads = await db.leads.count_documents({"status": "New"})
        contacted = await db.leads.count_documents({"status": "Contacted"})
        interested = await db.leads.count_documents({"status": "Interested"})
        sold = await db.leads.count_documents({"status": "Sold"})
        not_interested = await db.leads.count_documents({"status": "Not Interested"})
        
        # Get leads by area
        pipeline = [
            {"$group": {"_id": "$area", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        by_area = await db.leads.aggregate(pipeline).to_list(100)
        
        # Get leads by type
        pipeline = [
            {"$group": {"_id": "$type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        by_type = await db.leads.aggregate(pipeline).to_list(100)
        
        return {
            "total": total_leads,
            "by_status": {
                "new": new_leads,
                "contacted": contacted,
                "interested": interested,
                "sold": sold,
                "not_interested": not_interested
            },
            "by_area": [{"area": item["_id"], "count": item["count"]} for item in by_area],
            "by_type": [{"type": item["_id"], "count": item["count"]} for item in by_type]
        }
        
    except Exception as e:
        logger.error(f"Error getting lead stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@api_router.post("/conversational-ai/handle")
async def handle_conversation(
    request: Request,
    business_name: str = ""
):
    """Handle conversational AI turns (HTTP-based)"""
    try:
        from twilio.twiml.voice_response import VoiceResponse, Gather
        
        # Get form data from Twilio
        form_data = await request.form()
        speech_result = form_data.get('SpeechResult', '')
        call_sid_from_twilio = form_data.get('CallSid', '')
        
        logger.info(f"[{call_sid_from_twilio}] Received speech: {speech_result}")
        
        # Get or create conversation
        conversation = get_or_create_conversation(call_sid_from_twilio, business_name)
        
        # Get Marcus's response
        if speech_result:
            marcus_response = conversation.get_response(speech_result)
        else:
            # First turn - just get initial greeting
            marcus_response = conversation.get_response()
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Check if conversation should end
        if conversation.should_end_call():
            response.say(marcus_response, voice='Polly.Matthew')
            response.hangup()
            cleanup_conversation(call_sid_from_twilio)
        else:
            # Continue conversation
            public_url = os.environ.get('PUBLIC_URL', 'https://your-domain.ngrok-free.app')
            gather = Gather(
                input='speech',
                action=f'{public_url}/api/conversational-ai/handle?business_name={quote(business_name)}',
                method='POST',
                speech_timeout='auto',
                language='en-US',
                timeout=5
            )
            gather.say(marcus_response, voice='Polly.Matthew')
            response.append(gather)
            
            # If no response, end call
            response.say("Thank you for your time. Have a great day!", voice='Polly.Matthew')
            response.hangup()
        
        return Response(content=str(response), media_type="text/xml")
        
    except Exception as e:
        logger.error(f"Error in conversational AI handler: {str(e)}")
        response = VoiceResponse()
        response.say("I apologize, but I'm having technical difficulties. Please call us at 876-490-7208. Thank you!", voice='Polly.Matthew')
        response.hangup()
        return Response(content=str(response), media_type="text/xml")

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
        Hello, this is Marcus from Ice Solutions. We provide party ice deliveries for businesses in the corporate area and Kingston at a reasonable price.
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

# Product Notification Endpoints
class NotificationRequest(BaseModel):
    email: str
    product_name: str
    product_size: str

@api_router.post("/notifications/subscribe")
async def subscribe_to_notification(notification: NotificationRequest, background_tasks: BackgroundTasks):
    """Subscribe to product availability notifications and save to Google Sheets"""
    try:
        # Save to database
        notification_doc = {
            "email": notification.email,
            "product_name": notification.product_name,
            "product_size": notification.product_size,
            "subscribed_at": datetime.now(timezone.utc).isoformat(),
            "notified": False
        }
        
        await db.product_notifications.insert_one(notification_doc)
        
        # Send confirmation email (in background to not block response)
        background_tasks.add_task(
            send_notification_confirmation_email,
            notification.email,
            notification.product_name,
            notification.product_size
        )
        
        # Try to save to Google Sheets if configured
        try:
            sheets_manager = GoogleSheetsLeadManager()
            sheet_url = os.getenv('GOOGLE_SHEETS_NOTIFICATIONS_URL')
            
            if sheet_url and sheets_manager.connect_to_sheet(sheet_url, "Notifications"):
                sheets_manager.add_lead(
                    name=notification.email,
                    phone="N/A",
                    email=notification.email,
                    status="Waiting",
                    notes=f"Wants notification for {notification.product_size} {notification.product_name}"
                )
                logger.info(f"Saved notification to Google Sheets for {notification.email}")
        except Exception as e:
            logger.warning(f"Could not save to Google Sheets: {str(e)}")
            # Continue even if Google Sheets fails - we have it in database
        
        return {
            "status": "success",
            "message": f"You'll be notified when {notification.product_size} {notification.product_name} become available! Check your email for confirmation.",
            "email": notification.email
        }
        
    except Exception as e:
        logger.error(f"Error subscribing to notification: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to subscribe to notifications")

@api_router.get("/notifications")
async def get_notifications():
    """Get all product notification subscriptions"""
    try:
        notifications = await db.product_notifications.find({}, {"_id": 0}).to_list(1000)
        return {"notifications": notifications, "count": len(notifications)}
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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

# ==================== CHAT WIDGET ENDPOINTS ====================

# Load knowledge base
KNOWLEDGE_BASE = ""
try:
    with open('/app/TEMAR_MALCOLM_KNOWLEDGE_BASE.md', 'r') as f:
        KNOWLEDGE_BASE = f.read()
except Exception as e:
    logger.error(f"Failed to load knowledge base: {e}")
    KNOWLEDGE_BASE = "You are Temar Malcolm, a sales agent for Ice Solutions, a premium ice delivery service in Kingston, Jamaica."

# Chat models
class ChatMessage(BaseModel):
    message: str
    conversationHistory: List[Dict[str, str]] = []

class ChatLead(BaseModel):
    name: str
    phone: str
    email: str
    businessName: str = ""
    productInterest: str
    quantity: int
    inquiry: str = ""
    conversationHistory: str = ""

@api_router.post("/chat")
async def chat_with_temar(chat_input: ChatMessage):
    """
    Handle chat messages with Temar Malcolm AI agent
    """
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        # Get Emergent LLM key
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM API key not configured")
        
        # Create system message with knowledge base
        system_message = f"""You are Temar Malcolm, the friendly and professional owner of Ice Solutions.

{KNOWLEDGE_BASE}

IMPORTANT INSTRUCTIONS:
1. Be warm, friendly, and helpful - reflect Jamaican warmth
2. Answer questions about products, pricing, delivery, and services
3. Help calculate ice needs based on event details
4. ONLY ask for contact information when the customer:
   - Explicitly says they want to place an order
   - Asks for a quote and provides event details
   - Says they're ready to buy or schedule delivery
   - Shows clear buying intent (e.g., "I need to order", "I want to buy", "Can I get", "I'd like to schedule")
5. DO NOT ask for information if they're just asking questions about:
   - General information (pricing, delivery areas, products)
   - Bulk discounts or policies
   - How things work
   - Exploring options
6. When you determine the customer is ready to order or needs a quote, end your message with the exact phrase: "[COLLECT_INFO]"
7. Keep responses concise and conversational
8. Use the knowledge base to provide accurate information
9. Only 10lb bags are currently available - 50lb and 100lb are coming soon

Your goal is to help customers learn about Ice Solutions and collect information ONLY when they're ready to order."""

        # Initialize chat
        chat = LlmChat(
            api_key=api_key,
            session_id=str(uuid.uuid4()),
            system_message=system_message
        ).with_model("openai", "gpt-4o-mini")
        
        # Prepare conversation history
        for msg in chat_input.conversationHistory[-5:]:  # Last 5 messages for context
            if msg.get('role') == 'user':
                await chat.send_message(UserMessage(text=msg.get('content', '')))
        
        # Send current message
        user_message = UserMessage(text=chat_input.message)
        response = await chat.send_message(user_message)
        
        # Check if AI is requesting lead information
        request_lead = False
        if "[COLLECT_INFO]" in response:
            request_lead = True
            # Remove the marker from the response
            response = response.replace("[COLLECT_INFO]", "").strip()
        
        return {
            "response": response,
            "requestLeadInfo": request_lead
        }
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@api_router.post("/leads/chat")
async def create_chat_lead(lead: ChatLead):
    """
    Save lead information from chat widget to Google Sheets
    """
    try:
        # Prepare lead data for Google Sheets
        sheet_url = os.environ.get('GOOGLE_SHEETS_URL')
        if not sheet_url:
            raise HTTPException(status_code=500, detail="Google Sheets not configured")
        
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsLeadManager(
            credentials_json_path=os.environ.get('GOOGLE_SHEETS_CREDENTIALS_PATH', '/app/backend/google_sheets_credentials.json')
        )
        
        if not sheets_manager.authenticate():
            raise HTTPException(status_code=500, detail="Failed to authenticate with Google Sheets")
        
        if not sheets_manager.connect_to_sheet(sheet_url):
            raise HTTPException(status_code=500, detail="Failed to connect to Google Sheets")
        
        # Add lead to sheet
        # Expected columns: Name | Phone | Email | Business Name | Product Interest | Quantity | Inquiry | Date | Source
        lead_data = [
            lead.name,
            lead.phone,
            lead.email,
            lead.businessName or "",
            lead.productInterest,
            str(lead.quantity),
            lead.inquiry or "Chat inquiry",
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "Website Chat"
        ]
        
        sheets_manager.sheet.append_row(lead_data)
        logger.info(f"Chat lead saved to Google Sheets: {lead.name} - {lead.phone}")
        
        # Also save to MongoDB for internal tracking
        lead_doc = {
            "id": str(uuid.uuid4()),
            "name": lead.name,
            "phone": lead.phone,
            "email": lead.email,
            "businessName": lead.businessName,
            "productInterest": lead.productInterest,
            "quantity": lead.quantity,
            "inquiry": lead.inquiry,
            "conversationHistory": lead.conversationHistory,
            "source": "chat_widget",
            "status": "new",
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat()
        }
        
        await db.chat_leads.insert_one(lead_doc)
        logger.info(f"Chat lead saved to MongoDB: {lead.name}")
        
        return {
            "success": True,
            "message": "Lead information saved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error saving chat lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save lead: {str(e)}")

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