import sys
import db

print("[*] Started Migrating...")

print("[*] Initiating and connecting to the database...")
try:
    database = db.Mood()
    database.connect()
    print("[+] Connected successfully.")
except Exception as ex:
    print("[-] Error while connecting to the database.")
    print(ex)
    sys.exit(-1)

print("[*] Dropping, creating, and clearing the tables...")
try:
    database.dropTables()
    database.createTables()
    database.clearTables()
    print("[+] Tables dropped, created, cleared successfully.")
except Exception as ex:
    print("[-] Error while dropping, creating, and clearing the tables.")
    print(ex)
    sys.exit(-1)


print("[*] Inserting the moods...")
try:
    moods = ["Happy", "Sad", "Stressed", "Frustrated", "Angry", "Excited", "Content", "Confused", "Tired", "Apathetic"]
    for mood in moods:
        database.insertMood(mood.lower())
    print("[+] Moods inserted successfully")
except Exception as ex:
    print("[-] Error while inserting moods in the database")
    print(ex)
    sys.exit(-1)

print("[*] Committing the database...")
try:
    database.close()
    print("[+] Database committed and closed successfully")
except Exception as ex:
    print("[-] Error while committing the database")
    print(ex)
    sys.exit(-1)