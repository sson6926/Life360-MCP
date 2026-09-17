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

    @mcp.tool()
    async def life360_get_low_battery_members(
        circle_id: str,
        threshold: int = 20,
    ) -> list[dict]:
        """
        Get list of members with low battery (<= threshold %, default 20%) or not charging.
        """
        return await service.get_low_battery_members(circle_id, threshold)

    @mcp.tool()
    async def life360_get_active_drivers(
        circle_id: str,
    ) -> list[dict]:
        """
        Get list of members who are currently driving or moving at speed.
        """
        return await service.get_active_drivers(circle_id)

    @mcp.tool()
    async def life360_get_distance_between_members(
        circle_id: str,
        member_id_1: str,
        member_id_2: str,
    ) -> dict:
        """
        Calculate distance in kilometers/meters between two members in a circle.
        """
        return await service.get_distance_between_members(
            circle_id, member_id_1, member_id_2
        )

    @mcp.tool()
    async def life360_get_safety_digest(
        circle_id: str,
    ) -> dict:
        """
        Get an executive safety digest for the entire circle (low battery, active drivers, total summary).
        """
        return await service.get_safety_digest(circle_id)
