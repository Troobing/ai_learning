# 基础镜像：Python 3.11 精简版
FROM python:3.11-slim

# 设工作目录（所有代码放在这里）
WORKDIR /app

# 先只拷依赖文件（这样改代码不用重装依赖）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 拷代码
COPY *.py .

# 默认跑 01 文件（可以 docker run 时覆盖）
CMD ["python", "01_hello_deepseek.py"]
