import sys
import types

from max_rag_bot.max_api import MaxApiClient


class _FakeResponse:
    def __init__(self, data: dict):
        self._data = data
        self.content = b"{}"

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._data


class _FakeClient:
    def __init__(self, *, base_url: str, timeout: float):
        self.base_url = base_url
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def post(self, path: str, json: dict, headers: dict):
        assert path == "/messages"
        assert headers["Authorization"].startswith("Bearer ")
        assert "chat_id" in json
        assert "text" in json
        return _FakeResponse({"ok": True, "echo": json})


def test_send_text_uses_max_messages_endpoint(monkeypatch):
    fake_httpx = types.SimpleNamespace(Client=_FakeClient)
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)

    client = MaxApiClient(token="token-1", base_url="https://botapi.max.ru", timeout_seconds=5)
    result = client.send_text(chat_id="chat-1", text="hello", reply_to_message_id="m-1")

    assert result["ok"] is True
    assert result["echo"]["reply_to_message_id"] == "m-1"
