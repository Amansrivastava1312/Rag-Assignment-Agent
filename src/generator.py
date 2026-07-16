import os 
from dotenv import load_dotenv
from google import genai
import re
import json
class Generation:
   def __init__(self):
        pass
   def ask_question(self,user_question,context):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)

        
       
        sysprompt = f"""
You are a senior AI Model Advisor chatbot.
Your ONLY area of knowledge is: LLMs (Large Language Models), SLMs (Small Language Models),
their evolution, architecture, and related AI/ML topics.

You are given:
- User query: {user_question}
- Context: {context}

Follow these rules STRICTLY and in this exact order:

1) GREETING:
   If the user is only greeting or doing small talk (e.g. "hi", "hello", "hey", "good morning", "how are you"),
   reply exactly with a warm welcome:
   "Hello! 👋 How can I help you? You can ask me about Python, ML,DL,MLops LLMs, SLMs, their evolution, architecture, and related AI topics."

2) IN CONTEXT:
   If the answer to the user's query is present in the Context above,
   give a clear, well-arranged answer using ONLY the information in the Context.
   Do NOT make up or predict anything that is not in the Context.

3) OUT OF CONTEXT (unrelated topic):
   If the question is NOT related to LLMs, SLMs, or AI (for example: "Who is Narendra Modi?",
   sports, politics, cooking, etc.), reply exactly:
   "Not in context. I can only answer questions related to LLMs, SLMs, and their related AI topics."

Never break these rules. Do not guess. Keep answers relevant and to the point.
"""
        response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=sysprompt
        )
        return response.text

   def parse_intent(self, user_question):
      load_dotenv()
      client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

      prompt = f"""You are an intent router for an AI chatbot.
   Read the user's message and return ONLY valid JSON (no markdown, no explanation).

   Keys:
   - "question": the actual question to answer (remove any export/email words)
   - "export": "pdf", "txt", or null
   - "email": true or false
   - "email_to": recipient email if given, else null

   Examples:
   "what is an LLM, give me as pdf"
   -> {{"question": "what is an LLM", "export": "pdf", "email": false, "email_to": null}}
   "explain SLMs and mail it to raj@x.com"
   -> {{"question": "explain SLMs", "export": null, "email": true, "email_to": "raj@x.com"}}
   "convert LoRA explanation to text and mail me"
   -> {{"question": "explain LoRA", "export": "txt", "email": true, "email_to": null}}
   "hi"
   -> {{"question": "hi", "export": null, "email": false, "email_to": null}}

   USER MESSAGE: "{user_question}"

   JSON:"""

      response = client.models.generate_content(
         model='gemini-3.1-flash-lite',
         contents=prompt
      )
      raw = re.sub(r"```json|```", "", response.text).strip()
      try:
         return json.loads(raw)
      except json.JSONDecodeError:
         return {"question": user_question, "export": None,
                  "email": False, "email_to": None}