# tools/summary.py

from langchain.agents import Tool
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 要約処理
def gal_summary_tool(text: str) -> str:
    prompt = f"""
    あなたはポジティブで自分らしさを重んじてて、しかも勉強が得意なギャルの先生です💖
    以下の内容を、難しい言葉を使わずに、なるべく抽象的な言葉を使ってわかりやすく300文字以内で要約して！
    難しい概念がある時は、身の回りの誰もが知ってるギャルっぽいものに例えて教えてね！
    ギャルっぽいテンションで、最後に「何が大事か」必ず教えてね✨
    出力する文は必ず、「まずは要約していっちゃうぞー🌟」で始めてね！

    -----
    {text[:1500]}
    -----
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === LangChainのTool定義 ===
summary_tool = Tool(
    name="ギャルい要約ツール",
    func=gal_summary_tool,
    description="PDFの内容を明るくわかりやすく要約するギャルのツールだよ。要約は1回で十分！"
)
