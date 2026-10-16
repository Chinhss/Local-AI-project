import json

import httpx

from local_ai.prompts import SYSTEM_PROMPT


class OllamaClient:
    def __init__(
        self,
        model: str = "qwen3-coder:30b",
        base_url: str = "http://localhost:11434",
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.model = model
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.messages = []

    def clear(self) -> None:
        self.messages = []

    def _request_messages(self) -> list:
        return [{"role": "system", "content": self.system_prompt}] + self.messages

    def chat(self, prompt: str) -> str:
        self.messages.append({
            "role": "user",
            "content": prompt
        })

        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self._request_messages(),
                    "stream": False,
                },
                timeout=300.0,
            )
            response.raise_for_status()
            data = response.json()
            content = data["message"]["content"]
        except Exception:
            self.messages.pop()
            raise

        self.messages.append({
            "role": "assistant",
            "content": content
        })

        return content

    def stream_chat(self, prompt: str):
        self.messages.append({
            "role": "user",
            "content": prompt
        })
        assistant_message = ""

        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self._request_messages(),
                    "stream": True,
                },
                timeout=300.0,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue

                    data = json.loads(line)
                    content = data.get("message", {}).get("content", "")

                    if content:
                        assistant_message += content
                        yield content
        except BaseException:
            self.messages.pop()
            raise

        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })