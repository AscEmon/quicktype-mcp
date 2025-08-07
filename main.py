import json
import logging
from enum import Enum
from typing import Dict, Any, List

# Import MCP library
from mcp.server import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quicktype-mcp")

# Create the MCP server
mcp = FastMCP(name="quicktype-mcp")

# Sample complex response to use as context for model generation
SAMPLE_COMPLEX_RESPONSE = {
    "code": 200,
    "message": "Data retrieved successfully",
    "data": {
        "server": {
            "id": "SRV-001",
            "name": "Main Server",
            "enabled": True,
            "metadata": {
                "location": {
                    "building": "HQ",
                    "floor": 3
                },
                "installedDate": "2023-05-15T08:00:00Z"
            }
        },
        "devices": [
            {
                "deviceId": 1,
                "name": "Device One",
                "enabled": True,
                "registers": [
                    {
                        "registerId": 101,
                        "name": "Temperature",
                        "value": 25.5,
                        "unit": "°C"
                    }
                ]
            }
        ],
        "diagnostics": {
            "lastConnection": "2024-04-05T12:34:56.789Z",
            "errorCount": 0
        }
    }
}

# Models
class Language(str, Enum):
    DART = "dart"
    TYPESCRIPT = "typescript"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    PYTHON = "python"
    JAVA = "java"
    GO = "go"

