# TerminalGPT: Blazing Fast AI in Your Terminal

Get instant AI responses, especially terminal commands, right from your command line with **TerminalGPT**.  Powered by the lightning-fast [Groq API](https://console.groq.com/), TerminalGPT delivers answers in a snap, making your terminal even more powerful.

## Features

*   **Instant Answers:** Leverage the speed of Groq for near-instant AI responses.
*   **Completely Free:** Groq provides a free tier, with a generous 30 rq/m and 6k t/m, making this completely free! 
*   **Command-Line Focused:** Optimized for generating terminal commands and answering development-related questions.
*   **Chat Mode:**  Engage in interactive conversations with TerminalGPT.
*   **Configuration:** Customize system prompts, models, and history limits.
*   **History:**   сохраняет chat history (with configurable limit).
*   **Timing:** Optional display of API request and processing times.
*   **Simple Commands:** Control chat with easy commands like `/clear`, `/time`, `/exit`, and `/quit`.

## Setup

### Prerequisites

*   **Python 3.13+**
*   **Groq API Key:**  Get your free API key from [Groq Console](https://console.groq.com/) and set it as an environment variable:

    ```bash
    export GROQ_API_KEY="YOUR_API_KEY"
    ```

### Installation

1.  **Clone the repository (or download the files):**

    ```bash
    git clone [repository_url] # Replace with your repository URL if you have one
    cd ai-cli # Or whatever you named the directory
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt # If you create a requirements.txt, or just install rich and requests
    ```
    *(Alternatively, since this project uses script metadata, you might be able to use a tool like `pipx` if you package it correctly, but for now `pip install -r requirements.txt` is easiest)*

    *(If you don't have a `requirements.txt`, you can create one or install manually)*

    ```bash
    pip install requests rich
    ```
## Usage

### Single query

```bash
python hello.py "What is the command to list all files in the current directory?"
```

### Chat mode

```bash
python hello.py
```

### Configuration

```bash
python hello.py /clear or /c
```

```bash
python hello.py /time or /t
```
