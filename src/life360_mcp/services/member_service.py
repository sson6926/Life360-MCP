from life360_mcp.clients.life360 import Life360Client


class MemberService:

    def __init__(self, client: Life360Client):
        self.client = client

    async def get_members_summary(
        self,
        circle_id: str,
    ) -> list[dict]:

        data = await self.client.get_circle(circle_id)

        result = []

        for member in data.get("members", []):
            loc = member.get("location") or {}

            result.append({
                "id": member.get("id"),
                "name": (
                    f"{member.get('firstName', '')} "
                    f"{member.get('lastName', '')}"
                ).strip(),
                "phone": member.get("loginPhone"),
                "battery": loc.get("battery"),
                "is_charging": loc.get("charge") == "1",
                "address": (
                    loc.get("address1")
                    or loc.get("shortAddress")
                    or "Không xác định"
                ),
                "place_name": loc.get("name"),
                "latitude": loc.get("latitude"),
                "longitude": loc.get("longitude"),
                "is_driving": loc.get("isDriving") == "1",
                "speed": loc.get("speed"),
                "last_updated": loc.get("timestamp"),
            })

        return result
