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

You can optionally pass a `Node` instance that will be available as `PARENT_NODE` in the config file:

```python
from config_tree.executor import execute_config
from config_tree.node import Node

root = Node("root", type="container")
result = execute_config("/path/to/my_config.py", node=root)
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

| Variable     | Type         | Description                                      |
|--------------|--------------|--------------------------------------------------|
| `CONFIG_DIR` | str          | Absolute path to the directory containing the config file |
| `PARENT_NODE`| Node or None | The node passed to `execute_config`, or `None` if not provided. Also injected into each command module's namespace. |

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

## Node class

Config Tree provides a `Node` class for building tree structures.

```python
from config_tree.node import Node
```

### Creating nodes

```python
root = Node("root", type="container")
```

| Parameter    | Type   | Default | Description              |
|--------------|--------|---------|--------------------------|
| `name`       | str    | required| The name of the node     |
| `type`       | str    | `None`  | The type of the node     |
| `children`   | list   | `[]`    | Initial list of child nodes |
| `attributes` | list   | `[]`    | Initial list of attributes  |

### Adding children

```python
root = Node("root")
child = root.add_child(Node("child", type="leaf"))
```

`add_child` appends the child and returns it, so you can chain or capture the reference.

### Adding attributes

```python
node = Node("server", type="host")
node.add_attribute("ip_address")
node.add_attribute("port")
```

### Building a tree

```python
root = Node("datacenter", type="dc")
rack = root.add_child(Node("rack-1", type="rack"))
server = rack.add_child(Node("web-01", type="host"))
server.add_attribute("ip_address")
server.add_attribute("port")
```

## Built-in commands

### add.file

Creates a `Node` instance from a file path and adds it as a child of `PARENT_NODE`.

```python
from config_tree.commands.add import file

node = file("/path/to/config.txt", type="config", attributes=["readonly"])
```

| Parameter    | Type       | Default | Description                      |
|--------------|------------|---------|----------------------------------|
| `path`       | str        | required| The file path, used as the node name |
| `type`       | str        | `None`  | The type of the node             |
| `attributes` | list       | `[]`    | List of attributes for the node  |

Returns a `Node` with `name` set to the full path string. The node is automatically added as a child of `PARENT_NODE`.

**Example in a config file:**

When `add.py` is placed in the `commands/` directory, the `file` function is available directly:

```python
config = file("/etc/app/config.yaml", type="config", attributes=["readonly", "required"])
schema = file("/etc/app/schema.json", type="schema")
# Both nodes are now children of PARENT_NODE
```

## Notes

- If the `commands/` directory does not exist, the config file runs without any preloaded commands.
- If the config file does not exist, a `FileNotFoundError` is raised.
- Names starting with `_` in command modules are treated as private and are not exported.
