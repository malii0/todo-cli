import argparse
import json
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()
DATA_FILE = "todo_list.json"


def valid_positive_integer(value):
    """Checks if the value is a positive integer."""
    try:
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(
                f"Value must be a positive integer, got {value}"
            )
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Value must be an integer, got {value}")


def get_parser():
    """Creates and returns the argument parser."""
    parser = argparse.ArgumentParser(
        description="To-do List Manager", epilog="Use one command at a time."
    )

    list_group = parser.add_mutually_exclusive_group()
    list_group.add_argument("--list", action="store_true", help="Lists all tasks")
    list_group.add_argument(
        "--list-completed", action="store_true", help="Lists only completed tasks"
    )
    list_group.add_argument(
        "--list-pending", action="store_true", help="Lists only pending tasks"
    )
    list_group.add_argument(
        "--search", metavar="TERM", help="Searches for tasks containing a specific term"
    )

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--add", nargs="+", metavar="TASK_NAME", help="Adds one or more new tasks"
    )
    action_group.add_argument(
        "--remove",
        nargs="+",
        metavar="TASK_ID",
        type=int,
        help="Removes tasks by one or more IDs",
    )
    action_group.add_argument(
        "--remove-all", action="store_true", help="Removes all tasks from the list"
    )
    action_group.add_argument(
        "--complete",
        nargs="+",
        metavar="TASK_ID",
        type=int,
        help="Marks tasks as completed by one or more IDs",
    )
    action_group.add_argument(
        "--complete-all", action="store_true", help="Marks all tasks as completed"
    )
    action_group.add_argument(
        "--pending",
        nargs="+",
        metavar="TASK_ID",
        type=int,
        help="Marks tasks as pending by one or more IDs",
    )
    action_group.add_argument(
        "--pending-all", action="store_true", help="Marks all tasks as pending"
    )
    action_group.add_argument(
        "--update",
        nargs=2,
        metavar=("TASK_ID", "NEW_NAME"),
        help="Updates a task's name by its ID",
    )
    action_group.add_argument(
        "--repeat",
        nargs=2,
        metavar=("TASK_ID", "COUNT"),
        help="Repeats a task a given number of times",
    )

    return parser


def load_todos():
    """Loads the to-do list from a JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_todos(todos):
    """Saves the to-do list to a JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def find_todo_by_id(todos, todo_id):
    """Finds a todo item with the specified ID."""
    return next((todo for todo in todos if todo["id"] == todo_id), None)


def list_todos(todos, filter_status=None, search_term=None):
    """Lists to-do items based on filters and search term."""
    if not todos:
        console.print("[bold yellow]To-do list is empty.[/bold yellow]")
        return

    filtered_todos = todos
    if filter_status == "completed":
        filtered_todos = [todo for todo in filtered_todos if todo["done"]]
    elif filter_status == "pending":
        filtered_todos = [todo for todo in filtered_todos if not todo["done"]]

    if search_term:
        search_term = search_term.lower()
        filtered_todos = [
            todo for todo in filtered_todos if search_term in todo["task"].lower()
        ]

    if not filtered_todos:
        console.print(
            f"[bold yellow]No tasks found for the given criteria.[/bold yellow]"
        )
        return

    table = Table()
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Created At", style="blue")
    table.add_column("Completed At", style="yellow")
    for todo in filtered_todos:
        status_text = (
            Text("Completed", style="bold green")
            if todo["done"]
            else Text("Pending", style="bold red")
        )
        completed_at_text = todo.get("completed_at", "") if todo["done"] else ""
        table.add_row(
            str(todo["id"]),
            todo["task"],
            status_text,
            todo["created_at"],
            completed_at_text,
        )
    console.print(table)


def add_todos(todos, new_tasks):
    """Adds one or more new tasks to the list, handling duplicate names."""
    for new_task_name in new_tasks:
        original_task_name = new_task_name
        task_name_to_add = new_task_name
        counter = 1

        while any(todo["task"] == task_name_to_add for todo in todos):
            task_name_to_add = f"{original_task_name} ({counter})"
            counter += 1

        new_id = max((todo["id"] for todo in todos), default=0) + 1
        new_todo = {
            "id": new_id,
            "task": task_name_to_add,
            "done": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None,
        }
        todos.append(new_todo)
        console.print(f'[bold green]Added task:[/bold green] "{task_name_to_add}"')


def repeat_task(todos, todo_id, repeat_count):
    """Repeats a specified task a given number of times."""
    original_todo = find_todo_by_id(todos, todo_id)
    if not original_todo:
        console.print(f"[bold red]Task with ID {todo_id} not found.[/bold red]")
        return False

    tasks_to_add = [original_todo["task"]] * repeat_count
    add_todos(todos, tasks_to_add)
    console.print(
        f'[bold green]Task "{original_todo["task"]}" repeated {repeat_count} times.[/bold green]'
    )
    return True


