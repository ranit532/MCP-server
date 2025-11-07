"""
Example client script to interact with the MCP server
This demonstrates how to use the MCP server programmatically
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Example client interaction with MCP server"""
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.server"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            print("Available Tools:")
            tools = await session.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # List available resources
            print("\nAvailable Resources:")
            resources = await session.list_resources()
            for resource in resources:
                print(f"  - {resource.name}: {resource.description}")
            
            # Call a tool
            print("\nCalling calculate tool...")
            result = await session.call_tool("calculate", {"expression": "10 * 5 + 3"})
            print(f"Result: {result.content}")
            
            # Call another tool
            print("\nCalling process_data tool...")
            result = await session.call_tool(
                "process_data",
                {"data": "Hello MCP Server!", "operation": "uppercase"}
            )
            print(f"Result: {result.content}")
            
            # Get system info
            print("\nGetting system info...")
            result = await session.call_tool("get_system_info", {})
            print(f"System Info: {result.content}")


if __name__ == "__main__":
    asyncio.run(main())

