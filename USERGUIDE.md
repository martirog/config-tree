# Config Tree User Guide

Config Tree executes a Python config file with a pre-loaded environment. Before your config file runs, all Python modules in a sibling `commands/` directory are imported and their public names are made available in your config file's namespace.

## Installation

```bash
pip install .
```

## Usage

```python
from config_tree.executor import execute_config

result = execute_config("/path/to/my_config.py")
```

`execute_config` returns a dictionary containing the namespace after execution, including any variables or functions defined in the config file and the loaded commands.

## Directory structure

Place your config file and a `commands/` directory side by side:

```
my_project/
├── config.py
└── commands/
    ├── greet.py
    └── math_helpers.py
```

## Commands

Each `.py` file in the `commands/` directory is imported as a module. All public names (those not starting with `_`) are made available in your config file's namespace.

Command files are loaded in alphabetical order.

**commands/greet.py**
```python
def hello(name):
    return f"hello {name}"
```

**commands/math_helpers.py**
```python
def double(x):
    return x * 2
```

## Built-in variables

| Variable     | Type | Description                                      |
|--------------|------|--------------------------------------------------|
| `CONFIG_DIR` | str  | Absolute path to the directory containing the config file |

## Config file

Your config file is a regular Python file. It can use anything loaded from the `commands/` directory and the built-in variables.

**config.py**
```python
greeting = hello("world")
result = double(21)
print(f"Running from {CONFIG_DIR}")
```

## Accessing results

The namespace returned by `execute_config` contains everything defined during execution:

```python
ns = execute_config("my_project/config.py")
print(ns["greeting"])  # "hello world"
print(ns["result"])    # 42
```

## Notes

- If the `commands/` directory does not exist, the config file runs without any preloaded commands.
- If the config file does not exist, a `FileNotFoundError` is raised.
- Names starting with `_` in command modules are treated as private and are not exported.
