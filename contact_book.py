# ============================================================
# Contact Book — Session 1.4
# Concepts used: all from 1.3, plus:
#   - main() function pattern
#   - if __name__ == "__main__":
#   - return values instead of global variables
#   - helper functions to avoid repeated code
# ============================================================

import json

CONTACTS_FILE = "contacts.json"


# ------------------------------------------------------------
# FILE FUNCTIONS
# ------------------------------------------------------------

def load_contacts():
    """
    Reads contacts from the JSON file and RETURNS them as a list.

    Previously we used 'global contacts' to modify an outside variable.
    Now we simply return the data — the caller decides what to do with it.

    Return value: a list of contact dictionaries (may be empty).
    """
    try:
        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)
        print(f"  Loaded {len(contacts)} contact(s) from {CONTACTS_FILE}")
        return contacts               # ← hand the list back to the caller
    except FileNotFoundError:
        print("  No save file found — starting with empty contact list.")
        return []                     # ← return an empty list (not None)


def save_contacts(contacts):
    """
    Writes the contacts list to the JSON file.

    Previously this reached for the global 'contacts'.
    Now we receive it as a parameter — cleaner and more explicit.

    Parameter: contacts — the list of contact dictionaries to save.
    """
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def print_contact_row(contact):
    """
    Prints a single contact as a formatted row.

    This is a NEW helper we didn't have before.
    Previously, list_contacts() and search_contacts() both had
    their own print logic — slightly different, and duplicated.

    Rule of thumb: if you write the same thing twice, make it a function.

    Parameter: contact — one contact dictionary.
    """
    name  = contact["name"]
    phone = contact["phone"]
    email = contact["email"]
    print(f"    {name:<20} {phone:<15} {email}")


def print_contact_table(contact_list):
    """
    Prints a header row then calls print_contact_row() for each contact.

    Parameter: contact_list — a list of contact dictionaries.
    """
    print(f"  {'Name':<20} {'Phone':<15} {'Email'}")
    print(f"  {'-'*20} {'-'*15} {'-'*25}")
    for contact in contact_list:
        print_contact_row(contact)


# ------------------------------------------------------------
# CONTACT FUNCTIONS
# (each receives 'contacts', does its job, returns updated list)
# ------------------------------------------------------------

def add_contact(contacts, name, phone, email):
    """
    Creates a new contact dictionary and adds it to the list.

    Parameters:
        contacts — the current list (we'll add to it)
        name, phone, email — the new contact's details

    Return value: the updated contacts list.

    Notice the pattern:
      1. Receive contacts as input
      2. Modify it
      3. Save to disk
      4. Return it
    This replaces the old 'global contacts' approach.
    """
    contact = {
        "name":  name,
        "phone": phone,
        "email": email,
    }
    contacts.append(contact)
    save_contacts(contacts)
    print(f"  Contact '{name}' added.")
    return contacts                   # ← hand back the updated list


def list_contacts(contacts):
    """
    Prints all contacts in a table.

    Parameter: contacts — the list to display.
    No return value needed — this function only displays, never modifies.
    """
    if len(contacts) == 0:
        print("  No contacts yet.")
        return

    print(f"  {len(contacts)} contact(s):")
    print_contact_table(contacts)     # ← delegates to our helper


def search_contacts(contacts, query):
    """
    Searches for contacts whose name contains the query string.

    Parameters:
        contacts — the list to search
        query    — the string to look for

    No return value — this function only displays results.
    """
    query = query.lower()
    found = [c for c in contacts if query in c["name"].lower()]
    # ↑ This is called a "list comprehension" — a compact way to
    #   filter a list. It means: "give me every c in contacts where
    #   the query appears in the name."
    #   It's equivalent to the for-loop + append pattern from last session.

    if len(found) == 0:
        print(f"  No contacts matching '{query}'.")
    else:
        print(f"  Found {len(found)} match(es):")
        print_contact_table(found)    # ← same helper, different data


def delete_contact(contacts, name_to_delete):
    """
    Removes the first contact whose name matches (case-insensitive).

    Parameters:
        contacts       — the current list
        name_to_delete — the name to look for

    Return value: the updated contacts list (with the contact removed).
    """
    name_lower = name_to_delete.lower()

    for contact in contacts:
        if contact["name"].lower() == name_lower:
            contacts.remove(contact)
            save_contacts(contacts)
            print(f"  Deleted '{contact['name']}'.")
            return contacts           # ← return the shortened list

    print(f"  No contact named '{name_to_delete}' found.")
    return contacts                   # ← return unchanged (nothing was deleted)


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------

def main():
    """
    The entry point of the program.

    All the startup code and the main loop now live here,
    instead of floating loose at the bottom of the file.

    'contacts' is a regular local variable inside main().
    We pass it into each function and get it back when needed.
    No global variables required.
    """
    print("=== Contact Book ===")

    contacts = load_contacts()        # load_contacts() now RETURNS the list

    print("Commands: add | list | search | delete | quit")
    print()

    while True:
        command = input("Command: ").strip().lower()

        if command in ("quit", "q"):
            break

        elif command == "add":
            name  = input("  Name:  ").strip()
            phone = input("  Phone: ").strip()
            email = input("  Email: ").strip()
            contacts = add_contact(contacts, name, phone, email)
            # ↑ We assign the return value back to 'contacts'
            #   so our local variable always has the latest version.

        elif command == "list":
            list_contacts(contacts)

        elif command == "search":
            query = input("  Search name: ").strip()
            search_contacts(contacts, query)

        elif command == "delete":
            name = input("  Delete name: ").strip()
            contacts = delete_contact(contacts, name)
            # ↑ Same pattern as add — reassign so we have the updated list.

        else:
            print(f"  Unknown command '{command}'. Try: add | list | search | delete | quit")

        print()

    print("Goodbye!")


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()

# What does this do?
#
# Every Python file has a built-in variable called __name__.
#
# When you RUN this file directly:
#   python contact_book.py
#   → Python sets __name__ to "__main__"
#   → the condition is True → main() runs
#
# When another file IMPORTS this file:
#   import contact_book
#   → Python sets __name__ to "contact_book"
#   → the condition is False → main() does NOT run
#
# This means our functions (add_contact, search_contacts, etc.)
# can be safely imported and reused by other programs — without
# accidentally launching the interactive loop.
# That will matter a lot when we start building AI agents.
