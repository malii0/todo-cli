# To-Do List CLI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://camo.githubusercontent.com/eaa7fd024f419ac84bc627229cb7db7fa962c98447531e7002468f00d569b491/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d332e382532422d626c75653f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e) [![Rich](https://img.shields.io/badge/rich-4.0.0%2B-brightgreen?style=for-the-badge)](https://camo.githubusercontent.com/9f43600b912a0a5c9c4d6f15337a594762204e8e9bf8ad6500a8f70ba60eaf52/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f726963682d342e302e302532422d627269676874677265656e3f7374796c653d666f722d7468652d6261646765) [![GitHub](https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=github)](https://github.com/malii0/todo-cli)

A lightweight command-line to-do list app that runs entirely in your terminal. Output is formatted with the `rich` library, and tasks are saved to `todo_list.json` so they persist between sessions.

## Features

- Add, remove, or complete multiple tasks with a single command
- Tasks stored locally in JSON
- Table view showing task ID, status, creation date, and completion date
- Filter or search by completion status or keyword
- Quickly duplicate an existing task
- Command-line interface built on `argparse`

## Installation

Clone the repository:

```
git clone https://github.com/malii0/todo-cli.git
cd todo-cli
```

Install the required library:

```
pip install rich
```

## Usage

Run `python todo.py --help` to see all available commands.

```
python todo.py --help
```

### Examples

**Add tasks**

```
python todo.py --add "Buy groceries"
python todo.py --add "Read a book" "Do some exercise"
```

**List tasks**

```
python todo.py --list
```

**List by status**

```
python todo.py --list-completed
python todo.py --list-pending
```

**Search**

```
python todo.py --search "milk"
```

**Complete tasks**

```
python todo.py --complete 1
python todo.py --complete 2 4
```

**Mark as pending**

```
python todo.py --pending 3
```

**Remove tasks**

```
python todo.py --remove 3
```

**Rename a task**

```
python todo.py --update 2 "Read a new science fiction novel"
```

**Duplicate a task**

```
python todo.py --repeat 6 3
```

**Bulk actions**

```
python todo.py --remove-all
python todo.py --complete-all
python todo.py --pending-all
```

## Contributing

Found a bug or have an idea for a feature? Open an issue or submit a pull request.

## License

MIT License. See [LICENSE](https://github.com/malii0/todo-cli/blob/main/LICENSE) for details.
