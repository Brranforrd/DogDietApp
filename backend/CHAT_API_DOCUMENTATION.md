# Chat API Documentation

## Overview

The chatbot API provides AI-powered chat functionality for dog nutrition questions and advice. It uses OpenAI's GPT models to generate intelligent responses.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API Key**
   Add to your `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo  # Optional, defaults to gpt-3.5-turbo
   ```

   You can get an API key from: https://platform.openai.com/api-keys

## Endpoint

### POST `/api/chat`

Send a message to the AI chatbot and receive a response.

#### Request Body

```json
{
  "message": "What's the best food for a 2-year-old Golden Retriever?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you with your dog's nutrition today?"
    }
  ],
  "system_prompt": null
}
```

**Fields:**
- `message` (required, string): The user's message/input
- `conversation_history` (optional, array): Previous messages for context
  - Each message has `role` ("user" or "assistant") and `content` (string)
- `system_prompt` (optional, string): Custom system prompt (overrides default)

#### Response

```json
{
  "success": true,
  "message": "Chat response generated successfully",
  "response": "For a 2-year-old Golden Retriever, I recommend...",
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Failed to get AI response",
  "response": null,
  "error": "OpenAI API key not configured..."
}
```

#### Example cURL Request

```bash
curl -X POST "http://localhost:5000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I feed my puppy?",
    "conversation_history": []
  }'
```

#### Example JavaScript/Fetch

```javascript
async function sendChatMessage(userMessage, conversationHistory = []) {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: userMessage,
      conversation_history: conversationHistory
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
const result = await sendChatMessage("What's best for my dog?");
console.log(result.response);
```

#### Example Python

```python
import requests

def send_chat_message(message, conversation_history=None):
    url = "http://localhost:5000/api/chat"
    payload = {
        "message": message,
        "conversation_history": conversation_history or []
    }
    response = requests.post(url, json=payload)
    return response.json()

# Usage
result = send_chat_message("What food should I give my senior dog?")
print(result["response"])
```

## Conversation History

To maintain context in a conversation, include previous messages:

```javascript
let conversationHistory = [];

// First message
const response1 = await sendChatMessage("Hi, I have a Labrador");
conversationHistory.push(
  { role: "user", content: "Hi, I have a Labrador" },
  { role: "assistant", content: response1.response }
);

// Second message (with context)
const response2 = await sendChatMessage(
  "What should I feed him?",
  conversationHistory
);
```

## System Prompt

The default system prompt makes the AI act as a helpful dog nutrition assistant for WhiskerWorthy. You can customize it:

```json
{
  "message": "Tell me about dog food",
  "system_prompt": "You are a veterinary nutritionist. Provide detailed, scientific advice."
}
```

## Error Handling

- **503 Service Unavailable**: OpenAI not configured (missing API key or library)
- **500 Internal Server Error**: API call failed or other server error
- **400 Bad Request**: Invalid request format

## Notes

- The AI is configured with `temperature=0.7` for balanced creativity and accuracy
- Responses are limited to 500 tokens to control costs
- Always validate and sanitize user input on the frontend
- Consider rate limiting in production to prevent API abuse

