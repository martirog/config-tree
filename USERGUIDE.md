# Config Tree User Guide

Config Tree executes a Python config file with a pre-loaded environment. Before your config file runs, all Python modules in a sibling `commands/` directory are imported and made available in your config file's namespace as modules.

## Installation

```bash
pip install .
```

## Usage

The simplest way to parse a config tree is with `read_config`:

```python
from config_tree.executor import read_config

root = read_config("/path/to/my_config.py")
```

`read_config` creates a `TOP_NODE`, executes the config file with it as `PARENT_NODE`, and returns the populated node. All nodes created by commands in the config file are attached as children.

### Low-level usage

For more control, use `execute_config` directly:

```python
from config_tree.executor import execute_config

ns = execute_config("/path/to/my_config.py")
```

You can optionally pass a `Node` instance that will be available as `PARENT_NODE` in the config file:

```python
from config_tree.executor import execute_config
from config_tree.node import Node

root = Node("root", type="container")
ns = execute_config("/path/to/my_config.py", node=root)
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

Each `.py` file in the `commands/` directory is imported as a module and available in the config file's namespace under the filename (without `.py`). You access its contents using `module.attribute` syntax.

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
greeting = greet.hello("world")
result = math_helpers.double(21)
print(f"Running from {CONFIG_DIR}")
```

## Accessing results

The namespace returned by `execute_config` contains everything defined during execution:

```python
ns = execute_config("my_project/config.py")
print(ns["greeting"])  # "hello world"
print(ns["result"])    # 42
print(ns["greet"])     # <module 'greet' from '...'>
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
node = add.file("/path/to/config.txt", type="config", attributes=["readonly"])
```

| Parameter    | Type       | Default | Description                      |
|--------------|------------|---------|----------------------------------|
| `path`       | str        | required| The file path, used as the node name |
| `type`       | str        | `None`  | The type of the node             |
| `attributes` | list       | `[]`    | List of attributes for the node  |

Returns a `Node` with `name` set to the full path string. The node is automatically added as a child of `PARENT_NODE`.

**Example in a config file:**

```python
config = add.file("/etc/app/config.yaml", type="config", attributes=["readonly", "required"])
schema = add.file("/etc/app/schema.json", type="schema")
# Both nodes are now children of PARENT_NODE
```

### include.config

Executes another config file as a nested node in the tree. Creates a new `Node` of type `"CONFIG_NODE"`, adds it as a child of `PARENT_NODE`, then runs the given config file with the new node as its `PARENT_NODE`.

```python
node = include.config("/path/to/other/config.py")
```

| Parameter | Type | Default  | Description                              |
|-----------|------|----------|------------------------------------------|
| `path`    | str  | required | Path to the config file to include       |

Returns the newly created `CONFIG_NODE`. Any nodes created inside the included config file will be attached as its children, enabling recursive tree building.

**Example:**

```
my_project/
├── root.py
├── commands/
│   ├── add.py
│   └── include.py
└── subsystem/
    └── config.py
```

**root.py**
```python
subsystem = include.config(CONFIG_DIR + "/subsystem/config.py")
```

**subsystem/config.py**
```python
add.file("/etc/app/config.yaml", type="config")
add.file("/etc/app/schema.json", type="schema")
```

The resulting tree will be:

```
PARENT_NODE
└── subsystem/config.py  (CONFIG_NODE)
    ├── /etc/app/config.yaml
    └── /etc/app/schema.json
```

## Traversing a tree

The `traverse` function walks a node tree depth-first, notifying a listener at each node.

```python
from config_tree.traverse import traverse

traverse(root_node, listener)
```

| Parameter  | Type   | Description                        |
|------------|--------|------------------------------------|
| `node`     | Node   | The root node to start from        |
| `listener` | object | An object with `action`, `entry`, and `exit` methods |

### Listener base class

Config Tree provides an abstract base class for listeners:

```python
from config_tree.listener import Listener

class MyListener(Listener):
    def entry(self, node):
        pass

    def exit(self, node):
        pass
```

`entry` and `exit` are abstract and must be implemented. `action` has a default implementation that returns the node unchanged — override it only if you need to transform or replace nodes. Attempting to instantiate a subclass with `entry` or `exit` missing will raise a `TypeError`.

### Listener interface

A listener must implement three methods:

| Method           | Abstract | Description                                                                 |
|------------------|----------|-----------------------------------------------------------------------------|
| `action(node)`   | No       | Called first for each node. The return value replaces the node for subsequent calls. Defaults to returning the node unchanged. |
| `entry(node)`    | Yes      | Called after `action`, before visiting children.                            |
| `exit(node)`     | Yes      | Called after all children have been visited.                                |

### Traversal order

For each node the order is:
1. `action(node)` — transform or replace the node
2. `entry(node)` — node is entered
3. Recurse into each child
4. `exit(node)` — node is exited

### Example

```python
from config_tree.listener import Listener
from config_tree.node import Node
from config_tree.traverse import traverse


class PrintListener(Listener):
    def __init__(self):
        self.depth = 0

    def entry(self, node):
        print("  " * self.depth + f"+ {node.name}")
        self.depth += 1

    def exit(self, node):
        self.depth -= 1


root = Node("root")
child = root.add_child(Node("child"))
child.add_child(Node("grandchild"))

traverse(root, PrintListener())
```

Output:
```
+ root
  + child
    + grandchild
```

## Help system

`print_help` inspects one or more command directories and prints formatted help to stdout, based on module and function docstrings.

```python
from config_tree.help import print_help

print_help(["path/to/commands"])
```

| Parameter      | Type | Description                              |
|----------------|------|------------------------------------------|
| `command_dirs` | list | List of directories to inspect           |

For each command file it prints:
- The module name as a heading (`# module_name`)
- The module docstring as a description
- Each public function as `module_name.function_name` followed by its docstring

**Example output:**

```
# add
Commands for adding nodes to the config tree.

add.file
Create a node from a file path and add it as a child of PARENT_NODE.
...

# include
Commands for including nested config files in the tree.

include.config
Execute a config file as a nested node and add it as a child of PARENT_NODE.
...
```

Files are processed in alphabetical order. `__init__.py`, private functions (starting with `_`), and imported functions are excluded.

## Notes

- If the `commands/` directory does not exist, the config file runs without any preloaded commands.
- If the config file does not exist, a `FileNotFoundError` is raised.
- Command modules are accessed by their filename (without `.py`) using `module.attribute` syntax.
