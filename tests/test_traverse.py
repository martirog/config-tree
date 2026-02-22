from config_tree.node import Node
from config_tree.traverse import traverse


class RecordingListener:
    def __init__(self):
        self.actions = []
        self.entries = []
        self.exits = []

    def action(self, node):
        self.actions.append(node.name)
        return node

    def entry(self, node):
        self.entries.append(node.name)

    def exit(self, node):
        self.exits.append(node.name)


def test_action_called_with_node():
    listener = RecordingListener()
    node = Node("root")
    traverse(node, listener)
    assert listener.actions == ["root"]


def test_entry_called_with_node():
    listener = RecordingListener()
    node = Node("root")
    traverse(node, listener)
    assert listener.entries == ["root"]


def test_exit_called_with_node():
    listener = RecordingListener()
    node = Node("root")
    traverse(node, listener)
    assert listener.exits == ["root"]


def test_action_return_value_is_used():
    replacement = Node("replaced")

    class ReplacingListener:
        def action(self, node):
            return replacement

        def entry(self, node):
            self.entry_node = node

        def exit(self, node):
            self.exit_node = node

    listener = ReplacingListener()
    traverse(Node("original"), listener)
    assert listener.entry_node is replacement
    assert listener.exit_node is replacement


def test_children_are_traversed():
    listener = RecordingListener()
    root = Node("root")
    root.add_child(Node("child1"))
    root.add_child(Node("child2"))
    traverse(root, listener)
    assert listener.entries == ["root", "child1", "child2"]


def test_order_is_entry_children_exit():
    order = []

    class OrderListener:
        def action(self, node):
            return node

        def entry(self, node):
            order.append(("entry", node.name))

        def exit(self, node):
            order.append(("exit", node.name))

    root = Node("root")
    root.add_child(Node("child"))
    traverse(root, OrderListener())
    assert order == [
        ("entry", "root"),
        ("entry", "child"),
        ("exit", "child"),
        ("exit", "root"),
    ]


def test_deep_tree_traversal():
    listener = RecordingListener()
    root = Node("root")
    child = root.add_child(Node("child"))
    child.add_child(Node("grandchild"))
    traverse(root, listener)
    assert listener.entries == ["root", "child", "grandchild"]
    assert listener.exits == ["grandchild", "child", "root"]


def test_leaf_node_no_children_traversed():
    listener = RecordingListener()
    traverse(Node("leaf"), listener)
    assert listener.entries == ["leaf"]
    assert listener.exits == ["leaf"]