class QuicktypeService:
    """Service to interact with quicktype.io API."""
    
    @staticmethod
    def get_dart_type(value, make_nullable=True):
        """Get Dart type for a value, making it nullable by default"""
        if isinstance(value, bool):
            return 'bool?' if make_nullable else 'bool'
        elif isinstance(value, int):
            return 'int?' if make_nullable else 'int'
        elif isinstance(value, float):
            return 'double?' if make_nullable else 'double'
        elif isinstance(value, str):
            return 'String?' if make_nullable else 'String'
        elif isinstance(value, dict):
            return 'Map<String, dynamic>?' if make_nullable else 'Map<String, dynamic>'
        elif isinstance(value, list):
            if value and all(isinstance(item, dict) for item in value):
                item_class = f"{class_name}Item"
                return f'List<{item_class}>?' if make_nullable else f'List<{item_class}>'
            return 'List<dynamic>?' if make_nullable else 'List<dynamic>'
        return 'dynamic?' if make_nullable else 'dynamic'

    @staticmethod
    def _generate_class_name(parent_name, key):
        """Generate class name using parent class name as prefix"""
        if not parent_name:
            return key.title().replace('_', '')
        return f"{parent_name}{key.title().replace('_', '')}"

    @staticmethod
    def _generate_dart_model(json_data, class_name, parent_name='', nested_classes=None):
        """Generate Dart model class with nullable fields and proper handling of nested objects"""
        if nested_classes is None:
            nested_classes = {}
        
        class_code = [f"class {class_name} {{"]
        constructors = [f"  {class_name}({{"]
        from_json = [f"  factory {class_name}.fromJson(Map<String, dynamic> json) => {class_name}("]
        to_json = ["  Map<String, dynamic> toJson() => {"]

        for json_key, value in json_data.items():
            field_name = json_key
            
            # Handle nested objects
            if isinstance(value, dict):
                nested_class_name = QuicktypeService._generate_class_name(parent_name=class_name, key=json_key)
                field_type = f"{nested_class_name}?"
                
                # Generate nested class
                nested_classes[nested_class_name] = QuicktypeService._generate_dart_model(
                    value, nested_class_name, class_name, nested_classes
                )
                
                # Add field with proper null handling
                class_code.append(f"  final {field_type} {field_name};")
                constructors.append(f"    this.{field_name},")
                from_json.append(f"    {field_name}: json['{json_key}'] == null ? null : {nested_class_name}.fromJson(json['{json_key}']),")
                to_json.append(f"    '{json_key}': {field_name}?.toJson(),")
            
            # Handle arrays
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    # Array of objects - create a nested class for the items
                    item_class_name = QuicktypeService._generate_class_name(parent_name=class_name, key=json_key.rstrip('s'))
                    if not item_class_name.endswith('s') and json_key.endswith('s'):
                        item_class_name = item_class_name.rstrip('s')  # Remove trailing 's' if it exists
                    
                    field_type = f"List<{item_class_name}>?"
                    
                    # Generate nested class for array items
                    nested_classes[item_class_name] = QuicktypeService._generate_dart_model(
                        value[0], item_class_name, class_name, nested_classes
                    )
                    
                    # Add field with proper null handling for arrays
                    class_code.append(f"  final {field_type} {field_name};")
                    constructors.append(f"    this.{field_name},")
                    from_json.append(f"    {field_name}: json['{json_key}'] == null ? [] : List<{item_class_name}>.from(json['{json_key}']!.map((x) => x == null ? null : {item_class_name}.fromJson(x))),")
                    to_json.append(f"    '{json_key}': {field_name} == null ? [] : List<dynamic>.from({field_name}!.map((x) => x?.toJson())),")
                else:
                    # Simple array (strings, numbers, etc.)
                    element_type = "dynamic"
                    if value and all(isinstance(item, str) for item in value):
                        element_type = "String"
                    elif value and all(isinstance(item, int) for item in value):
                        element_type = "int"
                    elif value and all(isinstance(item, float) for item in value):
                        element_type = "double"
                    elif value and all(isinstance(item, bool) for item in value):
                        element_type = "bool"
                    
                    field_type = f"List<{element_type}>?"
                    class_code.append(f"  final {field_type} {field_name};")
                    constructors.append(f"    this.{field_name},")
                    from_json.append(f"    {field_name}: json['{json_key}'] == null ? [] : List<{element_type}>.from(json['{json_key}']!.map((x) => x)),")
                    to_json.append(f"    '{json_key}': {field_name} == null ? [] : List<dynamic>.from({field_name}!.map((x) => x)),")
            
            # Handle primitive types
            else:
                field_type = QuicktypeService.get_dart_type(value)
                
                # Special handling for DateTime
                if isinstance(value, str) and (
                    "date" in json_key.lower() or 
                    "time" in json_key.lower() or 
                    "created" in json_key.lower() or 
                    "updated" in json_key.lower()
                ) and (
                    "T" in value and "Z" in value or  # ISO format check
                    "-" in value and ":" in value      # Date with time check
                ):
                    field_type = "DateTime?"
                    class_code.append(f"  final {field_type} {field_name};")
                    constructors.append(f"    this.{field_name},")
                    from_json.append(f"    {field_name}: json['{json_key}'] == null ? null : DateTime.parse(json['{json_key}']),")
                    to_json.append(f"    '{json_key}': {field_name}?.toIso8601String(),")
                else:
                    # Regular primitive type
                    class_code.append(f"  final {field_type} {field_name};")
                    constructors.append(f"    this.{field_name},")
                    from_json.append(f"    {field_name}: json['{json_key}'],")
                    to_json.append(f"    '{json_key}': {field_name},")
        
        # Finalize the class code
        constructors.append("  });")
        from_json.append("  );")
        to_json.append("  };")
        
        # Combine all parts
        class_code.extend([""] + constructors + [""] + from_json + [""] + to_json + ["}"])
        
        # If this is the top-level call, combine with all nested classes
        if parent_name == '':
            # Add imports at the top
            imports = ["import 'dart:convert';", ""]
            
            # Add helper methods for the main class
            helpers = [
                f"{class_name} {class_name.lower()}FromJson(String str) => {class_name}.fromJson(json.decode(str));",
                "",
                f"String {class_name.lower()}ToJson({class_name} data) => json.encode(data.toJson());"
            ]
            
            # Combine everything
            full_code = imports + helpers + [""] + ["\n".join(class_code)]
            
            # Add all nested classes
            for nested_class in nested_classes.values():
                full_code.append("\n" + nested_class)
            
            return "\n".join(full_code)
        
        return "\n".join(class_code)

    @staticmethod
    def _generate_typescript_model(json_data: dict, class_name: str) -> str:
        """Generate a TypeScript model from JSON data."""
        # Placeholder for TypeScript model generation
        return f"// TypeScript model for {class_name}\n// Not implemented yet"
    
    @staticmethod
    def _generate_kotlin_model(json_data: dict, class_name: str) -> str:
        """Generate a Kotlin model from JSON data."""
        # Placeholder for Kotlin model generation
        return f"// Kotlin model for {class_name}\n// Not implemented yet"
    
    @staticmethod
    def _generate_swift_model(json_data: dict, class_name: str) -> str:
        """Generate a Swift model from JSON data."""
        # Placeholder for Swift model generation
        return f"// Swift model for {class_name}\n// Not implemented yet"
    
    @staticmethod
    def _generate_python_model(json_data: dict, class_name: str) -> str:
        """Generate a Python model from JSON data."""
        # Placeholder for Python model generation
        return f"# Python model for {class_name}\n# Not implemented yet"
    
    @staticmethod
    async def generate_model(json_input: str, class_name: str = "Model", language: str = "dart") -> Dict[str, Any]:
        """Generate a model from JSON input with null Safety.
        
        Args:
            json_input: The JSON string to generate a model from
            class_name: The name of the generated class
            language: The programming language to generate code for
            
        Returns:
            A dictionary containing the generated code and metadata
        """
        logger.info(f"Generating {language} model for class {class_name}")
        try:
            # Validate JSON
            try:
                if isinstance(json_input, str):
                    parsed_json = json.loads(json_input)
                else:
                    parsed_json = json_input
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON input: {str(e)}")
                return {"error": f"Invalid JSON: {str(e)}"}
            
            # For complex nested structures, use our sample as a reference
            if language.lower() == "dart":
                # Check if this is a complex nested structure that might need special handling
                if isinstance(parsed_json, dict) and "data" in parsed_json and isinstance(parsed_json.get("data"), dict):
                    logger.info("Using enhanced Dart model generation for complex nested structure")
                    code = QuicktypeService._generate_dart_model(parsed_json, class_name)
                else:
                    code = QuicktypeService._generate_dart_model(parsed_json, class_name)
            elif language.lower() == "typescript":
                code = QuicktypeService._generate_typescript_model(parsed_json, class_name)
            elif language.lower() == "kotlin":
                code = QuicktypeService._generate_kotlin_model(parsed_json, class_name)
            elif language.lower() == "swift":
                code = QuicktypeService._generate_swift_model(parsed_json, class_name)
            elif language.lower() == "python":
                code = QuicktypeService._generate_python_model(parsed_json, class_name)
            else:
                return {"error": f"Language '{language}' is not supported in offline mode"}
            
            logger.info(f"Successfully generated {language} model for {class_name}")
            
            return {
                "code": code,
                "language": language,
                "class_name": class_name,
                "message": f"{language.capitalize()} model generated successfully"
            }
        except Exception as e:
            error_msg = f"Failed to generate model: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
    @staticmethod
    def list_supported_languages() -> Dict[str, Any]:
        """List all languages supported by quicktype.io.
        
        Returns:
            A dictionary containing the list of supported languages
        """
        logger.info("Listing supported languages")
        # These are the main languages supported by quicktype.io
        languages = [
            "dart", "typescript", "kotlin", "swift", "python", "java", "go"
        ]
        
        return {"languages": languages}

    @staticmethod
    def fix_json(json_input: str) -> Dict[str, Any]:
        """Fix and format invalid JSON input.
        
        Args:
            json_input: The JSON string to fix
            
        Returns:
            A dictionary containing the fixed JSON and validation status
        """
        logger.info("Attempting to fix JSON input")
        try:
            # First try to parse as-is
            try:
                json.loads(json_input)
                logger.info("JSON is already valid")
                return {
                    "fixed_json": json_input,
                    "valid": True,
                    "message": "JSON is already valid"
                }
            except json.JSONDecodeError:
                logger.info("JSON is invalid, attempting to fix")
                pass
                
            # Common JSON issues to fix
            # 1. Replace single quotes with double quotes
            fixed_json = json_input.replace("'", '"')
            
            # 2. Add quotes to unquoted keys
            import re
            fixed_json = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', fixed_json)
            
            # 3. Fix trailing commas in objects and arrays
            fixed_json = re.sub(r',\s*}', '}', fixed_json)
            fixed_json = re.sub(r',\s*\]', ']', fixed_json)
            
            # 4. Fix missing quotes around string values
            # This is a simplified approach - more complex cases might need additional handling
            fixed_json = re.sub(r':\s*([a-zA-Z][a-zA-Z0-9_]*)\s*([,}])', r':"\1"\2', fixed_json)
            
            # Try to parse the fixed JSON
            parsed_json = json.loads(fixed_json)
            
            # Format the JSON with proper indentation
            formatted_json = json.dumps(parsed_json, indent=2)
            
            return {
                "fixed_json": formatted_json,
                "valid": True,
                "message": "JSON fixed and formatted successfully"
            }
        except json.JSONDecodeError as e:
            # If we still can't parse it, return the error
            return {
                "fixed_json": json_input,
                "valid": False,
                "message": f"Could not fix JSON: {str(e)}",
                "error_position": {
                    "line": e.lineno,
                    "column": e.colno,
                    "error_message": e.msg
                }
            }
        except Exception as e:
            return {
                "fixed_json": json_input,
                "valid": False,
                "message": f"Unexpected error: {str(e)}"
            }


