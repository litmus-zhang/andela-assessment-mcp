from dotenv import load_dotenv
from langchain.agents import create_agent
from opik import track
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI
import os
from deepagents import create_deep_agent

load_dotenv()

# Initialize with OpenRouter's base URL and your API key
base_url = os.getenv("AGENTIC_BASE_URL", "https://openrouter.ai/api/v1")

# Robust OpenRouter URL handling
if "openrouter.ai" in base_url:
    if "/api/v1" not in base_url:
        base_url = "https://openrouter.ai/api/v1"
    # Ensure it's not double-slashed or using the non-API endpoint
    base_url = base_url.replace("/v1/api/v1", "/api/v1")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini", 
    base_url=base_url,
    api_key=os.getenv("OPENAI_API_KEY"),
)

@track
async def create_meridian_agent(tools):
    system_prompt = (
        "You are a helpful customer support chatbot for Meridian Electronics. "
        "You can help customers check product availability, place orders, "
        "look up order history, and authenticate returning customers. "
        "Always be professional and polite."
    )
    
    agent = create_deep_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        debug=True,
        middleware=[
        # Redact emails in user input before sending to model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Block API keys - raise error if detected
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
    )

    return agent
