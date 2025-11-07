# Project Structure

This document describes the structure and purpose of each file in the MCP Server POC project.

## Root Directory

- **README.md**: Comprehensive documentation with architecture diagrams, setup instructions, and usage examples
- **QUICKSTART.md**: Quick start guide for getting up and running fast
- **LICENSE**: MIT License file
- **Makefile**: Convenience commands for common tasks (install, test, lint, format, run)
- **setup.sh**: Automated setup script for initial project configuration
- **.gitignore**: Git ignore rules for Python projects
- **.env.example**: Example environment configuration file
- **pyproject.toml**: Python project metadata and dependencies (PEP 518)
- **pytest.ini**: Pytest configuration
- **requirements.txt**: Production dependencies
- **requirements-dev.txt**: Development dependencies (includes testing tools)
- **example.txt**: Example file resource for testing

## Source Code (`src/`)

- **`__init__.py`**: Package initialization with version info
- **`server.py`**: Main MCP server implementation
  - Server initialization and configuration
  - Tool definitions (calculate, fetch_url, get_system_info, process_data, write_file)
  - Resource definitions (file resources, config resources)
  - Request handlers for tools and resources
- **`config.py`**: Configuration management using Pydantic settings

## Tests (`tests/`)

- **`__init__.py`**: Test package initialization
- **`test_server.py`**: Unit tests for server functionality
  - Tool execution tests
  - Resource listing tests
  - Integration tests

## Examples (`examples/`)

- **`example_client.py`**: Example client demonstrating how to interact with the MCP server
  - Shows how to list tools and resources
  - Demonstrates tool calls
  - Resource reading examples

## Scripts (`scripts/`)

- **`run_server.py`**: Convenience script to run the MCP server

## Key Technologies

1. **MCP SDK**: Official Model Context Protocol implementation
2. **Pydantic**: Data validation and settings management
3. **httpx**: Modern async HTTP client
4. **aiofiles**: Async file operations
5. **uvloop**: High-performance event loop
6. **pytest**: Testing framework with async support

## Architecture Highlights

- **Async/Await**: Full async implementation for high performance
- **Type Safety**: Complete type hints throughout
- **Modular Design**: Clear separation of concerns
- **Extensible**: Easy to add new tools and resources
- **Testable**: Comprehensive test suite
- **Configurable**: Environment-based configuration

## Adding New Features

### Adding a Tool

1. Add tool definition in `src/server.py` → `list_tools()`
2. Implement tool logic in `src/server.py` → `call_tool()`
3. Add tests in `tests/test_server.py`

### Adding a Resource

1. Add resource definition in `src/server.py` → `list_resources()`
2. Implement resource reading in `src/server.py` → `read_resource()`
3. Add tests in `tests/test_server.py`

