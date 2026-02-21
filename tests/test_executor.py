import tempfile
from pathlib import Path

from config_tree.executor import execute_config
from config_tree.node import Node


def make_config_tree(tmp_path, commands=None, config_content=""):
    config_dir = Path(tmp_path)
    if commands:
        cmd_dir = config_dir / "commands"
        cmd_dir.mkdir()
        for name, content in commands.items():
            (cmd_dir / name).write_text(content)
    config_file = config_dir / "config.py"
    config_file.write_text(config_content)
    return config_file


def test_config_dir_is_set():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = CONFIG_DIR")
        ns = execute_config(config_file)
        assert ns["result"] == str(Path(tmp).resolve())


def test_commands_are_loaded():
    with tempfile.TemporaryDirectory() as tmp:
        commands = {
            "greet.py": "def hello(name):\n    return f'hello {name}'\n",
        }
        config_file = make_config_tree(
            tmp,
            commands=commands,
            config_content="result = hello('world')",
        )
        ns = execute_config(config_file)
        assert ns["result"] == "hello world"


def test_multiple_commands_loaded_in_order():
    with tempfile.TemporaryDirectory() as tmp:
        commands = {
            "a_first.py": "value_a = 1\n",
            "b_second.py": "value_b = 2\n",
        }
        config_file = make_config_tree(
            tmp,
            commands=commands,
            config_content="result = value_a + value_b",
        )
        ns = execute_config(config_file)
        assert ns["result"] == 3


def test_missing_commands_dir_is_ok():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = 42")
        ns = execute_config(config_file)
        assert ns["result"] == 42


def test_missing_config_file_raises():
    try:
        execute_config("/nonexistent/path/config.py")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_private_names_not_exported():
    with tempfile.TemporaryDirectory() as tmp:
        commands = {
            "internal.py": "_secret = 42\npublic = 99\n",
        }
        config_file = make_config_tree(tmp, commands=commands, config_content="")
        ns = execute_config(config_file)
        assert ns["public"] == 99
        assert "_secret" not in ns


def test_node_is_available_in_namespace():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = node.name")
        n = Node("test-node")
        ns = execute_config(config_file, node=n)
        assert ns["result"] == "test-node"


def test_node_defaults_to_none():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = node")
        ns = execute_config(config_file)
        assert ns["result"] is None
