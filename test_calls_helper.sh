#!/bin/bash

# Ice Solutions - Sales Agent Testing Helper Script
# This script helps you easily test the calling system

echo "================================================"
echo "🧊 Ice Solutions - Sales Agent Testing Helper"
echo "================================================"
echo ""

# Function to make a call
make_call() {
    PHONE=$1
    BUSINESS_NAME=$2
    
    if [ -z "$PHONE" ] || [ -z "$BUSINESS_NAME" ]; then
        echo "❌ Error: Phone number and business name required"
        echo "Usage: make_call 876-XXX-XXXX \"Business Name\""
        return 1
    fi
    
    echo "📞 Initiating call to: $BUSINESS_NAME ($PHONE)"
    echo ""
    
    # URL encode the business name
    ENCODED_NAME=$(echo "$BUSINESS_NAME" | sed 's/ /%20/g' | sed "s/'/%27/g")
    
    # Make the API call
    RESPONSE=$(curl -s -X POST "http://localhost:8001/api/leads/call/$PHONE?lead_name=$ENCODED_NAME")
    
    echo "Response:"
    echo "$RESPONSE" | python3 -m json.tool
    echo ""
    
    # Check if successful
    if echo "$RESPONSE" | grep -q "success"; then
        echo "✅ Call initiated successfully!"
        echo "📱 The number should receive a call from: (229) 600-5631"
        echo "🎙️ Marcus will deliver the sales message"
    else
        echo "❌ Call failed. Check the error message above."
    fi
}

# Function to view all leads
view_leads() {
    echo "📋 Fetching all leads..."
    echo ""
    curl -s "http://localhost:8001/api/leads" | python3 -m json.tool | head -100
}

# Function to view stats
view_stats() {
    echo "📊 Fetching lead statistics..."
    echo ""
    curl -s "http://localhost:8001/api/leads/stats" | python3 -m json.tool
}

# Function to sync from Google Sheets
sync_leads() {
    echo "🔄 Syncing leads from Google Sheets..."
    echo ""
    curl -s "http://localhost:8001/api/leads/sync" | python3 -m json.tool
}

# Function to update call result
update_result() {
    PHONE=$1
    STATUS=$2
    NOTES=$3
    RESULT=$4
    
    if [ -z "$PHONE" ] || [ -z "$STATUS" ]; then
        echo "❌ Error: Phone number and status required"
        echo "Usage: update_result 876-XXX-XXXX \"Contacted\" \"Notes\" \"Result\""
        return 1
    fi
    
    echo "✏️ Updating lead: $PHONE"
    echo ""
    
    JSON_DATA=$(cat <<EOF
{
  "status": "$STATUS",
  "call_notes": "$NOTES",
  "result": "$RESULT"
}
EOF
)
    
    curl -s -X POST "http://localhost:8001/api/leads/update/$PHONE" \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" | python3 -m json.tool
    
    echo ""
    echo "✅ Lead updated!"
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1. View all leads"
    echo "2. View statistics"
    echo "3. Sync leads from Google Sheets"
    echo "4. Make a test call"
    echo "5. Update call result"
    echo "6. View Marcus's script"
    echo "7. Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            view_leads
            show_menu
            ;;
        2)
            view_stats
            show_menu
            ;;
        3)
            sync_leads
            show_menu
            ;;
        4)
            echo ""
            read -p "Enter phone number (876-XXX-XXXX): " phone
            read -p "Enter business name: " business
            make_call "$phone" "$business"
            show_menu
            ;;
        5)
            echo ""
            read -p "Enter phone number (876-XXX-XXXX): " phone
            read -p "Enter status (Contacted/Interested/Not Interested/Sold): " status
            read -p "Enter call notes: " notes
            read -p "Enter result: " result
            update_result "$phone" "$status" "$notes" "$result"
            show_menu
            ;;
        6)
            echo ""
            echo "🎙️ MARCUS'S CALL SCRIPT:"
            echo "========================"
            echo ""
            echo "Hello, this is Marcus from Ice Solutions."
            echo "We provide party ice deliveries for businesses in the corporate area"
            echo "and Kingston at a reasonable price."
            echo ""
            echo "[pause]"
            echo ""
            echo "We provide crystal-clear, restaurant-quality ice delivered fresh to your door."
            echo "Our 10-pound bags start at just 350 Jamaican dollars,"
            echo "with great bulk discounts available."
            echo ""
            echo "[pause]"
            echo ""
            echo "Whether you're planning a party, running a bar, or need ice for an event,"
            echo "we can help. We offer same-day delivery, and it's FREE in Washington Gardens!"
            echo ""
            echo "[pause]"
            echo ""
            echo "For more information or to place an order,"
            echo "please call us at 8 7 6, 4 9 0, 7 2 0 8."
            echo "That's 8 7 6, 4 9 0, 7 2 0 8."
            echo ""
            echo "[pause]"
            echo ""
            echo "You can also order online at our website."
            echo "Remember, More Ice equals More Vibes!"
            echo "Thank you and have a great day!"
            echo ""
            echo "========================"
            show_menu
            ;;
        7)
            echo ""
            echo "👋 Thank you for using Ice Solutions!"
            echo "🧊 More Ice = More Vibes!"
            echo ""
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Quick test mode
if [ "$1" == "quick-test" ]; then
    if [ -z "$2" ] || [ -z "$3" ]; then
        echo "Usage: $0 quick-test 876-XXX-XXXX \"Business Name\""
        exit 1
    fi
    make_call "$2" "$3"
    exit 0
fi

# Start the menu
show_menu
