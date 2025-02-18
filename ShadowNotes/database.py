import sqlite3

def init_db():
    conn = sqlite3.connect("data/notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_encrypted_note(title, encrypted_content):
    conn = sqlite3.connect("data/notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, encrypted_content))
    conn.commit()
    conn.close()

def get_all_notes():
    conn = sqlite3.connect("data/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes