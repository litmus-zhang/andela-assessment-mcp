import pytest
from unittest.mock import AsyncMock, patch
from meridian_mcp import get_meridian_tools
from agent import create_meridian_agent

@pytest.mark.asyncio
async def test_get_meridian_tools():
    with patch("meridian_mcp.MultiServerMCPClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get_tools = AsyncMock(return_value=["tool1", "tool2"])
        
        tools = await get_meridian_tools()
        assert tools == ["tool1", "tool2"]
        mock_instance.get_tools.assert_called_once()

@pytest.mark.asyncio
async def test_create_agent():
    tools = [] # Empty tools for simple test
    with patch("langchain.agents.create_agent") as mock_create:
        mock_create.return_value = AsyncMock()
        agent = await create_meridian_agent(tools)
        assert agent is not None
