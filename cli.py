#!/usr/bin/env python3
import os
import sys
import argparse
import threading
import logging
import time

# Import the MCP server from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import mcp, logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def start_server_thread():
    """Start the MCP server in a separate thread"""
    logger.info("Starting MCP server in background thread")
    server_thread = threading.Thread(target=mcp.run)
    server_thread.daemon = True
    server_thread.start()
    # Give the server a moment to start
    time.sleep(1)
    return server_thread

def main():
    parser = argparse.ArgumentParser(description="Quicktype MCP Server and Client")
    parser.add_argument("--server-only", action="store_true", help="Run only the MCP server")
    parser.add_argument("--json", type=str, help="JSON input to process")
    parser.add_argument("--language", type=str, default="dart", help="Target language (default: dart)")
    parser.add_argument("--class-name", type=str, default="Model", help="Class name for the generated model")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--windsurf", action="store_true", help="Run in Windsurf MCP compatibility mode")
    args = parser.parse_args()
    
    # If no arguments are provided or --windsurf flag is set, run in Windsurf MCP compatibility mode
    if len(sys.argv) == 1 or args.server_only or args.windsurf:
        # Run the server in the main thread
        logger.info("Starting MCP server in server-only mode")
        print("Starting Quicktype MCP server...")
        print("Available MCP tools:")
        print("  - generate_model: Generate code models from JSON")
        print("  - list_languages: List supported programming languages")
        print("  - fix_json: Fix invalid JSON")
        print("\nServer is running. Press Ctrl+C to stop.")
        
        try:
            # This will keep the server running until interrupted
            mcp.run()
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        except Exception as e:
            print(f"\nServer error: {str(e)}")
            logger.error(f"Server error: {str(e)}")
            sys.exit(1)
    elif args.json:
        # Process a single JSON input and exit
        import json
        import asyncio
        from main import QuicktypeService
        
        print(f"Processing JSON input for {args.language} model...")
        
        # Read JSON from file or use directly
        try:
            if os.path.isfile(args.json):
                with open(args.json, 'r') as f:
                    json_input = f.read()
                print(f"Read JSON from file: {args.json}")
            else:
                json_input = args.json
                print("Using provided JSON string")
            
            # Process the JSON
            result = asyncio.run(QuicktypeService.generate_model(
                json_input=json_input,
                class_name=args.class_name,
                language=args.language
            ))
            
            if "error" in result:
                print(f"Error: {result['error']}")
                sys.exit(1)
            
            # Output the generated code
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(result['code'])
                print(f"Generated {args.language} model saved to {args.output}")
            else:
                print("\nGenerated code:")
                print("=" * 40)
                print(result['code'])
                print("=" * 40)
            
            print("\nDone!")
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    else:
        print("Quicktype MCP Client")
        print("Usage:")
        print("  --server-only: Run the MCP server in continuous mode")
        print("  --json <input>: Process JSON input (string or file path)")
        print("  --language <lang>: Target language (default: dart)")
        print("  --class-name <name>: Class name for the model (default: Model)")
        print("  --output <file>: Output file path (optional)")
        print("\nExample:")
        print("  python cli.py --json input.json --language dart --class-name User --output user_model.dart")
        print("\nRun with --server-only to start the MCP server in continuous mode.")
        sys.exit(0)

if __name__ == "__main__":
    main()