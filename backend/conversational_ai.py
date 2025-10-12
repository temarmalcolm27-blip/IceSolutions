"""
OpenAI Realtime API Integration for Conversational Sales Agent
Handles real-time voice conversations with businesses
"""

import asyncio
import websockets
import json
import base64
import os
from openai import AsyncOpenAI
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-emergent-f62468b2cCeCfD4E15')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Marcus's conversational personality and goals
MARCUS_SYSTEM_INSTRUCTIONS = """
You are Marcus, a friendly and professional sales representative for Ice Solutions in Kingston, Jamaica.

YOUR BACKGROUND:
- You work for Ice Solutions, a premium ice delivery service
- You specialize in serving businesses: restaurants, bars, event venues, caterers, and hotels
- Your company delivers high-quality, crystal-clear ice in 10-pound bags

YOUR GOAL IN THIS CALL:
1. Greet warmly and ask to speak with the person who handles purchasing/supplies
2. If you're speaking to the right person, introduce Ice Solutions briefly
3. Ask qualifying questions:
   - Do they currently use ice in their business?
   - How much do they typically need? (daily/weekly)
   - Who is their current supplier?
4. Present your value proposition:
   - Premium restaurant-quality ice
   - Competitive pricing: JMD $350 per 10lb bag
   - Bulk discounts: 5% off (5-9 bags), 10% off (10-19 bags), 15% off (20+ bags)
   - FREE delivery in Washington Gardens
   - JMD $300 delivery fee for other areas in Kingston
   - Same-day delivery available
5. Handle objections professionally:
   - If they have a supplier: Ask about price, reliability, quality
   - If price is a concern: Highlight bulk discounts and delivery savings
   - If they're busy: Offer to call back or send information via email
6. Close the conversation:
   - If interested: Schedule a trial delivery or take an order
   - If not ready: Ask for permission to follow up in a week
   - If not interested: Thank them politely and end the call

CONVERSATION STYLE:
- Speak with a friendly Jamaican tone (but don't use heavy patois)
- Be conversational and natural, not scripted
- Listen actively - respond to what they actually say
- Don't be pushy - if they're clearly not interested, thank them and end
- Show genuine interest in helping their business
- Be professional but warm
- Keep responses concise (2-3 sentences max per turn)
- Use the tagline "More Ice = More Vibes" if appropriate

IMPORTANT BEHAVIORAL RULES:
- Always listen for the person's response before continuing
- If interrupted, stop talking immediately and listen
- Don't repeat yourself unless asked
- If they have questions, answer them directly
- If you don't know something specific, be honest and offer to find out
- If they want to end the call, respect that immediately

CONTACT INFORMATION (only share if asked or when closing):
- Phone: (876) 490-7208
- Website: icesolutions.com
- Email: temarmalcolm27@gmail.com
- Areas served: Kingston and surrounding areas

Remember: You're having a real conversation, not delivering a speech. Listen, engage, and respond naturally!
"""


