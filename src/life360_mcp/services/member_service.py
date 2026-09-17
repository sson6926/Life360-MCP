import math
from life360_mcp.clients.life360 import Life360Client


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in km using Haversine formula."""
    if None in (lat1, lon1, lat2, lon2):
        return -1.0
    
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


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

    async def get_low_battery_members(
        self,
        circle_id: str,
        threshold: int = 20,
    ) -> list[dict]:
        """Find members whose battery is below threshold or not charging."""
        members = await self.get_members_summary(circle_id)
        low_battery_list = []

        for m in members:
            try:
                bat_val = int(m.get("battery") or 100)
            except (ValueError, TypeError):
                bat_val = 100

            if bat_val <= threshold:
                low_battery_list.append({
                    "id": m["id"],
                    "name": m["name"],
                    "battery": bat_val,
                    "is_charging": m["is_charging"],
                    "address": m["address"],
                    "phone": m["phone"],
                })

        return low_battery_list

    async def get_active_drivers(
        self,
        circle_id: str,
    ) -> list[dict]:
        """Find members who are currently driving or moving at speed."""
        members = await self.get_members_summary(circle_id)
        drivers = []

        for m in members:
            speed_val = 0.0
            try:
                speed_val = float(m.get("speed") or 0.0)
            except (ValueError, TypeError):
                speed_val = 0.0

            if m["is_driving"] or speed_val > 5.0:
                drivers.append({
                    "id": m["id"],
                    "name": m["name"],
                    "is_driving": m["is_driving"],
                    "speed": speed_val,
                    "address": m["address"],
                    "latitude": m["latitude"],
                    "longitude": m["longitude"],
                    "last_updated": m["last_updated"],
                })

        return drivers

    async def get_distance_between_members(
        self,
        circle_id: str,
        member_id_1: str,
        member_id_2: str,
    ) -> dict:
        """Calculate real distance (in km) between two members."""
        members = await self.get_members_summary(circle_id)
        m1 = next((m for m in members if m["id"] == member_id_1), None)
        m2 = next((m for m in members if m["id"] == member_id_2), None)

        if not m1 or not m2:
            return {
                "error": "Không tìm thấy một hoặc cả hai thành viên trong Circle."
            }

        try:
            lat1, lon1 = float(m1["latitude"]), float(m1["longitude"])
            lat2, lon2 = float(m2["latitude"]), float(m2["longitude"])
        except (ValueError, TypeError):
            return {
                "error": "Tọa độ GPS của một trong hai thành viên không hợp lệ."
            }

        dist_km = calculate_distance_km(lat1, lon1, lat2, lon2)

        return {
            "member_1": {"id": m1["id"], "name": m1["name"], "address": m1["address"]},
            "member_2": {"id": m2["id"], "name": m2["name"], "address": m2["address"]},
            "distance_km": dist_km,
            "distance_meters": int(dist_km * 1000),
        }

    async def get_safety_digest(
        self,
        circle_id: str,
    ) -> dict:
        """Executive summary of safety status for the entire circle."""
        members = await self.get_members_summary(circle_id)
        total_members = len(members)

        low_battery = [m for m in members if m.get("battery") and int(m["battery"] or 100) <= 20]
        driving = [m for m in members if m.get("is_driving")]

        return {
            "total_members": total_members,
            "members_driving_count": len(driving),
            "members_low_battery_count": len(low_battery),
            "driving_members": [m["name"] for m in driving],
            "low_battery_members": [
                f"{m['name']} ({m['battery']}%)" for m in low_battery
            ],
            "summary_status": (
                "Cảnh báo: Có thành viên pin yếu hoặc đang di chuyển!"
                if (low_battery or driving)
                else "Tất cả thành viên an toàn, không có rủi ro phát hiện."
            ),
        }
