from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

# 1. 配置本地 Qwen3.5 模型 (通过 Ollama 提供服务)
llm_cfg = {
    'model': 'qwen/qwen3.5-9b',  # 确保这里的模型名称与你用 ollama pull 下载的一致
    'model_server': 'http://localhost:11434/v1',  # Ollama 的 API 地址
    'api_key': 'EMPTY',  # Ollama 本地服务不需要 API Key 
}

# 2. 定义你的工具，这里配置你之前创建的 MCP 服务
# 假设你的 server.py 文件位于 /path/to/your/server.py
tools = [
    {
        'mcpServers': {
            'Math': {  # 给你的服务起个名字
                'command': 'python3',  # 启动服务的命令
                'args': ['./mathserver.py']  # 你的 MCP 服务脚本的绝对路径
            },
            'Time': {
                'command': 'python3',
                'args': ['./timeserver.py']
            },
            'DB': {
                'command': 'python3',
                'args': ['./storeserver.py']
            }
        }
    }
]

# 3. 初始化 Qwen-Agent 助手
bot = Assistant(llm=llm_cfg, function_list=tools)

# 4. 发送消息并获取回复
messages = [{'role': 'user', 'content': '获取所有用户数据'}]

# 运行助手并打印结果
response_plain_text = ""
for responses in bot.run(messages=messages):
    response_plain_text = typewriter_print(responses, response_plain_text)
    pass

print("\n")
# 打印最终回复
# print(responses[-1]['content'])