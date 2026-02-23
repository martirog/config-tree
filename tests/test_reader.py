import tempfile
from pathlib import Path

from config_tree.executor import read_config
from config_tree.node import Node


def make_config_file(tmp_path, content=""):
    config_file = Path(tmp_path) / "config.py"
    config_file.write_text(content)
    return config_file


def test_read_config_returns_node():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = read_config(config_file)
        assert isinstance(node, Node)


def test_read_config_node_type_is_top_node():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = read_config(config_file)
        assert node.type == "TOP_NODE"


def test_read_config_node_name_is_path():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = read_config(config_file)
        assert node.name == str(config_file)


def test_read_config_executes_config_file():
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = Path(tmp) / "commands"
        cmd_dir.mkdir()
        (cmd_dir / "add.py").write_text(
            "from config_tree.node import Node\n"
            "def file(path):\n"
            "    child = Node(name=str(path))\n"
            "    PARENT_NODE.add_child(child)\n"
            "    return child\n"
        )
        config_file = make_config_file(tmp, content="add.file('child.txt')")
        node = read_config(config_file)
        assert len(node.children) == 1
        assert node.children[0].name == "child.txt"


def test_read_config_missing_file_raises():
    try:
        read_config("/nonexistent/path/config.py")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
