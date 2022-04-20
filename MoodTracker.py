import sqlite3

# keep track of daily moods along with allow user to input
def connect_db():
    conn_db = sqlite3.connect("moodtracker.db")
    db = conn_db.cursor()

def createTable():
    self.connect_db()
    db.execute("""CREATE TABLE IF NOT EXISTS mood_tracker
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            date DATETIME, mood TEXT, journal TEXT)""")

def insertData():
    db.execute("""INSERT INTO mood_tracker
                VALUES (1, "2022-04-19", "Excited", "Figured out how to code a 
                SQLite database, so I am excited!")""")

# db.execute("DELETE FROM mood_tracker")

conn_db.commit()
conn_db.close()