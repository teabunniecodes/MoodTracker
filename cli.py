# import modules
import os
import sys
# import files
import core
import db

# record user's mood (insert into tracker table)
def record_mood():
    # get the moods as a list of strings
    moods = core.map_moods_text_as_list(database.fetchMoods())

    # show the moods to the user
    print(f"[>] Are you {', '.join(moods)}?")

    # loop untill a valid mood entered
    while True:
        # asks the user for their mood
        mood = input("[?] What is your mood right now? ").lower()
        # check if the entered mood is in the moods table
        if mood.capitalize() in moods:
            mood_id = database.fetchMood(mood)["id"]
            break
        else:
            # if the entered mood is not in the moods table,
            # then it'll ask the user whether to add it or not
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

    # insert the current mood in the tracker table in the database,
    # if there's an error, show it and exit the app
    try:
        database.insertTracker(mood_id, journal)
        print("[+] Your current mood has been recorded")
    except Exception as ex:
        print("[-] Error while recording the tracker (your current mood) in the database")
        print(ex)
        sys.exit(-1)

    # commit and close the database
    database.commit()
    database.close()

# view all user's entries'
def view_entries():
    from prettytable import PrettyTable
    print("=============================================================")
    print("[>] DateTime is stored in your local time")
    table = PrettyTable(["ID", "DateTime", "Mood", "Journal"])
    trackers = database.fetchTrackers()
    for tracker in trackers:
        table.add_row([tracker["id"], tracker["datetime"], database.fetchMoodById(tracker["mood_id"])["mood"], tracker["journal"]])
    print(table)
    print("=============================================================")

# main entry to the app
if __name__ == "__main__":
    # ensure that the database file is exist,
    # otherwise, you need to migrate first
    if not os.path.exists(core.DB_FILE):
        print("[!] Please migrate first using `python migrate.py`")
        sys.exit(-1)

    # connect to the database
    database = db.MoodTracker()
    database.connect()

    # ask the user for an option
    user_option = input("""Please select an option?

(1) Record your Current Mood
(2) View all Entries
(0) Quit
[?] """)
    print("")

    # check the option and execute its function
    if user_option == "1":
        record_mood()
    elif user_option == "2":
        view_entries()
    elif user_option == "0":
        sys.exit(0)
    else:
        print("[X] Invalid option!")
        sys.exit(-1)