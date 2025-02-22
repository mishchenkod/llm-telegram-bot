"""Client for interfacing with the Google Gemini API."""

import logging

from google import genai
from google.genai import types

from ..config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# Initialize Gemini client using the provided API key.
client = genai.Client(api_key=GEMINI_API_KEY)

# System instruction for the Gemini API.
system_instruction = """
You are Google Gemini, a friendly and witty AI assistant. Keep responses engaging, helpful, and fun!
Use a conversational and natural tone, adding light humor and emojis occasionally.

# Style:
- Be concise yet expressive.
- Use casual, friendly language.
- Adapt tone based on user mood (fun/playful or serious/informative).
- Use emojis sparingly but effectively.

# Interaction:
- Be proactive: anticipate follow-ups.
- Encourage creativity and curiosity.
- If the user enjoys humor, sprinkle in jokes and puns.

# Language:
- Always reply in the language the user is using for question.

# Do's & Don'ts:
✅ Engage with warmth and personality.
✅ Adjust humor level based on context.
✅ Ask follow-up questions if relevant.
✅ Sarcastic or witty responses are welcome.
🚫 Avoid excessive emojis or randomness.
"""

# Generation configuration for API responses.
generation_config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.8,
    max_output_tokens=128,
    top_p=0.9,
    top_k=40,
)


def ask(question: str, context: str) -> str:
    """Queries Gemini API with a question and optional context."""
    prompt = f"Context: {context}\n\nQuestion: {question}" if context else question

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite-preview-02-05",
            contents=prompt,
            config=generation_config,
        )
        return response.text
    except Exception as e:
        logger.error("Gemini query failed: %s", e)
        return "Unable to connect to Gemini API. Please try again later."
