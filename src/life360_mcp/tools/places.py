from mcp.server.fastmcp import FastMCP
from life360_mcp.clients.life360 import Life360Client


def register_place_tools(
    mcp: FastMCP,
    client: Life360Client,
):

    @mcp.tool()
    async def life360_get_places(
        circle_id: str,
    ) -> dict:
        """
        Get saved places for a Life360 circle.
        """

        return await client.get_places(circle_id)
