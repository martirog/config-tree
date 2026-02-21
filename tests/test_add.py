from config_tree.commands.add import file
from config_tree.node import Node


def test_file_returns_node():
    node = file("/path/to/config.txt")
    assert isinstance(node, Node)


def test_file_sets_name_from_path():
    node = file("/path/to/config.txt")
    assert node.name == "/path/to/config.txt"


def test_file_with_type():
    node = file("/path/to/config.txt", type="config")
    assert node.type == "config"


def test_file_type_defaults_to_none():
    node = file("/path/to/config.txt")
    assert node.type is None


def test_file_with_attributes():
    node = file("/path/to/config.txt", attributes=["read", "write"])
    assert node.attributes == ["read", "write"]


def test_file_attributes_defaults_to_empty():
    node = file("/path/to/config.txt")
    assert node.attributes == []


def test_file_with_all_args():
    node = file("/etc/hosts", type="system", attributes=["readonly"])
    assert node.name == "/etc/hosts"
    assert node.type == "system"
    assert node.attributes == ["readonly"]
    assert node.children == []
