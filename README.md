# jarvisprojects

This repository contains a starter FRIDAY AI assistant project.

## Features
- Chat-based assistant using OpenAI-compatible APIs
- Local command support for `time`, `todo`, and `tasks`
- Memory of previous interactions
- Easy setup with `.env` configuration

## Run locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

4. Add your OpenAI API key to `.env`.

5. Start the assistant:
   ```bash
   python friday_assistant.py
   ```

## Example usage

```text
You: hello
FRIDAY: Hello! I am FRIDAY, your AI assistant. How can I help you today?

You: time
FRIDAY: The current time is 2026-10-27 12:34:56.

You: todo write project plan
FRIDAY: Added task: 'write project plan'
```
