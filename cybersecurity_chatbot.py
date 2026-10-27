import os
import re
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


class CyberSecurityAssistant:
    def __init__(self):
        self.name = "CYBERFRIDAY"
        self.memory: List[Dict[str, str]] = []

        if load_dotenv:
            load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def add_memory(self, user_input: str, response: str):
        self.memory.append({"user": user_input, "assistant": response})

    def analyze_password_strength(self, password: str) -> str:
        if len(password) < 8:
            return "Weak: Use at least 12+ characters."

        checks = {
            "length": len(password) >= 12,
            "uppercase": bool(re.search(r"[A-Z]", password)),
            "lowercase": bool(re.search(r"[a-z]", password)),
            "number": bool(re.search(r"\d", password)),
            "symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        }

        score = sum(checks.values())
        if score >= 5:
            return "Strong: Good length and complexity."
        if score >= 4:
            return "Moderate: Add a few more character types."
        return "Weak: Use a longer password with uppercase, numbers, and symbols."

    def analyze_phishing_email(self, email_text: str) -> str:
        email_lower = email_text.lower()
        indicators = []

        if any(word in email_lower for word in ["urgent", "immediate", "act now", "verify account", "limited time"]):
            indicators.append("Urgency language")
        if any(word in email_lower for word in ["click here", "update your credentials", "suspended account", "invoice due"]):
            indicators.append("Credential harvesting language")
        if "http://" in email_lower and "https://" not in email_lower:
            indicators.append("Potentially insecure URL")
        if any(word in email_lower for word in ["@gmail.com", "@outlook.com", "free", "winner", "prize"]):
            indicators.append("Suspicious sender or content pattern")

        if indicators:
            return (
                "Possible phishing attempt detected. Risk indicators: " + ", ".join(indicators)
                + ". Do not click links, verify via official channels, and report the email."
            )
        return "No clear phishing indicators detected from the sample, but remain cautious and verify sender legitimacy."

    def analyze_log_entry(self, log_line: str) -> str:
        if "failed password" in log_line.lower() or "authentication failed" in log_line.lower():
            return "Possible brute-force or credential attack. Block the source if it is unauthorized and review login logs."
        if "denied" in log_line.lower() and "firewall" in log_line.lower():
            return "Firewall policy triggered. Check whether the access was valid or malicious."
        if "malware" in log_line.lower() or "virus" in log_line.lower():
            return "Potential malware detection. Isolate the host and run full forensic review."
        if "unauthorized" in log_line.lower() or "access denied" in log_line.lower():
            return "Unauthorized access activity suspected. Review user permissions and incident response logs."
        return "Log pattern does not show an obvious security event, but investigate if it repeats or correlates with other alerts."

    def incident_summary(self, symptoms: str) -> str:
        summary = [
            "1. Contain the affected system or user account.",
            "2. Preserve logs, backups, and forensic evidence.",
            "3. Identify the entry point, affected systems, and scope of impact.",
            "4. Remove malware, revoke sessions, and reset credentials as needed.",
            "5. Communicate with stakeholders and document the incident response timeline."
        ]
        return "Incident response checklist:\n" + "\n".join(summary) + f"\n\nContext: {symptoms}"

    def handle_command(self, text: str):
        command = text.strip().lower()

        if command in ["hi", "hello", "hey"]:
            return "Hello. I am CYBERFRIDAY, your cybersecurity assistant. Ask me about phishing, password strength, malware, or incident response."

        if command.startswith("password "):
            password = text.split("password ", 1)[1].strip()
            if password:
                return self.analyze_password_strength(password)
            return "Usage: password <your_password>"

        if command.startswith("phishing "):
            sample = text.split("phishing ", 1)[1].strip()
            if sample:
                return self.analyze_phishing_email(sample)
            return "Usage: phishing <email text>"

        if command.startswith("log "):
            log_line = text.split("log ", 1)[1].strip()
            if log_line:
                return self.analyze_log_entry(log_line)
            return "Usage: log <log entry>"

        if command == "help":
            return (
                "Available commands:\n"
                "- hello\n"
                "- password <value>\n"
                "- phishing <email text>\n"
                "- log <log entry>\n"
                "- report <incident summary>\n"
                "- exit"
            )

        if command.startswith("report "):
            context = text.split("report ", 1)[1].strip()
            if context:
                return self.incident_summary(context)
            return "Usage: report <incident context>"

        if command == "tips":
            return (
                "Security tips:\n"
                "- Use MFA on all critical accounts.\n"
                "- Verify unexpected emails by contacting the sender through a trusted channel.\n"
                "- Patch systems regularly and monitor for suspicious login activity.\n"
                "- Back up important data and limit privilege escalation."
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
                "CYBERFRIDAY is running in offline mode. "
                "I can still help with common cyber hygiene checks and incident guidance. \n"
                "Try: password, phishing, log, or report."
            )

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are CYBERFRIDAY, a cybersecurity assistant. "
                    "Provide brief, practical, cyber-focused advice on phishing, endpoint security, log analysis, "
                    "password hygiene, and incident response."
                )
            },
            *self.memory,
            {"role": "user", "content": user_input},
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

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
                print("\nCYBERFRIDAY: Session closed.")
                break


if __name__ == "__main__":
    assistant = CyberSecurityAssistant()
    assistant.chat()

