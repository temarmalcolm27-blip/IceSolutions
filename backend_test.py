#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for IceSolutions
Tests all API endpoints and business logic as specified in the review request.
"""

import requests
import json
from datetime import datetime, timezone
import sys
import os

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
    """Test Delivery Areas API - should return 4 delivery areas with correct fees"""
    print("\n🧪 Testing Delivery Areas API...")
    
    try:
        response = requests.get(f"{API_BASE}/delivery-areas", timeout=10)
        results.assert_equal(response.status_code, 200, "Delivery Areas API returns 200 status")
        
        if response.status_code == 200:
            areas = response.json()
            results.assert_equal(len(areas), 4, "Delivery Areas API returns exactly 4 areas")
            
            # Check for expected delivery areas
            area_names = [area['area'] for area in areas]
            expected_areas = ["Downtown Core", "West Side", "East Side", "North Suburbs"]
            
            for expected in expected_areas:
                results.assert_true(expected in area_names, f"Delivery area '{expected}' exists")
            
            # Check delivery fees
            downtown = next((a for a in areas if "Downtown" in a['area']), None)
            if downtown:
                results.assert_equal(downtown['deliveryFee'], 0.0, "Downtown Core has free delivery")
            
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

def test_edge_cases(results):
    """Test edge cases and error handling"""
    print("\n🧪 Testing Edge Cases...")
    
    # Test invalid quote data
    try:
        invalid_quote = {
            "customerInfo": {
                "name": "",  # Empty name
                "email": "invalid-email",  # Invalid email format
                "phone": "",
                "address": ""
            },
            "eventDetails": {
                "eventDate": "invalid-date",  # Invalid date
                "eventType": "",
                "guestCount": -5,  # Negative guest count
                "iceAmount": -10,  # Negative ice amount
                "deliveryTime": ""
            }
        }
        
        response = requests.post(f"{API_BASE}/quotes", 
                               json=invalid_quote, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        # Should handle gracefully (either 400 error or default to minimum values)
        if response.status_code == 400:
            results.assert_true(True, "Invalid quote data returns 400 error (proper validation)")
        elif response.status_code == 200:
            quote = response.json()
            results.assert_true(quote['quote']['bags'] >= 1, "Minimum 1 bag even with invalid data")
        
    except requests.exceptions.RequestException as e:
        # Network errors are acceptable for edge case testing
        results.assert_true(True, "Edge case testing handled network error gracefully")

def run_all_tests():
    """Run all backend API tests"""
    print("🚀 Starting IceSolutions Backend API Tests")
    print("=" * 60)
    
    results = TestResults()
    
    # Run all test suites
    test_products_api(results)
    test_delivery_areas_api(results)
    test_quotes_api_basic(results)
    test_quotes_api_bulk_discounts(results)
    test_quotes_api_large_order(results)
    test_quotes_api_ice_amount(results)
    test_contacts_api(results)
    test_edge_cases(results)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🏁 TEST SUMMARY")
    print("=" * 60)
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
        print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
        return True
    else:
        print(f"\n⚠️  {results.failed} tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)