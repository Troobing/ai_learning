# ！！！函数调用！！！

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 一：定义函数
def get_weather(city: str) -> str:
    # 实际项目这里调用天气api。这里用模拟数据
    weather_data = {
        "北京": "晴, 25°C, 湿度40%",
        "上海": "多云, 28°C, 湿度65%",
        "深圳": "雷阵雨, 30°C, 湿度80%",
    }
    return weather_data.get(city, f"未找到{city}的天气数据")

def calculate(expression: str) -> str:
    # 安全的数学计算
    try:
        # 限制：只允许数字和基本运算符
        allowed = set("0123456789+-*/().%")
        if not all(c in allowed for c in expression):
            return "错误: 表达式中包含不允许的字符"
        # eval--把字符串当成python代码来执行，所以前面有白名单过滤
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"
    

# 二：定义工具描述，告诉模型有什么函数
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description":"查询指定城市的实时天气, 当用户询问天气相关问题时使用此工具",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"城市名称, 如'北京','上海'"
                    }
                },
                "required":["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算。当用户需要进行数学运算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如'2+3*4'、'(15+25)/2'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# 三：完整的Tool Use处理循环
def process_with_tools(user_message: str) -> str:

    messages = [{"role": "user", "content": user_message}]

    TOOL_MAP = {
        "get_weather": get_weather,
        "calculate": calculate,
    }

    # 核心循环，模型可能多轮调用工具
    while True:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            max_tokens=10000,
            messages=messages,
            tools=TOOLS         #工具传给模型
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            # 把模型回复包括tools_calls请求加入消息历史
            messages.append(msg)

            for tc in msg.tool_calls:
                tool_name = tc.function.name
                # 参数是json字符串，需要解析
                tool_input = json.loads(tc.function.arguments)

                # 真正执行函数
                result = TOOL_MAP[tool_name](**tool_input)

                # 工具结果用role = “tool”返回，需要 tool_call_id
                messages.append({
                    "role":"tool",
                    "tool_call_id":tc.id,
                    "content":result
                })
            continue        #继续循环，让模型基于结果再次决策

        else:
            # 模型不需要再调用工具，直接返回文本回复
            return msg.content


# 四：测试
if __name__ == "__main__":
    test_questions = [
        "北京今天天气怎么样？",
        "帮我算一下 (15 + 25) * 3 - 100 / 4",
        "上海和深圳哪边的湿度更高？",  # 这会触发两次 get_weather 调用！
    ]

    for q in test_questions:
        print(f"用户：{q}")
        answer = process_with_tools(q)
        print(f"回答：{answer}")






