import tempfile
from pathlib import Path

from config_tree.help import print_help


def make_command_dir(tmp_path, files):
    cmd_dir = Path(tmp_path) / "commands"
    cmd_dir.mkdir()
    for name, content in files.items():
        (cmd_dir / name).write_text(content)
    return cmd_dir


def test_module_name_printed_as_heading(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {"greet.py": ""})
        print_help([cmd_dir])
        assert "# greet" in capsys.readouterr().out


def test_module_docstring_printed(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "greet.py": '"""Commands for greeting people."""\n'
        })
        print_help([cmd_dir])
        assert "Commands for greeting people." in capsys.readouterr().out


def test_function_printed_as_module_dot_function(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "greet.py": "def hello(): pass\n"
        })
        print_help([cmd_dir])
        assert "greet.hello" in capsys.readouterr().out


def test_function_docstring_printed(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "greet.py": 'def hello():\n    """Say hello."""\n    pass\n'
        })
        print_help([cmd_dir])
        assert "Say hello." in capsys.readouterr().out


def test_private_functions_not_printed(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "greet.py": "def _internal(): pass\ndef hello(): pass\n"
        })
        print_help([cmd_dir])
        out = capsys.readouterr().out
        assert "_internal" not in out
        assert "greet.hello" in out


def test_imported_functions_not_printed(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "greet.py": "from os.path import join\ndef hello(): pass\n"
        })
        print_help([cmd_dir])
        out = capsys.readouterr().out
        assert "greet.join" not in out
        assert "greet.hello" in out


def test_init_file_skipped(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "__init__.py": '"""Should not appear."""\n',
            "greet.py": "",
        })
        print_help([cmd_dir])
        assert "__init__" not in capsys.readouterr().out


def test_multiple_command_dirs(capsys):
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        dir1 = make_command_dir(tmp1, {"greet.py": ""})
        dir2 = make_command_dir(tmp2, {"math.py": ""})
        print_help([dir1, dir2])
        out = capsys.readouterr().out
        assert "# greet" in out
        assert "# math" in out


def test_files_printed_in_alphabetical_order(capsys):
    with tempfile.TemporaryDirectory() as tmp:
        cmd_dir = make_command_dir(tmp, {
            "zebra.py": "",
            "apple.py": "",
        })
        print_help([cmd_dir])
        out = capsys.readouterr().out
        assert out.index("# apple") < out.index("# zebra")
