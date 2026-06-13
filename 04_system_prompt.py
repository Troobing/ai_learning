# !!!让ai扮演不同角色 + 交互式对话练习！！！

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

history = []

persons = [
    "你是一个毒舌的老师，说话尖酸刻薄但是一阵见血"
]

print("请输入请求,输入quit退出")

while True:

    prompt = input("你：").strip()
    
    if not prompt:
        continue
    if prompt.lower() == "quit":
        print("bye")
        break

    history.append({"role":"user", "content":prompt})

    respond = client.chat.completions.create(
        model = "deepseek-v4-falsh",
        max_tokens = 1024,
        # 这里+号前后类型不同会出错误
        messages = [{"role":"system","content":persons[0]}] + history,
        extra_body={"thinking":{"type":"disabled"}}         
    )

    reply = respond.choices[0].message.content

    history.append({"role":"assistant", "content": reply})

    print(reply)
