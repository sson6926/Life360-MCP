from mcp.server.fastmcp import FastMCP
from life360_mcp.clients.life360 import Life360Client


def register_circle_tools(
    mcp: FastMCP,
    client: Life360Client,
):

    @mcp.tool()
    async def life360_list_circles() -> dict:
        """List Life360 circles."""

        return await client.list_circles()

    @mcp.tool()
    async def life360_get_circle(
        circle_id: str,
    ) -> dict:
        """Get a Life360 circle."""

        return await client.get_circle(circle_id)
