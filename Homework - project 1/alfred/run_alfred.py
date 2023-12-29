from .addressbook import AddressBook
from thefuzz import fuzz


def clossest_match(querry: str, commands):
    """filters commands if they start with querry,
    if no command found querry is shortened by one char from the end
    and function tries again (recursively)"""
    if len(querry) == 0:
        return []
    matched_commands = list(filter(lambda x: x.startswith(querry), commands))
    if len(matched_commands) > 0:
        return matched_commands
    else:
        return clossest_match(querry[:-1], commands)


def command_hint(user_str: str, commands, threshold: int = 0) -> str:
    """return string with hint for user describing
    closest match to the available bot commands"""
    user_str = user_str.strip()
    hint = ""
    # for short string use startwith
    if len(user_str) <= 3:
        hits = clossest_match(user_str, commands)
    else:  # for longer strings use fuzzy string matching
        # calculate similarity scores for each command
        # ratio
        # scores = [fuzz.ratio(user_str, command) for command in commands]
        # partial
        # print(commands)
        scores = [fuzz.partial_ratio(user_str, command) for command in commands]

        # threshold = 0
        scores = list(filter(lambda x: x >= threshold, scores))
        # print(scores)
        # find best score
        best_score = max(scores)
        # print(best_score)
        # find all commands with best scores
        hits = [
            command for score, command in zip(scores, commands) if score == best_score
        ]
        # print(hits)

    if len(hits) > 0:
        hint = f"Did you mean?: {', '.join(hits)}"
    return hint


def get_contact_data():
    return {
        "name": input("Enter name: ").strip(),
        "phone": input("Enter phone: ").strip(),
        "email": input("Enter email: ").strip(),
        "birthday": input("Enter birthday: ").strip(),
        "address": input("Enter address: ").strip(),
        "tag": input("Enter tag: ").strip(),
        "notes": input("Enter your notes: ").strip(),
    }

def main():
    print(
        """
       db        88    ad88                                88  
      d88b       88   d8\"                                  88  
     d8\'`8b      88   88                                   88  
    d8\'  `8b     88 MM88MMM 8b,dPPYba,  ,adPPYba,  ,adPPYb,88  
   d8YaaaaY8b    88   88    88P\'   \"Y8 a8P_____88 a8\"    `Y88  
  d8\"\"\"\"\"\"\"\"8b   88   88    88         8PP\"\"\"\"\"\"\" 8b       88  
 d8\'        `8b  88   88    88         \"8b,   ,aa \"8a,   ,d88  
d8\'          `8b 88   88    88          `\"Ybbd8\"\'  `\"8bbdP\"Y8 

Hello! I am your virtual assistant.
What would you like to do with your Address Book?
Choose one of the commands:
    - hello - let's say hello,
    - find - to find a contact by name,
    - search - to find a contact after entering keyword (except tag and notes),
    - search notes - to find a contact name after entering keyword by searching by tag or notes,
    - show all - to show all of your contacts from address book,
    - show - to display N contacts from Address Book,
    - show notes - to display contact name with tag and notes,
    - add - to add new contact to Address Book,
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct in Address Book
    - edit phone - to change phone of the user,
    - edit email - to change email of the user,
    - edit birthday - to change birthday of the user,
    - edit address - to change address of the user,
    - edit tag - to change tag of the user,
    - edit notes - to change notes of the user,      
    - delete contact - to remove contact from Address Book
    - delete phone - to delete phone of the user,
    - delete email - to delete email of the user,
    - delete birthday - to delete birthday of the user,
    - delete address - to delete address of the user, 
    - delete tag - to delete tag of the user,
    - delete notes - to delete notes of the user,
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command."""
    )
    user_addr_book = AddressBook()
    user_addr_book.read_from_file()
    OPERATIONS_MAP = {
        "hello": user_addr_book.func_hello,
        "find": user_addr_book.func_find,
        "search": user_addr_book.func_search,
        "search notes": user_addr_book.func_search_notes,
        "show all": user_addr_book.func_show_all,
        "show": user_addr_book.func_show,
        "show notes": user_addr_book.func_show_notes,
        "add": user_addr_book.func_add,
        "birthday": user_addr_book.func_birthday,
        "upcoming birthdays": user_addr_book.func_upcoming_birthdays,
        "edit phone": user_addr_book.func_edit_phone,
        "edit email": user_addr_book.func_edit_email,
        "edit birthday": user_addr_book.func_edit_birthday,
        "edit address": user_addr_book.func_edit_address,
        "edit tag": user_addr_book.func_edit_tag,
        "edit notes": user_addr_book.func_edit_notes,
        "delete contact": user_addr_book.func_delete_contact,
        "delete phone": user_addr_book.func_delete_phone,
        "delete email": user_addr_book.func_delete_email,
        "delete birthday": user_addr_book.func_delete_birthday,
        "delete address": user_addr_book.func_delete_address,
        "delete tag": user_addr_book.func_delete_tag,
        "delete notes": user_addr_book.func_delete_notes,
        "good bye": user_addr_book.func_exit,
        "close": user_addr_book.func_exit,
        "exit": user_addr_book.func_exit,
        ".": user_addr_book.func_exit,
    }
    while True:
        listen_entered = input("\nEnter your command here: ")
        listen = listen_entered.lower().strip()
        try:
            if listen in OPERATIONS_MAP:
                if listen == "add":
                    user_data = get_contact_data()
                    OPERATIONS_MAP[listen](**user_data)
                elif listen in [
                    "find",
                    "birthday",
                    "delete contact",
                    "delete phone",
                    "delete email",
                    "delete birthday",
                    "delete address",
                    "delete tag",
                    "delete notes",
                ]:
                    name = input("Enter name: ").strip()
                    OPERATIONS_MAP[listen](name)
                elif listen == "upcoming birthdays":
                    keyword = input(
                        "Which time frame from today would you like to check? Please input the number of days from now: "
                    ).strip()
                    OPERATIONS_MAP[listen](keyword)
                elif listen in ["search", "search notes"]:
                    keyword = input("Enter keyword: ").strip()
                    OPERATIONS_MAP[listen](keyword)
                else:
                    OPERATIONS_MAP[listen]()
            elif listen in ["good bye", "close", "exit", "."]:
                user_addr_book.save_to_file()
                OPERATIONS_MAP[listen.lower()]()
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()