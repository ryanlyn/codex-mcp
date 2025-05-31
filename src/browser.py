"""Browser connection management for Codex MCP."""

import httpx

DEFAULT_CDP_PORT = 9242
DEFAULT_USER_DATA_DIR = "~/.config/browseruse/profiles/codex"


def get_default_launch_command() -> str:
    """Get the command to launch Chrome with remote debugging."""
    return (
        f"/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome "
        f"--remote-debugging-port={DEFAULT_CDP_PORT} "
        f"--user-data-dir={DEFAULT_USER_DATA_DIR}"
    )


class BrowserConnection:
    """Manages browser connection via Chrome DevTools Protocol."""

    def __init__(self, port: int = DEFAULT_CDP_PORT):
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self._connection_status: bool | None = None

    async def test_connection(self, force: bool = False) -> bool:
        if not force and not self._connection_status:  # retry when missing or False
            return self._connection_status

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/json/version")
                self._connection_status = response.status_code == 200
                return self._connection_status
        except (httpx.ConnectError, httpx.TimeoutException):
            self._connection_status = False
            return False

    def test_connection_sync(self, force: bool = False) -> bool:
        if not force and not self._connection_status:  # retry when missing or False
            return self._connection_status

        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{self.base_url}/json/version")
                self._connection_status = response.status_code == 200
                return self._connection_status
        except (httpx.ConnectError, httpx.TimeoutException):
            self._connection_status = False
            return False
