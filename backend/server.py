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
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Connect
from twilio.request_validator import RequestValidator


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
    delivery_fee = 0.0 if base_price > 500 else 300.00  # Free delivery over JMD $500, otherwise JMD $300
    
    # Calculate bulk discount
    savings = 0.0
    if recommended_bags >= 5:
        savings = base_price * 0.05  # 5% discount for 5+ bags
    if recommended_bags >= 10:
        savings = base_price * 0.10  # 10% discount for 10+ bags
    
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
        
        # Create Twilio call
        call = twilio_client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url=f"{os.environ.get('BACKEND_URL', 'http://localhost:8001')}/api/ai-agent/twiml?quote_id={quote_id}&customer_name={customer_name}",
            status_callback=f"{os.environ.get('BACKEND_URL', 'http://localhost:8001')}/api/ai-agent/status-callback",
            status_callback_event=["initiated", "ringing", "answered", "completed"]
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
@api_router.get("/ai-agent/twiml")
async def get_ai_twiml(quote_id: str, customer_name: str):
    """Generate TwiML for AI agent call"""
    response = VoiceResponse()
    
    # Create Connect with ConversationRelay
    connect = Connect()
    conversation_relay = connect.conversation_relay(
        url=f"wss://{os.environ.get('DOMAIN', 'localhost:8001')}/api/ai-agent/websocket",
        welcome_greeting=f"Hello {customer_name}, this is a callback from Ice Solutions regarding your recent ice delivery quote. I can help answer questions about your order and arrange delivery. How can I assist you today?",
        voice="Polly.Matthew-Neural",  # Friendly male voice
        language="en-US",
        transcription_provider="google",
        speech_model="enhanced"
    )
    
    # Add custom parameters for the WebSocket session
    conversation_relay.parameter(name="quote_id", value=quote_id)
    conversation_relay.parameter(name="customer_name", value=customer_name)
    
    response.append(connect)
    
    return Response(content=str(response), media_type="application/xml")

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