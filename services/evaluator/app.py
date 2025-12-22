from flask import Flask, request, jsonify
import psycopg2
import json
import random

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "microlern_db",
    "user": "microlern",
    "password": "microlern123",
    "host": "db",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/evaluate", methods=["POST"])
def evaluate_model():
    data = request.json
    model_id = data.get("model_id")

    if not model_id:
        return jsonify({"error": "model_id is required"}), 400

    # dummy evaluation simulation
    accuracy = round(random.uniform(0.7, 0.99), 3)
    precision = round(random.uniform(0.7, 0.99), 3)
    recall = round(random.uniform(0.7, 0.99), 3)
    f1 = round((2 * precision * recall) / (precision + recall), 3)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO evaluations(model_id, accuracy, precision, recall, f1_score)
        VALUES (%s,%s,%s,%s,%s) RETURNING id;
    """, (model_id, accuracy, precision, recall, f1))

    eval_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "evaluation_id": eval_id,
        "model_id": model_id,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }), 201


@app.route("/evaluations", methods=["GET"])
def get_all_evaluations():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM evaluations;")
    rows = cur.fetchall()

    evaluations = []
    for r in rows:
        evaluations.append({
            "id": r[0],
            "model_id": r[1],
            "accuracy": r[2],
            "precision": r[3],
            "recall": r[4],
            "f1_score": r[5]
        })

    cur.close()
    conn.close()
    return jsonify(evaluations)

@app.route("/", methods=["GET"])
def health():
    return "Evaluator Service Running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
