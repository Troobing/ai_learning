# !!!流式输出！！！

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

stream = client.chat.completions.create(
    model="deepseek-v4-flash",
    max_tokens=5000,
    messages=[{"role": "user", "content": "写出滕王阁序全篇"}],
    stream=True,
    stream_options={"include_usage":True}
)

usage = None
for chunk in stream:
    if chunk.choices[0].delta.content:
        text = chunk.choices[0].delta.content
        print(text, end = "", flush = True)
    # 确定chunk有非None的usage属性
    if hasattr(chunk, "usage") and chunk.usage:
        usage = chunk.usage

print()
if usage:
    print(f"Token用量: 输入：{usage.prompt_tokens}, 输出：{usage.completion_tokens}, 总计：{usage.total_tokens}")
else:
    print("未获取到token用量")