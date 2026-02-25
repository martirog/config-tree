# config-tree

> **Disclaimer:** This is a proof of concept. It is not intended for production use.

A Python library for executing config files as programs and building tree structures from the results.

Config files are plain Python scripts executed in a pre-loaded environment. Before execution, command modules from one or more `commands/` directories are imported into the namespace, giving config files access to helper functions for building a node tree.

## Installation

```bash
pip install .
```

## Quick start

```python
from config_tree.executor import read_config

root = read_config("/path/to/config.py")
```

`read_config` returns a `TOP_NODE` populated with any nodes created during execution.

## Key concepts

- **Config files** — plain Python scripts executed with a pre-loaded environment
- **Commands** — Python modules loaded from `commands/` directories and available in config files as `module.function(...)`
- **Nodes** — tree nodes with a name, type, children, and attributes, built up by commands during execution
- **Traversal** — depth-first tree walking with a listener interface

## Modules

| Module | Description |
|---|---|
| `config_tree.executor` | `read_config` and `execute_config` — execute config files and build the tree |
| `config_tree.node` | `Node` — base tree node class |
| `config_tree.traverse` | `traverse` — depth-first tree traversal with a listener |
| `config_tree.listener` | `Listener` — abstract base class for traversal listeners |
| `config_tree.help` | `print_help` — print help text from command module docstrings |

## Built-in commands

| Command | Description |
|---|---|
| `add.file(path, type, attributes)` | Create a node from a file path and attach it to the tree |
| `include.config(path)` | Execute a nested config file as a subtree |

## Built-in namespace variables

| Variable | Description |
|---|---|
| `CONFIG_DIR` | Absolute path to the directory containing the config file |
| `PARENT_NODE` | The node that child nodes will be attached to |

## Documentation

See [USERGUIDE.md](USERGUIDE.md) for full documentation.
