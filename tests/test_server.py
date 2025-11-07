"""
Unit tests for MCP Server
"""
import pytest
import asyncio
from src.server import app, call_tool


@pytest.mark.asyncio
async def test_calculate_tool():
    """Test the calculate tool"""
    result = await call_tool("calculate", {"expression": "2 + 2"})
    assert len(result) > 0
    assert "4" in result[0].text


@pytest.mark.asyncio
async def test_process_data_tool():
    """Test the process_data tool"""
    result = await call_tool("process_data", {"data": "hello", "operation": "uppercase"})
    assert len(result) > 0
    assert "HELLO" in result[0].text


@pytest.mark.asyncio
async def test_get_system_info_tool():
    """Test the get_system_info tool"""
    result = await call_tool("get_system_info", {})
    assert len(result) > 0
    assert "timestamp" in result[0].text


@pytest.mark.asyncio
async def test_list_tools():
    """Test listing tools"""
    tools = await app.list_tools()
    assert len(tools) > 0
    tool_names = [tool.name for tool in tools]
    assert "calculate" in tool_names
    assert "fetch_url" in tool_names
    assert "get_system_info" in tool_names


@pytest.mark.asyncio
async def test_list_resources():
    """Test listing resources"""
    resources = await app.list_resources()
    assert len(resources) > 0

