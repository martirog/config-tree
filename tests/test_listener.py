import pytest
from config_tree.listener import Listener


def test_listener_is_abstract():
    try:
        Listener()
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_listener_requires_action():
    class MissingAction(Listener):
        def entry(self, node):
            pass

        def exit(self, node):
            pass

    try:
        MissingAction()
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_listener_requires_entry():
    class MissingEntry(Listener):
        def action(self, node):
            return node

        def exit(self, node):
            pass

    try:
        MissingEntry()
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_listener_requires_exit():
    class MissingExit(Listener):
        def action(self, node):
            return node

        def entry(self, node):
            pass

    try:
        MissingExit()
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_concrete_listener_can_be_instantiated():
    class ConcreteListener(Listener):
        def action(self, node):
            return node

        def entry(self, node):
            pass

        def exit(self, node):
            pass

    listener = ConcreteListener()
    assert isinstance(listener, Listener)
