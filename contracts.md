# IceSolutions Backend API Contracts

## Overview
This document outlines the API contracts and backend implementation plan for the IceSolutions ice delivery website. The frontend is currently using mock data that needs to be replaced with real backend API calls.

## Current Mock Data (to be replaced)
Located in `/frontend/src/data/mock.js`:
- Company information and contact details
- Product catalog (10lb, 50lb, 100lb ice bags)
- Services information
- Delivery areas and pricing
- Customer testimonials
- Quote requests storage
- Order storage
- Contact form submissions

## Database Models Needed

### 1. Products Collection
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  price: Number,
  weight: String,
  inStock: Boolean,
  comingSoon: Boolean,
  features: [String],
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Quotes Collection
```javascript
{
  _id: ObjectId,
  customerInfo: {
    name: String,
    email: String,
    phone: String,
    address: String
  },
  eventDetails: {
    eventDate: Date,
    eventType: String,
    guestCount: Number,
    iceAmount: Number,
    deliveryTime: String
  },
  quote: {
    bags: Number,
    basePrice: Number,
    deliveryFee: Number,
    total: Number,
    savings: Number
  },
  specialRequests: String,
  status: String, // 'pending', 'contacted', 'confirmed', 'completed'
  createdAt: Date,
  updatedAt: Date
}
```

### 3. Orders Collection
```javascript
{
  _id: ObjectId,
  quoteId: ObjectId, // Reference to quote
  customerInfo: {
    name: String,
    email: String,
    phone: String,
    address: String
  },
  orderItems: [{
    productId: ObjectId,
    quantity: Number,
    price: Number
  }],
  deliveryInfo: {
    date: Date,
    timeSlot: String,
    area: String,
    fee: Number
  },
  pricing: {
    subtotal: Number,
    deliveryFee: Number,
    total: Number
  },
  status: String, // 'pending', 'confirmed', 'delivered', 'cancelled'
  createdAt: Date,
  updatedAt: Date
}
```

### 4. Contacts Collection
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String,
  subject: String,
  message: String,
  inquiryType: String,
  status: String, // 'new', 'replied', 'resolved'
  createdAt: Date,
  updatedAt: Date
}
```

### 5. Delivery Areas Collection
```javascript
{
  _id: ObjectId,
  area: String,
  deliveryFee: Number,
  timeSlots: [String],
  isActive: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

## API Endpoints to Implement

### Products API
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get specific product
- `POST /api/products` - Create new product (admin)
- `PUT /api/products/:id` - Update product (admin)

### Quotes API
- `POST /api/quotes` - Submit quote request
- `GET /api/quotes/:id` - Get quote by ID
- `PUT /api/quotes/:id/status` - Update quote status (admin)

### Orders API
- `POST /api/orders` - Create new order from quote
- `GET /api/orders/:id` - Get order details
- `PUT /api/orders/:id/status` - Update order status (admin)

### Contacts API
- `POST /api/contacts` - Submit contact form
- `GET /api/contacts` - Get all contacts (admin)
- `PUT /api/contacts/:id/status` - Update contact status (admin)

### Delivery Areas API
- `GET /api/delivery-areas` - Get all delivery areas
- `POST /api/delivery-areas` - Create delivery area (admin)

## Frontend Integration Plan

### 1. Remove Mock Data Usage
Replace mock data imports with API calls in:
- `/pages/HomePage.jsx` - Products, services, testimonials
- `/pages/ProductsPage.jsx` - Products catalog
- `/pages/QuotePage.jsx` - Quote submission, delivery areas
- `/pages/ContactPage.jsx` - Contact form submission
- `/pages/AboutPage.jsx` - Company info

### 2. API Service Layer
Create `/src/services/api.js` with:
- Axios configuration using `REACT_APP_BACKEND_URL`
- Error handling wrapper functions
- API call functions for each endpoint

### 3. State Management
- Add loading states for API calls
- Error handling for failed requests
- Success notifications using Sonner toast

### 4. Data Flow Changes
- Homepage: Fetch products and company info on load
- Quote Page: Submit form to API, get instant response
- Contact Page: Submit contact form to API
- Products Page: Fetch products dynamically

## Database Seeding
Populate initial data:
- Products (10lb, 50lb, 100lb ice bags)
- Delivery areas with current mock data
- Company information

## Testing Requirements
- Test all API endpoints with proper data validation
- Test quote calculation logic
- Test contact form submissions
- Verify database connections and CRUD operations
- Test frontend-backend integration

## Security Considerations
- Input validation on all endpoints
- Rate limiting for contact forms
- Environment variables for sensitive data
- CORS configuration for frontend domain

## Deployment Notes
- MongoDB connection via MONGO_URL environment variable
- Backend runs on port 8001 (supervisor managed)
- Frontend connects via REACT_APP_BACKEND_URL
- All API routes prefixed with /api for Kubernetes ingress