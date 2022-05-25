# import modules
import datetime
import os
import sys
# import files
import db

# ensure that the database file is exist,
# otherwise, you need to migrate first
if not os.path.exists("./moodtracker.db"):
    print("[!] Please migrate first using `python migrate.py`")
    sys.exit(-1)

# connect to the database
database = db.Mood()
database.connect()

# pulls the date automatically in the correct format
curr_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# pulls the moods from the database to show it to the users,
# and convert it to list of moods
def get_moods_txt(item):
    return item['mood'].capitalize()

moods = list(map(get_moods_txt, database.fetchMoods()))

print(f"[>] Are you {', '.join(moods)}?")

while True:
    # asks the user for their mood
    mood = input("[?] What is your mood right now? ").lower()
    # checks to make sure that it is a valid choice,
    # if it's not valid, ask the user whether to add it or not
    if mood.capitalize() in moods:
        mood_id = database.fetchMood(mood)['id']
        break
    else:
        add_mood = input("[>] This mood does not exist. [?] Do you want to add it? [y/n] ")
        if add_mood[0] == "y":
            mood_id = database.insertMood(mood)
            break

# if cannot get any mood,
# show an error message and exit the app
if not mood_id:
    print("[X] Invalid Mood!")
    sys.exit(-1)

# ask the user about the reason why they feel that
journal = input(f"[?] Why do you feel {mood.capitalize()}? ")

# insert the tracker
try:
    database.insertTracker(curr_datetime, mood_id, journal)
    print("[+] Tracker has been recorded")
except Exception as ex:
    print("[-] Error while recording the tracker in the database")
    print(ex)
    sys.exit(-1)

# commit and close the database
database.close()