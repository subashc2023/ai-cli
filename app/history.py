import json
from pathlib import Path
from rich.console import Console
from app.config import load_config

HISTORY_FILE = Path.home() / '.terminal_gpt_history.json'
console = Console() # Need console for warnings

def load_chat_history():
    """Load chat history from file, return empty list if error or file DNE"""
    config = load_config()
    history_limit = config.get("history_limit")
    try:
        if HISTORY_FILE.exists():
            history = json.loads(HISTORY_FILE.read_text())
            return history[-history_limit:] if history_limit else history
    except json.JSONDecodeError:
        console.print("[yellow]Warning: Chat history file corrupted. Starting fresh.")
    return []

def save_chat_history(history):
    """Save chat history to file"""
    config = load_config()
    history_limit = config.get("history_limit")
    if history_limit:
        history = history[-history_limit:]
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

def clear_chat_history():
    """Clear the chat history file"""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
        console.print("[green]Chat history cleared!")
        return True # Indicate history was cleared
    else:
        console.print("[yellow]No chat history found.")
        return False # Indicate history was not cleared 