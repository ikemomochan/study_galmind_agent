# app.py（Flaskサーバー）
# app.py

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
from agents.gal_agent import run_gal_agent_with_steps

from tools.question_gen import gal_question_tool, parse_qa  

from vector_store import load_vectorstore
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from save_log import save_conversation_log

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# PDFをテキストに変換
def extract_text_from_pdf(file_storage):
    text = ""
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file_storage.filename))
    file_storage.save(filepath)
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

#ルート：UI表示
@app.route("/")
def index():
    return render_template("gal_index.html")

# PDFアップロード＆ギャル思考処理
@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify({"error": "PDFファイルが必要だよ〜😭"}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "ファイル名が空だよ〜😭"}), 400

    # テキスト抽出
    text = extract_text_from_pdf(file)

    # ギャルに思考してもらう✨
    steps = run_gal_agent_with_steps(text)

    # Q&Aギャル文を生成
    raw_qa_text = gal_question_tool(text)
    qa_pairs = parse_qa(raw_qa_text)

    # チャットにQだけ表示（ギャルからの出題風！）
    for idx, qa in enumerate(qa_pairs, 1):
        steps.append({
            "type": "quiz",
            "question": f"Q{idx}: {qa['question']}",
            "answer": qa["answer"]
        })

    return jsonify({"steps": steps})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "質問が空っぽだったよ〜💦"}), 400

    try:
        # FAISS検索
        vs = load_vectorstore("sample_pdf")
        results = vs.similarity_search(question, k=3)
        context = "\n---\n".join([doc.page_content for doc in results])

        # ギャルっぽいプロンプトで回答
        prompt = PromptTemplate.from_template(
            "あなたは明るくてポジティブで優しい、ノリのいいギャル先生です💖\n"
        "以下の知識は、参考にしてもいいし、しなくてもOK✌️\n"
        "質問には、できるだけギャルらしいテンションで楽しく、でも分かりやすく答えてね✨\n"
        "知識（あったら使ってね）：\n{context}\n\n質問：{question}\n\nギャルの返答："
        )
        final_prompt = prompt.format(context=context, question=question)

        qa_llm = ChatOpenAI(temperature=0.8, openai_api_key=os.getenv("OPENAI_API_KEY"))
        answer = qa_llm.invoke(final_prompt)
        
        save_conversation_log(question, answer.content)

        return jsonify({"answer": answer.content})
    except Exception as e:
        return jsonify({"answer": f"エラーが出ちゃった💦: {str(e)}"}), 500


# 実行
if __name__ == "__main__":
    app.run(debug=True)
