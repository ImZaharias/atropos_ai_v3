from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3, os, json, datetime
from rules import init_scores, apply_effects, finalize_result, TROLL_LINES

app = Flask(__name__)
app.secret_key = "atropos-ai-secret"

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        session_id TEXT,
        qid TEXT,
        answer TEXT,
        scores TEXT,
        motivation TEXT,
        step INTEGER,
        final_role TEXT,
        feedback INTEGER
    )
    """)
    return con

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html", title="Atropos AI")

@app.post("/start")
def start():
    session["scores"] = init_scores()
    session["motivation"] = {"Money":0,"Stability":0,"Challenge":0,"Ease":0,"Prestige":0,"Impact":0}
    session["answers"] = {}
    session["trace"] = []
    session["step"] = 0
    session["session_id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    return redirect(url_for("question", i=0))

@app.get("/question/<int:i>")
def question(i: int):
    questions = load_questions()
    if i >= len(questions):
        return redirect(url_for("result"))
    q = questions[i]
    troll = TROLL_LINES[i % len(TROLL_LINES)]
    return render_template("question.html", q=q, idx=i, total=len(questions), troll=troll, int=int, title="Atropos AI — Question")

@app.post("/answer")
def answer():
    data = request.form
    i = int(data.get("idx", 0))
    choice = data.get("choice", "").strip()
    questions = load_questions()
    if i >= len(questions):
        return redirect(url_for("result"))
    q = questions[i]

    effective = choice
    scores = session.get("scores")
    motivation = session.get("motivation")

    applied_effects = {}
    rule_id = ""
    if q["type"] == "single":
        for opt in q["options"]:
            if opt["text"] == choice:
                applied_effects = opt.get("effects", {})
                rule_id = opt.get("rule_id","")
                break
    elif q["type"] == "yn":
        for opt in q["options"]:
            if opt["value"] == choice:
                applied_effects = opt.get("effects", {})
                rule_id = opt.get("rule_id","")
                break

    apply_effects(scores, motivation, applied_effects)

    session["trace"].append({"qid": q["id"], "rule_id": rule_id, "effects": applied_effects})

    session["scores"] = scores
    session["motivation"] = motivation
    session["answers"][q["id"]] = effective
    session["step"] = i + 1

    con = get_db()
    con.execute(
        "INSERT INTO interactions(ts,session_id,qid,answer,scores,motivation,step) VALUES(?,?,?,?,?,?,?)",
        (datetime.datetime.now().isoformat(), session["session_id"], q["id"], effective, json.dumps(scores, ensure_ascii=False), json.dumps(motivation, ensure_ascii=False), i+1)
    )
    con.commit(); con.close()

    return redirect(url_for("question", i=i+1))

@app.get("/result")
def result():
    questions = load_questions()
    if session.get("step", 0) < len(questions):
        return redirect(url_for("question", i=session.get("step", 0)))
    scores = session.get("scores")
    motivation = session.get("motivation")
    role, reasoning, ordered = finalize_result(scores, motivation)

    con = get_db()
    con.execute(
        "INSERT INTO interactions(ts,session_id,qid,answer,scores,motivation,step,final_role) VALUES(?,?,?,?,?,?,?,?)",
        (datetime.datetime.now().isoformat(), session.get("session_id"), "FINAL", "", json.dumps(scores, ensure_ascii=False), json.dumps(motivation, ensure_ascii=False), session.get("step", 0), role)
    )
    con.commit(); con.close()

    show_trace = request.args.get("trace") == "1"

    return render_template("result.html",
        role=role,
        reasoning=reasoning,
        ordered=ordered,
        answers=session.get("answers", {}),
        trace=session.get("trace", []),
        show_trace=show_trace,
        title="Atropos AI — Result")

@app.post("/feedback")
def feedback():
    val = request.form.get("rating", type=int)
    con = get_db()
    con.execute("UPDATE interactions SET feedback=? WHERE session_id=? AND qid='FINAL'", (val, session.get("session_id")))
    con.commit(); con.close()
    return jsonify({"ok": True})

@app.get("/admin")
def admin():
    con = get_db()
    totals = con.execute("SELECT final_role, COUNT(*) c FROM interactions WHERE qid='FINAL' GROUP BY final_role ORDER BY c DESC").fetchall()
    latest = con.execute("SELECT ts, session_id, final_role, feedback FROM interactions WHERE qid='FINAL' ORDER BY id DESC LIMIT 10").fetchall()
    con.close()
    return render_template("admin.html", totals=totals, latest=latest, title="Atropos AI — Admin")


if __name__ == "__main__":
    app.run(debug=True)
