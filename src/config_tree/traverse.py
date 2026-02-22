def traverse(node, listener):
    node = listener.action(node)
    listener.entry(node)
    for child in node.children:
        traverse(child, listener)
    listener.exit(node)
