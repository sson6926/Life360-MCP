import httpx

from life360_mcp.config import (
    BASE_URL,
    DEFAULT_USER_AGENT,
    DEVICE_ID,
    get_access_token,
)


class Life360Client:

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=BASE_URL,
            follow_redirects=True,
            timeout=15.0,
        )

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {get_access_token()}",
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/json",
            "X-Device-ID": DEVICE_ID,
        }

    async def _get(self, path: str) -> dict:
        response = await self.client.get(
            path,
            headers=self._headers(),
        )

        response.raise_for_status()

        return response.json()

    async def get_me(self):
        return await self._get("/v3/users/me")

    async def list_circles(self):
        return await self._get("/v3/circles")

    async def get_circle(self, circle_id: str):
        return await self._get(
            f"/v3/circles/{circle_id}"
        )

    async def get_places(self, circle_id: str):
        return await self._get(
            f"/v3/circles/{circle_id}/places"
        )

    async def close(self):
        await self.client.aclose()
