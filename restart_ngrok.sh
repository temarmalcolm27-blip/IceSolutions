#!/bin/bash
# Ngrok Restart Helper Script

echo "🔄 Restarting ngrok tunnel..."
echo ""

# Kill existing ngrok processes
pkill ngrok
sleep 2

# Start new tunnel on port 8001 (backend)
nohup ngrok http 8001 > /tmp/ngrok.log 2>&1 &
echo "⏳ Starting ngrok... (waiting 5 seconds)"
sleep 5

# Get public URL
URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -z "$URL" ]; then
    echo "❌ Failed to start ngrok"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if ngrok is installed: ngrok version"
    echo "2. Check logs: cat /tmp/ngrok.log"
    echo "3. Try manually: ngrok http 8001"
    exit 1
fi

echo "✅ Ngrok is running!"
echo ""
echo "📡 Public URL: $URL"
echo "🔌 Local Port: 8001 (backend API)"
echo ""

# Check if URL is different from .env
CURRENT_URL=$(grep "PUBLIC_URL=" /app/backend/.env | cut -d'"' -f2)

if [ "$URL" != "$CURRENT_URL" ]; then
    echo "⚠️  WARNING: URL has changed!"
    echo ""
    echo "Old URL: $CURRENT_URL"
    echo "New URL: $URL"
    echo ""
    echo "You need to update /app/backend/.env:"
    echo "PUBLIC_URL=\"$URL\""
    echo ""
    echo "Then restart backend:"
    echo "sudo supervisorctl restart backend"
else
    echo "✅ URL matches .env file - no update needed"
fi

echo ""
echo "🧪 Test the endpoint:"
echo "curl -I $URL/api/conversational-ai/handle"
echo ""
echo "📞 Make a test call:"
echo "curl -X POST \"http://localhost:8001/api/leads/call/876-XXX-XXXX?lead_name=Test\""
echo ""
