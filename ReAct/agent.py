import re
from openai import OpenAI

class Agent:
    def __init__(self, model: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key="ollama", base_url=base_url)
    
    def generate(self, user_prompt: str, system_prompt: str) -> str:
        try:
            message = [{"role": "system", "content": system_prompt},
                       {"role": "user", "content": user_prompt}]
            responnse = self.client.chat.completions.create(model=self.model, messages=message)
            return responnse.choices[0].message.content
        except Exception as e: 
            return "llm calling error."
    