from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
client=AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=60,
)
async def chat(prompt:str) -> str:
    try: 
        response=await client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.2", 
        messages=[{"role": "user",
                 "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
        top_p=0.9,
     )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI 调用失败: {str(e)}"
if __name__ == "__main__":
    import asyncio
    print(asyncio.run(chat("你好"))  )      
