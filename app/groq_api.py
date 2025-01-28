import os
import sys
import requests
import time
import json
from rich.console import Console
from rich.status import Status
from rich.pretty import pprint
from rich.style import Style
from app.config import load_config

console = Console() # Console for API module's output
rin_style = Style(color="magenta", bold=True) # Style for Rin's output

def call_groq(query, history=[], timer=None, retries=3, initial_delay=1):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[red]Error: GROQ_API_KEY env var not set")
        sys.exit(1)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    config = load_config() # Load config to get system prompt
    system_prompt = config.get("system_prompt") # Get system prompt from config
    model = config.get("model") # Get model from config
    messages = [{"role": "system", "content": system_prompt}, *history, {"role": "user", "content": query}] # Construct messages

    data = {"model": model, "messages": messages}

    for attempt in range(retries):
        try:
            start_time = time.time() # Start time for timer
            with Status("[bold blue]Thinking... ", spinner="dots2") as status:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
                if timer:
                    timer.split("API Request Complete")
                elapsed_time = time.time() - start_time # Calculate elapsed time
                status.update(f"[bold blue]{elapsed_time:.2f}s Thinking...", spinner="dots2")
                response.raise_for_status()
                result = response.json()
                if timer:
                    timer.split("Response Processed")
                return _process_api_result(result)

        except requests.exceptions.RequestException as e:
            console.print(f"[red]Request Error (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(initial_delay * (attempt + 1))
            continue

        except json.JSONDecodeError as e:
            console.print(f"[red]JSON Decode Error (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(initial_delay * (attempt + 1))
            continue

        except Exception as e:
            console.print(f"[red]Unexpected API error (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(initial_delay * (attempt + 1))
            continue

    console.print("[red]Max retries reached. API call failed.")
    return None

def _process_api_result(result):
    if result.get("choices"): # Check if choices are in result
        message = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        token_counts = f"({usage.get('prompt_tokens', 0)}/{usage.get('completion_tokens', 0)}/{usage.get('total_tokens', 0)})"

        console_width = console.width # Get console width
        rin_text = "Rin: "
        padding_length = max(0, console_width - len(rin_text) - len(token_counts)) # Calculate padding
        padding = " " * padding_length # Create padding string
        rin_header = f"\nRin:{padding}{token_counts}" # Combine Rin name, padding, and token counts

        console.print(rin_header, style=rin_style, justify="left") # Print Rin's response header with right-aligned token counts
        console.print(message)

        return {"role": "assistant", "content": message}
    else:
        console.print("[red]Error: Unexpected response format")
        pprint(result)
        return None 