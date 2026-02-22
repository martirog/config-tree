from config_tree.executor import execute_config
from config_tree.node import Node


def config(path):
    node = Node(name=str(path), type="CONFIG_NODE")
    PARENT_NODE.add_child(node)
    execute_config(str(path), node=node)
    return node
