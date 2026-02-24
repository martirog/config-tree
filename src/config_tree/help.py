import importlib.util
import inspect
from pathlib import Path


def print_help(command_dirs):
    for cmd_dir in command_dirs:
        cmd_dir = Path(cmd_dir)
        for cmd_file in sorted(cmd_dir.glob("*.py")):
            module_name = cmd_file.stem
            if module_name.startswith("_"):
                continue

            spec = importlib.util.spec_from_file_location(module_name, cmd_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(f"# {module_name}")
            if module.__doc__:
                print(module.__doc__.strip())
            print()

            for name, obj in inspect.getmembers(module, inspect.isfunction):
                if not name.startswith("_") and obj.__module__ == module_name:
                    print(f"{module_name}.{name}")
                    if obj.__doc__:
                        print(obj.__doc__.strip())
                    print()
