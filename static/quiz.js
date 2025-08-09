let current = 0;
let score = 0;
let questions = [];

async function loadQuestions() {
  const res = await fetch("/get_questions");
  questions = await res.json();
  showQuestion();
}

function showQuestion() {
  const q = questions[current];
  const container = document.getElementById("quiz-container");
  container.innerHTML = `<h2>${q.question}</h2>`;
  q.choices.forEach(choice => {
    const btn = document.createElement("button");
    btn.textContent = choice;
    btn.onclick = () => checkAnswer(choice, q.answer);
    container.appendChild(btn);
  });
}

function checkAnswer(selected, correct) {
  const result = document.createElement("p");
  result.textContent = selected === correct ? "✅ 正解！" : "❌ 不正解";
  if (selected === correct) score++;
  document.getElementById("quiz-container").appendChild(result);

  current++;
  setTimeout(() => {
    if (current < questions.length) {
      showQuestion();
    } else {
      showResult();
    }
  }, 1000);
}

function showResult() {
  const container = document.getElementById("quiz-container");
  const rate = Math.round((score / questions.length) * 100);
  container.innerHTML = `<h2>終了！正答率：${rate}%</h2>`;
}

loadQuestions();

