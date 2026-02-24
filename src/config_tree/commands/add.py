"""Commands for adding nodes to the config tree."""

from config_tree.node import Node


def file(path, type=None, attributes=None):
    """Create a node from a file path and add it as a child of PARENT_NODE.

    Args:
        path: Path to the file. Used as the node name.
        type: Optional type for the node.
        attributes: Optional list of attributes for the node.

    Returns:
        The created Node.
    """
    node = Node(name=str(path), type=type, attributes=attributes or [])
    PARENT_NODE.add_child(node)
    return node
