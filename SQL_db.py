import sqlite3

class MoodDatabase:
 # keep track of daily moods along with allow user to input
    def connect_db(self):
        self.conn_db = sqlite3.connect("moodtracker.db")
        self.db = self.conn_db.cursor()

    def createTable(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS mood_tracker
                (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Date DATETIME, Mood TEXT, Journal TEXT)""")

    def insertData(self, date, mood, journal):
        sql = f"""INSERT INTO mood_tracker(Date, Mood, Journal)
                    VALUES ('{date}', '{mood}', '{journal}')"""
        self.db.execute(sql)

    def clearTable(self):
        self.db.execute("DELETE FROM mood_tracker")

    def close_db(self):
        self.conn_db.commit()
        self.conn_db.close()