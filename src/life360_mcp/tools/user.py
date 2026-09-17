from mcp.server.fastmcp import FastMCP
from life360_mcp.clients.life360 import Life360Client


def register_user_tools(
    mcp: FastMCP,
    client: Life360Client,
):

    @mcp.tool()
    async def life360_get_me() -> dict:
        """Get current Life360 user."""

        return await client.get_me()
