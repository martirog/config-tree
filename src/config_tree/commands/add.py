from config_tree.node import Node


def file(path, type=None, attributes=None):
    node = Node(name=str(path), type=type, attributes=attributes or [])
    return node
