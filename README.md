# Life360 MCP Server (Python)

Model Context Protocol (MCP) Server cho Life360 API, được thiết kế theo kiến trúc layered (Tools -> Services -> Clients -> API).

## 🏗️ Kiến trúc dự án

```
life360-mcp/
├── pyproject.toml
├── .env.example
├── README.md
│
└── src/
    └── life360_mcp/
        ├── __init__.py
        ├── server.py        # Wiring dependencies & MCP entrypoint
        ├── config.py        # Centralized config
        ├── exceptions.py    # Custom exceptions
        │
        ├── clients/         # HTTP API abstraction (Single Client Instance)
        │   └── life360.py
        │
        ├── services/        # Business logic & data transformations cho LLM
        │   ├── circle_service.py
        │   └── member_service.py
        │
        ├── tools/           # FastMCP Tool Registrations
        │   ├── user.py
        │   ├── circles.py
        │   ├── members.py
        │   └── places.py
        │
        └── models/          # Data models / Schemas
            └── member.py
```

## 🚀 Hướng dẫn cài đặt & Chạy

### 1. Cài đặt package
```bash
pip install -e .
```
Hoặc cài đặt dependencies thủ công:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình MCP Client (Ví dụ: Claude Desktop)
Thêm vào file `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "life360": {
      "command": "python3",
      "args": [
        "-m",
        "life360_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "/path/to/life360-mcp/src",
        "LIFE360_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```
