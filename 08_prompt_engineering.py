# !!! Prompt_engineering !!!

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def compare(prompt_bad, prompt_good, title):
    # 对比差prompt和好prompt输出
    print(title)
    for label, prompt in [("差的Prompt", prompt_bad), ("好的Prompt", prompt_good)]:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            max_tokens=30000,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"thinking":{"type":"disabled"}}
        )
        print(f"\n{label}:")
        print(f"  输入: {prompt[:80]}...")
        print(f"  输出: {response.choices[0].message.content[:200]}...")

# 一：给模型一个“角色”
compare(
    prompt_bad="写一个Python代码审查",
    prompt_good="你是一个有10年经验的Python后端工程师。审查以下代码, 从性能、安全、可读性三个维度给出建议, 每个维度至少2条。",
    title="一：角色扮演"
)



# 二：Few-shot(给示例)
few_shot_prompt = """将以下用户查询转换为SQL：

示例1:
用户: 查所有技术部员工
SQL: SELECT * FROM users WHERE dept = '技术部'

示例2:
用户: 张三的邮箱是什么
SQL: SELECT email FROM users WHERE name = '张三'

示例3:
用户: 各部门有多少人
SQL: SELECT dept, COUNT(*) FROM users GROUP BY dept

现在请转换:
用户: 技术部工资大于10000的员工姓名和邮箱
SQL:"""

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    max_tokens=200,
    messages=[{"role": "user", "content": few_shot_prompt}]
)
print("二: Few-shot(给示例)")
print(response.choices[0].message.content)


# 三：chain of thought (让模型"思考过程")
compare(
    prompt_bad="这个Python函数有bug吗? def divide(a,b): return a/b",
    prompt_good="""分析以下Python函数的潜在问题。请按以下步骤思考:
1. 先列出函数的所有假设
2. 逐一检查每个假设在什么情况下会失败
3. 给出修复建议
函数: def divide(a, b): return a / b""",
    title="三: Chain of Thought (思维链)"
)


# 四：结构化输出
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": """分析以下代码的复杂度, 用JSON格式返回:
{
    "time_complexity": "O(?)",
    "space_complexity": "O(?)",
    "explanation": "简短解释"
}

代码：
for i in range(n):
    for j in range(n):
        print(i * j)
"""
    }]
)
print(f"四: 结构化输出 (指定JSON格式)")
print(response.choices[0].message.content)


# 五：设定约束条件
compare(
    prompt_bad="解释什么是REST API",
    prompt_good="""用以下格式解释REST API:
- 用一句话概括核心思想 (不超过20字)
- 用3个要点说明关键原则
- 给一个简单的Python Flask示例 (不超过10行)
- 整体回答不超过150字""",
    title="五: 设定约束条件"
)



# 六: Multi-Step(任务拆分)
print(f"六: 任务拆分(Multi-Step)")
print("""
错误做法 ❌: "帮我设计一个完整的用户认证系统"
正确做法 ✅:
  第1步: "列出用户认证系统的核心功能点"
  第2步: "基于上面的列表，设计数据库表结构"
  第3步: "基于表结构, 写FastAPI的API端点"
  第4步: "添加JWT token的生成和验证逻辑"
  
每一步都可以检查和调整，比一次性生成靠谱得多。
""")