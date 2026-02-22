import importlib.util
from pathlib import Path


def execute_config(config_path, node=None):
    config_path = Path(config_path).resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config_dir = config_path.parent
    namespace = {"CONFIG_DIR": str(config_dir), "PARENT_NODE": node}

    commands_dir = config_dir / "commands"
    if commands_dir.is_dir():
        for cmd_file in sorted(commands_dir.glob("*.py")):
            module_name = cmd_file.stem
            spec = importlib.util.spec_from_file_location(module_name, cmd_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.PARENT_NODE = node
            namespace[module_name] = module

    exec(compile(config_path.read_text(), str(config_path), "exec"), namespace)

    return namespace
