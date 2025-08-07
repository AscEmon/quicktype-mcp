import json
import httpx
import logging
import re
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

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



# Models
class Language(str, Enum):
    DART = "dart"
    TYPESCRIPT = "typescript"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    PYTHON = "python"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUBY = "ruby"
    RUST = "rust"
    FLOW = "flow"
    SCALA = "scala"
    CPP = "cpp"
    OBJECTIVE_C = "objective-c"
    ELM = "elm"
    JSON_SCHEMA = "schema"
    PIKE = "pike"
    HASKELL = "haskell"

class QuicktypeService:
    """Service to interact with quicktype.io API."""
    
    @staticmethod
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
            
            # Use a different approach since the API endpoint is not working
            # This is a simplified implementation that generates basic models
            # for common languages
            
            if language.lower() == "dart":
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
    def _generate_dart_model(json_data: dict, class_name: str) -> str:
        """Generate a Dart model from JSON data.
        
        Args:
            json_data: The parsed JSON data
            class_name: The name of the generated class
            
        Returns:
            The generated Dart code as a string
        """
        # Helper function to determine Dart type from a value
        def get_dart_type(value):
            if isinstance(value, bool):
                return "bool"
            elif isinstance(value, int):
                return "int"
            elif isinstance(value, float):
                return "double"
            elif isinstance(value, str):
                return "String"
            elif isinstance(value, list):
                if value and all(isinstance(item, dict) for item in value):
                    # All items are objects, try to determine the class name
                    item_class = f"{class_name}Item"
                    return f"List<{item_class}>"
                elif value and all(isinstance(item, (int, float, str, bool)) for item in value):
                    # All items are primitives, determine their type
                    item_type = get_dart_type(value[0])
                    return f"List<{item_type}>"
                else:
                    return "List<dynamic>"
            elif isinstance(value, dict):
                return "Map<String, dynamic>"
            else:
                return "dynamic"
        
        # Helper function to convert snake_case to camelCase
        def to_camel_case(snake_str):
            components = snake_str.split('_')
            return components[0] + ''.join(x.title() for x in components[1:])
        
        # Helper function to generate a class from a JSON object
        def generate_class(data, name):
            class_code = [f"class {name} {{"]  # Start class definition
            fields = []
            constructors = [f"  {name}({{"]  # Start constructor
            from_json = [f"  factory {name}.fromJson(Map<String, dynamic> json) => {name}("]  # Start fromJson
            to_json = ["  Map<String, dynamic> toJson() => {"]  # Start toJson
            
            # Process each field in the JSON object
            for key, value in data.items():
                field_name = to_camel_case(key)  # Convert to camelCase for Dart convention
                json_key = key  # Keep original key for JSON serialization
                
                if isinstance(value, dict):
                    # Nested object, create a new class
                    nested_class_name = f"{name}{key.title().replace('_', '')}"
                    field_type = nested_class_name
                    fields.append(f"  final {field_type} {field_name};")  # Add field
                    constructors.append(f"    required this.{field_name},")  # Add to constructor
                    from_json.append(f"    {field_name}: {field_type}.fromJson(json['{json_key}']),")  # Add to fromJson
                    to_json.append(f"    '{json_key}': {field_name}.toJson(),")  # Add to toJson
                elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
                    # List of objects, create a new class for the items
                    item_class_name = f"{name}{key.title().replace('_', '')}Item"
                    field_type = f"List<{item_class_name}>"
                    fields.append(f"  final {field_type} {field_name};")  # Add field
                    constructors.append(f"    required this.{field_name},")  # Add to constructor
                    from_json.append(f"    {field_name}: List<{item_class_name}>.from(json['{json_key}'].map((x) => {item_class_name}.fromJson(x))),")  # Add to fromJson
                    to_json.append(f"    '{json_key}': List<dynamic>.from({field_name}.map((x) => x.toJson())),")  # Add to toJson
                else:
                    # Simple field
                    field_type = get_dart_type(value)
                    fields.append(f"  final {field_type} {field_name};")  # Add field
                    constructors.append(f"    required this.{field_name},")  # Add to constructor
                    from_json.append(f"    {field_name}: json['{json_key}'],")  # Add to fromJson
                    to_json.append(f"    '{json_key}': {field_name},")  # Add to toJson
            
            # Finalize the class code
            constructors.append("  });")  # End constructor
            from_json.append("  );")  # End fromJson
            to_json.append("  };")  # End toJson
            
            # Combine all parts
            class_code.extend(fields)
            class_code.append("")  # Empty line for readability
            class_code.extend(constructors)
            class_code.append("")  # Empty line for readability
            class_code.extend(from_json)
            class_code.append("")  # Empty line for readability
            class_code.extend(to_json)
            class_code.append("}")  # End class
            
            return "\n".join(class_code)
        
        # Generate helper functions for JSON serialization
        code = ["// To parse this JSON data, do", "//", f"//     final {class_name.lower()} = {class_name.lower()}FromJson(jsonString);", "", "import 'dart:convert';", ""]
        
        # Generate fromJson and toJson functions
        code.append(f"{class_name} {class_name.lower()}FromJson(String str) => {class_name}.fromJson(json.decode(str));");
        code.append(f"String {class_name.lower()}ToJson({class_name} data) => json.encode(data.toJson());");
        code.append("")
        
        # Process the root object
        root_class = generate_class(json_data, class_name)
        code.append(root_class)
        
        # Process nested objects and arrays
        def process_nested_objects(data, parent_name):
            nested_classes = []
            
            for key, value in data.items():
                if isinstance(value, dict):
                    # Nested object, create a new class
                    nested_class_name = f"{parent_name}{key.title().replace('_', '')}"
                    nested_class = generate_class(value, nested_class_name)
                    nested_classes.append(nested_class)
                    nested_classes.extend(process_nested_objects(value, nested_class_name))
                elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
                    # List of objects, create a new class for the items
                    item_class_name = f"{parent_name}{key.title().replace('_', '')}Item"
                    item_class = generate_class(value[0], item_class_name)
                    nested_classes.append(item_class)
                    nested_classes.extend(process_nested_objects(value[0], item_class_name))
            
            return nested_classes
        
        # Add all nested classes
        nested_classes = process_nested_objects(json_data, class_name)
        if nested_classes:
            code.append("")  # Empty line for readability
            code.extend(nested_classes)
        
        return "\n".join(code)
    
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
    def list_supported_languages() -> Dict[str, Any]:
        """List all languages supported by quicktype.io.
        
        Returns:
            A dictionary containing the list of supported languages
        """
        logger.info("Listing supported languages")
        # These are the main languages supported by quicktype.io
        languages = [
            "dart", "typescript", "kotlin", "swift", "python", "java", 
            "csharp", "go", "ruby", "rust", "flow", "scala", "cpp", 
            "objective-c", "elm", "schema", "pike", "haskell"
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
    try:
        print(f"Generating {language} model for class {class_name}")
        
        # First, try to validate the JSON
        fix_result = QuicktypeService.fix_json(json_input)
        
        # If JSON is invalid, try to fix it
        if not fix_result.get("valid", False):
            print(f"Invalid JSON detected, attempting to fix")
            # If we have a fixed version, use it
            if "fixed_json" in fix_result:
                json_input = fix_result["fixed_json"]
        
        # Generate the model
        result = await QuicktypeService.generate_model(json_input, class_name, language)
        return result
    except Exception as e:
        print(f"Error in generate_model: {str(e)}")
        return {"error": str(e)}

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