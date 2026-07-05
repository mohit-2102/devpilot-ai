from dotenv import load_dotenv

load_dotenv()

from app.services.llm_service import LLMService

service = LLMService()

response = service.provider.generate(
"""
You are a senior backend engineer.

Answer in exactly two sentences.

Rules:

- Answer in exactly 2 complete sentences.
- Keep the response between 40 and 70 words.
- Use professional technical language.
- Do not add unnecessary introductions or conclusions.

Question:
What is FastAPI?
"""
)

print(response)