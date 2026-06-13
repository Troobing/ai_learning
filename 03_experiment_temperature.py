# ！！！测试不同temperature！！！

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

prompt = "用一句话描述夕阳"


for temp in [0, 0.5, 1, 2]:
    respond = client.chat.completions.create(
        model = "deepseek-v4-flash",
        max_tokens = 1024,
        temperature = temp,
        messages=[
            {"role":"user","content":prompt}
        ],
        extra_body={"thinking":{"type":"disabled"}}
    )

    print(f"temperature = {temp}")
    print(respond.choices[0].message.content)

# 可以观察到temperature = 2的时候已经在胡说八道了