def remove_todo(todos, todo_id):
    """Removes a task by its ID."""
    todo_to_remove = find_todo_by_id(todos, todo_id)
    if todo_to_remove:
        todos.remove(todo_to_remove)
        console.print(
            f'[bold green]Removed task:[/bold green] "{todo_to_remove["task"]}"'
        )
        return True
    else:
        console.print(f"[bold red]Task with ID {todo_id} not found.[/bold red]")
        return False


def remove_all_todos(todos):
    """Removes all tasks from the list."""
    if not todos:
        console.print("[bold yellow]To-do list is already empty.[/bold yellow]")
        return False

    del todos[:]
    console.print("[bold green]All tasks have been removed.[/bold green]")
    return True


def complete_todo(todos, todo_id):
    """Marks a task as completed by its ID."""
    todo_to_update = find_todo_by_id(todos, todo_id)
    if todo_to_update:
        if not todo_to_update["done"]:
            todo_to_update["done"] = True
            todo_to_update["completed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            console.print(
                f'[bold green]Task "{todo_to_update["task"]}" marked as completed.[/bold green]'
            )
        else:
            console.print(
                f'[bold yellow]Task "{todo_to_update["task"]}" is already completed.[/bold yellow]'
            )
        return True
    else:
        console.print(f"[bold red]Task with ID {todo_id} not found.[/bold red]")
        return False


def complete_all_todos(todos):
    """Marks all tasks as completed."""
    if not todos:
        console.print(
            "[bold yellow]To-do list is empty. No tasks to complete.[/bold yellow]"
        )
        return False

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for todo in todos:
        if not todo["done"]:
            todo["done"] = True
            todo["completed_at"] = now
    console.print("[bold green]All tasks have been marked as completed.[/bold green]")
    return True


def pending_todo(todos, todo_id):
    """Marks a task as pending by its ID."""
    todo_to_update = find_todo_by_id(todos, todo_id)
    if todo_to_update:
        if todo_to_update["done"]:
            todo_to_update["done"] = False
            todo_to_update["completed_at"] = None
            console.print(
                f'[bold green]Task "{todo_to_update["task"]}" marked as pending.[/bold green]'
            )
        else:
            console.print(
                f'[bold yellow]Task "{todo_to_update["task"]}" is already pending.[/bold yellow]'
            )
        return True
    else:
        console.print(f"[bold red]Task with ID {todo_id} not found.[/bold red]")
        return False


def pending_all_todos(todos):
    """Marks all tasks as pending."""
    if not todos:
        console.print(
            "[bold yellow]To-do list is empty. No tasks to mark as pending.[/bold yellow]"
        )
        return False

    for todo in todos:
        todo["done"] = False
        todo["completed_at"] = None
    console.print("[bold green]All tasks have been marked as pending.[/bold green]")
    return True


def update_todo(todos, todo_id, new_name):
    """Updates a task's name by its ID."""
    todo_to_update = find_todo_by_id(todos, todo_id)
    if todo_to_update:
        old_name = todo_to_update["task"]
        todo_to_update["task"] = new_name
        console.print(
            f'[bold green]Task name updated from "{old_name}" to "{new_name}".[/bold green]'
        )
        return True
    else:
        console.print(f"[bold red]Task with ID {todo_id} not found.[/bold red]")
        return False


def main():
    """Main function of the application."""
    parser = get_parser()
    args = parser.parse_args()
    todos = load_todos()

    action_taken = False

    if args.list:
        list_todos(todos)
    elif args.list_completed:
        list_todos(todos, filter_status="completed")
    elif args.list_pending:
        list_todos(todos, filter_status="pending")
    elif args.search:
        list_todos(todos, search_term=args.search)
    elif args.add:
        add_todos(todos, args.add)
        save_todos(todos)
        action_taken = True
    elif args.remove is not None:
        for todo_id in args.remove:
            action_taken = remove_todo(todos, todo_id) or action_taken
        save_todos(todos)
    elif args.remove_all:
        action_taken = remove_all_todos(todos)
        save_todos(todos)
    elif args.complete is not None:
        for todo_id in args.complete:
            action_taken = complete_todo(todos, todo_id) or action_taken
        save_todos(todos)
    elif args.complete_all:
        action_taken = complete_all_todos(todos)
        save_todos(todos)
    elif args.pending is not None:
        for todo_id in args.pending:
            action_taken = pending_todo(todos, todo_id) or action_taken
        save_todos(todos)
    elif args.pending_all:
        action_taken = pending_all_todos(todos)
        save_todos(todos)
    elif args.update:
        try:
            todo_id = valid_positive_integer(args.update[0])
            new_name = args.update[1]
            action_taken = update_todo(todos, todo_id, new_name)
            save_todos(todos)
        except argparse.ArgumentTypeError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
    elif args.repeat:
        try:
            todo_id = valid_positive_integer(args.repeat[0])
            count = valid_positive_integer(args.repeat[1])
            action_taken = repeat_task(todos, todo_id, count)
            save_todos(todos)
        except argparse.ArgumentTypeError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
    else:
        parser.print_help()

    if action_taken:
        console.print("\n[bold]Updated List:[/bold]")
        list_todos(todos)


if __name__ == "__main__":
    main()
