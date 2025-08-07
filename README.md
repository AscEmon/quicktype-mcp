# Quicktype MCP Server

An MCP (Model Context Protocol) server specifically designed for generating Dart models from JSON. This tool simplifies the process of creating type-safe Dart models for Flutter and Dart applications.

## Features

- Specialized for Dart model generation
- Automatic JSON validation and fixing
- Generates null-safe Dart models
- Handles complex nested JSON structures
- Includes serialization/deserialization methods

## Prerequisites

- Python 3.10 or higher
- Internet connection (to access the quicktype.io API)

## Usage as MCP Server

This tool is designed to be used as an MCP server that other applications can connect to. The server exposes a simple API for generating Dart models from JSON input.

### API

The server exposes the following endpoint:

- `generate_model`: Generates a Dart model from JSON input

Parameters:
- `json_input`: The JSON string to generate a model from
- `class_name`: The name of the generated class (default: Model)
- `language`: Currently only supports 'dart'

```json
{
  "quicktype-mcp": {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/quicktype-mcp",
      "run",
      "main.py",
    ]
  }
}
```

### Available MCP Tools

1. **generate_model**: Generate Dart models from JSON
   - Parameters:
     - `json_input`: The JSON string to generate a model from
     - `class_name`: The name of the generated class (default: "Model")
     - `language`: Currently only supports 'dart'

```

## Troubleshooting

If you encounter issues with the server not running, make sure:

1. You have an active internet connection
2. All dependencies are installed
3. The correct Python version is being used (3.10+)

For issues with the generated models:
1. Ensure your JSON is valid
2. Try simplifying complex JSON structures if you encounter errors
3. Check that the class name follows Dart naming conventions

## Features of Generated Dart Models

- **Null Safety**: All fields are properly marked as nullable when appropriate
- **JSON Serialization**: Includes `fromJson` and `toJson` methods
- **Nested Objects**: Properly handles nested objects with their own classes
- **Lists and Maps**: Correctly handles collections and their generic types
- **Type Safety**: Uses appropriate Dart types for JSON values

## License

This project is licensed under the MIT License - see the LICENSE file for details.