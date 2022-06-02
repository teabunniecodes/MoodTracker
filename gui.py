# import modules
import os
import sys
import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.uic
# import files
import core
import db
import migrate

class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        # call the __init__ method from the parent class
        super(MainWindow, self).__init__()
        # load the ui file
        PyQt5.uic.loadUi("./ui/main.ui", self)
        # check if migration is needed
        self.check_migration()
        # connect to the database
        self.database = db.MoodTracker()
        self.database.connect()
        # find the widgets and assign them to variables
        self.why_frame = self.findChild(PyQt5.QtWidgets.QFrame, "why_frame")
        self.viewall_frame = self.findChild(PyQt5.QtWidgets.QFrame, "viewall_frame")
        self.viewall_table = self.findChild(PyQt5.QtWidgets.QTableWidget, "viewall_table")
        self.viewall_btn = self.findChild(PyQt5.QtWidgets.QPushButton, "viewall_btn")
        self.moods_label = self.findChild(PyQt5.QtWidgets.QLabel, "moods_label")
        self.mood_input = self.findChild(PyQt5.QtWidgets.QLineEdit, "mood_input")
        self.next_btn = self.findChild(PyQt5.QtWidgets.QPushButton, "next_btn")
        self.why_feel_label = self.findChild(PyQt5.QtWidgets.QLabel, "why_feel_label")
        self.why_feel_input = self.findChild(PyQt5.QtWidgets.QLineEdit, "why_feel_input")
        self.record_mood_btn = self.findChild(PyQt5.QtWidgets.QPushButton, "record_mood_btn")
        # do an action when clicked enter button on a specific input
        # go next when clicked enter button on the mood input
        self.mood_input.returnPressed.connect(self.next_btn.click)
        # create a record when clicked enter button on the why feel input
        self.why_feel_input.returnPressed.connect(self.record_mood_btn.click)
        # get the moods from the database, and
        # change the text of the moods to the moods in the database
        self.update_moods_label()
        # do an action when clicked on buttons
        # view all entries button when clicked
        self.viewall_btn.clicked.connect(self.view_all_items)
        # show "why do u feel ..." when clicked on next
        self.next_btn.clicked.connect(self.show_why)
        # create record when clicked
        self.record_mood_btn.clicked.connect(self.create_record)
        # show the main window
        self.show_main_window()

    def show_main_window(self):
        # show the app window
        self.show()
        # and hide the other widgets, that are not needed rn
        self.why_frame.hide()
        self.viewall_frame.hide()

    def view_all_items(self):
        # clear the table
        self.viewall_table.setRowCount(0)
        # get the items from the database
        trackers = self.database.fetchTrackers()
        for tracker in trackers:
            # get the last row poisition
            rowPosition = self.viewall_table.rowCount()
            # insert the row at the last position
            self.viewall_table.insertRow(rowPosition)
            # insert the columns
            self.viewall_table.setItem(rowPosition, 0, PyQt5.QtWidgets.QTableWidgetItem(str(tracker["id"])))
            self.viewall_table.setItem(rowPosition, 1, PyQt5.QtWidgets.QTableWidgetItem(tracker["datetime"]))
            self.viewall_table.setItem(rowPosition, 2, PyQt5.QtWidgets.QTableWidgetItem(self.database.fetchMoodById(tracker["mood_id"])["mood"]))
            self.viewall_table.setItem(rowPosition, 3, PyQt5.QtWidgets.QTableWidgetItem(tracker["journal"]))

    def show_why(self):
        # get the mood input
        mood = self.mood_input.text()
        # then show it to the user to ask them
        self.why_feel_label.setText(f"Why do you feel {mood}?")

    def create_record(self):
        try:
            # get the text inputs
            mood = self.mood_input.text()
            why = self.why_feel_input.text()
            # check if the entered mood is in the moods table
            if mood.capitalize() in self.moods:
                mood_id = self.database.fetchMood(mood)["id"]
            else:
                # if not then ask the user whether to add it or not
                qm = PyQt5.QtWidgets.QMessageBox
                qm.question(self, "Warning", "This mood does not exist.\nDo you want to add it?", qm.Yes | qm.No)
                if qm.Yes:
                    # if yes, then add it the moods table and return its ID
                    mood_id = self.database.insertMood(mood)
                else:
                    # if no, then clear the inputs and don't do anything
                    mood_id = None
                    self.mood_input.setText("")
                    self.why_feel_input.setText("")
                    PyQt5.QtWidgets.QMessageBox.warning(self, "Cancelled", "You have selected not to add the mood.")
            if mood_id:
                # insert the tracker into the database
                self.database.insertTracker(mood_id, why)
                # commit the database
                # (NOTE: YOU DON'T CLOSE THE DATABASE IN A GUI APP,
                # UNLESS YOU CHANGE THE CODE STRUCTURE, CONNECT IT WITH EVERY ACTION OR ANYTHING)
                self.database.commit()
                # update the moods label
                self.update_moods_label()
                # clear the inputs
                self.mood_input.setText("")
                self.why_feel_input.setText("")
                # show successfull message
                PyQt5.QtWidgets.QMessageBox.about(self, "Done", "Your current mood has been recorded.")
        except:
            PyQt5.QtWidgets.QMessageBox.critical(self, "Error", "Error while recording the tracker (your current mood) in the database")

    def get_moods(self):
        # get the moods from the table as a list of strings
        return core.map_moods_text_as_list(self.database.fetchMoods())

    def update_moods_label(self):
        # get moods string and set it into the label
        self.moods = self.get_moods()
        self.moods_label.setText(f"[>] Are you {', '.join(self.moods)}?")

    def check_migration(self):
        # if database file does not exist
        if not os.path.exists(core.DB_FILE):
            try:
                # try to migrate
                PyQt5.QtWidgets.QMessageBox.warning(self, "Migration", "Please wait while migrating the database...")
                migrate.migrate()
                # if successfull show a sucess message
                PyQt5.QtWidgets.QMessageBox.about(self, "Done", "Migrated Successfully")
            except:
                # if not, show error message
                PyQt5.QtWidgets.QMessageBox.critical(self, "Error", "Migration error. Try to migrate manually from the console `python migrate.py`.")
                # and exit the app
                sys.exit(-1)

# main entry to the app
if __name__ == "__main__":
    # init the Qt5 app
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    # init the main window
    window = MainWindow()
    # execute the app
    sys.exit(app.exec_())