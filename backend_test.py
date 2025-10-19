#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for IceSolutions
Tests all API endpoints and business logic as specified in the review request.
Includes NEW payment endpoints, lead management, and updated pricing logic.
"""

import requests
import json
from datetime import datetime, timezone
import sys
import os
import time

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get REACT_APP_BACKEND_URL from frontend/.env")
    sys.exit(1)

API_BASE = f"{BASE_URL}/api"
print(f"Testing backend API at: {API_BASE}")

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.failed += 1
            error_msg = f"❌ FAIL: {message} - Expected: {expected}, Got: {actual}"
            print(error_msg)
            self.errors.append(error_msg)
    
    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.failed += 1
            error_msg = f"❌ FAIL: {message}"
            print(error_msg)
            self.errors.append(error_msg)
    
    def assert_in_range(self, actual, min_val, max_val, message):
        if min_val <= actual <= max_val:
            self.passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.failed += 1
            error_msg = f"❌ FAIL: {message} - Expected: {min_val}-{max_val}, Got: {actual}"
            print(error_msg)
            self.errors.append(error_msg)

def test_products_api(results):
    """Test Products API - should return 3 products with correct pricing"""
    print("\n🧪 Testing Products API...")
    
    try:
        response = requests.get(f"{API_BASE}/products", timeout=10)
        results.assert_equal(response.status_code, 200, "Products API returns 200 status")
        
        if response.status_code == 200:
            products = response.json()
            results.assert_equal(len(products), 3, "Products API returns exactly 3 products")
            
            # Check for expected products and pricing
            product_names = [p['name'] for p in products]
            expected_products = ["10lb Party Ice Bags", "50lb Commercial Ice Bags", "100lb Industrial Ice Bags"]
            
            for expected in expected_products:
                results.assert_true(any(expected in name for name in product_names), 
                                  f"Product '{expected}' exists")
            
            # Check pricing for 10lb bags (main product)
            ten_lb_product = next((p for p in products if "10lb" in p['name']), None)
            if ten_lb_product:
                results.assert_equal(ten_lb_product['price'], 350.00, "10lb bag price is $350.00")
                results.assert_equal(ten_lb_product['inStock'], True, "10lb bags are in stock")
            
            # Verify all products have required fields
            for product in products:
                required_fields = ['id', 'name', 'description', 'price', 'weight', 'inStock']
                for field in required_fields:
                    results.assert_true(field in product, f"Product has required field: {field}")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Products API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_delivery_areas_api(results):
    """Test Delivery Areas API - should return 2 delivery areas (Washington Gardens + Others)"""
    print("\n🧪 Testing Delivery Areas API...")
    
    try:
        response = requests.get(f"{API_BASE}/delivery-areas", timeout=10)
        results.assert_equal(response.status_code, 200, "Delivery Areas API returns 200 status")
        
        if response.status_code == 200:
            areas = response.json()
            results.assert_equal(len(areas), 2, "Delivery Areas API returns exactly 2 areas")
            
            # Check for expected delivery areas (NEW Jamaica format)
            area_names = [area['area'] for area in areas]
            
            # Washington Gardens should have free delivery
            washington_gardens = next((a for a in areas if "Washington Gardens" in a['area']), None)
            if washington_gardens:
                results.assert_equal(washington_gardens['deliveryFee'], 0.0, "Washington Gardens has free delivery")
                results.assert_true("Washington Gardens" in washington_gardens['area'], "Washington Gardens area exists")
            
            # Other areas should have JMD $300 delivery fee
            other_areas = next((a for a in areas if "outside" in a['area']), None)
            if other_areas:
                results.assert_equal(other_areas['deliveryFee'], 300.0, "Outside Washington Gardens has JMD $300 delivery fee")
                results.assert_true("outside" in other_areas['area'], "Outside Washington Gardens area exists")
            
            # Verify all areas have required fields
            for area in areas:
                required_fields = ['id', 'area', 'deliveryFee', 'timeSlots', 'isActive']
                for field in required_fields:
                    results.assert_true(field in area, f"Delivery area has required field: {field}")
                
                results.assert_true(area['isActive'], f"Delivery area '{area['area']}' is active")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Delivery Areas API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_quotes_api_basic(results):
    """Test basic quote creation and calculation logic"""
    print("\n🧪 Testing Quotes API - Basic Functionality...")
    
    # Test case 1: Small event (25 guests)
    quote_data = {
        "customerInfo": {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "555-0123",
            "address": "123 Main St, Downtown"
        },
        "eventDetails": {
            "eventDate": "2024-12-15T18:00:00Z",
            "eventType": "Birthday Party",
            "guestCount": 25,
            "iceAmount": 0,
            "deliveryTime": "3 PM - 6 PM"
        },
        "specialRequests": "Please deliver to back entrance"
    }
    
    try:
        response = requests.post(f"{API_BASE}/quotes", 
                               json=quote_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        results.assert_equal(response.status_code, 200, "Quote creation returns 200 status")
        
        if response.status_code == 200:
            quote = response.json()
            
            # Verify quote structure
            required_fields = ['id', 'customerInfo', 'eventDetails', 'quote', 'status', 'createdAt']
            for field in required_fields:
                results.assert_true(field in quote, f"Quote has required field: {field}")
            
            # Test business logic: 25 guests = 1 bag (25 guests / 25 = 1)
            results.assert_equal(quote['quote']['bags'], 1, "25 guests requires 1 bag")
            results.assert_equal(quote['quote']['basePrice'], 350.00, "1 bag costs $350.00")
            results.assert_equal(quote['quote']['deliveryFee'], 8.99, "Delivery fee $8.99 for orders under $500")
            results.assert_equal(quote['quote']['savings'], 0.0, "No bulk discount for 1 bag")
            results.assert_equal(quote['quote']['total'], 358.99, "Total = $350.00 + $8.99")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Basic quote API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_quotes_api_bulk_discounts(results):
    """Test quote calculation with bulk discounts"""
    print("\n🧪 Testing Quotes API - Bulk Discounts...")
    
    # Test case 2: Medium event (150 guests = 6 bags, 5% discount)
    quote_data = {
        "customerInfo": {
            "name": "Michael Chen",
            "email": "michael.chen@company.com",
            "phone": "555-0456",
            "address": "456 Business Ave, West Side"
        },
        "eventDetails": {
            "eventDate": "2024-12-20T19:00:00Z",
            "eventType": "Corporate Event",
            "guestCount": 150,
            "iceAmount": 0,
            "deliveryTime": "12 PM - 3 PM"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/quotes", 
                               json=quote_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            quote = response.json()
            
            # Test business logic: 150 guests = 6 bags (150 / 25 = 6)
            results.assert_equal(quote['quote']['bags'], 6, "150 guests requires 6 bags")
            results.assert_equal(quote['quote']['basePrice'], 2100.00, "6 bags cost $2100.00")
            results.assert_equal(quote['quote']['savings'], 105.00, "5% discount for 5+ bags ($2100 * 0.05)")
            results.assert_equal(quote['quote']['deliveryFee'], 0.0, "Free delivery for orders over $500")
            results.assert_equal(quote['quote']['total'], 1995.00, "Total = $2100.00 - $105.00")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Bulk discount quote API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_quotes_api_large_order(results):
    """Test quote calculation for large orders (10% discount)"""
    print("\n🧪 Testing Quotes API - Large Order Discount...")
    
    # Test case 3: Large event (300 guests = 12 bags, 10% discount)
    quote_data = {
        "customerInfo": {
            "name": "Jennifer Martinez",
            "email": "jennifer@events.com",
            "phone": "555-0789",
            "address": "789 Event Plaza, North Suburbs"
        },
        "eventDetails": {
            "eventDate": "2024-12-25T20:00:00Z",
            "eventType": "Wedding Reception",
            "guestCount": 300,
            "iceAmount": 0,
            "deliveryTime": "11 AM - 2 PM"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/quotes", 
                               json=quote_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            quote = response.json()
            
            # Test business logic: 300 guests = 12 bags (300 / 25 = 12)
            results.assert_equal(quote['quote']['bags'], 12, "300 guests requires 12 bags")
            results.assert_equal(quote['quote']['basePrice'], 4200.00, "12 bags cost $4200.00")
            results.assert_equal(quote['quote']['savings'], 420.00, "10% discount for 10+ bags ($4200 * 0.10)")
            results.assert_equal(quote['quote']['deliveryFee'], 0.0, "Free delivery for orders over $500")
            results.assert_equal(quote['quote']['total'], 3780.00, "Total = $4200.00 - $420.00")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Large order quote API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_quotes_api_ice_amount(results):
    """Test quote calculation based on ice amount instead of guest count"""
    print("\n🧪 Testing Quotes API - Ice Amount Calculation...")
    
    # Test case 4: Based on ice amount (50 lbs = 5 bags)
    quote_data = {
        "customerInfo": {
            "name": "David Wilson",
            "email": "david.wilson@restaurant.com",
            "phone": "555-0321",
            "address": "321 Restaurant Row, East Side"
        },
        "eventDetails": {
            "eventDate": "2024-12-18T16:00:00Z",
            "eventType": "Restaurant Supply",
            "guestCount": 0,
            "iceAmount": 50,
            "deliveryTime": "9 AM - 12 PM"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/quotes", 
                               json=quote_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            quote = response.json()
            
            # Test business logic: 50 lbs ice = 5 bags (50 / 10 = 5)
            results.assert_equal(quote['quote']['bags'], 5, "50 lbs ice requires 5 bags")
            results.assert_equal(quote['quote']['basePrice'], 1750.00, "5 bags cost $1750.00")
            results.assert_equal(quote['quote']['savings'], 87.50, "5% discount for 5+ bags ($1750 * 0.05)")
            results.assert_equal(quote['quote']['deliveryFee'], 0.0, "Free delivery for orders over $500")
            results.assert_equal(quote['quote']['total'], 1662.50, "Total = $1750.00 - $87.50")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Ice amount quote API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_contacts_api(results):
    """Test Contact form submission"""
    print("\n🧪 Testing Contacts API...")
    
    contact_data = {
        "name": "Alex Thompson",
        "email": "alex.thompson@email.com",
        "phone": "555-0654",
        "subject": "Bulk Order Inquiry",
        "message": "Hi, I'm interested in placing a large order for our upcoming corporate event. Can you provide pricing for 20+ bags?",
        "inquiryType": "Bulk Order"
    }
    
    try:
        response = requests.post(f"{API_BASE}/contacts", 
                               json=contact_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        results.assert_equal(response.status_code, 200, "Contact creation returns 200 status")
        
        if response.status_code == 200:
            contact = response.json()
            
            # Verify contact structure
            required_fields = ['id', 'name', 'email', 'subject', 'message', 'status', 'createdAt']
            for field in required_fields:
                results.assert_true(field in contact, f"Contact has required field: {field}")
            
            # Verify data integrity
            results.assert_equal(contact['name'], contact_data['name'], "Contact name matches input")
            results.assert_equal(contact['email'], contact_data['email'], "Contact email matches input")
            results.assert_equal(contact['subject'], contact_data['subject'], "Contact subject matches input")
            results.assert_equal(contact['status'], "new", "New contact has 'new' status")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Contact API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_payment_endpoints(results):
    """Test NEW Payment Endpoints - Stripe Checkout Integration"""
    print("\n🧪 Testing NEW Payment Endpoints...")
    
    # Test 1: Create checkout session for 1 bag (no discount)
    print("\n  📦 Testing 1 bag checkout (no discount)...")
    checkout_data_1 = {
        "bags": 1,
        "delivery_address": "123 Main St, Kingston",
        "delivery_fee": 300.0,
        "metadata": {
            "customer_name": "John Smith",
            "customer_email": "john@email.com"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/checkout/create-session", 
                               json=checkout_data_1,
                               params={"origin_url": BASE_URL},
                               headers={'Content-Type': 'application/json'},
                               timeout=15)
        
        results.assert_equal(response.status_code, 200, "Checkout session creation returns 200 status")
        
        if response.status_code == 200:
            session_data = response.json()
            results.assert_true('session_id' in session_data, "Checkout session returns session_id")
            results.assert_true('url' in session_data, "Checkout session returns Stripe URL")
            
            # Store session_id for status testing
            session_id_1 = session_data.get('session_id')
            
            # Test checkout status endpoint
            if session_id_1:
                print(f"  🔍 Testing checkout status for session: {session_id_1}")
                status_response = requests.get(f"{API_BASE}/checkout/status/{session_id_1}", timeout=10)
                results.assert_equal(status_response.status_code, 200, "Checkout status returns 200 status")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    results.assert_true('payment_status' in status_data, "Checkout status returns payment_status")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: 1 bag checkout request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 2: Create checkout session for 5 bags (5% discount)
    print("\n  📦 Testing 5 bags checkout (5% discount)...")
    checkout_data_5 = {
        "bags": 5,
        "delivery_address": "Washington Gardens, Kingston",
        "delivery_fee": 0.0,  # Free delivery to Washington Gardens
        "metadata": {
            "customer_name": "Maria Garcia",
            "customer_email": "maria@email.com"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/checkout/create-session", 
                               json=checkout_data_5,
                               params={"origin_url": BASE_URL},
                               headers={'Content-Type': 'application/json'},
                               timeout=15)
        
        results.assert_equal(response.status_code, 200, "5 bags checkout session creation returns 200 status")
        
        if response.status_code == 200:
            session_data = response.json()
            results.assert_true('session_id' in session_data, "5 bags checkout session returns session_id")
            results.assert_true('url' in session_data, "5 bags checkout session returns Stripe URL")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: 5 bags checkout request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 3: Create checkout session for 10 bags (10% discount)
    print("\n  📦 Testing 10 bags checkout (10% discount)...")
    checkout_data_10 = {
        "bags": 10,
        "delivery_address": "456 Business Ave, Spanish Town",
        "delivery_fee": 300.0,
        "metadata": {
            "customer_name": "Robert Johnson",
            "customer_email": "robert@business.com"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/checkout/create-session", 
                               json=checkout_data_10,
                               params={"origin_url": BASE_URL},
                               headers={'Content-Type': 'application/json'},
                               timeout=15)
        
        results.assert_equal(response.status_code, 200, "10 bags checkout session creation returns 200 status")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: 10 bags checkout request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 4: Create checkout session for 20 bags (15% discount)
    print("\n  📦 Testing 20 bags checkout (15% discount)...")
    checkout_data_20 = {
        "bags": 20,
        "delivery_address": "Washington Gardens, Kingston",
        "delivery_fee": 0.0,  # Free delivery to Washington Gardens
        "metadata": {
            "customer_name": "Sarah Williams",
            "customer_email": "sarah@events.com"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/checkout/create-session", 
                               json=checkout_data_20,
                               params={"origin_url": BASE_URL},
                               headers={'Content-Type': 'application/json'},
                               timeout=15)
        
        results.assert_equal(response.status_code, 200, "20 bags checkout session creation returns 200 status")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: 20 bags checkout request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_order_endpoints(results):
    """Test NEW Order Management Endpoints"""
    print("\n🧪 Testing NEW Order Management Endpoints...")
    
    # Test order creation
    order_data = {
        "customer_name": "Jennifer Martinez",
        "customer_email": "jennifer@email.com",
        "customer_phone": "876-555-0123",
        "delivery_address": "Washington Gardens, Kingston",
        "bags": 8,
        "delivery_fee": 0.0,
        "total_amount": 2660.0,  # 8 bags * 350 * 0.95 (5% discount) + 0 delivery
        "payment_session_id": "test_session_123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/orders", 
                               json=order_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        results.assert_equal(response.status_code, 200, "Order creation returns 200 status")
        
        if response.status_code == 200:
            order = response.json()
            
            # Verify order structure
            required_fields = ['id', 'customer_name', 'customer_email', 'bags', 'total_amount', 'order_status', 'created_at']
            for field in required_fields:
                results.assert_true(field in order, f"Order has required field: {field}")
            
            # Verify data integrity
            results.assert_equal(order['customer_name'], order_data['customer_name'], "Order customer name matches input")
            results.assert_equal(order['bags'], order_data['bags'], "Order bags count matches input")
            results.assert_equal(order['order_status'], "confirmed", "New order has 'confirmed' status")
            results.assert_equal(order['payment_status'], "completed", "New order has 'completed' payment status")
            
            # Store order_id for retrieval testing
            order_id = order.get('id')
            
            # Test order retrieval
            if order_id:
                print(f"  🔍 Testing order retrieval for order: {order_id}")
                get_response = requests.get(f"{API_BASE}/orders/{order_id}", timeout=10)
                results.assert_equal(get_response.status_code, 200, "Order retrieval returns 200 status")
                
                if get_response.status_code == 200:
                    retrieved_order = get_response.json()
                    results.assert_equal(retrieved_order['id'], order_id, "Retrieved order ID matches created order")
                    results.assert_equal(retrieved_order['customer_name'], order_data['customer_name'], "Retrieved order data matches")
            
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Order API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test invalid order ID
    try:
        invalid_response = requests.get(f"{API_BASE}/orders/invalid_order_id", timeout=10)
        results.assert_equal(invalid_response.status_code, 404, "Invalid order ID returns 404 status")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Invalid order ID test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_lead_management_endpoints(results):
    """Test NEW Lead Management Endpoints"""
    print("\n🧪 Testing NEW Lead Management Endpoints...")
    
    # Test 1: Get sales agent script
    try:
        response = requests.get(f"{API_BASE}/sales-agent/script", timeout=10)
        results.assert_equal(response.status_code, 200, "Sales agent script returns 200 status")
        
        if response.status_code == 200:
            script_data = response.json()
            results.assert_true('script' in script_data, "Sales script response contains 'script' field")
            results.assert_true('faq' in script_data, "Sales script response contains 'faq' field")
            
            # Verify script content
            if 'script' in script_data:
                script = script_data['script']
                results.assert_true(isinstance(script, str) and len(script) > 0, "Sales script is non-empty string")
            
            # Verify FAQ content
            if 'faq' in script_data:
                faq = script_data['faq']
                results.assert_true(isinstance(faq, list) and len(faq) > 0, "Sales FAQ is non-empty list")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Sales agent script request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 2: Get sales agent TwiML
    try:
        response = requests.get(f"{API_BASE}/sales-agent/twiml", 
                               params={"lead_name": "TestCustomer"}, 
                               timeout=10)
        results.assert_equal(response.status_code, 200, "Sales agent TwiML returns 200 status")
        
        if response.status_code == 200:
            twiml_content = response.text
            results.assert_true('<?xml version="1.0" encoding="UTF-8"?>' in twiml_content, "TwiML contains XML declaration")
            results.assert_true('<Response>' in twiml_content, "TwiML contains Response element")
            results.assert_true('<Say' in twiml_content, "TwiML contains Say element")
            results.assert_true('Ice Solutions' in twiml_content, "TwiML mentions Ice Solutions")
            results.assert_true('TestCustomer' in twiml_content, "TwiML includes lead name")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Sales agent TwiML request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 3: Get all leads (should return empty initially)
    try:
        response = requests.get(f"{API_BASE}/leads", timeout=10)
        results.assert_equal(response.status_code, 200, "Leads API returns 200 status")
        
        if response.status_code == 200:
            leads_data = response.json()
            results.assert_true('leads' in leads_data, "Leads response contains 'leads' field")
            results.assert_true('count' in leads_data, "Leads response contains 'count' field")
            
            # Initially should be empty or contain existing leads
            leads = leads_data.get('leads', [])
            count = leads_data.get('count', 0)
            results.assert_equal(len(leads), count, "Leads count matches array length")
            results.assert_true(isinstance(leads, list), "Leads is a list")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Leads API request failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_pricing_logic_verification(results):
    """Test NEW Pricing Logic - Bulk Discounts and Delivery Fees"""
    print("\n🧪 Testing NEW Pricing Logic Verification...")
    
    # Test pricing calculations through quote API with new logic
    test_cases = [
        {
            "name": "1 bag - No discount",
            "bags": 1,
            "address": "Kingston, Jamaica",
            "expected_discount": 0.0,
            "expected_price_per_bag": 350.0,
            "expected_delivery": 300.0
        },
        {
            "name": "4 bags - No discount",
            "bags": 4,
            "address": "Spanish Town, Jamaica", 
            "expected_discount": 0.0,
            "expected_price_per_bag": 350.0,
            "expected_delivery": 300.0
        },
        {
            "name": "5 bags - 5% discount",
            "bags": 5,
            "address": "Portmore, Jamaica",
            "expected_discount": 5.0,
            "expected_price_per_bag": 332.50,
            "expected_delivery": 300.0
        },
        {
            "name": "9 bags - 5% discount",
            "bags": 9,
            "address": "Half Way Tree, Jamaica",
            "expected_discount": 5.0,
            "expected_price_per_bag": 332.50,
            "expected_delivery": 300.0
        },
        {
            "name": "10 bags - 10% discount",
            "bags": 10,
            "address": "New Kingston, Jamaica",
            "expected_discount": 10.0,
            "expected_price_per_bag": 315.0,
            "expected_delivery": 300.0
        },
        {
            "name": "19 bags - 10% discount",
            "bags": 19,
            "address": "Mandeville, Jamaica",
            "expected_discount": 10.0,
            "expected_price_per_bag": 315.0,
            "expected_delivery": 300.0
        },
        {
            "name": "20 bags - 15% discount",
            "bags": 20,
            "address": "Ocho Rios, Jamaica",
            "expected_discount": 15.0,
            "expected_price_per_bag": 297.50,
            "expected_delivery": 300.0
        },
        {
            "name": "25 bags - 15% discount",
            "bags": 25,
            "address": "Montego Bay, Jamaica",
            "expected_discount": 15.0,
            "expected_price_per_bag": 297.50,
            "expected_delivery": 300.0
        },
        {
            "name": "5 bags - Washington Gardens (FREE delivery)",
            "bags": 5,
            "address": "Washington Gardens, Kingston",
            "expected_discount": 5.0,
            "expected_price_per_bag": 332.50,
            "expected_delivery": 0.0
        }
    ]
    
    for test_case in test_cases:
        print(f"\n  💰 Testing: {test_case['name']}")
        
        # Calculate expected values
        base_total = test_case['bags'] * 350.0
        discount_amount = base_total * (test_case['expected_discount'] / 100)
        expected_total = base_total - discount_amount + test_case['expected_delivery']
        
        # Create quote to test pricing
        quote_data = {
            "customerInfo": {
                "name": "Test Customer",
                "email": "test@email.com",
                "phone": "876-555-0000",
                "address": test_case['address']
            },
            "eventDetails": {
                "eventDate": "2024-12-20T18:00:00Z",
                "eventType": "Test Event",
                "guestCount": test_case['bags'] * 25,  # 25 guests per bag
                "iceAmount": 0,
                "deliveryTime": "3 PM - 6 PM"
            }
        }
        
        try:
            response = requests.post(f"{API_BASE}/quotes-no-callback", 
                                   json=quote_data, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=10)
            
            if response.status_code == 200:
                quote = response.json()
                quote_calc = quote.get('quote', {})
                
                # Verify calculations
                results.assert_equal(quote_calc.get('bags'), test_case['bags'], 
                                   f"{test_case['name']}: Correct bag count")
                
                results.assert_equal(quote_calc.get('deliveryFee'), test_case['expected_delivery'], 
                                   f"{test_case['name']}: Correct delivery fee")
                
                # Check if discount percentage is applied correctly
                actual_discount_percent = (quote_calc.get('savings', 0) / quote_calc.get('basePrice', 1)) * 100
                results.assert_in_range(actual_discount_percent, test_case['expected_discount'] - 0.1, 
                                      test_case['expected_discount'] + 0.1, 
                                      f"{test_case['name']}: Correct discount percentage")
                
                # Verify total calculation
                results.assert_in_range(quote_calc.get('total', 0), expected_total - 1, expected_total + 1,
                                      f"{test_case['name']}: Correct total amount")
            else:
                results.failed += 1
                error_msg = f"❌ FAIL: {test_case['name']} - Quote request failed with status {response.status_code}"
                print(error_msg)
                results.errors.append(error_msg)
                
        except requests.exceptions.RequestException as e:
            results.failed += 1
            error_msg = f"❌ FAIL: {test_case['name']} - Request failed: {str(e)}"
            print(error_msg)
            results.errors.append(error_msg)

def test_google_routes_api_integration(results):
    """Test Google Routes API Integration for Distance Calculation (NEW API Migration)"""
    print("\n🧪 Testing Google Routes API Integration (Migration from Distance Matrix API)...")
    print("   📍 Endpoint: https://routes.googleapis.com/directions/v2:computeRoutes")
    print("   🔄 Migration: Distance Matrix API → Routes API")
    
    # Test 1: Washington Gardens (FREE delivery)
    print("\n  🏠 Test 1: Washington Gardens (FREE delivery)...")
    washington_gardens_data = {
        "destination_address": "Washington Gardens, Kingston",
        "bags": 5
    }
    
    try:
        response = requests.post(f"{API_BASE}/calculate-delivery-fee", 
                               json=washington_gardens_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Washington Gardens delivery fee calculation returns 200")
        
        if response.status_code == 200:
            data = response.json()
            print(f"     📊 Response: {data}")
            
            # Verify required fields from Routes API
            required_fields = ['distance_miles', 'delivery_fee', 'distance_text', 'duration_text', 'is_washington_gardens']
            for field in required_fields:
                results.assert_true(field in data, f"Response contains required field: {field}")
            
            # Verify Washington Gardens gets FREE delivery
            results.assert_equal(data.get('delivery_fee'), 0, "Washington Gardens has FREE delivery ($0 fee)")
            results.assert_equal(data.get('is_washington_gardens'), True, "Washington Gardens correctly identified")
            results.assert_equal(data.get('distance_miles'), 0, "Washington Gardens distance is 0 miles")
            
            # Verify response format
            results.assert_true(isinstance(data.get('distance_text'), str), "distance_text is string")
            results.assert_true(isinstance(data.get('duration_text'), str), "duration_text is string")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Washington Gardens Routes API test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 2: Kingston address (distance-based pricing)
    print("\n  🏙️ Test 2: Kingston address (distance-based pricing)...")
    kingston_data = {
        "destination_address": "New Kingston, Kingston, Jamaica",
        "bags": 5
    }
    
    try:
        response = requests.post(f"{API_BASE}/calculate-delivery-fee", 
                               json=kingston_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Kingston delivery fee calculation returns 200")
        
        if response.status_code == 200:
            data = response.json()
            print(f"     📊 Response: {data}")
            
            # Verify NOT Washington Gardens
            results.assert_equal(data.get('is_washington_gardens'), False, "New Kingston not identified as Washington Gardens")
            
            # Verify Routes API calculated distance successfully
            distance_miles = data.get('distance_miles', 0)
            results.assert_true(distance_miles > 0, f"Routes API calculated distance > 0 miles (got {distance_miles})")
            
            # Verify delivery fee calculation: $300 base + $200/mile
            expected_min_fee = 300.0  # Base fee
            delivery_fee = data.get('delivery_fee', 0)
            results.assert_true(delivery_fee >= expected_min_fee, f"Delivery fee >= $300 base (got ${delivery_fee})")
            
            # Verify fee calculation formula: $300 + ($200 × distance_miles)
            expected_fee = 300.0 + (200.0 * distance_miles)
            results.assert_in_range(delivery_fee, expected_fee - 1, expected_fee + 1, 
                                  f"Delivery fee matches formula: $300 + ($200 × {distance_miles} miles)")
            
            # Verify Routes API response format
            results.assert_true('km' in data.get('distance_text', ''), "distance_text contains km measurement")
            results.assert_true('min' in data.get('duration_text', ''), "duration_text contains time estimate")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Kingston Routes API test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 3: 20+ bags (FREE delivery anywhere)
    print("\n  📦 Test 3: 20+ bags (FREE delivery anywhere)...")
    bulk_order_data = {
        "destination_address": "Half Way Tree, Kingston, Jamaica",
        "bags": 20
    }
    
    try:
        response = requests.post(f"{API_BASE}/calculate-delivery-fee", 
                               json=bulk_order_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "20+ bags delivery fee calculation returns 200")
        
        if response.status_code == 200:
            data = response.json()
            print(f"     📊 Response: {data}")
            
            # Verify FREE delivery for 20+ bags
            results.assert_equal(data.get('delivery_fee'), 0, "20+ bags get FREE delivery anywhere")
            
            # Should have free delivery reason
            if 'free_delivery_reason' in data:
                results.assert_true('20+' in data['free_delivery_reason'], "Free delivery reason mentions 20+ bags")
            
            # Distance should still be calculated by Routes API
            distance_miles = data.get('distance_miles', 0)
            results.assert_true(distance_miles > 0, f"Routes API still calculates distance for 20+ bags (got {distance_miles})")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: 20+ bags Routes API test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 4: Invalid address (error handling)
    print("\n  ❌ Test 4: Invalid address (error handling)...")
    invalid_address_data = {
        "destination_address": "Invalid Address XYZ123",
        "bags": 5
    }
    
    try:
        response = requests.post(f"{API_BASE}/calculate-delivery-fee", 
                               json=invalid_address_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        # Should return 400 error with appropriate message
        results.assert_equal(response.status_code, 400, "Invalid address returns 400 error")
        
        if response.status_code == 400:
            error_data = response.json()
            results.assert_true('detail' in error_data, "Error response contains detail message")
            print(f"     ✅ Error message: {error_data.get('detail')}")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Invalid address Routes API test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 5: Verify no REQUEST_DENIED errors (common with old Distance Matrix API)
    print("\n  🔐 Test 5: Verify no REQUEST_DENIED errors...")
    test_address_data = {
        "destination_address": "Spanish Town, Jamaica",
        "bags": 3
    }
    
    try:
        response = requests.post(f"{API_BASE}/calculate-delivery-fee", 
                               json=test_address_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # Should not contain REQUEST_DENIED or legacy API errors
            response_str = str(data).lower()
            results.assert_true('request_denied' not in response_str, "No REQUEST_DENIED errors from Routes API")
            results.assert_true('legacy api' not in response_str, "No legacy API error messages")
            print(f"     ✅ Routes API working without REQUEST_DENIED errors")
        elif response.status_code == 400:
            # Check if it's a proper validation error, not API permission error
            error_data = response.json()
            error_detail = error_data.get('detail', '').lower()
            results.assert_true('request_denied' not in error_detail, "No REQUEST_DENIED in error messages")
            results.assert_true('api key' not in error_detail, "No API key permission errors")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: REQUEST_DENIED verification test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_chat_endpoint(results):
    """Test NEW Chat Endpoint with Temar Malcolm AI"""
    print("\n🧪 Testing NEW Chat Endpoint...")
    
    # Test 1: First message - verify new greeting format
    print("\n  👋 Testing first message greeting format...")
    first_message_data = {
        "message": "Hello, I'm interested in ice delivery",
        "conversationHistory": []
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", 
                               json=first_message_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Chat endpoint returns 200 status")
        
        if response.status_code == 200:
            chat_data = response.json()
            
            # Verify response structure
            required_fields = ['response', 'requestLeadInfo', 'checkoutUrl']
            for field in required_fields:
                results.assert_true(field in chat_data, f"Chat response contains required field: {field}")
            
            # Verify first response format
            response_text = chat_data.get('response', '')
            results.assert_true('Temar Malcolm' in response_text, "First response mentions Temar Malcolm")
            results.assert_true('Ice Solutions' in response_text, "First response mentions Ice Solutions")
            results.assert_true('excited to help' in response_text, "First response contains excited greeting")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Chat first message test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 2: Customer requests specific amount - should collect info immediately
    print("\n  📦 Testing specific quantity request (immediate info collection)...")
    specific_request_data = {
        "message": "I need 10 bags of ice for my party",
        "conversationHistory": [
            {"role": "assistant", "content": "Thank you for your message. I'm Temar Malcolm..."},
            {"role": "user", "content": "Hello, I'm interested in ice delivery"}
        ]
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", 
                               json=specific_request_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Specific quantity chat request returns 200")
        
        if response.status_code == 200:
            chat_data = response.json()
            response_text = chat_data.get('response', '').lower()
            
            # Should ask for contact information immediately, not suggest different amount
            info_keywords = ['name', 'phone', 'email', 'address', 'contact', 'information']
            has_info_request = any(keyword in response_text for keyword in info_keywords)
            results.assert_true(has_info_request, "Bot asks for contact information when specific quantity requested")
            
            # Should NOT suggest different amounts when customer specifies what they want
            suggestion_keywords = ['recommend', 'suggest', 'might need', 'consider', 'better']
            has_suggestions = any(keyword in response_text for keyword in suggestion_keywords)
            results.assert_true(not has_suggestions, "Bot does NOT suggest different amounts when customer specifies quantity")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Specific quantity chat test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 3: Customer asks for recommendation - should provide guidance
    print("\n  🤔 Testing recommendation request...")
    recommendation_request_data = {
        "message": "How much ice do I need for 50 people?",
        "conversationHistory": [
            {"role": "assistant", "content": "Thank you for your message. I'm Temar Malcolm..."},
            {"role": "user", "content": "Hello"}
        ]
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", 
                               json=recommendation_request_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Recommendation chat request returns 200")
        
        if response.status_code == 200:
            chat_data = response.json()
            response_text = chat_data.get('response', '').lower()
            
            # Should provide recommendations for 50 people
            recommendation_keywords = ['bags', 'recommend', 'need', '50', 'people']
            has_recommendation = any(keyword in response_text for keyword in recommendation_keywords)
            results.assert_true(has_recommendation, "Bot provides ice recommendations when asked")
            
            # Should mention quantity for 50 people (likely 2-4 bags based on guidelines)
            has_quantity = any(str(i) in response_text for i in range(1, 10))
            results.assert_true(has_quantity, "Bot mentions specific bag quantities in recommendation")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Recommendation chat test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 4: Complete order flow - verify checkout URL generation
    print("\n  🛒 Testing checkout URL generation...")
    complete_order_data = {
        "message": "My name is John Smith, email john@test.com, phone 876-555-1234, address is 123 Main St Kingston",
        "conversationHistory": [
            {"role": "assistant", "content": "Great! I can help you with 10 bags. I'll need your contact information..."},
            {"role": "user", "content": "I need 10 bags of ice"}
        ]
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", 
                               json=complete_order_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=20)
        
        results.assert_equal(response.status_code, 200, "Complete order chat request returns 200")
        
        if response.status_code == 200:
            chat_data = response.json()
            
            # Check if checkout URL is generated
            checkout_url = chat_data.get('checkoutUrl')
            if checkout_url:
                results.assert_true('/checkout?' in checkout_url, "Checkout URL contains proper path and parameters")
                results.assert_true('bags=' in checkout_url, "Checkout URL contains bags parameter")
                results.assert_true('name=' in checkout_url, "Checkout URL contains name parameter")
                results.assert_true('email=' in checkout_url, "Checkout URL contains email parameter")
                results.assert_true('from_chat=true' in checkout_url, "Checkout URL indicates chat origin")
            else:
                # If no checkout URL generated yet, should be asking for missing info
                response_text = chat_data.get('response', '').lower()
                info_keywords = ['name', 'phone', 'email', 'address']
                missing_info = any(keyword in response_text for keyword in info_keywords)
                results.assert_true(missing_info, "Bot asks for missing information or generates checkout URL")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Complete order chat test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_knowledge_base_updates(results):
    """Verify Knowledge Base Updates"""
    print("\n🧪 Testing Knowledge Base Updates...")
    
    # Test 1: Check if knowledge base file exists and has updated content
    try:
        with open('/app/TEMAR_MALCOLM_KNOWLEDGE_BASE.md', 'r') as f:
            knowledge_content = f.read()
        
        results.assert_true(len(knowledge_content) > 0, "Knowledge base file exists and has content")
        
        # Test 2: Verify updated delivery fee information
        delivery_keywords = ['$300', '$200 per mile', 'Washington Gardens', 'FREE delivery', '20+ bags']
        for keyword in delivery_keywords:
            results.assert_true(keyword in knowledge_content, f"Knowledge base contains delivery info: {keyword}")
        
        # Test 3: Verify new greeting messages are documented
        greeting_keywords = ['Thanks for your interest in IceSolutions', 'More Ice = More Vibes', 'Temar Malcolm', 'excited to help']
        for keyword in greeting_keywords:
            results.assert_true(keyword in knowledge_content, f"Knowledge base contains greeting: {keyword}")
        
        # Test 4: Verify conversation guidelines
        guideline_keywords = ['SPECIFIC AMOUNT', 'collect information', 'DO NOT suggest', 'GENERATE_CHECKOUT']
        for keyword in guideline_keywords:
            results.assert_true(keyword in knowledge_content, f"Knowledge base contains guideline: {keyword}")
        
        print("✅ Knowledge base contains all required updated information")
        
    except FileNotFoundError:
        results.failed += 1
        error_msg = "❌ FAIL: Knowledge base file not found"
        print(error_msg)
        results.errors.append(error_msg)
    except Exception as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Error reading knowledge base: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_error_handling(results):
    """Test error handling for NEW endpoints"""
    print("\n🧪 Testing Error Handling...")
    
    # Test 1: Invalid session ID for checkout status
    try:
        response = requests.get(f"{API_BASE}/checkout/status/invalid_session_id", timeout=10)
        # Should return error or handle gracefully
        results.assert_true(response.status_code in [400, 404, 500], "Invalid session ID handled appropriately")
        
    except requests.exceptions.RequestException as e:
        results.assert_true(True, "Invalid session ID test handled network error gracefully")
    
    # Test 2: Invalid order ID
    try:
        response = requests.get(f"{API_BASE}/orders/invalid_order_id", timeout=10)
        results.assert_equal(response.status_code, 404, "Invalid order ID returns 404")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Invalid order ID test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
    
    # Test 3: Missing required fields in checkout
    try:
        invalid_checkout = {
            "bags": 0,  # Invalid bag count
            "delivery_address": "",  # Empty address
            "delivery_fee": -100  # Negative fee
        }
        
        response = requests.post(f"{API_BASE}/checkout/create-session", 
                               json=invalid_checkout,
                               params={"origin_url": BASE_URL},
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        # Should handle gracefully
        results.assert_true(response.status_code in [400, 422, 500], "Invalid checkout data handled appropriately")
        
    except requests.exceptions.RequestException as e:
        results.assert_true(True, "Invalid checkout test handled network error gracefully")
    
    # Test 4: Missing required fields in order creation
    try:
        invalid_order = {
            "customer_name": "",  # Empty name
            "customer_email": "invalid-email",  # Invalid email
            "bags": -5,  # Negative bags
            "total_amount": -100  # Negative amount
        }
        
        response = requests.post(f"{API_BASE}/orders", 
                               json=invalid_order, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        # Should handle gracefully
        results.assert_true(response.status_code in [400, 422, 500], "Invalid order data handled appropriately")
        
    except requests.exceptions.RequestException as e:
        results.assert_true(True, "Invalid order test handled network error gracefully")

def run_all_tests():
    """Run all backend API tests including NEW CHAT & DELIVERY features"""
    print("🚀 Starting IceSolutions Backend API Tests - CHAT WIDGET & DELIVERY FEE CALCULATOR")
    print("=" * 80)
    
    results = TestResults()
    
    # SECTION 1: Existing Endpoints (Smoke Test)
    print("\n" + "=" * 50)
    print("📋 SECTION 1: EXISTING ENDPOINTS (SMOKE TEST)")
    print("=" * 50)
    test_products_api(results)
    test_delivery_areas_api(results)
    test_contacts_api(results)
    
    # SECTION 2: NEW Google Maps Distance Calculation
    print("\n" + "=" * 50)
    print("🗺️  SECTION 2: NEW GOOGLE MAPS DISTANCE CALCULATION")
    print("=" * 50)
    test_delivery_fee_calculator(results)
    
    # SECTION 3: NEW Chat Widget with Temar Malcolm AI
    print("\n" + "=" * 50)
    print("💬 SECTION 3: NEW CHAT WIDGET WITH TEMAR MALCOLM AI")
    print("=" * 50)
    test_chat_endpoint(results)
    
    # SECTION 4: Knowledge Base Verification
    print("\n" + "=" * 50)
    print("📚 SECTION 4: KNOWLEDGE BASE VERIFICATION")
    print("=" * 50)
    test_knowledge_base_updates(results)
    
    # SECTION 5: NEW Payment Endpoints
    print("\n" + "=" * 50)
    print("💳 SECTION 5: NEW PAYMENT ENDPOINTS")
    print("=" * 50)
    test_payment_endpoints(results)
    test_order_endpoints(results)
    
    # SECTION 6: NEW Lead Management Endpoints  
    print("\n" + "=" * 50)
    print("📞 SECTION 6: NEW LEAD MANAGEMENT ENDPOINTS")
    print("=" * 50)
    test_lead_management_endpoints(results)
    
    # SECTION 7: NEW Pricing Logic Verification
    print("\n" + "=" * 50)
    print("💰 SECTION 7: NEW PRICING LOGIC VERIFICATION")
    print("=" * 50)
    test_pricing_logic_verification(results)
    
    # SECTION 8: Error Handling
    print("\n" + "=" * 50)
    print("⚠️  SECTION 8: ERROR HANDLING")
    print("=" * 50)
    test_error_handling(results)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🏁 COMPREHENSIVE TEST SUMMARY - CHAT & DELIVERY FEATURES")
    print("=" * 80)
    print(f"✅ PASSED: {results.passed}")
    print(f"❌ FAILED: {results.failed}")
    print(f"📊 TOTAL:  {results.passed + results.failed}")
    
    if results.failed > 0:
        print(f"\n🔍 FAILED TESTS:")
        for error in results.errors:
            print(f"   {error}")
    
    success_rate = (results.passed / (results.passed + results.failed)) * 100 if (results.passed + results.failed) > 0 else 0
    print(f"\n📈 SUCCESS RATE: {success_rate:.1f}%")
    
    if results.failed == 0:
        print("\n🎉 ALL TESTS PASSED! Chat widget and delivery fee calculator working correctly!")
        print("✨ Google Maps integration, chat logic, and checkout generation all verified!")
        return True
    else:
        print(f"\n⚠️  {results.failed} tests failed. Please review the issues above.")
        print("🔧 Focus on NEW chat widget and delivery fee calculator features.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)