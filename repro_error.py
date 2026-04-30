import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from deepagents import create_deep_agent
from langchain.agents.middleware import PIIMiddleware

load_dotenv()

async def test():
    base_url = os.getenv("AGENTIC_BASE_URL", "https://openrouter.ai/api/v1")
    if "openrouter.ai" in base_url and "/api/v1" not in base_url:
        base_url = "https://openrouter.ai/api/v1"

    llm = ChatOpenAI(
        model="openai/gpt-4o-mini", 
        base_url=base_url,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    print(f"Testing LLM directly...")
    try:
        resp = llm.invoke("Hi")
        print(f"LLM Response Type: {type(resp)}")
        print(f"LLM Response: {resp}")
    except Exception as e:
        print(f"Direct LLM call failed: {e}")
        import traceback
        traceback.print_exc()
    
    tools = [] # Empty tools
    system_prompt = "You are a helpful assistant."
    
    agent = create_deep_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        debug=True,
        middleware=[
            PIIMiddleware("email", strategy="redact", apply_to_input=True),
        ],
    )
    
    messages = [HumanMessage(content="hello")]
    
    try:
        print("Invoking agent...")
        result = await agent.ainvoke({"messages": messages})
        print(f"Result: {result}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
