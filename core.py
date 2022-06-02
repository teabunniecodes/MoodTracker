import datetime

DB_FILE = './db/moodtracker.db'

# get the current datetime in YYYY-mm-dd HH:ii:ss format
def current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# get the moods from the database as a list of strings
def map_moods_text_as_list(moods):
    # get the mood's text
    def get_moods_txt(item):
        return item["mood"].capitalize()
    # get the moods from the database,
    # and convert it to list of moods texts' as a list of strings
    return list(map(get_moods_txt, moods))