import sqlite3, json, uuid, hashlib, datetime, os

DB_PATH = os.path.join(os.path.dirname(__file__), "mediscan.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            pw_hash  TEXT    NOT NULL,
            created  TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reports (
            id        TEXT    PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            timestamp TEXT    NOT NULL,
            conditions TEXT   NOT NULL,
            params    INTEGER NOT NULL,
            abnormal  INTEGER NOT NULL,
            data      TEXT    NOT NULL,
            summary   TEXT    NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    conn.commit(); conn.close()

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def create_user(name, email, password):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name,email,pw_hash,created) VALUES (?,?,?,?)",
            (name.strip(), email.strip().lower(), hash_pw(password),
             datetime.datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit(); conn.close()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND pw_hash=?",
        (email.strip().lower(), hash_pw(password))
    ).fetchone()
    conn.close()
    if row:
        return True, dict(row)
    return False, None

def save_report(user_id, final_data, conditions, summary):
    rid = str(uuid.uuid4())[:8].upper()
    conn = get_db()
    conn.execute(
        "INSERT INTO reports (id,user_id,timestamp,conditions,params,abnormal,data,summary) VALUES (?,?,?,?,?,?,?,?)",
        (rid, user_id,
         datetime.datetime.now().isoformat(timespec="seconds"),
         json.dumps(conditions),
         len(final_data),
         sum(1 for d in final_data.values() if d.get("status","").lower() in ("high","low")),
         json.dumps(final_data, default=str),
         summary)
    )
    conn.commit(); conn.close()
    return rid

def get_user_reports(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reports WHERE user_id=? ORDER BY timestamp DESC LIMIT 50",
        (user_id,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["conditions"] = json.loads(d["conditions"])
        d["data"]       = json.loads(d["data"])
        result.append(d)
    return result
