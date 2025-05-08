from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ギャル風のQ&Aを生成（1プロンプトでまとめて）
def gal_question_tool(text: str) -> str:
    prompt = f"""
    あなたはポジティブで自分らしさを大切にする、明るくて面倒見のいいギャル先生です💖
    以下の文章を読んで、読解確認用の質問とその答えを3つ作ってください📚✨

    出力形式は以下のようにしてください：

    Q1: ○○○？
    A1: △△△

    Q2: ...
    A2: ...

    Q3: ...
    A3: ...

    ※テンションはギャルっぽくてもOKだけど、フォーマットは必ず守ってね💅
    -----
    {text[:1500]}
    -----
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Q&Aを分割してリストにする
def parse_qa(text: str):
    questions = []
    lines = text.split("\n")
    q, a = "", ""
    for line in lines:
        line = line.strip()
        if line.startswith("Q"):
            q = line.split(":", 1)[1].strip()
        elif line.startswith("A"):
            a = line.split(":", 1)[1].strip()
            if q and a:
                questions.append({"question": q, "answer": a})
                q, a = "", ""
    return questions
