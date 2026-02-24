# ============================================================
# Contact Book — Session 1.2
# Concepts used: lists, dictionaries, for loops, f-strings,
#                enumerate(), .lower(), in operator
# ============================================================


# ------------------------------------------------------------
# THE DATA STORE
# ------------------------------------------------------------
# A list is written with square brackets: []
# This starts empty — we'll add contacts as the program runs.
# In VBA terms: think of this as a dynamic array of records.

contacts = []   # each item in here will be a dictionary


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
            print(f"  Deleted '{contact['name']}'.")
            return   # stop after deleting the first match

    print(f"  No contact named '{name_to_delete}' found.")


# ------------------------------------------------------------
# MAIN PROGRAM LOOP
# ------------------------------------------------------------

print("=== Contact Book ===")
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
