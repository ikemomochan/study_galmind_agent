//ギャルのランダムなセリフ集
const galPhrases = [
  "どう、学習進んでる？👀",
  "え、てか全然関係ないけど最近どぉ？",
  "てかさ、最近なんか嬉しいことあった？",
  "てかなんか話したいことあったら聞くかんね〜〜💖",
  "なんかあたしに聞きたいことあったらなんでも言ってな✌"
];

//最後のユーザー操作時間（初期化）
let lastInteractionTime = new Date();

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("upload-form");
  const questionForm = document.getElementById("question-form");
  const chatLog = document.getElementById("chat-log");
  const questionInput = document.getElementById("user-question");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("pdf");
    const file = fileInput.files[0];
    if (!file) return;

    appendBubble("user", `PDF「${file.name}」をアップロードしたよ！`);
    showStudyingGal();

    const loadingBubble = appendBubble("gal loading", "ギャルが頑張って勉強してるからちょっと待ってね〜📚✨");

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      chatLog.removeChild(loadingBubble);

      //ここ
      if (data.steps && Array.isArray(data.steps)) {
        for (const step of data.steps) {
          await delay(800);
          if (step.type === "quiz") {
            appendBubble("gal", `${step.question}（答えは「練習問題」のタブから確認してね！）`);
            appendQuiz(step.question, step.answer);
          } else {
            appendBubble(`gal ${step.type}`, step.text);
          }
        }
      }
      
  
      showNormalGal();
    } catch (err) {
      chatLog.removeChild(loadingBubble);
      appendBubble("gal", "うわ〜ネットワークエラーかも〜💦 もう一回試してみてねっ！");
      showNormalGal();
    }
  });

  questionForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    appendBubble("user", question);
    showThinkingGal();

    const loadingBubble = appendBubble("gal loading", "ちょっと待ってね〜考え中💭");

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      const data = await response.json();
      chatLog.removeChild(loadingBubble);
      appendBubble("gal", data.answer || "ごめん〜うまく答えられなかったかも🥺");
      showNormalGal();
    } catch (err) {
      chatLog.removeChild(loadingBubble);
      appendBubble("gal", "ネットワークエラーっぽい！もう一回試してみてね💦");
      showNormalGal();
    }

    questionInput.value = "";
    lastInteractionTime = new Date(); // 質問後はリセット
  });

  //操作があればリセット
  ["click", "keydown"].forEach(event => {
    document.addEventListener(event, () => {
      lastInteractionTime = new Date();
    });
  });

  //ギャルから自動で話しかける処理
  setInterval(() => {
    const now = new Date();
    const diffMinutes = (now - lastInteractionTime) / 1000 / 60;
    if (diffMinutes >= 2) {
      const random = Math.floor(Math.random() * galPhrases.length);
      appendBubble("gal", galPhrases[random]);
      lastInteractionTime = new Date(); // 話したらリセット
    }
  }, 60000); // 毎分チェック

  //吹き出し追加＆ギャル画像制御関数
  function showStudyingGal() {
    const galImage = document.getElementById("gal-image");
    galImage.src = "/static/gal_studying.png";
  }

  function showThinkingGal() {
    const galImage = document.getElementById("gal-image");
    galImage.src = "/static/gal_thinking.png";
  }

  function showNormalGal() {
    const galImage = document.getElementById("gal-image");
    galImage.src = "/static/gal_greeting.png";
  }

  function appendBubble(classes, text) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${classes}`;
    bubble.innerHTML = text.replace(/\n/g, "<br>");
    chatLog.appendChild(bubble);
    chatLog.scrollTop = chatLog.scrollHeight;
    return bubble;
  }

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
});

// タブ切り替え処理
document.querySelectorAll(".tab-button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-button").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((tab) => tab.classList.remove("active"));

    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

// 練習問題の表示関数（サーバー応答後に呼び出す想定）
function appendQuiz(question, answer) {
  const quizBox = document.createElement("div");
  quizBox.className = "question-box";
  quizBox.innerHTML = `
    <p class="question-text">Q: ${question}</p>
    <button class="show-answer-btn">答えを見る</button>
    <p class="answer-text">A: ${answer}</p>
  `;
  document.getElementById("quiz-list").appendChild(quizBox);

  quizBox.querySelector(".show-answer-btn").addEventListener("click", () => {
    const ans = quizBox.querySelector(".answer-text");
    ans.style.display = ans.style.display === "none" ? "block" : "none";
  });
}
