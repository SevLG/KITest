import datetime

# class DatabaseInputProcessor
# class that handles type checking, sending input to 'insert_into_karda' as well as adding
# changes to the logfile "history"
#
# CONSTRUCTOR INPUT: String username - the name of the person inserting data
import util


class DatabaseInputProcessor:
    def __init__(self, username):
        self.user = username
        self.existing_tables = ["inleverans", "lagersaldo", "förbrukning", "kapacitet", "beställning"]
        self.table_name = ""
        # tänkte här att vi vill hålla oss till några specifikt angivna leverantörer,
        # särskilt då de skulle vara i en drop down i frontend
        self.leverantorer = ["Astra Zeneca", "Moderna", "Pfizer"]
        self.data_list = []
        self.types = []

    # send_input
    # the only method that is called from outside the class, uses inputs of table name
    # and a list of data values, together with the other methods of the class, to
    # set everything up for type checking, sending values to the database as well as
    # logging changes to history
    #
    # INPUT: String table_name -- name of a table in KARDA.db to which values will be inserted
    #        List data_list -- list of values to be added to KARDA.db
    # OUTPUT: bool -- telling the system outside of the class if it was successful or not
    #
    # jag ville egentligen använda någon slags throw custom exception för när saker går fel
    # men vet inte hur man gör egna exceptions i python, så jag gjorde return bool +
    # print av felet som en lat lösning
    def send_input(self, table_name, data_list):
        if table_name not in self.existing_tables:
            print("No such table exists")
            return False
        self.table_name = table_name
        # table types gets a list of types that the current table should contain
        self.table_types()
        # if you have given more or fewer values than there are types then something
        # has gone wrong
        if len(data_list) != len(self.types):
            print("Number of args does not match number of columns in given table")
            return False
        else:
            self.data_list = data_list
        # check input does a type check over data_list using the types gotten from
        # table_types(). It returns false if there is a missmatch, otherwise true
        if self.check_input():
            # everything went well and we insert the values to the table and
            # add event to history
            insert_into_karda(self.table_name, self.data_list)
            self.add_history()
            return True
        else:
            # the input failed check_input, an "error" message is printed from inside
            # check_input()
            return False

    # check_input
    # accesses class attributes data_list and types and compares them one by one
    # there are a limited number of types, so these become cases in which we
    # do a type check on the same index of data_list. All input will presumably be strings
    # at first so no need to type check string
    #
    # OUTPUT: bool -- telling caller that check_input has failed or succeeded
    def check_input(self):
        # we go through the indices of data_list and types concurrently,
        # finding type cases using if-else and testing data_list based on type case
        for i in range(len(self.data_list)):
            if self.types[i] == "date":
                try:
                    # of the element at position i in data_list is not in a
                    # date format we will get a ValueError which is caught by the try-catch.
                    # if it is in an incorrect format we return false and print
                    # what has gone wrong
                    # from the example table in instructions I also believe dates can be left
                    # blank, so we add an option for that
                    if self.data_list[i] == "":
                        pass
                    elif not isinstance(datetime.datetime.strptime(self.data_list[i], '%Y-%m-%d'),
                                      datetime.date):
                        print(str(self.data_list[i]) + "should be date in format " +
                              "Year-Month-Day")
                        return False
                except ValueError:
                    print("Input: " + str(self.data_list[i]) + " should be date in format " +
                          "Year-Month-Day")
                    return False
            elif self.types[i] == "leverantor":
                # we use self.leverantorer to see if a known leverantör has been given
                # as value
                if not self.data_list[i] in self.leverantorer:
                    print("Supplier name " + str(self.data_list[i]) + " not recognized")
                    return False
            elif self.types[i] == "int":
                # if data_list[i] cannot be converted to int it is of the wrong type
                try:
                    int(self.data_list[i])
                except ValueError:
                    print(self.data_list[i] + " should be of type 'int'")
                    return False
        return True

    # table_types
    # based on the class attribute table_name we set the configuration for the attribute
    # types, containing a list telling us what type each index of the data_list should be
    #
    # lite jobbigt hårdkodad del som jag tror är nödvändig då det är lite godtyckligt hur
    # datan ligger mellan de olika tabellerna. Använder "table_name" för att hämta vilka typer
    # den aktuella tabellen ska innehålla, vilket sen kan användas för att typchecka
    def table_types(self):
        if self.table_name == "inleverans":
            self.types = ["date", "date", "leverantor", "int", "string"]
        elif self.table_name == "lagersaldo":
            self.types = ["date", "leverantor", "int", "int"]
        elif self.table_name == "förbrukning":
            self.types = ["date", "leverantor", "int"]
        elif self.table_name == "kapacitet":
            self.types = ["date", "int"]
        elif self.table_name == "beställning":
            self.types = ["date", "date", "int", "string"]
        else:
            # a name that does not exist in tables of KARDA.db has been given
            print(self.table_name + " is not a valid table name")
            del self

    # add_history
    # writes the current date and time, the user name and what values were added to which
    # table to an outfile called history
    def add_history(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_list_string = ""
        # since this is python we magically have non-string items in the list
        # that we convert to str
        for item in self.data_list:
            data_list_string += str(item) + " "
        history = current_time + " user: " + self.user + " added " + \
                  data_list_string + "to " + self.table_name + "\n"
        outfile = open('data/history', 'a')
        outfile.write(history)
        outfile.close()


# insert_into_karda
# takes input in the form of the name of a table in KARDA as well as a list of inputs
# sets up an sqlite3 connection with KARDA.db and inserts the values from this list
#
# INPUT: String table_name -- name of the table in KARDA.db where data will be inserted
#        List data_list -- list of values to insert into KARDA.db
def insert_into_karda(table_name, data_list):
    con, cur = util.get_connection("data/KARDA.db")
    # Vi använder f' -notationen för att kunna sätta in variabler i queryn enkelt på '?'-tecken
    # eftersom de olika db-tablesen har olika många argument så låter vi antalet '?'-tecken vara
    # dynamiskt efter antalet argument i data_list, genom att använda arg_len stycken '?'-tecken
    arg_len = len(data_list)
    statement = f'INSERT INTO ' + table_name + ' VALUES (' + '?, ' * (arg_len - 1) + '?);'
    with con:
        # *data_list, packar automatiskt upp listan data_list som en tupel,
        # vilket gör att vi slipper hålla reda på listans längd
        cur.execute(statement, (*data_list,))
    con.close()


# tables set up to be part of a dictionary, which is used in the cmd line to display
# available data columns in the given table
inleverans = [
    "Lev datum",
    "Planerat lev datum",
    "Vaccinleverantör",
    "Kvantitet vial",
    "GLN-mottagare"
]

lagersaldo = [
    "Datum tid",
    "Vaccinleverantör",
    "Kvantitet vial",
    "Kvantitet dos"
]

forbrukning = [
    "Förbrukningsdatum",
    "Vaccinleverantör",
    "Kvantitet vial"
]

kapacitet = [
    "Kapacitetsdatum (prognos)",
    "Kapacitet (doser)"
]

bestallning = [
    "Beställningsdatum",
    "Önskat lev datum",
    "Kvantitet dos",
    "GLN-mottagare"
]

table_dict = {
    "inleverans": inleverans,
    "lagersaldo": lagersaldo,
    "förbrukning": forbrukning,
    "kapacitet": kapacitet,
    "beställning": bestallning
}
