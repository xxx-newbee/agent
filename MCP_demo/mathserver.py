import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# 初始化服务器
app = Server("calculator")

# --- 定义资源 ---
# 资源通常用于提供静态或动态的数据上下文
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="greeting://hello",
            name="欢迎语",
            description="一个简单的问候资源",
            mimeType="text/plain",
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "greeting://hello":
        return "你好！这是一个简单的计算器 MCP 服务示例。"
    raise ValueError(f"未知资源: {uri}")

# --- 定义工具 ---
# 工具允许模型执行操作或计算
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add",
            description="将两个数字相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="将两个数字相减",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="将两个数字相乘",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="将两个数字相除",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个非零数字"},
                },
                "required": ["a", "b"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "add":
        a = arguments.get("a")
        b = arguments.get("b")
        result = a + b
        return [TextContent(type="text", text=f"结果是: {result}")]
    elif name == "subtract":
        a = arguments.get("a")
        b = arguments.get("b")
        result = a - b
        return [TextContent(type="text", text=f"结果是: {result}")]
    elif name == "multiply":
        a = arguments.get("a")
        b = arguments.get("b")
        result = a * b
        return [TextContent(type="text", text=f"结果是: {result}")]
    elif name == "divide":
        a = arguments.get("a")
        b = arguments.get("b")
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        return [TextContent(type="text", text=f"结果是: {result}")]
    raise ValueError(f"未知工具: {name}")

# --- 启动服务 ---
async def main():
    # 使用 stdio_server 通过标准输入输出进行通信
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())