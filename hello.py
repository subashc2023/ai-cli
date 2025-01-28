# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests<3",
#     "rich",
# ]
# ///
import os
import json
import requests
import sys
import time
import argparse # Import argparse
from rich.pretty import pprint
from rich.console import Console
from rich.style import Style
from rich.status import Status
from rich.table import Table
from pathlib import Path

from app.timer import Timer  # Import Timer class from app folder
from app.config import load_config, save_config
from app.history import load_chat_history, save_chat_history, clear_chat_history
from app.groq_api import call_groq

console = Console()

def handle_command(command, config):
    """Handles special commands like /clear, /time, /exit, /quit."""
    if command in ["/clear", "/c"]:
        if clear_chat_history(): # clear_chat_history now returns bool
            return True, None # Indicate history cleared, no query to process
        return True, None # Command handled, no query to process
    elif command in ["/time", "/t"]:
        config["show_timing"] = not config.get("show_timing", False)
        save_config(config)
        console.print(f"[green]Timing is now {'on' if config['show_timing'] else 'off'}.[/green]")
        return True, None # Command handled, no query to process
    elif command in ["/exit", "/quit"]:
        return True, None # Indicate exit, no query to process
    return False, command # Not a special command, return original command

def main():
    config = load_config()
    show_timing = config.get("show_timing", False)

    parser = argparse.ArgumentParser(description="TerminalGPT")
    parser.add_argument("query", nargs="?", help="The query to ask TerminalGPT")
    args = parser.parse_args()

    timer = Timer().start() if show_timing else None


    history = load_chat_history()

    if args.query:
        # Initial query from command line
        command_handled, query = handle_command(args.query.lower(), config) # Handle command
        if command_handled:
            sys.exit(0) # Exit if command was handled (like /clear or /time in CLI mode)
        assistant_response = call_groq(query, history, timer)

        if assistant_response:
            history.append({"role": "user", "content": query})
            history.append(assistant_response)
            save_chat_history(history)
            if timer:
                timer.split("History Saved")
                console.print("\n")
                console.print(timer.get_table())

    else:
        # Free-flowing chat mode
        console.print("[bold green]Entering chat mode. Type '/exit', '/quit', '/clear'(/c), or '/time'(/t) to control the chat.[/bold green]")
        while True:
            query = console.input("[bold blue]You: ")
            command_handled, query = handle_command(query.lower(), config) # Handle command
            if command_handled:
                if query is None and command in ["/clear", "/c"]: # Special case for /clear in chat mode
                    history = [] # Reset history in chat mode after /clear
                if query is None and command in ["/exit", "/quit"]: # Exit chat loop
                    break # Exit chat mode loop
                continue # For /time and /clear, continue to next loop iteration

            assistant_response = call_groq(query, history, timer)
            if assistant_response:
                history.append({"role": "user", "content": query})
                history.append(assistant_response)
                save_chat_history(history)
                if timer:
                    timer.split("History Saved")
                    console.print("\n")
                    console.print(timer.get_table())


if __name__ == "__main__":
    main()