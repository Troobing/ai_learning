# ！！！RAG + Embedding ！！！

from openai import OpenAI
import os
import json
import math
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)



# 一:Embedding--把文本变向量
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding模型加载完成")
# 取向量维度:随便编码一个词,看向量长度（通用,不依赖版本）
dimension = len(embedding_model.encode("hello"))
print(f"向量维度:{dimension}")

# 演示:两句话的相似度
text1 = "苹果是一种很好吃的水果"
text2 = "这个水果味道很甜"
text3 = "今天天气真不错"

emb1 = embedding_model.encode(text1)
emb2 = embedding_model.encode(text2)
emb3 = embedding_model.encode(text3)

# 余弦相似度
def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(x*x for x in b))
    return dot / (norm_a * norm_b)

print("语义相似度测试")
print(f"  '{text1}' vs '{text2}': 相似度:{cosine_similarity(emb1, emb2):.4f} ")
print(f"  '{text1}' vs '{text3}': 相似度:{cosine_similarity(emb1, emb3):.4f} ")




# 二:向量数据库（chromaDB）
import chromadb

# 创建ChromaDB客户端（数据存在本地文件
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 创建或获取集合
try:
    chroma_client.delete_collection("my_docs")
except:
    pass
collection = chroma_client.create_collection(
    name="my_docs",
    metadata={"hnsw:space": "cosine"}  # 用余弦相似度
)



# 三:加载文档 & 存入向量数据库
# 实例文档
DOCUMENTS = [
    {
        "title": "智能客服系统使用指南",
        "content": """
智能客服系统是一个基于AI的自动化客户服务解决方案。
支持Docker和Kubernetes两种部署方式。
系统提供RESTful API:POST /api/chat 发送消息,GET /api/history 获取历史。
支持中文、英文、日文三种语言。
平均响应时间小于500ms,并发支持1000QPS。
当遇到无法回答的问题时,系统自动转接人工客服。
        """
    },
    {
        "title": "员工手册2025版",
        "content": """
公司实行弹性工作制,核心工作时间为上午10点到下午4点。
年假:入职第一年5天,每满一年增加1天,上限15天。
病假需提供医院证明,紧急情况可事后补交。
报销流程:提交发票→直属领导审批→财务审核→打款,周期通常为5个工作日。
办公室位于科技园B栋12层,提供免费咖啡和零食。
        """
    },
    {
        "title": "项目开发规范",
        "content": """
所有代码必须通过Code Review才能合并到主分支。
使用Git进行版本管理,遵循Git Flow分支策略。
Python代码遵循PEP 8规范,使用Black进行格式化。
单元测试覆盖率要求不低于80%。
API文档使用OpenAPI 3.0规范,自动生成。
        """
    },
]

# 将文档切块并存入ChromaDB
for doc in DOCUMENTS:
    # 简单切块（每300字符一块）
    content = doc["content"]
    for i in range(0, len(content), 300):
        chunk = content[i:i+300]
        if len(chunk.strip()) < 20:
            continue
        
        # 生成embedding
        embedding = embedding_model.encode(chunk).tolist()
        
        # 存入ChromaDB
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"title": doc["title"], "chunk_index": i//300}],
            ids=[f"{doc['title']}_chunk_{i//300}"]
        )

print(f"向量数据库中共有 {collection.count()} 个文档片段")



# 第四步：检索 + 生成（完整RAG）
def rag_search(query: str, top_k: int = 3) -> str:
    """完整的RAG流程"""
    
    # 1. 把用户问题也变成向量
    query_embedding = embedding_model.encode(query).tolist()
    
    # 2. 在向量数据库中搜索最相似的片段
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # 3. 提取检索到的内容
    contexts = []
    print(f"检索结果：")
    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"  {i+1}. [{metadata['title']}] 相似度: {1-distance:.3f}")
        print(f"     {doc[:100]}...")
        contexts.append(doc)
    
    # 4. 增强Prompt
    context_text = "\n\n---\n\n".join(contexts)
    
    augmented_prompt = f"""你是一个基于内部文档的问答助手。请严格根据以下参考文档回答问题。
如果文档中找不到相关信息，明确说"根据现有文档无法回答"，不要编造。

【参考文档】
{context_text}

【用户问题】
{query}

【回答要求】
- 引用具体的文档来源
- 如果涉及具体数据或流程，精确引用
"""

    # 5. 生成回答
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        max_tokens=500,
        messages=[{"role": "user", "content": augmented_prompt}]
    )
    return response.choices[0].message.content



# 测试
if __name__ == "__main__":
    questions = [
        "公司的年假政策是怎样的？",
        "代码审查有什么要求？",
        "客服系统支持并发多少？",
        "公司地址在哪里？",
        "Python版本要求是多少?",  # 文档里没有
    ]
    
    for q in questions:
        print(f"\n{'='*60}")
        print(f"👤 {q}")
        print(f"{'='*60}")
        answer = rag_search(q)
        print(f"\n🤖 {answer}")
























