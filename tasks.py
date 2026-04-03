# ============================================================
# Task Manager — Session 1.7
# Concepts used: all from previous sessions, plus:
#   - auto-generated IDs: giving each record a unique number
#   - optional CLI flags: --priority high
#   - updating records: changing a field in an existing item
#   - datetime: getting today's date from Python
# ============================================================

import json
import argparse
from datetime import date   # ← NEW: lets us get today's date

TASKS_FILE = "tasks.json"


# ------------------------------------------------------------
# FILE FUNCTIONS  (identical pattern to contact_book.py)
# ------------------------------------------------------------

def load_tasks():
    """
    Reads tasks from the JSON file and returns them as a list.
    Returns an empty list if the file doesn't exist yet.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted. Starting fresh.")
        return []


def save_tasks(tasks):
    """
    Writes the tasks list to the JSON file.
    Parameter: tasks — the list of task dictionaries to save.
    """
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# ------------------------------------------------------------
# TASK FUNCTIONS  (we'll fill these in one by one)
# ------------------------------------------------------------

def add_task(tasks, title, priority):
    """
    Creates a new task and adds it to the list.

    Parameters:
        tasks    — the current list of task dictionaries
        title    — the task description (e.g. "Buy groceries")
        priority — "normal" or "high"

    NEW CONCEPT — auto-generated ID:
        We look at all existing IDs, take the highest one, and add 1.
        If there are no tasks yet, we start at 1.
    """
    if not title:
        raise ValueError("Task title cannot be empty.")

    # Generate the next ID
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = max(t["id"] for t in tasks) + 1
        # ↑ 'max(... for t in tasks)' is a generator expression —
        #   like a list comprehension, but it feeds values into max()
        #   without building a whole list first.
        #   Think of it as: "find the highest id value among all tasks."

    task = {
        "id":       new_id,
        "title":    title,
        "status":   "todo",              # all tasks start as todo
        "priority": priority,
        "created":  str(date.today()),   # e.g. "2026-04-03"
        # ↑ date.today() returns a date object; str() converts it to a string
        #   so JSON can store it (JSON doesn't understand date objects).
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"  Added task #{new_id}: {title}  [{priority} priority]")
    return tasks


def list_tasks(tasks, show_done):
    """
    Prints tasks in a formatted table.

    Parameters:
        tasks     — the full list of task dictionaries
        show_done — True = show completed tasks, False = show pending tasks

    Uses a list comprehension to filter before displaying.
    """
    # Filter to just the tasks we want to show
    if show_done:
        filtered = [t for t in tasks if t["status"] == "done"]
        label = "Completed tasks"
    else:
        filtered = [t for t in tasks if t["status"] == "todo"]
        label = "Pending tasks"
    # ↑ Same pattern as search_contacts: build a smaller list from the big one.
    #   [t for t in tasks if <condition>] means:
    #   "give me every t in tasks where the condition is true."

    if len(filtered) == 0:
        print(f"  No {label.lower()}.")
        return

    print(f"\n  {label} ({len(filtered)}):")
    print(f"  {'ID':<5} {'Priority':<10} {'Created':<12} {'Title'}")
    print(f"  {'-'*5} {'-'*10} {'-'*12} {'-'*30}")

    for t in filtered:
        # Mark high-priority tasks with a star
        flag = "*" if t["priority"] == "high" else " "
        print(f"  {t['id']:<5} {t['priority']:<10} {t['created']:<12} {flag}{t['title']}")
    print()


def done_task(tasks, task_id):
    """
    Marks a task as done by finding it by ID and updating its status.

    Parameter:
        tasks   — the full list
        task_id — the integer ID of the task to mark done

    NEW CONCEPT — updating a record in place:
        We loop through the list. When we find the matching task,
        we change one of its fields directly. Because dictionaries
        are mutable (changeable), this edit sticks — we don't need
        to rebuild the whole list.
    """
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                print(f"  Task #{task_id} is already marked done.")
                return tasks

            task["status"] = "done"   # ← mutate (change) the field directly
            save_tasks(tasks)
            print(f"  Task #{task_id} marked as done: {task['title']}")
            return tasks

    # If we get here, no task had that ID
    print(f"  No task with ID #{task_id} found.")
    return tasks


def delete_task(tasks, task_id):
    """
    Removes a task by ID.

    Parameters:
        tasks   — the full list
        task_id — the integer ID of the task to remove

    Same find-and-remove pattern as delete_contact, but we search
    by numeric ID instead of by name string.
    """
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"  Deleted task #{task_id}: {task['title']}")
            return tasks

    print(f"  No task with ID #{task_id} found.")
    return tasks


# ------------------------------------------------------------
# MAIN FUNCTION  (we'll fill this in Stage 6)
# ------------------------------------------------------------

def main():
    """
    Parses command-line arguments and calls the right function.

    Subcommands:
        add    — add a new task (with optional --priority flag)
        list   — list tasks (with optional --done flag)
        done   — mark a task as done by ID
        delete — delete a task by ID
    """
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Manage your tasks from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.required = True

    # --- add ---
    # Usage: python3 tasks.py add "Buy groceries"
    # Usage: python3 tasks.py add "Write notes" --priority high
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument(
        "--priority",           # ← optional flag (note the -- prefix)
        choices=["normal", "high"],   # only these two values are allowed
        default="normal",       # if the user omits --priority, use "normal"
        help="Priority level (default: normal)",
    )
    # NEW CONCEPT — optional flags:
    #   Positional args: required, no prefix, matched by position
    #   Optional flags:  start with --, skippable, have a default value
    #   'choices' restricts the allowed values and gives a nice error message
    #   if the user passes something else.

    # --- list ---
    # Usage: python3 tasks.py list
    # Usage: python3 tasks.py list --done
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument(
        "--done",
        action="store_true",    # ← this flag stores True when present, False when absent
        help="Show completed tasks instead of pending",
    )
    # 'action="store_true"' means: no value needed after the flag.
    # If the user writes --done, args.done = True.
    # If they don't write --done, args.done = False.

    # --- done ---
    # Usage: python3 tasks.py done 3
    p_done = subparsers.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID to mark as done")
    # 'type=int' tells argparse to convert the argument from a string to
    # an integer automatically. Command-line input is always text;
    # type=int makes argparse do the conversion and give an error if it fails.

    # --- delete ---
    # Usage: python3 tasks.py delete 3
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()
    tasks = load_tasks()

    if args.command == "add":
        try:
            add_task(tasks, args.title, args.priority)
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        list_tasks(tasks, args.done)

    elif args.command == "done":
        done_task(tasks, args.id)

    elif args.command == "delete":
        delete_task(tasks, args.id)


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
