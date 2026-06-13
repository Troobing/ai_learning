# ！！！LLM的api调用-改-交互式聊天！！！

# ai不能记住上一轮说了什么，每次调用都要把完整的历史对话传回去，所以messages是一个列表


# 加入history储存历史对话，用循环可以进行重复对话

#  - 交互式聊天
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

# Windows 终端 UTF-8 支持
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 记录对话历史
history = []

print("🤖 DeepSeek 交互式聊天 (输入 quit 退出, clear 清空历史)\n")

while True:
    # 获取用户输入
    user_input = input("你: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "quit":
        print("👋 再见！")
        break

    if user_input.lower() == "clear":
        history = []
        print("🧹 对话历史已清空\n")
        continue

    # 把用户消息加入历史
    history.append({"role": "user", "content": user_input})

    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        max_tokens=1024,
        messages=history,
        extra_body={"thinking":{"type":"disabled"}}
    )

    reply = response.choices[0].message.content

    # 把 AI 回复也加入历史
    history.append({"role": "assistant", "content": reply})

    print(f"\nAI: {reply}\n")
