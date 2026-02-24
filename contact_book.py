# ============================================================
# Contact Book — Session 1.3
# Concepts used: lists, dictionaries, for loops, f-strings,
#                enumerate(), .lower(), in operator,
#                import, open(), with, json.dump/load, try/except
# ============================================================

import json   # built-in module — no install needed
              # gives us json.dump() and json.load()

# ------------------------------------------------------------
# THE DATA STORE
# ------------------------------------------------------------
# A list is written with square brackets: []
# This starts empty — load_contacts() will fill it from disk.
# In VBA terms: think of this as a dynamic array of records.

CONTACTS_FILE = "contacts.json"   # the file we'll save to/load from
                                  # ALL_CAPS = a constant (convention only,
                                  # Python doesn't enforce it)

contacts = []   # each item in here will be a dictionary


# ------------------------------------------------------------
# FILE FUNCTIONS
# ------------------------------------------------------------

def load_contacts():
    """
    Reads contacts from the JSON file into our 'contacts' list.
    Runs once when the program starts.

    'global contacts' tells Python we want to replace the list
    defined at the top of the file, not create a local variable.

    try/except catches errors so the program doesn't crash when
    the file doesn't exist yet (first run).
    """
    global contacts
    try:
        with open(CONTACTS_FILE, "r") as f:
            # json.load() reads the file and converts JSON → Python
            # The result is our list of dictionaries, ready to use
            contacts = json.load(f)
        print(f"  Loaded {len(contacts)} contact(s) from {CONTACTS_FILE}")
    except FileNotFoundError:
        # This is fine — it just means no contacts have been saved yet
        contacts = []
        print("  No save file found — starting with empty contact list.")


def save_contacts():
    """
    Writes the current 'contacts' list to the JSON file.
    Called after every add or delete so data is never lost.

    "w" mode creates the file if it doesn't exist, or
    overwrites it if it does — we always want the full list.

    indent=2 makes the JSON file human-readable (pretty-printed).
    """
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)
        # json.dump() converts Python → JSON and writes to the file


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def add_contact(name, phone, email):
    """
    Creates a new contact dictionary and appends it to the list.

    A dictionary is written with curly braces: {}
    Each entry is a key: value pair, separated by commas.
    Keys are strings (in quotes). Values can be anything.
    """
    contact = {
        "name":  name,
        "phone": phone,
        "email": email,
    }
    contacts.append(contact)   # .append() adds an item to the end of a list
    save_contacts()            # immediately persist to disk
    print(f"  Contact '{name}' added.")


def list_contacts():
    """
    Loops through every contact and prints it.

    enumerate() gives us both the position number AND the item
    at the same time — handy for numbered lists.
    """
    if len(contacts) == 0:     # len() counts items in a list
        print("  No contacts yet.")
        return

    print(f"  {'#':<4} {'Name':<20} {'Phone':<15} {'Email'}")
    print(f"  {'-'*4} {'-'*20} {'-'*15} {'-'*25}")

    for index, contact in enumerate(contacts):
        # enumerate() gives us: index=0,1,2... and contact=each dict
        # contact["name"] looks up the value stored under the key "name"
        num    = index + 1             # start numbering from 1, not 0
        name   = contact["name"]
        phone  = contact["phone"]
        email  = contact["email"]
        print(f"  {num:<4} {name:<20} {phone:<15} {email}")
        #       ^ The :<20 means: left-align and pad to 20 characters wide


def search_contacts(query):
    """
    Searches for contacts whose name contains the query string.

    .lower() converts to lowercase so the search isn't case-sensitive.
    'in' checks whether one string appears inside another:
        "ali" in "Alice"  → True
    """
    query = query.lower()
    found = []   # we'll collect matching contacts in a new list

    for contact in contacts:
        if query in contact["name"].lower():
            found.append(contact)

    if len(found) == 0:
        print(f"  No contacts matching '{query}'.")
    else:
        print(f"  Found {len(found)} match(es):")
        for contact in found:
            print(f"    {contact['name']}  |  {contact['phone']}  |  {contact['email']}")


def delete_contact(name_to_delete):
    """
    Removes the first contact whose name matches (case-insensitive).

    We loop through the list, find the right dictionary,
    then use .remove() to take it out of the list.
    """
    name_lower = name_to_delete.lower()

    for contact in contacts:
        if contact["name"].lower() == name_lower:
            contacts.remove(contact)   # .remove() deletes this exact item
            save_contacts()            # immediately persist to disk
            print(f"  Deleted '{contact['name']}'.")
            return   # stop after deleting the first match

    print(f"  No contact named '{name_to_delete}' found.")


# ------------------------------------------------------------
# MAIN PROGRAM LOOP
# ------------------------------------------------------------

print("=== Contact Book ===")
load_contacts()   # read saved data before showing the menu
print("Commands: add | list | search | delete | quit")
print()

while True:
    command = input("Command: ").strip().lower()
    # .strip() removes accidental spaces around the input
    # .lower() makes 'ADD' and 'Add' work the same as 'add'

    if command == "quit" or command == "q":
        break

    elif command == "add":
        name  = input("  Name:  ").strip()
        phone = input("  Phone: ").strip()
        email = input("  Email: ").strip()
        add_contact(name, phone, email)

    elif command == "list":
        list_contacts()

    elif command == "search":
        query = input("  Search name: ").strip()
        search_contacts(query)

    elif command == "delete":
        name = input("  Delete name: ").strip()
        delete_contact(name)

    else:
        print(f"  Unknown command '{command}'. Try: add | list | search | delete | quit")

    print()   # blank line between interactions

print("Goodbye!")
