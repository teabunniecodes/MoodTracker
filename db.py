import sqlite3
import core

class DatabaseCore:
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class MoodTracker:
    def connect(self):
        self.con = sqlite3.connect(core.DB_FILE)
        self.con.row_factory = DatabaseCore.dict_factory
        self.cur = self.con.cursor()

    def createTables(self):
        self.cur.execute("""
            PRAGMA foreign_keys = ON;
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                mood TEXT
            );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                datetime DATETIME NOT NULL,
                mood_id INTEGER NOT NULL,
                journal TEXT,

                FOREIGN KEY(mood_id) REFERENCES moods(id)
            );
        """)

    def dropTables(self):
        self.cur.execute("DROP TABLE IF EXISTS tracker")
        self.cur.execute("DROP TABLE IF EXISTS moods")

    def clearTables(self):
        self.cur.execute("DELETE FROM tracker")
        self.cur.execute("DELETE FROM moods")
        self.cur.execute("DELETE FROM sqlite_sequence")

    def insertMood(self, mood):
        self.cur.execute(f"""INSERT INTO moods (mood) VALUES (?)""", [mood])
        return self.cur.lastrowid

    def insertTracker(self, mood_id, journal):
        datetime = core.current_datetime()
        self.cur.execute(f"""INSERT INTO tracker (datetime, mood_id, journal) VALUES (?, ?, ?)""", [datetime, int(mood_id), journal])
        return self.cur.lastrowid

    def fetchTrackers(self):
        self.cur.execute(f"""SELECT * FROM tracker""")
        return self.cur.fetchall()

    def fetchMoods(self):
        self.cur.execute(f"""SELECT * FROM moods""")
        return self.cur.fetchall()

    def fetchMoodById(self, id):
        self.cur.execute(f"""SELECT * FROM moods WHERE id = ?""", [int(id)])
        return self.cur.fetchone()

    def fetchMood(self, mood):
        self.cur.execute(f"""SELECT * FROM moods WHERE mood = ?""", [mood])
        return self.cur.fetchone()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()