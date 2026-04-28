from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MaxApiClient:
    """HTTP client for MAX Bot API."""

    token: str
    base_url: str = "https://botapi.max.ru"
    timeout_seconds: float = 30.0

    def send_text(self, chat_id: str, text: str, reply_to_message_id: str | None = None) -> dict:
        """Send a text message to MAX chat via Bot API.

        Endpoint follows the common bot pattern:
        POST /messages with bearer token + JSON payload.
        """
        payload: dict[str, str] = {
            "chat_id": chat_id,
            "text": text,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        import httpx

        with httpx.Client(base_url=self.base_url, timeout=self.timeout_seconds) as client:
            response = client.post("/messages", json=payload, headers=headers)
            response.raise_for_status()
            return response.json() if response.content else {"ok": True}
