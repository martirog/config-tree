import importlib.util
from pathlib import Path

from config_tree.node import Node

LOCAL_COMMANDS = object()


def read_config(path, command_dirs=None):
    node = Node(name=str(path), type="TOP_NODE")
    execute_config(str(path), node=node, command_dirs=command_dirs)
    return node


def execute_config(config_path, node=None, command_dirs=None):
    config_path = Path(config_path).resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config_dir = config_path.parent

    if command_dirs is None:
        command_dirs = [LOCAL_COMMANDS]

    namespace = {"CONFIG_DIR": str(config_dir), "PARENT_NODE": node}

    for cmd_dir in command_dirs:
        if cmd_dir is LOCAL_COMMANDS:
            cmd_dir = config_dir / "commands"
            if not cmd_dir.is_dir():
                continue
        else:
            cmd_dir = Path(cmd_dir)
            if not cmd_dir.is_dir():
                raise NotADirectoryError(f"Command directory not found: {cmd_dir}")

        for cmd_file in sorted(cmd_dir.glob("*.py")):
            module_name = cmd_file.stem
            spec = importlib.util.spec_from_file_location(module_name, cmd_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.PARENT_NODE = node
            module.COMMAND_DIRS = command_dirs
            namespace[module_name] = module

    exec(compile(config_path.read_text(), str(config_path), "exec"), namespace)

    return namespace
