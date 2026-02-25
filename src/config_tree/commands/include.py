"""Commands for including nested config files in the tree."""

from config_tree.executor import execute_config
from config_tree.node import Node


def config(path):
    """Execute a config file as a nested node and add it as a child of PARENT_NODE.

    Creates a CONFIG_NODE, adds it as a child of PARENT_NODE, then executes
    the given config file with the new node as its PARENT_NODE, enabling
    recursive tree building.

    Args:
        path: Path to the config file to include.

    Returns:
        The created CONFIG_NODE with any child nodes attached by the included config.
    """
    node = Node(name=str(path), type="CONFIG_NODE")
    PARENT_NODE.add_child(node)
    execute_config(str(path), node=node, command_dirs=COMMAND_DIRS)
    return node
