from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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
async def create_quote(quote_input: QuoteCreate):
    # Calculate quote pricing
    guest_count = quote_input.eventDetails.guestCount or 0
    ice_amount = quote_input.eventDetails.iceAmount or 0
    
    # Calculate recommended bags (1 bag per 25 guests or based on ice amount)
    recommended_bags = max(1, guest_count // 25) if guest_count else max(1, ice_amount // 10)
    
    base_price = recommended_bags * 350.00  # $350 per 10lb bag
    delivery_fee = 0.0 if base_price > 500 else 8.99  # Free delivery over $500
    
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