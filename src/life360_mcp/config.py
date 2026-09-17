import os

BASE_URL = "https://api-cloudfront.life360.com"

DEFAULT_USER_AGENT = (
    "com.life360.android.safetymapd/KOKO/"
    "26.31.0 android/14/"
    "00000000-0000-0000-0000-000000000001"
)

DEVICE_ID = "00000000-0000-0000-0000-000000000001"


def get_access_token() -> str:
    token = os.getenv("LIFE360_ACCESS_TOKEN")

    if not token:
        raise RuntimeError(
            "Missing environment variable LIFE360_ACCESS_TOKEN"
        )

    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    return token
