# Quicktype MCP Server

An MCP (Model Context Protocol) server for generating models from JSON. This tool simplifies the process of creating type-safe models for various programming languages.

## Features

- No local dependencies (no Node.js or npm required)
- Generates models from JSON input for multiple languages
- Automatic JSON validation and fixing
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
- Go


## Using with Windsurf MCP

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

```

## Troubleshooting

If you encounter issues with the server not running, make sure:

1. You have an active internet connection
2. All dependencies are installed
3. The correct Python version is being used (3.10+)

For issues with the generated models:
1. Ensure your JSON is valid (use the `fix_json` tool if needed)
2. Check that the requested language is supported
3. Try simplifying complex JSON structures if you encounter errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.