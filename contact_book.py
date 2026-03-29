# ============================================================
# Contact Book — Session 1.6
# Concepts used: all from previous sessions, plus:
#   - argparse: reading arguments from the command line
#   - subcommands: add / list / search / delete as CLI verbs
#   - positional arguments: required values identified by position
# ============================================================

import json
import argparse

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
        return contacts
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: contacts.json is corrupted. Starting fresh.")
        return []


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

    Raises ValueError if any field is empty.
    'raise' is how a function says "something is wrong — I refuse to
    continue." The caller catches it and decides what to show the user.
    """
    # Validate inputs before doing anything
    if not name:
        raise ValueError("Name cannot be empty.")
    if not phone:
        raise ValueError("Phone cannot be empty.")
    if not email:
        raise ValueError("Email cannot be empty.")
    # 'not name' is True when name is an empty string "", None, or whitespace
    # after .strip() — all of those mean "the user gave us nothing useful"

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
    Parses command-line arguments and calls the right function.

    argparse replaces the old while True / input() loop entirely.
    The user now passes everything on the command line when launching
    the script — no interactive prompts needed.
    """

    # Step 1: Create the top-level parser.
    # 'description' is what appears at the top of --help output.
    parser = argparse.ArgumentParser(
        prog="contact_book",
        description="Manage your contacts from the command line.",
    )

    # Step 2: Create a subparsers object.
    # This is what enables subcommands like: contact_book.py add ...
    # 'dest="command"' means the chosen subcommand will be stored
    # in args.command so we can check it later.
    # 'metavar="command"' controls how it looks in --help output.
    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.required = True   # print help (not a cryptic error) if no command given

    # Step 3: Register each subcommand and its arguments.
    #
    # add_parser() creates a new sub-parser for that subcommand.
    # add_argument() defines a positional argument for that subcommand.
    # Positional = required, no flag prefix, matched by order.
    #
    # Usage: python3 contact_book.py add "John Smith" "555-1234" "j@email.com"
    p_add = subparsers.add_parser("add", help="Add a new contact")
    p_add.add_argument("name",  help="Contact's full name (use quotes for spaces)")
    p_add.add_argument("phone", help="Phone number")
    p_add.add_argument("email", help="Email address")

    # Usage: python3 contact_book.py list
    subparsers.add_parser("list", help="List all contacts")

    # Usage: python3 contact_book.py search john
    p_search = subparsers.add_parser("search", help="Search contacts by name")
    p_search.add_argument("query", help="Name (or part of a name) to search for")

    # Usage: python3 contact_book.py delete "John Smith"
    p_delete = subparsers.add_parser("delete", help="Delete a contact by name")
    p_delete.add_argument("name", help="Exact name of the contact to delete")

    # Step 4: Parse the arguments.
    # parse_args() reads sys.argv (the actual command-line words),
    # matches them against our definitions above, and returns a
    # Namespace object — basically a bundle of named values.
    #
    # After this line:
    #   args.command → "add", "list", "search", or "delete"
    #   args.name    → the name string (for add/delete)
    #   args.phone   → the phone string (for add)
    #   args.email   → the email string (for add)
    #   args.query   → the search string (for search)
    args = parser.parse_args()

    # Step 5: Load contacts then dispatch to the right function.
    contacts = load_contacts()

    if args.command == "add":
        try:
            add_contact(contacts, args.name, args.phone, args.email)
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        list_contacts(contacts)

    elif args.command == "search":
        search_contacts(contacts, args.query)

    elif args.command == "delete":
        delete_contact(contacts, args.name)


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
