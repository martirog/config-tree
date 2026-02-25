import tempfile
from pathlib import Path

from config_tree.executor import execute_config, LOCAL_COMMANDS
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
            config_content="result = greet.hello('world')",
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
            config_content="result = a_first.value_a + b_second.value_b",
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


def test_command_loaded_as_module():
    with tempfile.TemporaryDirectory() as tmp:
        commands = {
            "mymod.py": "value = 99\n",
        }
        config_file = make_config_tree(
            tmp,
            commands=commands,
            config_content="result = mymod.value",
        )
        ns = execute_config(config_file)
        assert ns["result"] == 99


def test_node_is_available_in_namespace():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = PARENT_NODE.name")
        n = Node("test-node")
        ns = execute_config(config_file, node=n)
        assert ns["result"] == "test-node"


def test_node_defaults_to_none():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="result = PARENT_NODE")
        ns = execute_config(config_file)
        assert ns["result"] is None


def test_explicit_command_dir():
    with tempfile.TemporaryDirectory() as tmp_config, tempfile.TemporaryDirectory() as tmp_cmds:
        cmd_dir = Path(tmp_cmds) / "mycmds"
        cmd_dir.mkdir()
        (cmd_dir / "mymod.py").write_text("value = 42\n")
        config_file = make_config_tree(tmp_config, config_content="result = mymod.value")
        ns = execute_config(config_file, command_dirs=[cmd_dir])
        assert ns["result"] == 42


def test_local_commands_sentinel_loads_sibling_dir():
    with tempfile.TemporaryDirectory() as tmp:
        commands = {"greet.py": "def hello():\n    return 'hi'\n"}
        config_file = make_config_tree(tmp, commands=commands, config_content="result = greet.hello()")
        ns = execute_config(config_file, command_dirs=[LOCAL_COMMANDS])
        assert ns["result"] == "hi"


def test_mixed_command_dirs():
    with tempfile.TemporaryDirectory() as tmp_config, tempfile.TemporaryDirectory() as tmp_extra:
        extra_dir = Path(tmp_extra) / "extra"
        extra_dir.mkdir()
        (extra_dir / "extra_mod.py").write_text("value = 99\n")
        commands = {"local_mod.py": "value = 1\n"}
        config_file = make_config_tree(
            tmp_config,
            commands=commands,
            config_content="result = local_mod.value + extra_mod.value",
        )
        ns = execute_config(config_file, command_dirs=[LOCAL_COMMANDS, extra_dir])
        assert ns["result"] == 100


def test_invalid_command_dir_raises():
    with tempfile.TemporaryDirectory() as tmp:
        config_file = make_config_tree(tmp, config_content="")
        try:
            execute_config(config_file, command_dirs=["/nonexistent/cmds"])
            assert False, "Expected NotADirectoryError"
        except NotADirectoryError:
            pass
