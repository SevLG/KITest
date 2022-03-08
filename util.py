import os.path
import sqlite3


# get_connection
# takes the name of a database file and sets up an sqlite  connection, returning
# the connection and cursor
#
# INPUT: String db_file -- the name of a database file
# OUTPUT: sqlite3.connection
#         connection.cursor
#
# kod stulen från mig själv, som jag använt i en kurs för 1-2 år sedan
# baserad på något jag hittade på stackoverflow om jag minns rätt
def get_connection(db_file):
    # om jag minns rätt så behövde jag hitta en abspath för att få
    # allt att fungera korrekt här
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_file)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor

# check_history
# if the given username is an admin, they are allowed to check the history file
#
# INPUT: String user -- username
# OUTPUT: List events -- list of all added events in history
def check_history(user):
    admins = ["admin"]
    if user in admins:
        infile = open('data/history', 'r')
        event_list = infile.readlines()
        infile.close()
        return event_list
    print("Access denied\n")
    return []