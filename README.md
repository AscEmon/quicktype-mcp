# Quicktype MCP Server

An MCP (Model Context Protocol) server for generating models from JSON using the quicktype.io web API. This tool simplifies the process of creating type-safe models for various programming languages, with a focus on Flutter/Dart development.

## Features

- No local dependencies (no Node.js or npm required)
- Generates models from JSON input for multiple languages
- Default focus on Dart for Flutter development
- Simple command-line interface
- Automatic JSON validation and fixing
- Integrates with Windsurf MCP
- Supports both interactive and file-based JSON input
- Background server mode for continuous operation

## Prerequisites

- Python 3.10 or higher
- Internet connection (to access the quicktype.io API)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/quicktype-mcp.git
   cd quicktype-mcp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### CLI Options

```bash
python cli.py [options]
```

Available options:
- `--server-only`: Run only the MCP server
- `--json <json_input>`: JSON input to process (string or file path)
- `--language <language>`: Target language (default: dart)
- `--class-name <name>`: Class name for the generated model (default: Model)
- `--output <file_path>`: Output file path
- `--windsurf`: Run in Windsurf MCP compatibility mode

### Running the Server

You can run the server in two modes:

#### Server-only mode

This mode runs the MCP server in the foreground:

```bash
python cli.py --server-only
```

#### Background server mode

This mode runs the MCP server in the background:

```bash
python cli.py
```

### Processing JSON directly

You can process JSON directly from the command line:

```bash
# Process JSON from a string
python cli.py --json '{"name": "John", "age": 30}' --class-name Person --language dart

# Process JSON from a file
python cli.py --json input.json --class-name Person --language kotlin --output Person.kt
```

## Supported Languages

The tool supports generating models for the following languages:

- Dart (default)
- TypeScript
- Kotlin
- Swift
- Python
- Java
- C#
- Go
- Ruby
- Rust
- Flow
- Scala
- C++
- Objective-C
- Elm
- JSON Schema
- Pike
- Haskell

## Using with Windsurf MCP

To use this MCP server with Windsurf, ensure the server is configured in your `windsurf_config.json`:

```json
{
  "quicktype-mcp": {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/quicktype-mcp",
      "run",
      "cli.py",
      "--windsurf"
    ]
  }
}
```

### Available MCP Tools

1. **generate_model**: Generate code models from JSON
   - Parameters:
     - `json_input`: The JSON string to generate a model from
     - `class_name`: The name of the generated class (default: "Model")
     - `language`: The programming language to generate code for (default: "dart")

2. **list_languages**: List supported programming languages
   - No parameters required

3. **fix_json**: Fix invalid JSON
   - Parameters:
     - `json_input`: The JSON string to fix

### Example Usage in Python

```python
# Example of using the MCP client
from mcp.client import MCPClient

# Connect to the MCP server
client = MCPClient("quicktype-mcp")

# List supported languages
languages = client.list_languages()
print(languages)

# Generate a model from JSON
json_input = '{"name": "John", "age": 30}'
result = client.generate_model(json_input=json_input, class_name="Person", language="dart")
print(result["code"])

# Fix invalid JSON
invalid_json = '{"name": "John", "age": 30,}'
result = client.fix_json(json_input=invalid_json)
print(result["fixed_json"])
```

### Example Usage in Windsurf

```python
# Using the quicktype-mcp MCP server in Windsurf
result = mcp1_generate_model(json_input='{"name": "John", "age": 30}', class_name="Person", language="dart")
print(result["code"])
```

## Troubleshooting

If you encounter issues with the server not running, make sure:

1. You have an active internet connection
2. The virtual environment is activated
3. All dependencies are installed
4. The correct Python version is being used (3.10+)

For issues with the generated models:
1. Ensure your JSON is valid (use the `fix_json` tool if needed)
2. Check that the requested language is supported
3. Try simplifying complex JSON structures if you encounter errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.