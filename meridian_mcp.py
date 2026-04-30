import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient  

async def get_meridian_tools():
    client = MultiServerMCPClient(
        {
            
            "meridia": {
                "transport": "http",  # HTTP-based remote server
                "url": "https://order-mcp-74afyau24q-uc.a.run.app/mcp",
            }
        }
    )

    tools = await client.get_tools()

    # print("tools",tools )

    return tools
   