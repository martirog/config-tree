class Node:
    def __init__(self, name, type=None, children=None, attributes=None):
        self.name = name
        self.type = type
        self.children = children or []
        self.attributes = attributes or []

    def add_child(self, child):
        self.children.append(child)
        return child

    def add_attribute(self, attribute):
        self.attributes.append(attribute)
        return attribute
