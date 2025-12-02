from tree_design import DecisionNode, LeafNode, PreOrderIterator, DepthVisitor, CountLeavesVisitor

if __name__ == "__main__":

    root = DecisionNode("root")
    a = DecisionNode("A")
    b = LeafNode("B")
    c = LeafNode("C")

    root.add(a)
    root.add(b)
    a.add(c)

    print("\nPercorrendo com PreOrderIterator:")
    for node in PreOrderIterator(root):
        # Simula aplicar um visitor em cada nó
        pass

    print("\nExecutando visitantes:")
    depth_v = DepthVisitor(expected_depth=3)
    leaves_v = CountLeavesVisitor(expected_count=2)

    # Simula visitas
    for node in PreOrderIterator(root):
        node.accept(depth_v)
        node.accept(leaves_v)

    # Finaliza e pega resultados
    depth_v.finish()
    leaves_v.finish()
