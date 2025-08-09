# To-Do List CLI 📋

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python) ![Rich](https://img.shields.io/badge/rich-4.0.0%2B-brightgreen?style=for-the-badge) ![GitHub](https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=github)

This project is a lightweight and stylish command-line to-do list application that you can easily manage through your terminal. It provides visually appealing and formatted output using the `rich` library. Your tasks are stored in a file named `todo_list.json`, ensuring your list persists across sessions.

## ✨ Features

* **Manage Multiple Tasks:** Add, remove, or complete multiple tasks with a single command.
* **Persistent Data:** All tasks are stored locally in JSON format.
* **Detailed List View:** Displays well-organized tables with task ID, status, creation date, and completion date.
* **Filtering and Searching:** List tasks that are completed, pending, or contain a specific keyword.
* **Repeating Tasks:** Quickly add multiple copies of an existing task.
* **Easy to Use:** Intuitive and straightforward command-line interface powered by the `argparse` library.

## ⚙️ Installation

To use this project, you first need to install the required library.

1.  Clone or download the repository:
    ```bash
    git clone [https://github.com/malii0/todo-cli.git](https://github.com/malii0/todo-cli.git)
    cd todo-cli
    ```
2.  Install the necessary Python library (`rich`):
    ```bash
    pip install rich
    ```

## 💻 Usage

The main command for the application is `python todo.py`. You can see all available commands and their arguments using the `--help` flag.

```bash
python todo.py --help
```

### 💡 Examples

#### Adding Tasks

Add one or more new tasks to your to-do list.

```bash
python todo.py --add "Buy groceries"
python todo.py --add "Read a book" "Do some exercise"
```

#### Listing Tasks

View all tasks in your to-do list.

```bash
python todo.py --list
```

#### Listing Tasks by Status

Show only the completed or pending tasks.

```bash
python todo.py --list-completed
python todo.py --list-pending
```

#### Searching Tasks

Find tasks that contain a specific term.

```bash
python todo.py --search "milk"
```

#### Completing Tasks

Mark one or more tasks as completed by their ID.

```bash
python todo.py --complete 1
python todo.py --complete 2 4
```

#### Marking Tasks as Pending

Mark one or more completed tasks as pending by their ID.

```bash
python todo.py --pending 3
```

#### Removing Tasks

Delete one or more tasks by their ID.

```bash
python todo.py --remove 3
```

#### Updating a Task Name

Change the name of a task by its ID.

```bash
python todo.py --update 2 "Read a new science fiction novel"
```

#### Repeating a Task

Add multiple copies of an existing task by its ID.

```bash
python todo.py --repeat 6 3
```

#### Removing or Completing All Tasks

Clear the entire to-do list or mark all tasks as completed.

```bash
python todo.py --remove-all
python todo.py --complete-all
python todo.py --pending-all
```

---

## 🤝 Contributing

Feel free to contribute to this project! If you find a bug or want to add a new feature, please open an issue or submit a pull request.
