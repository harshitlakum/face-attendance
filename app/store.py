import sqlite3, os, numpy as np, base64, json
DB_PATH = os.getenv("DB_PATH", "data/embeddings.sqlite")

def _conn():
    os.makedirs("data", exist_ok=True)
    cx = sqlite3.connect(DB_PATH)
    cx.execute("""CREATE TABLE IF NOT EXISTS faces(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT NOT NULL,
        emb TEXT NOT NULL,
        meta TEXT
    )""")
    return cx

def insert_face(label: str, emb: np.ndarray, meta: dict):
    cx = _conn()
    emb64 = base64.b64encode(emb.tobytes()).decode()
    cx.execute("INSERT INTO faces(label, emb, meta) VALUES(?,?,?)", (label, emb64, json.dumps(meta)))
    cx.commit(); cx.close()

def load_all():
    cx = _conn()
    rows = cx.execute("SELECT label, emb FROM faces").fetchall()
    cx.close()
    labels, embs = [], []
    for label, emb64 in rows:
        arr = np.frombuffer(base64.b64decode(emb64), dtype=np.float32)
        labels.append(label); embs.append(arr)
    return (np.vstack(embs) if embs else np.empty((0,128), dtype=np.float32), labels)
