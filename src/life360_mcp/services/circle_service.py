from life360_mcp.clients.life360 import Life360Client


class CircleService:

    def __init__(self, client: Life360Client):
        self.client = client

    async def list_circles(self) -> dict:
        return await self.client.list_circles()

    async def get_circle(self, circle_id: str) -> dict:
        return await self.client.get_circle(circle_id)
