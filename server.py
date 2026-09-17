import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Life360 MCP Server")

BASE_URL = "https://api-cloudfront.life360.com"
DEFAULT_USER_AGENT = "com.life360.android.safetymapd/KOKO/26.31.0 android/14/00000000-0000-0000-0000-000000000001"

def get_headers():
    token = os.getenv("LIFE360_ACCESS_TOKEN")
    if not token:
        raise ValueError("Thiếu biến môi trường LIFE360_ACCESS_TOKEN!")
    
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json",
        "X-Device-ID": "00000000-0000-0000-0000-000000000001"
    }

@mcp.tool()
async def life360_get_me() -> dict:
    """Lấy thông tin tài khoản cá nhân Life360 (Tên, Email, SĐT, Cài đặt)."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{BASE_URL}/v3/users/me", headers=get_headers())
        res.raise_for_status()
        return res.json()

@mcp.tool()
async def life360_list_circles() -> dict:
    """Lấy danh sách các Nhóm (Circles) mà bạn tham gia (ID, tên nhóm, số thành viên)."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{BASE_URL}/v3/circles", headers=get_headers())
        res.raise_for_status()
        return res.json()

@mcp.tool()
async def life360_get_circle(circle_id: str) -> dict:
    """
    Lấy toàn bộ thông tin của 1 Nhóm (Circle), bao gồm danh sách thành viên:
    tên, địa chỉ hiện tại, tọa độ GPS, % pin, trạng thái sạc, tốc độ, trạng thái di chuyển/lái xe.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{BASE_URL}/v3/circles/{circle_id}", headers=get_headers())
        res.raise_for_status()
        return res.json()

@mcp.tool()
async def life360_get_members_summary(circle_id: str) -> list:
    """
    Lấy bản tóm tắt gọn gàng vị trí & trạng thái của tất cả thành viên trong Nhóm (Circle).
    Dễ đọc cho AI: Tên, Địa chỉ, Tọa độ GPS, % Pin, Trạng thái di chuyển.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{BASE_URL}/v3/circles/{circle_id}", headers=get_headers())
        res.raise_for_status()
        data = res.json()
        
        summary = []
        for member in data.get("members", []):
            loc = member.get("location") or {}
            summary.append({
                "id": member.get("id"),
                "name": f"{member.get('firstName', '')} {member.get('lastName', '')}".strip(),
                "phone": member.get("loginPhone"),
                "battery": f"{loc.get('battery', 'N/A')}%",
                "is_charging": loc.get("charge") == "1",
                "address": loc.get("address1") or loc.get("shortAddress") or "Không xác định",
                "place_name": loc.get("name"), # Nếu đang ở Địa điểm đã lưu (như Home, PTIT...)
                "latitude": loc.get("latitude"),
                "longitude": loc.get("longitude"),
                "is_driving": loc.get("isDriving") == "1",
                "speed": loc.get("speed"),
                "last_updated": loc.get("timestamp")
            })
        return summary

@mcp.tool()
async def life360_get_places(circle_id: str) -> dict:
    """Lấy danh sách các Địa điểm cố định đã lưu trong Nhóm (Nhà, Trường học, Công ty...) kèm bán kính geofence."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{BASE_URL}/v3/circles/{circle_id}/places", headers=get_headers())
        res.raise_for_status()
        return res.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
