from tree_design import DecisionNode, LeafNode, PreOrderIterator, DepthVisitor, CountLeavesVisitor, TreeBuilder

if __name__ == "__main__":
    # Composite
    root = DecisionNode("root")
    a = DecisionNode("A")
    b = LeafNode("B")
    c = LeafNode("C")
    root.add(a); root.add(b); a.add(c)

    # Iterator
    print("\nPercorrendo com PreOrderIterator:")
    for _ in PreOrderIterator(root):
        pass

    # Visitor
    print("\nExecutando visitantes:")
    depth_v = DepthVisitor(expected_depth=3)
    leaves_v = CountLeavesVisitor(expected_count=2)
    for node in PreOrderIterator(root):
        node.accept(depth_v)
        node.accept(leaves_v)
    depth_v.finish()
    leaves_v.finish()

    # State
    print("\nSimulando construção da árvore com State:")
    builder = TreeBuilder()
    builder.next()  # Splitting
    builder.next()  # Stopping
    builder.next()  # Pruning
    builder.next()  # Fim