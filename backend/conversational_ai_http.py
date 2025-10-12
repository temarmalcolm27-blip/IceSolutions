"""
HTTP-based Conversational AI using OpenAI APIs
More reliable alternative to WebSocket Realtime API
"""

import os
import logging
from typing import List, Dict
from openai import OpenAI
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-emergent-f62468b2cCeCfD4E15')
client = OpenAI(api_key=OPENAI_API_KEY)

# Marcus's conversation context
MARCUS_SYSTEM_PROMPT = """You are Marcus, a friendly and professional sales representative for Ice Solutions in Kingston, Jamaica.

YOUR ROLE:
You're having a phone conversation with a business owner or manager. Your goal is to qualify them and sell ice delivery services.

YOUR PERSONALITY:
- Warm and professional Jamaican tone (but not heavy patois)
- Conversational and natural
- Good listener who responds to what they actually say
- Helpful and consultative, not pushy
- Persistent but respectful

CONVERSATION FLOW:
1. Opening: Greet and ask to speak with purchasing manager
2. Qualification: Ask about their ice needs and current supplier
3. Presentation: Share pricing and benefits based on their needs
4. Handle objections professionally
5. Close: Try to schedule delivery or get permission to follow up

KEY INFORMATION:
- Product: Premium restaurant-quality ice in 10lb bags
- Price: JMD $350 per bag
- Bulk discounts: 5% (5-9 bags), 10% (10-19 bags), 15% (20+ bags)
- FREE delivery in Washington Gardens
- JMD $300 delivery fee for other Kingston areas
- Same-day delivery available
- Contact: (876) 490-7208, icesolutions.com

IMPORTANT RULES:
- Keep responses SHORT (1-3 sentences max)
- Don't repeat yourself unless asked
- Listen and adapt to their responses
- If they're clearly not interested, thank them and end politely
- If they're busy, offer to call back
- Be conversational, not scripted

Remember: This is a real phone conversation. Speak naturally like you would to a business owner you're trying to help."""

# Store conversation history in memory (in production, use Redis or database)
conversation_store = {}

class ConversationManager:
    """Manages conversational state for each call"""
    
    def __init__(self, call_sid: str, business_name: str = ""):
        self.call_sid = call_sid
        self.business_name = business_name
        self.conversation_history: List[Dict] = []
        self.turn_count = 0
        self.started_at = datetime.now(timezone.utc)
        
        # Initialize with system prompt
        self.conversation_history.append({
            "role": "system",
            "content": MARCUS_SYSTEM_PROMPT
        })
        
        # Add initial context
        if business_name:
            self.conversation_history.append({
                "role": "system",
                "content": f"You are calling {business_name}. Start by greeting them and asking to speak with the purchasing manager."
            })
    
    def add_user_message(self, message: str):
        """Add what the person said"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self.turn_count += 1
        logger.info(f"[{self.call_sid}] Customer: {message}")
    
    def add_assistant_message(self, message: str):
        """Add what Marcus said"""
        self.conversation_history.append({
            "role": "assistant",
            "content": message
        })
        logger.info(f"[{self.call_sid}] Marcus: {message}")
    
    def get_response(self, user_input: str = None) -> str:
        """Get Marcus's response to user input"""
        try:
            # Add user input if provided
            if user_input:
                self.add_user_message(user_input)
            
            # Get response from GPT-4
            response = client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history,
                max_tokens=150,  # Keep responses concise
                temperature=0.8,
                presence_penalty=0.6,
                frequency_penalty=0.6
            )
            
            marcus_response = response.choices[0].message.content
            self.add_assistant_message(marcus_response)
            
            return marcus_response
            
        except Exception as e:
            logger.error(f"Error getting GPT response: {str(e)}")
            # Fallback response
            return "I apologize, I'm having a brief connection issue. Can you repeat that?"
    
    def should_end_call(self) -> bool:
        """Determine if the call should end"""
        # End if too many turns (avoid infinite loops)
        if self.turn_count > 15:
            return True
        
        # Check if conversation reached natural end
        if self.conversation_history:
            last_message = self.conversation_history[-1].get("content", "").lower()
            end_phrases = ["have a great day", "thank you for your time", "goodbye", "talk to you later"]
            if any(phrase in last_message for phrase in end_phrases):
                return True
        
        return False


def get_or_create_conversation(call_sid: str, business_name: str = "") -> ConversationManager:
    """Get existing conversation or create new one"""
    if call_sid not in conversation_store:
        conversation_store[call_sid] = ConversationManager(call_sid, business_name)
    return conversation_store[call_sid]


def cleanup_conversation(call_sid: str):
    """Remove conversation from memory"""
    if call_sid in conversation_store:
        del conversation_store[call_sid]
        logger.info(f"Cleaned up conversation for call {call_sid}")


def transcribe_audio(audio_url: str) -> str:
    """Transcribe audio using Whisper"""
    try:
        import requests
        
        # Download audio file
        response = requests.get(audio_url)
        if response.status_code != 200:
            logger.error(f"Failed to download audio: {response.status_code}")
            return ""
        
        # Save temporarily
        temp_file = f"/tmp/audio_{datetime.now().timestamp()}.wav"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # Transcribe with Whisper
        with open(temp_file, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        
        # Cleanup
        os.remove(temp_file)
        
        return transcript.text
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return ""


def generate_speech(text: str) -> str:
    """Generate speech using OpenAI TTS"""
    try:
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Male voice (alternatives: alloy, echo, fable, nova, shimmer)
            input=text,
            speed=1.0
        )
        
        # Save to temporary file
        temp_file = f"/tmp/speech_{datetime.now().timestamp()}.mp3"
        response.stream_to_file(temp_file)
        
        return temp_file
        
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        return None
