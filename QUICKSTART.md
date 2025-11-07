# Quick Start Guide

Get the MCP Server POC up and running in minutes!

## Prerequisites Check

```bash
python3 --version  # Should be 3.10 or higher
```

## Installation (3 Steps)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests (Optional but Recommended)

```bash
pip install -r requirements-dev.txt
pytest
```

## Running the Server

### Basic Run

```bash
python -m src.server
```

### Using Make (if available)

```bash
make run
```

## Testing the Server

### Run Example Client

```bash
python examples/example_client.py
```

### Run Unit Tests

```bash
pytest -v
```

## What's Next?

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the tools in `src/server.py`
3. Add your own custom tools
4. Integrate with your AI assistant

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'mcp'`
**Solution**: Make sure you've activated the virtual environment and installed dependencies

**Issue**: `Permission denied` when writing files
**Solution**: Check file permissions or use absolute paths

**Issue**: Python version too old
**Solution**: Upgrade to Python 3.10+ using pyenv or your system package manager

