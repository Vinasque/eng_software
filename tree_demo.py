from tree_design import DecisionNode, LeafNode, PreOrderIterator, DepthVisitor, CountLeavesVisitor, TreeBuilder, print_tree

def montar_arvore_mock():
    root = DecisionNode("root")
    a = DecisionNode("A")
    b = LeafNode("B")
    c = LeafNode("C")
    root.add(a); root.add(b); a.add(c)
    return root

if __name__ == "__main__":
    print("Projeto: Árvore de Decisão")

    # 1) Composite
    root = montar_arvore_mock()
    print("\n[1] Estrutura inicial (Composite):")
    print_tree(root)

    # 2) State
    print("\n[2] Construção com State:")
    builder = TreeBuilder(root=root)
    builder.next()   # Splitting
    builder.next()   # Stopping
    builder.next()   # Pruning
    builder.next()   # Fim

    print("\n[3] Estrutura após State:")
    print_tree(root)

    # 3) Iterator
    print("\n[4] Percurso com PreOrderIterator:")
    for _ in PreOrderIterator(root):
        pass

    # 4) Visitors
    print("\n[5] Visitors:")
    depth_v = DepthVisitor(expected_depth=3)
    leaves_v = CountLeavesVisitor(expected_count=1)
    for node in PreOrderIterator(root):
        node.accept(depth_v)
        node.accept(leaves_v)
    depth_v.finish()
    leaves_v.finish()