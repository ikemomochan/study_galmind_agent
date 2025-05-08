# tools/keywords.py

from langchain.agents import Tool
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#キーワード抽出処理
def gal_keywords_tool(text: str) -> str:
    prompt = f"""
    あなたはポジティブで自分らしさを重んじてて、しかも勉強が得意なギャルの先生です💖
    以下の文章から重要なキーワードやトピックを10個以内で抜き出して！
    ちゃんと有用な単語を選んでね✨
    出力するときは必ず「次の単語たちが重要そうだね！」で始めて、そのあと単語を箇条書きで出してね！

    -----
    {text[:1500]}
    -----
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# LangChainのTool定義
keywords_tool = Tool(
    name="ギャルキーワード抽出ツール",
    func=gal_keywords_tool,
    description="PDFの内容から大事なキーワードをピックアップしてくれるギャルのツール💖抽出は1回で十分！"
)
