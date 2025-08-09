from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

def load_questions():
    questions = []
    with open("questions.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append({
                "no": row["No"],
                "category": row["カテゴリ"],
                "question": row["問題文"],
                "choices": [row["選択肢1"], row["選択肢2"], row["選択肢3"], row["選択肢4"], row["選択肢5"]],
                "answer": row["正解"]
            })
    return questions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_questions")
def get_questions():
    return jsonify(load_questions())

if __name__ == "__main__":
    app.run(debug=True)
