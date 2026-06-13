# ！！！用api调用来观察token消耗！！！

# 语言被切成块，每一个块就是一个token，是模型处理的最小单位

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    max_tokens=10000,
    messages=[
        {"role":"user","content":"用一句话介绍python"},
        {"role":"user","content":"deepseek的token收费标准是?"}
        ],
)

print(f"输入token:{response.usage.prompt_tokens}")
print(f"输出token:{response.usage.completion_tokens}")
print(f"总token:{response.usage.total_tokens}")
print(f"回复内容:{response.choices[0].message.content}")

# 返回模型思考过程
print(response.choices[0].message.reasoning_content)

