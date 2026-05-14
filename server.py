import os
import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from pydantic_settings import BaseSettings

# 1. Settings Configuration (Pydantic-settings)
class Settings(BaseSettings):
    gemini_api_key: str
    model_id: str = "gemini-3.1-flash-lite"
    class ConfigDict:
        env_file = ".env"

settings = Settings()
client = genai.Client(api_key=settings.gemini_api_key)

app = FastAPI()

# 2. CORS Configuration (CRITICAL for Frontend/Backend communication)
# CORS 配置：前端 5173 访问后端 8000 必须开启
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Align with Vercel AI SDK Payload
# 对齐 Vercel AI SDK 的数据结构
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message] # useChat sends a list of messages

async def sse_ai_generator(messages: List[Message]):
    # Get the last message content as the prompt
    # 获取最后一条消息作为 AI 的输入
    last_user_message = messages[-1].content
    
    stream = await client.aio.models.generate_content_stream(
        model=settings.model_id,
        contents=last_user_message
    )

    async for chunk in stream:
        if chunk.text:
            yield chunk.text

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    # We return a plain text stream which useChat understands
    return StreamingResponse(
        sse_ai_generator(req.messages),
        media_type="text/plain" 
    )

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)