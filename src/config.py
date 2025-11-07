"""
Configuration management for MCP Server
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class ServerConfig(BaseSettings):
    """Server configuration settings"""
    
    server_name: str = Field(
        default="mcp-server-poc",
        env="MCP_SERVER_NAME"
    )
    server_version: str = Field(
        default="0.1.0",
        env="MCP_SERVER_VERSION"
    )
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL"
    )
    enable_metrics: bool = Field(
        default=True,
        env="ENABLE_METRICS"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = ServerConfig()

