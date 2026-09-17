from mcp.server.fastmcp import FastMCP

from life360_mcp.clients.life360 import Life360Client
from life360_mcp.services.member_service import MemberService

from life360_mcp.tools.user import register_user_tools
from life360_mcp.tools.circles import register_circle_tools
from life360_mcp.tools.members import register_member_tools
from life360_mcp.tools.places import register_place_tools


mcp = FastMCP("Life360 MCP Server")

client = Life360Client()

member_service = MemberService(client)


register_user_tools(
    mcp,
    client,
)

register_circle_tools(
    mcp,
    client,
)

register_member_tools(
    mcp,
    member_service,
)

register_place_tools(
    mcp,
    client,
)


def main():
    mcp.run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()
