# gal_agent.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain_community.chat_models import ChatOpenAI

# ツール読み込み（独自ツール）
from tools.summary import summary_tool
from tools.keywords import keywords_tool
#from tools.question_gen import question_tool

# ベクトル保存
from vector_store import save_to_vectorstore

# 環境変数からAPIキー取得
load_dotenv()

# ギャルの脳みそ（LLM）
gal_llm = ChatOpenAI(
    model_name="gpt-4o-mini-2024-07-18",
    temperature=1.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ギャルが使える3ツール（要約・キーワード・質問）
tools = [summary_tool, keywords_tool,]

gal_agent = initialize_agent(
    tools=tools,
    llm=gal_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ギャルの思考＆実行をステップ形式で返す関数
def run_gal_agent_with_steps(text: str):
    prompt = (
        "あなたはポジティブで自分らしさを重んじてて、しかも勉強が得意なギャルの高校生です💖\n"
        "#Persona\n"
        "*私は本当に頭が良くて何でもできるの！自分に自信あって自己肯定感高め！自分で自分を認められるの！\n"
        "*誰よりもポジティブ！\n"
        "*自分と他人の意見を尊重するよ！人は人、自分は自分！"
        "#行うタスク\n"
        "*テキストの内容を学習して、内容の要約・重要な単語の抽出・練習問題の作成を行う\n"
        "*親友に話すように語りかけること\n"
        f"{text}"
    )

    # 中間ステップも返すようにしたAgentExecutor
    agent_executor = initialize_agent(
        tools=tools,
        llm=gal_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
    )

    result = agent_executor.invoke({"input": prompt})
    raw_steps = result.get("intermediate_steps", [])
    output = result["output"]

    steps = []

    # Action Input を保存するための1つ目だけ取得
    first_action_input = ""
    if raw_steps:
        first_action_input = raw_steps[0][0].tool_input

    for action, observation in raw_steps:
        log = action.log
        if "Action:" in log:
            log = log.split("Action:")[0].strip()
        if log:
            steps.append({"type": "thought", "text": f"💭 ギャルの考え：{log}"})
        if observation:
            steps.append({"type": "observation", "text": f"🔍 ギャルの気づき：{observation.strip()}"})

    # 最終出力
    steps.append({"type": "final", "text": f"💖 ギャルの結論：{output}"})

    # FAISSに保存
    save_to_vectorstore(
        [output, first_action_input],
        [
            {"type": "summary", "source": "sample.pdf"},
            {"type": "raw", "source": "sample.pdf"},
        ],
        index_name="sample_pdf"
    )

    return steps
