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
        """Generate Dart model class with nullable fields and proper handling of nested objects
        
        Args:
            json_data: The JSON data to generate a model from
            class_name: The name of the generated class
            parent_name: The name of the parent class (used for nested objects)
            nested_classes: A dictionary of nested classes (used for recursive generation)
        
        Sample JSON:
        {
            "data": {
                "id": 101,
                "name": "Test User",
                "active": true,
                "created": "2023-10-15T08:30:00Z",
                "scores": [
                85.5,
                null,
                90
                ],
                "address": {
                "city": "San Francisco",
                "coordinates": {
                    "lat": 37.7749,
                    "lng": -122.4194
                }
                },
                "tags": [
                "user",
                "premium"
                ],
                "meta": {
                "devices": [
                    "mobile",
                    "desktop"
                ],
                "preferences": {
                    "theme": "dark",
                    "notifications": {
                    "email": true,
                    "push": null
                    }
                },
                "lastSeen": "2023-10-20T14:00:00Z"
                },
                "groups": [
                {
                    "id": 1,
                    "name": "Admin"
                }
                ],
                "expires": null
            }
        }

        Generated Dart Model:
                // To parse this JSON data, do
                //
                //     final sampleResponse = sampleResponseFromJson(jsonString);

                import 'dart:convert';

                SampleResponse sampleResponseFromJson(String str) => SampleResponse.fromJson(json.decode(str));

                String sampleResponseToJson(SampleResponse data) => json.encode(data.toJson());

                class SampleResponse {
                    SampleResponseData? data;

                    SampleResponse({
                        this.data,
                    });

                    factory SampleResponse.fromJson(Map<String, dynamic> json) => SampleResponse(
                        data: json["data"] == null ? null : SampleResponseData.fromJson(json["data"]),
                    );

                    Map<String, dynamic> toJson() => {
                        "data": data?.toJson(),
                    };
                }

                class SampleResponseData {
                    int? id;
                    String? name;
                    bool? active;
                    DateTime? created;
                    List<double?>? scores;
                    Address? address;
                    List<String>? tags;
                    Meta? meta;
                    List<Group>? groups;
                    dynamic expires;

                    SampleResponseData({
                        this.id,
                        this.name,
                        this.active,
                        this.created,
                        this.scores,
                        this.address,
                        this.tags,
                        this.meta,
                        this.groups,
                        this.expires,
                    });

                    factory SampleResponseData.fromJson(Map<String, dynamic> json) => SampleResponseData(
                        id: json["id"],
                        name: json["name"],
                        active: json["active"],
                        created: json["created"] == null ? null : DateTime.parse(json["created"]),
                        scores: json["scores"] == null ? [] : List<double?>.from(json["scores"]!.map((x) => x?.toDouble())),
                        address: json["address"] == null ? null : Address.fromJson(json["address"]),
                        tags: json["tags"] == null ? [] : List<String>.from(json["tags"]!.map((x) => x)),
                        meta: json["meta"] == null ? null : Meta.fromJson(json["meta"]),
                        groups: json["groups"] == null ? [] : List<Group>.from(json["groups"]!.map((x) => Group.fromJson(x))),
                        expires: json["expires"],
                    );

                    Map<String, dynamic> toJson() => {
                        "id": id,
                        "name": name,
                        "active": active,
                        "created": created?.toIso8601String(),
                        "scores": scores == null ? [] : List<dynamic>.from(scores!.map((x) => x)),
                        "address": address?.toJson(),
                        "tags": tags == null ? [] : List<dynamic>.from(tags!.map((x) => x)),
                        "meta": meta?.toJson(),
                        "groups": groups == null ? [] : List<dynamic>.from(groups!.map((x) => x.toJson())),
                        "expires": expires,
                    };
                }

                class Address {
                    String? city;
                    Coordinates? coordinates;

                    Address({
                        this.city,
                        this.coordinates,
                    });

                    factory Address.fromJson(Map<String, dynamic> json) => Address(
                        city: json["city"],
                        coordinates: json["coordinates"] == null ? null : Coordinates.fromJson(json["coordinates"]),
                    );

                    Map<String, dynamic> toJson() => {
                        "city": city,
                        "coordinates": coordinates?.toJson(),
                    };
                }

                class Coordinates {
                    double? lat;
                    double? lng;

                    Coordinates({
                        this.lat,
                        this.lng,
                    });

                    factory Coordinates.fromJson(Map<String, dynamic> json) => Coordinates(
                        lat: json["lat"]?.toDouble(),
                        lng: json["lng"]?.toDouble(),
                    );

                    Map<String, dynamic> toJson() => {
                        "lat": lat,
                        "lng": lng,
                    };
                }

                class Group {
                    int? id;
                    String? name;

                    Group({
                        this.id,
                        this.name,
                    });

                    factory Group.fromJson(Map<String, dynamic> json) => Group(
                        id: json["id"],
                        name: json["name"],
                    );

                    Map<String, dynamic> toJson() => {
                        "id": id,
                        "name": name,
                    };
                }

                class Meta {
                    List<String>? devices;
                    Preferences? preferences;
                    DateTime? lastSeen;

                    Meta({
                        this.devices,
                        this.preferences,
                        this.lastSeen,
                    });

                    factory Meta.fromJson(Map<String, dynamic> json) => Meta(
                        devices: json["devices"] == null ? [] : List<String>.from(json["devices"]!.map((x) => x)),
                        preferences: json["preferences"] == null ? null : Preferences.fromJson(json["preferences"]),
                        lastSeen: json["lastSeen"] == null ? null : DateTime.parse(json["lastSeen"]),
                    );

                    Map<String, dynamic> toJson() => {
                        "devices": devices == null ? [] : List<dynamic>.from(devices!.map((x) => x)),
                        "preferences": preferences?.toJson(),
                        "lastSeen": lastSeen?.toIso8601String(),
                    };
                }

                class Preferences {
                    String? theme;
                    Notifications? notifications;

                    Preferences({
                        this.theme,
                        this.notifications,
                    });

                    factory Preferences.fromJson(Map<String, dynamic> json) => Preferences(
                        theme: json["theme"],
                        notifications: json["notifications"] == null ? null : Notifications.fromJson(json["notifications"]),
                    );

                    Map<String, dynamic> toJson() => {
                        "theme": theme,
                        "notifications": notifications?.toJson(),
                    };
                }

                class Notifications {
                    bool? email;
                    dynamic push;

                    Notifications({
                        this.email,
                        this.push,
                    });

                    factory Notifications.fromJson(Map<String, dynamic> json) => Notifications(
                        email: json["email"],
                        push: json["push"],
                    );

                    Map<String, dynamic> toJson() => {
                        "email": email,
                        "push": push,
                    };
                }


        Returns:
            A string containing the generated Dart model code
        """
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
    
    # @staticmethod
    # def _generate_kotlin_model(json_data: dict, class_name: str) -> str:
    #     """Generate a Kotlin model from JSON data."""
    #     # Placeholder for Kotlin model generation
    #     return f"// Kotlin model for {class_name}\n// Not implemented yet"
    
 
    
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