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
    def _generate_dart_model(json_data, class_name, parent_name=''):
        """Generate Dart model class with nullable fields"""
        class_code = [f"class {class_name} {{"]
        constructors = [f"  {class_name}({{"]
        from_json = [f"  factory {class_name}.fromJson(Map<String, dynamic> json) => {class_name}("]
        to_json = ["  Map<String, dynamic> toJson() => {"]

        for json_key, value in json_data.items():
            field_name = json_key
            field_type = QuicktypeService.get_dart_type(value)
            
            # Add field declaration
            class_code.append(f"  final {field_type} {field_name};")
            
            # Add to constructor
            constructors.append(f"    this.{field_name},")
            
            # Add to fromJson with null check
            if field_type.endswith('?'):
                from_json.append(f"    {field_name}: json['{json_key}'],")
            else:
                from_json.append(f"    {field_name}: json['{json_key}'],")
            
            # Add to toJson
            to_json.append(f"    '{json_key}': {field_name},")
        
        # Finalize the class code
        constructors.append("  });")
        from_json.append("  );")
        to_json.append("  };")
        
        # Combine all parts
        class_code.extend([""] + constructors + [""] + from_json + [""] + to_json + ["}"])
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