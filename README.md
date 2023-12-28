# Project Name

**_'Alfred'_ the CLI Bot assistant.**

![Alfred-sign](https://github.com/rafalradx/alfred-assist-bot/blob/main/alfred/Alfred.jpg)

## Table of Contents

- [General Info](#general-information)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Screenshots](#screenshots)
- [Setup](#setup)
- [Usage](#usage)
- [Project Status](#project-status)
- [Room for Improvement](#room-for-improvement)
- [Contributing](#contributing)
- [Info](#info)
- [Contact](#contact)
- [License](#license)

## General Information

_Alfred_ streamlines the management of your address book, offering a comprehensive set of features that empower users to add, edit, delete, search, and organize contacts with ease.

The inclusion of birthday notifications, tags, and notes enhances the overall utility of the address book, making _Alfred_ a valuable tool for effective contact management.

_Alfred_ is designed with a user-friendly command-line interface for intuitive interaction. The command-line interface simplifies user commands and makes the address book management process efficient and accessible.

## Technologies Used

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3115/)

Requirements:
   - [thefuzz](https://pypi.org/project/thefuzz/) - package for fuzzy text matching 

No additional configurations are required. _Alfred_ stores the address book data locally.

## Features

_Alfred_ provides a range of essential functionalities for managing your address book effectively. Here's an expanded overview of its capabilities:

1. **Adding Contacts** - allows users to seamlessly add new contacts to their address book.
2. **Editing Contacts** - users can easily modify contact details, such as phone numbers, email addresses, birthdays, addresses, tags, and notes.
3. **Deleting Contacts** - enables users to remove contacts from the address book when they are no longer relevant or needed.
4. **Searching Contacts** - allows users to quickly find specific contacts.
5. **Birthday Notifications** - a convenient way to check the days remaining until the birthday of a specified contact.
6. **Upcoming Birthdays** - enable users to check and plan for upcoming birthdays within a specified timeframe.
7. **Tagging Contacts** - allows users to assign tags to contacts for easy categorization and grouping.
8. **Adding Notes** - users can attach notes to contacts, providing additional information or context.

## Screenshots

Sample table of contacts:
![Alfred-show-all](https://github.com/rafalradx/alfred-assist-bot/blob/main/alfred/show_all.jpg)

Sample table of upcoming birthdays within a specified timeframe:
![Alfred-birthdays](https://github.com/rafalradx/alfred-assist-bot/blob/main/alfred/birthdays.jpg)

Sample table of notes:
![Alfred-show_notes](https://github.com/rafalradx/alfred-assist-bot/blob/main/alfred/show_notes.jpg)

## Setup

1. **Clone the Repository:**

   - Clone this repository into a folder of choice on your local machine using the following command:
     ```
     git clone https://github.com/rafalradx/alfred-assist-bot
     ```

2. **Install dependencies:**
   - Install ![thefuzz](https://pypi.org/project/thefuzz/) package:
     ```
     pip install thefuzz
     ```

3. **Setup the Application:**

   - Navigate to the project directory:
     ```
     cd alfred-assist-bot
     ```
   - Run the following command to install application:
     ```
     pip install .
     ```
     or
     ```
     python setup.py install
     ```

4. **Run the Application:**

   - Start the Address Book application using the following command:
     ```
     alfred-run
     ```
   - Follow the on-screen instructions to interact with the application.

5. **Uninstall:**
   - To remove Alfred run the following command:
     ```
     pip uninstall alfred
     ```

## Usage

Follow the prompts to perform various operations on your address book.
Enter commands as instructed to manage your contacts effectively:

- `hello`: Start the interaction with a friendly greeting.
- `find`: Look up a contact by name.
- `search`: Find contacts using a keyword.
- `search notes`: Find a contact name by entering a keyword in tags or notes.
- `show all`: Display all contacts in the address book.
- `show`: Display a specified number of contacts from the address book.
- `add`: Add a new contact to the address book.
- `birthday`: Display the days until a contact's birthday.
- `upcoming birthdays`: Check upcoming birthdays within a specified timeframe.
- `edit phone`: Change a contact's phone number.
- `edit email`: Change a contact's email address.
- `edit birthday`: Change a contact's birthday.
- `edit address`: Change a contact's address.
- `edit tag`: Change a contact's tag.
- `edit notes`: Change a contact's notes.
- `delete contact`: Remove a contact from the address book.
- `delete phone`: Delete a contact's phone number.
- `delete email`: Delete a contact's email address.
- `delete birthday`: Delete a contact's birthday.
- `delete address`: Delete a contact's address.
- `delete tag`: Delete a contact's tag.
- `delete notes`: Delete a contact's notes.
- `good bye`, `close`, `exit`, `.`: Say goodbye and exit the program.

## Project Status

Current project version: _**1.0.0**_

Project is: _**in progress**_.

## Room for Improvement

1. Database Interaction: enhance by incorporating database support for persistent storage and retrieval of contacts.
2. Data Export and Import: allow users to export and import data, facilitating seamless data transfer between different program installations.
3. Image Attachment: introduce the capability to add images to contacts for easier identification.
4. Integration with External Sources: add an automatic contact information completion feature by leveraging external sources through web service APIs.
5. External Communication: transition _Alfred_ into a server mode to enable remote access to functions via an API, useful for integration with other tools.
6. Authentication and Security: implement user authentication features and secure access to editing or deletion functions with a password.
7. Activity History: allow users to track the history of changes for each contact, facilitating monitoring of who made edits and when.
8. Command Extensions: provide an easy way to add new commands and extend _Alfred's_ capabilities without modifying existing code.

## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request with your change.

## Info

This project was completed during the "Python Developer" course organized by GOIT POLSKA Sp. z o.o.

## Contact

Created by **'Gotham Devs'**

**Katarzyna Drajok** _katarzyna.drajok@gmail.com_

**Katarzyna Czempiel** _katarzyna.czempiel@gmail.com_

**Rafał Pietras** _rafal.radx@gmail.com_

**Dawid Radzimski** _dawid.radzimski@gmail.com_

**Adrian Karwat** _adr.karwat@gmail.com_

Feel free to contact us!
Thank you for using _Alfred_!

## License

This project is licensed under the MIT License.
