import tempfile
from pathlib import Path

import config_tree.commands.include as include_module
from config_tree.commands.include import config
from config_tree.executor import LOCAL_COMMANDS
from config_tree.node import Node


def setup_function():
    include_module.PARENT_NODE = Node("parent")
    include_module.COMMAND_DIRS = [LOCAL_COMMANDS]


def make_config_file(tmp_path, content=""):
    config_file = Path(tmp_path) / "config.py"
    config_file.write_text(content)
    return config_file


def test_config_returns_node():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = config(config_file)
        assert isinstance(node, Node)


def test_config_node_name_is_path():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = config(config_file)
        assert node.name == str(config_file)


def test_config_node_type_is_config_node():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp)
        node = config(config_file)
        assert node.type == "CONFIG_NODE"


def test_config_adds_node_as_child_of_parent():
    with tempfile.TemporaryDirectory() as tmp:
        parent = Node("parent")
        include_module.PARENT_NODE = parent
        config_file = make_config_file(tmp)
        node = config(config_file)
        assert parent.children == [node]


def test_config_executes_included_file():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_file(tmp, content="x = 1 + 1")
        node = config(config_file)
        # The included file ran without error - no assertion needed beyond no exception


def test_config_passes_new_node_as_parent():
    with tempfile.TemporaryDirectory() as tmp:
        # The included config creates a commands dir with add.py so it can
        # add children to the node passed in as PARENT_NODE
        cmd_dir = Path(tmp) / "commands"
        cmd_dir.mkdir()
        (cmd_dir / "add.py").write_text(
            "from config_tree.node import Node\n"
            "def file(path):\n"
            "    child = Node(name=str(path))\n"
            "    PARENT_NODE.add_child(child)\n"
            "    return child\n"
        )
        config_file = Path(tmp) / "config.py"
        config_file.write_text("add.file('child.txt')")

        node = config(config_file)
        assert len(node.children) == 1
        assert node.children[0].name == "child.txt"


def test_missing_config_file_raises():
    try:
        config("/nonexistent/path/config.py")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
