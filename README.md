# StudyGal Agent 

Flask + OpenAI APIを活用した、PDF文書の内容をギャルマインドで要約・キーワード抽出・質問生成する学習支援エージェントです。

---

## 概要

- ✅ PDFアップロード機能（ブラウザUIから選択）
- ✅ LLMを活用した3つの自動処理：
  - 要約（Summary）
  - キーワード抽出（Keyword Extraction）
  - 理解度チェック用の質問生成（Question Generation）
- ✅ FAISSベースのベクトル検索で質問応答も可能
- ✅ ギャル風UIで楽しく学べる（学習者への親しみやすさを考慮）

---

## 技術スタック

| 技術 | 内容 |
|------|------|
| Python | アプリケーション本体の実装 |
| Flask | Webサーバー（APIエンドポイント） |
| OpenAI API | GPT-4o-miniを利用した自然言語処理 |
| LangChain | ツール管理・Agent構築 |
| FAISS | ベクトルデータによる類似検索 |
| HTML/CSS/JS | フロントエンド（チャットUI） |
| PyMuPDF | PDFのテキスト抽出 |

---

## 使用方法

1. `.env` ファイルをルートに作成し、以下のようにAPIキーを設定：
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
※ご自身のものを入力してください

2. 必要なライブラリをインストール：
pip install -r requirements.txt

3. Flaskアプリ起動：
python app.py

4. ブラウザで http://localhost:5000 を開く

---
