import json
from pathlib import Path
from rich.console import Console
from typing import Dict, Any # Import Dict and Any for type hints

CONFIG_FILE = Path.home() / '.terminal_gpt_config.json'
console = Console() # Need console for warnings in config loading

def load_config() -> Dict[str, Any]: # Add return type hint
    """Load config from file, return default config if error or file DNE"""
    default_config: Dict[str, Any] = { # Add type hint for default_config
        "show_timing": False,
        "system_prompt": "You are TerminalGPT, An artificial intelligence in my WSL Ubuntu. Your primary function is to help the user find and understand terminal commands for their needs. Respond with the command or list of commands that fulfill the users query, unless the user asks a question.", # Default system prompt
        "model": "llama-3.3-70b-versatile", # Default model
        "history_limit": 10 # Default history limit
    }
    config: Dict[str, Any] = default_config.copy() # Start with default config, add type hint

    if CONFIG_FILE.exists(): # Check for file existence
        try:
            user_config: Dict[str, Any] = json.loads(CONFIG_FILE.read_text()) # Add type hint for user_config
            config.update(user_config) # Update with user config, overwriting defaults
        except json.JSONDecodeError:
            console.print("[yellow]Warning: Config file corrupted. Using default config.[/yellow]")
            # config remains as default_config

    # Ensure system_prompt is always set, even if config file is broken or missing key
    if "system_prompt" not in config or not config["system_prompt"]:
        config["system_prompt"] = default_config["system_prompt"] # Fallback to default prompt
    # Ensure model is always set
    if "model" not in config or not config["model"]:
        config["model"] = default_config["model"] # Fallback to default model
    # Ensure history_limit is always set
    if "history_limit" not in config or not config["history_limit"]:
        config["history_limit"] = default_config["history_limit"] # Fallback to default history_limit

    return config


def save_config(config: Dict[str, Any]): # Add type hint for config parameter
    """Save config to file"""
    CONFIG_FILE.write_text(json.dumps(config, indent=2)) 