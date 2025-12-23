"""
Chat service for AI chatbot integration.
Supports OpenAI GPT models by default, can be extended for other providers.
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI, handle gracefully if not installed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not installed. Install with: pip install openai")

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo for cost efficiency

# Initialize OpenAI client if available
client = None
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def get_chat_response(
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    system_prompt: Optional[str] = None
) -> Dict[str, str]:
    """
    Get AI chat response from OpenAI.
    
    Args:
        user_message: The user's message/input
        conversation_history: List of previous messages in format [{"role": "user", "content": "..."}, ...]
        system_prompt: Optional system prompt to set AI behavior (defaults to dog nutrition assistant)
    
    Returns:
        Dictionary with 'response' (AI's reply) and 'error' (if any)
    
    Raises:
        ValueError: If OpenAI is not configured or available
    """
    if not OPENAI_AVAILABLE:
        raise ValueError(
            "OpenAI library not available. Please install it with: pip install openai"
        )
    
    if not client:
        raise ValueError(
            "OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file"
        )
    
    # Default system prompt for dog nutrition assistant
    default_system_prompt = """You are a helpful assistant for WhiskerWorthy, a dog nutrition and diet recommendation app. 
    You help users with questions about:
    - Dog breeds and their nutritional needs
    - Dog food recommendations
    - Feeding guidelines
    - Diet-related health concerns for dogs
    - General dog nutrition advice
    
    Be friendly, informative, and professional. Always emphasize consulting with a veterinarian for serious health concerns.
    If you don't know something, it's okay to say so and suggest consulting a vet."""
    
    system_message = system_prompt if system_prompt else default_system_prompt
    
    # Build messages array
    messages = [{"role": "system", "content": system_message}]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,  # Controls randomness: 0 = deterministic, 1 = creative
            max_tokens=500,   # Limit response length
        )
        
        ai_response = response.choices[0].message.content
        
        return {
            "response": ai_response,
            "error": None
        }
    
    except Exception as e:
        return {
            "response": None,
            "error": f"Failed to get AI response: {str(e)}"
        }


def format_conversation_history(
    messages: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Format conversation history for API.
    Ensures messages have correct structure: {"role": "...", "content": "..."}
    
    Args:
        messages: List of message dictionaries
    
    Returns:
        Formatted list of messages
    """
    formatted = []
    for msg in messages:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            # Ensure role is valid
            if msg["role"] in ["user", "assistant", "system"]:
                formatted.append({
                    "role": msg["role"],
                    "content": str(msg["content"])
                })
    return formatted

