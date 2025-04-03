from flask import Flask, render_template, request, redirect, url_for, session
import random
from full_questions import questions

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def quiz():
    if "questions" not in session:
        session["questions"] = random.sample(questions, len(questions))
        session["current"] = 0
        session["score"] = 0
        session["answers"] = []

    if session["current"] >= len(session["questions"]):
        return redirect(url_for("result"))

    current_q = session["questions"][session["current"]]
    feedback = ""
    correct = None

    if request.method == "POST":
        selected = int(request.form["choice"])
        correct = (selected == current_q["answer"])
        feedback = "✅ Correct!" if correct else f"❌ Incorrect! The correct answer was: {current_q['choices'][current_q['answer']]}"
        if correct:
            session["score"] += 1

        session["answers"].append({
            "question": current_q["question"],
            "your_answer": current_q["choices"][selected],
            "is_correct": correct,
            "correct_answer": current_q["choices"][current_q["answer"]]
        })

        session["current"] += 1
        session.modified = True

        if session["current"] >= len(session["questions"]):
            return redirect(url_for("result"))

        return render_template("quiz.html", q=session["questions"][session["current"]],
                               qnum=session["current"] + 1, total=len(session["questions"]),
                               feedback=None, correct=None)

    return render_template("quiz.html", q=current_q, qnum=session["current"] + 1,
                           total=len(session["questions"]), feedback=None, correct=None)

@app.route("/result")
def result():
    answers = session.get("answers", [])
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    session.clear()
    return render_template("result.html", score=score, total=total, answers=answers)

if __name__ == "__main__":
    app.run(debug=True)
