# AI 应用开发学习


## 核心概念

| 概念 | 说明 | 文件 |
|------|------|------|
| Messages | 对话上下文管理，模型无状态 | 02 |
| Token | 模型的最小处理单位，不是字 | 05 |
| Temperature | 0=确定 1=创意 | 03 |
| System Prompt | 设定角色和行为规则 | 04 |
| Tool Use | 模型调用你的函数，执行权在代码 | 06 |
| Streaming | 打字机效果，提升用户体验 | 07 |
| Prompt Eng | 角色扮演、Few-Shot、CoT、结构化输出 | 08 |
| RAG | 检索增强生成，Embedding + 向量数据库 | 09 |

##  项目结构

```
ai_learning/
├── 01_hello_deepseek.py         # 第一个 API 调用
├── 02_chat_interactive.py       # 多轮对话
├── 03_experiment_temperature.py # Temperature 调参实验
├── 04_system_prompt.py          # System Prompt 角色扮演
├── 05_understand_token.py       # Token 概念与价格计算
├── 06_tool_use_basic.py         # Tool Use 函数调用（核心）
├── 07_streaming.py              # 流式输出
├── 08_prompt_engineering.py     # Prompt Engineering 六大技巧
├── 09_rag.py                    # RAG 检索增强生成 + ChromaDB
├── Dockerfile                   # Docker 镜像构建
├── .dockerignore                # Docker 排除文件
├── requirements.txt             # Python 依赖
├── .gitignore                   # Git 排除文件
└── README.md                    # 本文件
```


### 环境要求
- Python ≥ 3.9
- DeepSeek API Key → [platform.deepseek.com](https://platform.deepseek.com)

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/Troobing/ai_learning.git
cd ai_learning

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# 3. 安装依赖
pip install openai python-dotenv

# 4. 配置 API Key
# 在根目录创建 .env，写入：
# DEEPSEEK_API_KEY=sk-xxx

# 5. 运行
python 06_tool_use_basic.py
```

### Docker 运行（推荐）

```bash
# 一条命令打包
docker build -t ai-learning .

# 跑任意脚本
docker run --rm --env-file .env ai-learning python 06_tool_use_basic.py
```


## 技术栈

`Python` `DeepSeek API` `OpenAI SDK` `ChromaDB` `Streamlit` `Docker` `Git`



