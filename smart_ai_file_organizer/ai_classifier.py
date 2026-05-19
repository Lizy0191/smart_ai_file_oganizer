import requests

OLLAMA_API = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"

def ask_ai(content):

    prompt = f"""
你是一个文件分类助手。

请根据文件内容，
只返回一个分类名称。

分类只能是：

- 财务
- 学习
- 编程
- 工作
- 求职
- 图片
- 视频
- 音乐
- 未分类

文件内容：

{content}

只返回分类名称，不要解释。
"""

    try:

        response = requests.post(
            OLLAMA_API,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        result = response.json()

        category = result["response"].strip()

        return category

    except Exception as e:

        print("AI错误:", e)

        return "未分类"