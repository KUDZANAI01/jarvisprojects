import os
import json
from datetime import datetime
from typing import List, Dict

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class FridayAssistant:
    def __init__(self):
        self.name = "FRIDAY"
        self.memory: List[Dict[str, str]] = []
        self.todos: List[str] = []

        if load_dotenv:
            load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def add_memory(self, user_input: str, response: str):
        self.memory.append({"user": user_input, "assistant": response})

    def handle_command(self, text: str) -> str:
        command = text.strip().lower()

        if command in ["hi", "hello", "hey"]:
            return "Hello! I am FRIDAY, your AI assistant. How can I help you today?"

        if command.startswith("todo"):
            if len(command) <= 4:
                return f"Current tasks: {self.todos if self.todos else 'No tasks yet.'}"
            task = command[5:].strip()
            if task:
                self.todos.append(task)
                return f"Added task: '{task}'"
            return "Usage: todo <task>"

        if command.startswith("remove todo"):
            task = command[11:].strip()
            if task:
                if task in self.todos:
                    self.todos.remove(task)
                    return f"Removed task: '{task}'"
                return f"Task not found: '{task}'"
            return "Usage: remove todo <task>"

        if command == "tasks":
            return f"Current tasks: {self.todos if self.todos else 'No tasks yet.'}"

        if command == "time":
            return f"The current time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

        if command == "help":
            return (
                "Available commands:\n"
                "- hi / hello / hey\n"
                "- time\n"
                "- todo <task>\n"
                "- tasks\n"
                "- remove todo <task>\n"
                "- exit"
            )

        if command == "exit":
            raise KeyboardInterrupt

        return None

    def generate_reply(self, user_input: str) -> str:
        command_response = self.handle_command(user_input)
        if command_response is not None:
            return command_response

        if not self.api_key or OpenAI is None:
            return (
                f"FRIDAY: I’m running in local demo mode. "
                f"You said: '{user_input}'\n"
                "If you add an OpenAI API key, I can respond with real AI-generated answers."
            )

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        messages = [
            {"role": "system", "content": "You are FRIDAY, a helpful AI assistant."},
            *self.memory,
            {"role": "user", "content": user_input},
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )

        result = response.choices[0].message.content.strip()
        return result

    def chat(self):
        print(f"{self.name} is online. Type 'help' for commands or 'exit' to quit.")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                response = self.generate_reply(user_input)
                print(f"{self.name}: {response}")
                self.add_memory(user_input, response)

            except KeyboardInterrupt:
                print("\nFRIDAY: Goodbye.")
                break


if __name__ == "__main__":
    assistant = FridayAssistant()
    assistant.chat()
