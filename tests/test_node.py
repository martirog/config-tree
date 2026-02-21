from config_tree.node import Node


def test_create_node_with_defaults():
    node = Node("root")
    assert node.name == "root"
    assert node.type is None
    assert node.children == []
    assert node.attributes == []


def test_create_node_with_all_fields():
    child = Node("child")
    node = Node("root", type="container", children=[child], attributes=["attr1"])
    assert node.name == "root"
    assert node.type == "container"
    assert node.children == [child]
    assert node.attributes == ["attr1"]


def test_add_child():
    parent = Node("parent")
    child = Node("child")
    returned = parent.add_child(child)
    assert returned is child
    assert parent.children == [child]


def test_add_multiple_children():
    parent = Node("parent")
    a = parent.add_child(Node("a"))
    b = parent.add_child(Node("b"))
    assert len(parent.children) == 2
    assert parent.children[0] is a
    assert parent.children[1] is b


def test_add_attribute():
    node = Node("node")
    returned = node.add_attribute("color")
    assert returned == "color"
    assert node.attributes == ["color"]


def test_add_multiple_attributes():
    node = Node("node")
    node.add_attribute("color")
    node.add_attribute("size")
    assert node.attributes == ["color", "size"]


def test_children_default_not_shared():
    a = Node("a")
    b = Node("b")
    a.add_child(Node("child"))
    assert b.children == []
