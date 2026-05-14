from google import genai
import os

# 确保你在终端已经执行过 export GEMINI_API_KEY="xxx"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- 正在查询当前 API Key 可用的文本生成模型 ---")

try:
    for model in client.models.list():
        # 筛选出支持 generateContent (文本生成) 的模型
        if "generateContent" in model.supported_generation_methods:
             print(f"✅ 可用模型: {model.name}")
except Exception as e:
    print(f"查询失败，请检查 API Key 是否正确: {e}")