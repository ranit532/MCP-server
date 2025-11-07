"""
MCP Server POC - Main server implementation with tools and resources
"""
import asyncio
import json
import logging
import os
import sys
from typing import Any, Sequence
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from pydantic import AnyUrl
import httpx
import aiofiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize MCP Server
app = Server("mcp-server-poc")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools in the MCP server
    """
    return [
        Tool(
            name="calculate",
            description="Perform mathematical calculations. Supports basic arithmetic operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')",
                    }
                },
                "required": ["expression"],
            },
        ),
        Tool(
            name="fetch_url",
            description="Fetch content from a URL and return the response",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch",
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, etc.)",
                        "default": "GET",
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="get_system_info",
            description="Get system information including timestamp and environment details",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="process_data",
            description="Process and transform data (example: reverse string, uppercase, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Data to process",
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform: 'reverse', 'uppercase', 'lowercase', 'count'",
                        "enum": ["reverse", "uppercase", "lowercase", "count"],
                    },
                },
                "required": ["data", "operation"],
            },
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to write",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file",
                    },
                },
                "required": ["filepath", "content"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
    Handle tool execution requests
    """
    logger.info(f"Tool called: {name} with arguments: {arguments}")

    try:
        if name == "calculate":
            expression = arguments.get("expression", "")
            # Safe evaluation (in production, use a proper expression evaluator)
            try:
                result = eval(expression, {"__builtins__": {}}, {})
                return [TextContent(
                    type="text",
                    text=f"Result: {result}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error calculating: {str(e)}"
                )]

        elif name == "fetch_url":
            url = arguments.get("url")
            method = arguments.get("method", "GET")
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, timeout=10.0)
                return [TextContent(
                    type="text",
                    text=f"Status: {response.status_code}\nContent:\n{response.text[:1000]}"
                )]

        elif name == "get_system_info":
            info = {
                "timestamp": datetime.now().isoformat(),
                "server_name": os.getenv("MCP_SERVER_NAME", "mcp-server-poc"),
                "server_version": os.getenv("MCP_SERVER_VERSION", "0.1.0"),
                "python_version": sys.version,
                "environment_vars": {k: v for k, v in os.environ.items() if not k.startswith("_")},
            }
            return [TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]

        elif name == "process_data":
            data = arguments.get("data", "")
            operation = arguments.get("operation", "")
            
            if operation == "reverse":
                result = data[::-1]
            elif operation == "uppercase":
                result = data.upper()
            elif operation == "lowercase":
                result = data.lower()
            elif operation == "count":
                result = str(len(data))
            else:
                result = f"Unknown operation: {operation}"
            
            return [TextContent(
                type="text",
                text=f"Operation '{operation}' result: {result}"
            )]

        elif name == "write_file":
            filepath = arguments.get("filepath")
            content = arguments.get("content")
            
            async with aiofiles.open(filepath, "w") as f:
                await f.write(content)
            
            return [TextContent(
                type="text",
                text=f"Successfully wrote {len(content)} characters to {filepath}"
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available resources
    """
    return [
        Resource(
            uri=AnyUrl("file://example.txt"),
            name="Example File",
            description="An example file resource",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("config://server-config"),
            name="Server Configuration",
            description="Current server configuration",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """
    Read a resource by URI
    """
    logger.info(f"Reading resource: {uri}")
    
    if str(uri).startswith("file://"):
        filepath = str(uri).replace("file://", "")
        try:
            async with aiofiles.open(filepath, "r") as f:
                return await f.read()
        except FileNotFoundError:
            return f"File not found: {filepath}"
    
    elif str(uri).startswith("config://"):
        config = {
            "server_name": os.getenv("MCP_SERVER_NAME", "mcp-server-poc"),
            "server_version": os.getenv("MCP_SERVER_VERSION", "0.1.0"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        }
        return json.dumps(config, indent=2)
    
    return f"Unknown resource: {uri}"


async def main():
    """
    Main entry point for the MCP server
    """
    logger.info("Starting MCP Server POC...")
    
    # Use stdio transport for MCP communication
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    # Use uvloop for better async performance if available
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass
    
    asyncio.run(main())

