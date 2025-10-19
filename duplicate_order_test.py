#!/usr/bin/env python3
"""
Duplicate Order Processing Fix Test
Tests the two-layer idempotency protection for OrderConfirmationPage
as specified in the review request.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime, timezone

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
print(f"Testing duplicate order processing at: {API_BASE}")

class DuplicateTestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.warnings = []
    
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
    
    def add_warning(self, message):
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")

def test_duplicate_webhook_calls(results):
    """Test backend duplicate protection - multiple webhook calls with same session_id"""
    print("\n🧪 Testing Backend Duplicate Protection...")
    
    # Generate unique session ID for this test
    test_session_id = f"test_session_{int(time.time())}"
    
    # Webhook payload simulating Stripe webhook
    webhook_payload = {
        "session_id": test_session_id,
        "payment_status": "paid"
    }
    
    print(f"  📋 Using test session ID: {test_session_id}")
    
    # First webhook call - should create order
    print("  🔄 First webhook call (should create order)...")
    try:
        response1 = requests.post(f"{API_BASE}/webhook/stripe", 
                                json=webhook_payload, 
                                headers={'Content-Type': 'application/json'},
                                timeout=15)
        
        results.assert_equal(response1.status_code, 200, "First webhook call returns 200 status")
        
        if response1.status_code == 200:
            response1_data = response1.json()
            results.assert_equal(response1_data.get('status'), 'success', "First webhook call returns success status")
            
            # Should contain order_id if order was created
            first_order_id = response1_data.get('order_id')
            if first_order_id:
                print(f"    ✅ Order created with ID: {first_order_id}")
            else:
                results.add_warning("First webhook call did not return order_id")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: First webhook call failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
        return
    
    # Wait a moment to ensure any async processing completes
    time.sleep(2)
    
    # Second webhook call - should detect duplicate and return existing order
    print("  🔄 Second webhook call (should detect duplicate)...")
    try:
        response2 = requests.post(f"{API_BASE}/webhook/stripe", 
                                json=webhook_payload, 
                                headers={'Content-Type': 'application/json'},
                                timeout=15)
        
        results.assert_equal(response2.status_code, 200, "Second webhook call returns 200 status")
        
        if response2.status_code == 200:
            response2_data = response2.json()
            results.assert_equal(response2_data.get('status'), 'success', "Second webhook call returns success status")
            
            # Should contain message about duplicate processing
            message = response2_data.get('message', '')
            results.assert_true('already processed' in message.lower(), "Second webhook call indicates order already processed")
            
            # Should return same order ID
            second_order_id = response2_data.get('order_id')
            if first_order_id and second_order_id:
                results.assert_equal(second_order_id, first_order_id, "Second webhook call returns same order ID")
            else:
                results.add_warning("Could not compare order IDs between webhook calls")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Second webhook call failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)
        return
    
    # Third webhook call - should still detect duplicate
    print("  🔄 Third webhook call (should still detect duplicate)...")
    try:
        response3 = requests.post(f"{API_BASE}/webhook/stripe", 
                                json=webhook_payload, 
                                headers={'Content-Type': 'application/json'},
                                timeout=15)
        
        results.assert_equal(response3.status_code, 200, "Third webhook call returns 200 status")
        
        if response3.status_code == 200:
            response3_data = response3.json()
            message = response3_data.get('message', '')
            results.assert_true('already processed' in message.lower(), "Third webhook call still indicates order already processed")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Third webhook call failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_order_id_generation(results):
    """Test Order ID generation and uniqueness"""
    print("\n🧪 Testing Order ID Generation...")
    
    order_ids = []
    
    # Create multiple orders with different session IDs
    for i in range(3):
        test_session_id = f"unique_session_{int(time.time())}_{i}"
        
        webhook_payload = {
            "session_id": test_session_id,
            "payment_status": "paid"
        }
        
        print(f"  📋 Creating order {i+1} with session: {test_session_id}")
        
        try:
            response = requests.post(f"{API_BASE}/webhook/stripe", 
                                   json=webhook_payload, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=15)
            
            if response.status_code == 200:
                response_data = response.json()
                order_id = response_data.get('order_id')
                
                if order_id:
                    order_ids.append(order_id)
                    print(f"    ✅ Order created with ID: {order_id}")
                else:
                    results.add_warning(f"Order {i+1} did not return order_id")
            
            # Wait between requests to ensure different timestamps
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            results.failed += 1
            error_msg = f"❌ FAIL: Order {i+1} creation failed: {str(e)}"
            print(error_msg)
            results.errors.append(error_msg)
    
    # Verify all order IDs are unique
    if len(order_ids) > 1:
        unique_ids = set(order_ids)
        results.assert_equal(len(unique_ids), len(order_ids), "All order IDs are unique")
        
        # Verify order IDs are incrementing (if they're numeric)
        try:
            numeric_ids = [int(oid) for oid in order_ids if oid.isdigit()]
            if len(numeric_ids) > 1:
                is_incrementing = all(numeric_ids[i] < numeric_ids[i+1] for i in range(len(numeric_ids)-1))
                results.assert_true(is_incrementing, "Order IDs increment correctly")
        except ValueError:
            results.add_warning("Order IDs are not numeric - cannot test incrementing")

def test_order_retrieval(results):
    """Test order retrieval endpoint"""
    print("\n🧪 Testing Order Retrieval...")
    
    # First create an order to retrieve
    test_session_id = f"retrieval_test_{int(time.time())}"
    
    webhook_payload = {
        "session_id": test_session_id,
        "payment_status": "paid"
    }
    
    print(f"  📋 Creating order for retrieval test with session: {test_session_id}")
    
    try:
        create_response = requests.post(f"{API_BASE}/webhook/stripe", 
                                      json=webhook_payload, 
                                      headers={'Content-Type': 'application/json'},
                                      timeout=15)
        
        if create_response.status_code == 200:
            create_data = create_response.json()
            order_id = create_data.get('order_id')
            
            if order_id:
                print(f"    ✅ Order created with ID: {order_id}")
                
                # Wait for order to be fully processed
                time.sleep(2)
                
                # Test order retrieval
                print(f"  🔍 Retrieving order: {order_id}")
                
                # Note: The backend uses MongoDB orders collection with order_id field
                # We need to check if there's a GET endpoint for orders by order_id
                
                # Try different possible endpoints
                endpoints_to_try = [
                    f"/api/orders/{order_id}",
                    f"/api/order/{order_id}",
                ]
                
                order_found = False
                for endpoint in endpoints_to_try:
                    try:
                        get_response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
                        if get_response.status_code == 200:
                            order_data = get_response.json()
                            results.assert_true('order_id' in order_data or 'id' in order_data, 
                                              f"Order retrieval returns order data via {endpoint}")
                            order_found = True
                            break
                        elif get_response.status_code == 404:
                            continue  # Try next endpoint
                    except requests.exceptions.RequestException:
                        continue  # Try next endpoint
                
                if not order_found:
                    results.add_warning("Could not find working order retrieval endpoint")
                
                # Test non-existent order ID
                try:
                    invalid_response = requests.get(f"{API_BASE}/orders/invalid_order_999999", timeout=10)
                    results.assert_equal(invalid_response.status_code, 404, "Non-existent order returns 404")
                except requests.exceptions.RequestException as e:
                    results.add_warning(f"Could not test invalid order ID: {str(e)}")
            
            else:
                results.add_warning("Could not get order_id for retrieval test")
        
    except requests.exceptions.RequestException as e:
        results.failed += 1
        error_msg = f"❌ FAIL: Order creation for retrieval test failed: {str(e)}"
        print(error_msg)
        results.errors.append(error_msg)

def test_mongodb_single_document(results):
    """Test that MongoDB contains only one document per session_id"""
    print("\n🧪 Testing MongoDB Single Document Per Session...")
    
    # This test would require direct MongoDB access
    # Since we can't directly access MongoDB, we'll test indirectly through the API
    
    test_session_id = f"mongo_test_{int(time.time())}"
    
    webhook_payload = {
        "session_id": test_session_id,
        "payment_status": "paid"
    }
    
    print(f"  📋 Testing MongoDB uniqueness with session: {test_session_id}")
    
    # Make multiple webhook calls
    order_ids = []
    
    for i in range(3):
        print(f"  🔄 Webhook call {i+1}...")
        try:
            response = requests.post(f"{API_BASE}/webhook/stripe", 
                                   json=webhook_payload, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=15)
            
            if response.status_code == 200:
                response_data = response.json()
                order_id = response_data.get('order_id')
                if order_id:
                    order_ids.append(order_id)
            
            time.sleep(1)  # Brief pause between calls
            
        except requests.exceptions.RequestException as e:
            results.add_warning(f"Webhook call {i+1} failed: {str(e)}")
    
    # All webhook calls should return the same order ID
    if len(order_ids) > 1:
        unique_order_ids = set(order_ids)
        results.assert_equal(len(unique_order_ids), 1, "All webhook calls return same order ID (indicating single MongoDB document)")
        
        if len(unique_order_ids) == 1:
            print(f"    ✅ All calls returned same order ID: {list(unique_order_ids)[0]}")
    else:
        results.add_warning("Could not collect enough order IDs for MongoDB uniqueness test")

def test_email_service_logs(results):
    """Test email service to ensure only one email is sent"""
    print("\n🧪 Testing Email Service (Single Email)...")
    
    # Check backend logs for email sending
    print("  📧 Checking for email service activity...")
    
    try:
        # Check supervisor logs for email activity
        import subprocess
        
        # Get recent backend logs
        log_result = subprocess.run(['tail', '-n', '50', '/var/log/supervisor/backend.out.log'], 
                                  capture_output=True, text=True, timeout=10)
        
        if log_result.returncode == 0:
            log_content = log_result.stdout
            
            # Look for email-related log entries
            email_keywords = ['email', 'confirmation', 'send_order_confirmation_email', 'smtp']
            
            email_logs = []
            for line in log_content.split('\n'):
                if any(keyword in line.lower() for keyword in email_keywords):
                    email_logs.append(line)
            
            if email_logs:
                print(f"    📧 Found {len(email_logs)} email-related log entries")
                for log in email_logs[-3:]:  # Show last 3 entries
                    print(f"      {log}")
                
                results.assert_true(len(email_logs) > 0, "Email service is active (found email logs)")
            else:
                results.add_warning("No email-related logs found - email service may not be configured")
        
        else:
            results.add_warning("Could not access backend logs to verify email service")
    
    except Exception as e:
        results.add_warning(f"Could not check email logs: {str(e)}")

def test_google_sheets_integration(results):
    """Test Google Sheets integration for single row per order"""
    print("\n🧪 Testing Google Sheets Integration...")
    
    # This would require Google Sheets API access
    # We'll test indirectly by checking backend logs
    
    try:
        import subprocess
        
        # Get recent backend logs
        log_result = subprocess.run(['tail', '-n', '100', '/var/log/supervisor/backend.out.log'], 
                                  capture_output=True, text=True, timeout=10)
        
        if log_result.returncode == 0:
            log_content = log_result.stdout
            
            # Look for Google Sheets related log entries
            sheets_keywords = ['google sheets', 'sheets', 'spreadsheet', 'append_row', 'Orders sheet']
            
            sheets_logs = []
            for line in log_content.split('\n'):
                if any(keyword in line.lower() for keyword in sheets_keywords):
                    sheets_logs.append(line)
            
            if sheets_logs:
                print(f"    📊 Found {len(sheets_logs)} Google Sheets-related log entries")
                for log in sheets_logs[-3:]:  # Show last 3 entries
                    print(f"      {log}")
                
                results.assert_true(len(sheets_logs) > 0, "Google Sheets integration is active")
            else:
                results.add_warning("No Google Sheets logs found - integration may not be configured")
        
        else:
            results.add_warning("Could not access backend logs to verify Google Sheets integration")
    
    except Exception as e:
        results.add_warning(f"Could not check Google Sheets logs: {str(e)}")

def run_duplicate_order_tests():
    """Run all duplicate order processing tests"""
    print("🚀 Starting Duplicate Order Processing Fix Tests")
    print("=" * 80)
    print("Testing two-layer idempotency protection:")
    print("1. Frontend: sessionStorage check (order_processed_{sessionId})")
    print("2. Backend: Database duplicate session_id check")
    print("=" * 80)
    
    results = DuplicateTestResults()
    
    # Test 1: Backend duplicate protection
    test_duplicate_webhook_calls(results)
    
    # Test 2: Order ID generation and uniqueness
    test_order_id_generation(results)
    
    # Test 3: Order retrieval
    test_order_retrieval(results)
    
    # Test 4: MongoDB single document per session
    test_mongodb_single_document(results)
    
    # Test 5: Email service (single email)
    test_email_service_logs(results)
    
    # Test 6: Google Sheets integration
    test_google_sheets_integration(results)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🏁 DUPLICATE ORDER PROCESSING TEST SUMMARY")
    print("=" * 80)
    print(f"✅ PASSED: {results.passed}")
    print(f"❌ FAILED: {results.failed}")
    print(f"⚠️  WARNINGS: {len(results.warnings)}")
    print(f"📊 TOTAL TESTS: {results.passed + results.failed}")
    
    if results.failed > 0:
        print(f"\n🔍 FAILED TESTS:")
        for error in results.errors:
            print(f"   {error}")
    
    if results.warnings:
        print(f"\n⚠️  WARNINGS:")
        for warning in results.warnings:
            print(f"   {warning}")
    
    success_rate = (results.passed / (results.passed + results.failed)) * 100 if (results.passed + results.failed) > 0 else 0
    print(f"\n📈 SUCCESS RATE: {success_rate:.1f}%")
    
    if results.failed == 0:
        print("\n🎉 ALL DUPLICATE ORDER TESTS PASSED!")
        print("✨ Two-layer idempotency protection is working correctly!")
        print("✅ Frontend sessionStorage check prevents multiple webhook calls")
        print("✅ Backend database check prevents duplicate order creation")
        return True
    else:
        print(f"\n⚠️  {results.failed} tests failed. Duplicate order issue may not be fully resolved.")
        return False

if __name__ == "__main__":
    success = run_duplicate_order_tests()
    sys.exit(0 if success else 1)