# Define MCP tools
@mcp.tool("generate_model")
async def generate_model(json_input: str, class_name: str = "Model", language: str = "dart") -> Dict[str, Any]:
    """Generate a model from JSON input.
    
    Args:
        json_input: The JSON string to generate a model from
        class_name: The name of the generated class
        language: The programming language to generate code for
        
    Returns:
        A dictionary containing the generated code and metadata
    """
    logger.info(f"Generating {language} model for class {class_name}")
    
    # Check if the json_input is nested and needs special handling
    try:
        is_nested = False
        if isinstance(json_input, str):
            parsed_json = json.loads(json_input)
            
            # Check if this is a nested structure similar to our sample
            if isinstance(parsed_json, dict) and "data" in parsed_json and isinstance(parsed_json["data"], dict):
                # This appears to be a nested API response
                is_nested = True
                logger.info("Detected nested API response structure")
        else:
            parsed_json = json_input
            
        # Use our enhanced model generation
        result = await QuicktypeService.generate_model(
            json_input=parsed_json, 
            class_name=class_name, 
            language=language
        )
        
        return result
    except Exception as e:
        error_msg = f"Error generating model: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

@mcp.tool("list_languages")
def list_languages() -> Dict[str, List[str]]:
    """List all languages supported by quicktype.io.
    
    Returns:
        A dictionary containing the list of supported languages
    """
    return QuicktypeService.list_supported_languages()

@mcp.tool("fix_json")
def fix_json(json_input: str) -> Dict[str, Any]:
    """Fix and format invalid JSON input.
    
    Args:
        json_input: The JSON string to fix
        
    Returns:
        A dictionary containing the fixed JSON and validation status
    """
    return QuicktypeService.fix_json(json_input)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()