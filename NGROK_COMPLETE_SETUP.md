# 🌐 Ngrok Complete Setup Guide

## ✅ What We Just Did

Successfully installed and configured ngrok to expose the conversational AI backend publicly.

---

## 📋 Installation Summary

### 1. Installed Ngrok
```bash
cd /tmp
curl -L https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz -o ngrok.tgz
tar -xzf ngrok.tgz
sudo mv ngrok /usr/local/bin/
sudo chmod +x /usr/local/bin/ngrok
```

**Verification**:
```bash
ngrok version
# Output: ngrok version 3.30.0
```

### 2. Started Ngrok Tunnel
```bash
nohup ngrok http 8001 > /tmp/ngrok.log 2>&1 &
```

**Why port 8001?**
- Port 8001 = Your FastAPI backend (where conversational AI endpoints are)
- Port 8080 = WebSocket server (not used with HTTP approach)
- Port 3000 = React frontend (not needed for calls)

### 3. Verified Public URL
```bash
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool
```

**Current URL**: `https://criticizable-newton-overplausibly.ngrok-free.dev`

---

## 🔧 Current Configuration

| Component | Value | Status |
|-----------|-------|--------|
| Ngrok Binary | `/usr/local/bin/ngrok` | ✅ Installed |
| Ngrok Version | 3.30.0 | ✅ Latest |
| Local Port | 8001 | ✅ Backend API |
| Public URL | criticizable-newton-overplausibly.ngrok-free.dev | ✅ Active |
| Auth Token | Not configured (free tier) | ⚠️ May change |

---

## 🎯 How It Works

```
Twilio Call → Public Internet → Ngrok Tunnel → Backend (8001) → Conversational AI
```

**Flow**:
1. Twilio initiates call to your number
2. Plays Marcus's greeting
3. Captures your speech
4. Sends to: `https://criticizable-newton-overplausibly.ngrok-free.dev/api/conversational-ai/handle`
5. Ngrok forwards to: `http://localhost:8001/api/conversational-ai/handle`
6. Your backend processes with GPT-4
7. Returns TwiML with Marcus's response
8. Loop continues until conversation ends

---

## 📱 Testing Commands

### Check if Ngrok is Running
```bash
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool | grep "public_url"
```

### Test Endpoint is Accessible
```bash
curl -I https://criticizable-newton-overplausibly.ngrok-free.dev/api/conversational-ai/handle
# Should return: HTTP/2 405 (correct - it expects POST)
```

### Make a Test Call
```bash
curl -X POST "http://localhost:8001/api/leads/call/876-XXX-XXXX?lead_name=Business%20Name"
```

### Monitor Backend Logs (See Conversation)
```bash
tail -f /var/log/supervisor/backend.err.log | grep -E "Customer:|Marcus:"
```

---

## 🔄 Restarting Ngrok

If ngrok stops or you need to restart:

### Method 1: Quick Restart
```bash
# Kill existing
pkill ngrok

# Start new tunnel
nohup ngrok http 8001 > /tmp/ngrok.log 2>&1 &

# Wait for it to start
sleep 5

# Get new URL
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool | grep "public_url"
```

### Method 2: If URL Changes
If the public URL changes (different random subdomain):

```bash
# Get new URL
NEW_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])")

# Update .env
echo "New URL: $NEW_URL"
# Manually edit /app/backend/.env and update PUBLIC_URL

# Restart backend
sudo supervisorctl restart backend
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- URL changes on every restart (random subdomain)
- Session expires after 2 hours
- No authentication (anyone can call the URL)

### Recommended for Production
Get a paid ngrok account ($8/month) for:
- Static domain (doesn't change)
- No session timeout
- Better security

**Or use a production setup**:
- Deploy to cloud (AWS, Google Cloud, DigitalOcean)
- Use real domain with SSL
- No ngrok needed

---

## 🛠️ Helper Script

I'll create a helper script to make this easier:

```bash
#!/bin/bash
# /app/restart_ngrok.sh

echo "🔄 Restarting ngrok..."

# Kill existing
pkill ngrok
sleep 2

# Start new tunnel
nohup ngrok http 8001 > /tmp/ngrok.log 2>&1 &
sleep 5

# Get URL
URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -z "$URL" ]; then
    echo "❌ Failed to start ngrok"
    exit 1
fi

echo "✅ Ngrok running on: $URL"
echo ""
echo "If this is a new URL, update /app/backend/.env:"
echo "PUBLIC_URL=\"$URL\""
echo ""
echo "Then restart backend:"
echo "sudo supervisorctl restart backend"
```

---

## 📞 Testing Checklist

After setup, verify:

- [ ] Ngrok is running: `ps aux | grep ngrok`
- [ ] URL is accessible: `curl -I YOUR_NGROK_URL/api/conversational-ai/handle`
- [ ] Backend is running: `sudo supervisorctl status backend`
- [ ] Make test call: Call responds and continues conversation
- [ ] Monitor logs: See "Customer:" and "Marcus:" in logs

---

## 🔍 Troubleshooting

### Issue: "ERR_NGROK_4018 - authentication required"
**Cause**: Ngrok v3 requires auth token for some features
**Solution**: 
- Sign up at https://dashboard.ngrok.com/signup
- Get auth token
- Run: `ngrok config add-authtoken YOUR_TOKEN`

### Issue: "Connection refused" or "404 Not Found"
**Cause**: Ngrok pointing to wrong port
**Solution**: Make sure using port 8001 (not 8080)
```bash
ngrok http 8001  # NOT 8080
```

### Issue: "Ngrok tunnel expired"
**Cause**: Free tier sessions timeout after 2 hours
**Solution**: Restart ngrok (see restart commands above)

### Issue: "Can't reach localhost:4040"
**Cause**: Ngrok's web interface not available
**Solution**: 
```bash
pkill ngrok
ngrok http 8001
# Don't use nohup for debugging
```

---

## 🎉 Current Status

✅ **Ngrok is properly installed and configured**
✅ **Pointing to correct port (8001)**
✅ **Public URL is active**
✅ **Backend can receive Twilio webhooks**
✅ **Conversational AI is ready**

**Your next test call should have full conversation capability!**

---

## 🚀 Next Steps

1. **Answer your test call**
2. **Respond to Marcus** and see if conversation continues
3. **Monitor logs** to see the conversation flow
4. **Test different scenarios**
5. **If working**: Test on friendly businesses
6. **If not working**: Check troubleshooting section above

**More Ice = More Vibes! 🧊**
