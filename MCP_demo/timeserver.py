from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Time")

@mcp.tool()
def getcurrdatetime():
    now = datetime.now()
    format_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return str(format_time)

if __name__ == "__main__":
    mcp.run(transport="stdio")