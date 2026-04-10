import sqlite3
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 初始化 MCP 服务器
app = Server("db-crud-tool")

# 初始化 SQLite 数据库 (演示用)
def init_db():
    conn = sqlite3.connect("./tmp/demo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER
        )
    """)
    conn.commit()
    conn.close()

# 数据库连接辅助函数
def get_connection():
    return sqlite3.connect("./tmp/demo.db")

# --- 定义 MCP 工具 ---

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_user",
            description="在数据库中创建一个新的用户记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户姓名"},
                    "email": {"type": "string", "description": "用户邮箱 (必须唯一)"},
                    "age": {"type": "integer", "description": "用户年龄"}
                },
                "required": ["name", "email"]
            }
        ),
        Tool(
            name="read_users",
            description="查询数据库中的用户，可以带条件查询",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "可选：按ID查询特定用户"},
                    "name_filter": {"type": "string", "description": "可选：按姓名模糊查询"}
                }
            }
        ),
        Tool(
            name="update_user",
            description="根据ID更新用户信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "要更新的用户ID"},
                    "name": {"type": "string", "description": "新姓名 (可选)"},
                    "email": {"type": "string", "description": "新邮箱 (可选)"},
                    "age": {"type": "integer", "description": "新年龄 (可选)"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="delete_user",
            description="根据ID删除用户",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "要删除的用户ID"}
                },
                "required": ["user_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        result = {}
        
        if name == "create_user":
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (arguments["name"], arguments["email"], arguments.get("age"))
            )
            conn.commit()
            result = {"status": "success", "message": "用户创建成功", "id": cursor.lastrowid}

        elif name == "read_users":
            query = "SELECT id, name, email, age FROM users"
            params = []
            
            if "user_id" in arguments:
                query += " WHERE id = ?"
                params.append(arguments["user_id"])
            elif "name_filter" in arguments:
                query += " WHERE name LIKE ?"
                params.append(f"%{arguments['name_filter']}%")
                
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # 将元组转换为字典列表以便 LLM 理解
            columns = ["id", "name", "email", "age"]
            result = {"status": "success", "data": [dict(zip(columns, row)) for row in rows]}

        elif name == "update_user":
            user_id = arguments["user_id"]
            updates = []
            params = []
            
            if "name" in arguments:
                updates.append("name = ?")
                params.append(arguments["name"])
            if "email" in arguments:
                updates.append("email = ?")
                params.append(arguments["email"])
            if "age" in arguments:
                updates.append("age = ?")
                params.append(arguments["age"])
            
            if not updates:
                return [TextContent(type="text", text="未提供要更新的字段")]

            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            result = {"status": "success", "message": f"更新了 {cursor.rowcount} 行"}

        elif name == "delete_user":
            cursor.execute("DELETE FROM users WHERE id = ?", (arguments["user_id"],))
            conn.commit()
            result = {"status": "success", "message": f"删除了 {cursor.rowcount} 行"}
            
        else:
            result = {"status": "error", "message": f"未知工具: {name}"}

        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}, indent=2, ensure_ascii=False))]
    finally:
        conn.close()

# --- 启动服务器 ---
async def main():
    init_db() # 确保数据库表存在
    # 使用 stdio 传输模式，这是 MCP 的标准模式
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())