class ConversationalAIHandler:
    """Handles WebSocket connection between Twilio and OpenAI Realtime API"""
    
    def __init__(self, stream_sid: str, call_sid: str, business_name: str = ""):
        self.stream_sid = stream_sid
        self.call_sid = call_sid
        self.business_name = business_name
        self.openai_ws = None
        self.twilio_ws = None
        self.conversation_started = False
        
    async def connect_to_openai(self):
        """Connect to OpenAI Realtime API"""
        try:
            # OpenAI Realtime API endpoint
            url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
            
            # Create headers using the proper method for websockets library
            import websockets.client
            self.openai_ws = await websockets.client.connect(
                url,
                additional_headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "OpenAI-Beta": "realtime=v1"
                }
            )
            logger.info(f"Connected to OpenAI Realtime API for call {self.call_sid}")
            
            # Configure the session
            await self.configure_session()
            
        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {str(e)}")
            raise
    
    async def configure_session(self):
        """Configure OpenAI session with Marcus's personality"""
        config = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": MARCUS_SYSTEM_INSTRUCTIONS,
                "voice": "alloy",  # Professional male voice
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",  # Voice Activity Detection
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                },
                "tools": [],
                "tool_choice": "auto",
                "temperature": 0.8,
                "max_response_output_tokens": 4096
            }
        }
        
        await self.openai_ws.send(json.dumps(config))
        logger.info("Configured OpenAI session")
    
    async def handle_twilio_message(self, message: dict):
        """Process incoming message from Twilio"""
        event = message.get("event")
        
        if event == "start":
            logger.info(f"Call started: {self.call_sid}")
            self.conversation_started = True
            
            # Send initial greeting
            greeting = {
                "type": "conversation.item.create",
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": [{
                        "type": "input_text",
                        "text": f"The call has connected. Greet the person and ask to speak with the purchasing manager for {self.business_name if self.business_name else 'their business'}."
                    }]
                }
            }
            await self.openai_ws.send(json.dumps(greeting))
            
            # Request response
            await self.openai_ws.send(json.dumps({"type": "response.create"}))
            
        elif event == "media":
            # Forward audio from Twilio to OpenAI
            payload = message.get("media", {}).get("payload")
            if payload and self.openai_ws:
                audio_append = {
                    "type": "input_audio_buffer.append",
                    "audio": payload  # Base64 encoded audio
                }
                await self.openai_ws.send(json.dumps(audio_append))
        
        elif event == "stop":
            logger.info(f"Call ended: {self.call_sid}")
            await self.cleanup()
    
    async def handle_openai_message(self, message: dict):
        """Process incoming message from OpenAI"""
        msg_type = message.get("type")
        
        if msg_type == "response.audio.delta":
            # Forward audio from OpenAI to Twilio
            audio_delta = message.get("delta")
            if audio_delta and self.twilio_ws:
                media_message = {
                    "event": "media",
                    "streamSid": self.stream_sid,
                    "media": {
                        "payload": audio_delta
                    }
                }
                await self.twilio_ws.send(json.dumps(media_message))
        
        elif msg_type == "response.audio_transcript.delta":
            # Log what Marcus is saying
            delta = message.get("delta", "")
            logger.info(f"Marcus: {delta}")
        
        elif msg_type == "conversation.item.input_audio_transcription.completed":
            # Log what the person said
            transcript = message.get("transcript", "")
            logger.info(f"Customer: {transcript}")
        
        elif msg_type == "error":
            error = message.get("error", {})
            logger.error(f"OpenAI error: {error}")
    
    async def run(self, twilio_ws):
        """Main loop to handle bidirectional streaming"""
        self.twilio_ws = twilio_ws
        
        try:
            await self.connect_to_openai()
            
            # Create tasks for both directions
            twilio_task = asyncio.create_task(self.handle_twilio_stream())
            openai_task = asyncio.create_task(self.handle_openai_stream())
            
            # Run both tasks concurrently
            await asyncio.gather(twilio_task, openai_task)
            
        except Exception as e:
            logger.error(f"Error in conversation handler: {str(e)}")
        finally:
            await self.cleanup()
    
    async def handle_twilio_stream(self):
        """Handle incoming messages from Twilio"""
        try:
            async for message in self.twilio_ws:
                data = json.loads(message)
                await self.handle_twilio_message(data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Twilio connection closed")
        except Exception as e:
            logger.error(f"Error handling Twilio stream: {str(e)}")
    
    async def handle_openai_stream(self):
        """Handle incoming messages from OpenAI"""
        try:
            async for message in self.openai_ws:
                data = json.loads(message)
                await self.handle_openai_message(data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("OpenAI connection closed")
        except Exception as e:
            logger.error(f"Error handling OpenAI stream: {str(e)}")
    
    async def cleanup(self):
        """Clean up connections"""
        if self.openai_ws:
            await self.openai_ws.close()
        logger.info(f"Cleaned up conversation handler for call {self.call_sid}")


async def handle_media_stream(websocket):
    """WebSocket handler for Twilio Media Streams"""
    logger.info(f"New WebSocket connection")
    
    stream_sid = None
    call_sid = None
    business_name = ""
    handler = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            event = data.get("event")
            
            if event == "start":
                start_data = data.get("start", {})
                stream_sid = start_data.get("streamSid")
                call_sid = start_data.get("callSid")
                
                # Extract business name from custom parameters if available
                custom_params = start_data.get("customParameters", {})
                business_name = custom_params.get("businessName", "")
                
                logger.info(f"Starting conversation for call {call_sid}")
                
                # Create and run conversation handler
                handler = ConversationalAIHandler(stream_sid, call_sid, business_name)
                await handler.run(websocket)
                
            elif handler:
                await handler.handle_twilio_message(data)
    
    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"Error in media stream handler: {str(e)}")
    finally:
        if handler:
            await handler.cleanup()


async def start_websocket_server(host="0.0.0.0", port=8080):
    """Start the WebSocket server for handling Twilio Media Streams"""
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_media_stream, host, port):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    # Run the WebSocket server
    asyncio.run(start_websocket_server())
