from mcp.server.fastmcp import FastMCP

from life360_mcp.services.member_service import MemberService


def register_member_tools(
    mcp: FastMCP,
    service: MemberService,
):

    @mcp.tool()
    async def life360_get_members_summary(
        circle_id: str,
    ) -> list[dict]:
        """
        Get location and status summary
        for members of a Life360 circle.
        """

        return await service.get_members_summary(circle_id)
