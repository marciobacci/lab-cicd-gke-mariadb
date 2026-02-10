import os
import time
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "mariadb.aplicacao.svc.cluster.local")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "appdb")


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/")
def index():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS hits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ts BIGINT NOT NULL
                )
                """
            )
            cur.execute("INSERT INTO hits (ts) VALUES (%s)", (int(time.time()),))
            cur.execute("SELECT COUNT(*) AS total FROM hits")
            row = cur.fetchone()
        conn.close()
        return f"OK - hits={row['total']}\n", 200
    except Exception as e:
        return f"ERRO BD: {e}\n", 500
