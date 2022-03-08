import util
import DatabaseInputProcessor

# simpel interface for kommandoraden, kollar vilket val man fått som input
# och låter en antingen lägga till data i KARDA.db
# eller kolla historiken ifall man är admin
def basic_cmd_interface(user, choice):
    if choice == 1:
        db_processor = DatabaseInputProcessor.DatabaseInputProcessor(user)
        print("Which table are you adding data to?")
        for i in range(len(db_processor.existing_tables)):
            print(db_processor.existing_tables[i])
        table_name = input(": ")
        required_data_list = DatabaseInputProcessor.table_dict.get(table_name)
        data_list = []
        for col in required_data_list:
            data_list.append(input(col + ": "))
        db_processor.send_input(table_name, data_list)

    if choice == 2:
        events = util.check_history(user)
        # ifall user inte är admin så kommer events vara en tom lista
        for event in events:
            print(event)


def main():
    print("Använd username: 'admin' för rättigheter att kolla KARDA.db's historik")
    user = input("Username: ")
    choice = 0
    while choice != 3:
        print("What do you want to do?")
        print("1. Input data into KARDA.db")
        print("2. Check KARDA.db history")
        print("3. Log out")
        choice = int(input(": "))
        basic_cmd_interface(user, choice)
    print("Goodbye")


main()
