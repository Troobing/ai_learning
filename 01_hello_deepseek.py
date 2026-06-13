# ！！！LLM的api调用 ！！！

# 这个程序做三件事：
#   ① 加载你电脑上的 .env 文件（里面有 API 密钥）
#   ② 用密钥连接 DeepSeek 服务器
#   ③ 发送message部分，然后打印 AI 的回复

# ---------- 第 1 步：导入工具包 ----------

# openai 是一个"外包公司"。
# 虽然叫 openai，但它不光能调 OpenAI 的模型，
# 因为 DeepSeek 的接口长得跟 OpenAI 一模一样，
# 所以我们可以用同一个工具包来调 DeepSeek。
# 安装方式：pip install openai
from openai import OpenAI

# sys 是 Python 自带的"系统管家"。
# 负责程序跟操作系统之间的交互，比如控制台输出、命令行参数等。
# 不需要安装，Python 自带。
import sys

# os 是 Python 自带的"操作系统翻译官"。
# 它可以读系统环境变量，比如你的 API 密钥藏在哪。
# 不需要安装，Python 自带。
import os

# do-to-env
# dotenv 是一个"读密码本的工具"。
# 你项目里有个 .env 文件，里面写了 DEEPSEEK_API_KEY=xxx
# dotenv 能把这个文件的内容读到程序里。
# 安装方式：pip install python-dotenv
from dotenv import load_dotenv


# ---------- 第 2 步：加载 .env 文件里的密钥 ----------

# 不写文件名时，默认找.env文件
# 这一行执行后，.env 文件里的所有 KEY=VALUE 都会被读入"环境变量"。
# 之后用 os.getenv("名字") 就能取到对应的值。
load_dotenv()

# Windows 系统的终端默认用 GBK 编码（中文老标准），
# 它不认识 emoji（😊🎉）和生僻字，遇到就会崩溃。
# 这行把输出编码改成 utf-8（全球通用编码，啥字都认）。
# 改完之后 AI 回复里的表情符号就不会报错了。
sys.stdout.reconfigure(encoding='utf-8')


# ---------- 第 3 步：创建 API 客户端（相当于向ai拨通电话） ----------

client = OpenAI(
    # api_key 就是你的"密码"，DeepSeek 靠它知道你是谁、该不该收钱。
    # os.getenv("DEEPSEEK_API_KEY") 的意思是：
    #   去环境变量里找一个叫 DEEPSEEK_API_KEY 的东西，把它的值取出来。
    #   这个值是你在 .env 文件里写的。
    api_key=os.getenv("DEEPSEEK_API_KEY"),

    # base_url 是 DeepSeek 服务器的"门牌号"。
    # 所有请求都发到这个地址。
    base_url="https://api.deepseek.com"
)


# ---------- 第 4 步：发送消息，获取回复 ----------

response = client.chat.completions.create(
    # model：选哪个 AI 模型来回答。
    # "deepseek-chat" 是 DeepSeek 的通用聊天模型（非推理模式）。
    # 如果想用深度思考模式，改成 "deepseek-reasoner"。
    model="deepseek-v4-flash",

    # max_tokens：限制 AI 最多回复多少个"token"。
    # token 不是字数——英文大约 1 个单词 = 1~2 个 token，
    # 中文大约 1 个字 = 1~2 个 token。
    # 设为 256 表示"最多回大约 100~200 个中文字"。
    # 设太小 AI 话没说完就断了；设太大可能浪费钱。
    max_tokens=256,

    # messages：你跟 AI 的对话内容。
    # 这是一个"列表"，因为对话可能有很多轮。
    # 每一轮是一个"字典" {}，包含两个字段：
    #   role    — 谁说的话。有三种角色：
    #              "system"  = 给 AI 设定人设（比如"你是一个老师"）
    #              "user"    = 你 （用户）
    #              "assistant" = AI（助手）
    #   content — 说话的具体内容。
    messages=[
        {"role": "system", "content": "每句话结束都加喵~"},
        {"role": "user", "content": "生成5个随机数"} 
    ],
   
    #关掉思考
    extra_body={"thinking":{"type":"disabled"}}
)


# ---------- 第 5 步：打印 AI 的回复 ----------

# response 是服务器返回的完整结果，结构像这样（简化版）：
#   response
#     └── choices           ← 一个列表，通常只有一项
#           └── [0]          ← ai返回好多个值，取第一项
#                └── message
#                     └── content   ← AI 回复的文字
#
# 所以 response.choices[0].message.content
# 翻译成人话就是："返回结果 → 第一个选项 → 消息 → 正文"
print(response.choices[0].message.content)


