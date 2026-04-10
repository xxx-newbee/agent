import re 
from agent import Agent
import system_prompt
import tool

BASE_URL = "http://localhost:11434/v1"
MODEL = "qwen/qwen3.5-9b"

llm = Agent(model=MODEL, base_url=BASE_URL)
user_prompt = input()
# user_prompt = "用python帮我写一个可执行的贪吃蛇游戏，文件名称为snake.py"
prompt_history = [f"用户请求：{user_prompt}"]
print(f"用户输入：{user_prompt}\n " + "="*40)
while True:
    full_prompt = "\n".join(prompt_history)
    llm_output = llm.generate(full_prompt, system_prompt=system_prompt.AGENT_SYSTEM_PROMPT)
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
        print(llm_output)
        prompt_history.append(llm_output)
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            print("解析错误：模型输出中未找到 Action")
            break
        action_str = action_match.group(1).strip()
        if action_str.startswith("finish"):
            final_answer = re.search(r'finish\(answer="(.*)"\)', action_str).group(1)
            print(f"任务完成：{final_answer}")
            break

        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
        if tool_name in tool.available_tools:
            observation = tool.available_tools[tool_name](**kwargs)
        else:
            observation = f"错误：未定义的工具 '{tool_name}'"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)