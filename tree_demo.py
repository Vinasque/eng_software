from __future__ import annotations
from tree_design import DecisionNode, LeafNode, PreOrderIterator, BFSIterator, DepthVisitor, CountLeavesVisitor, TreeBuilder, print_tree

def montar_arvore():
    root = DecisionNode("root")
    a = DecisionNode("A")
    b = LeafNode("B")
    c = LeafNode("C")
    root.add(a)
    root.add(b)
    a.add(c)
    return root

if __name__ == "__main__":
    print("Projeto: Árvore de Decisão")

    # 1) Composite
    root = montar_arvore()
    print("\n[1] Estrutura inicial (Composite):")
    print_tree(root)

    # 2) State
    print("\n[2] Construção com State:")
    builder = TreeBuilder(root=root)
    builder.run()   # Splitting -> Stopping -> Pruning -> Fim

    print("\n[3] Estrutura após State:")
    print_tree(root)

    # 3) Iterators
    print("\n[4a] Percurso com PreOrderIterator:")
    for _node, _depth in PreOrderIterator(root):
        pass

    print("\n[4b] Percurso com BFSIterator:")
    for _node, _depth in BFSIterator(root):
        pass

    # 4) Visitors
    print("\n[5] Visitors:")
    depth_v = DepthVisitor()
    leaves_v = CountLeavesVisitor()

    for node, depth in PreOrderIterator(root):
        # profundidade de fora, com ajuda do iterator
        depth_v.note_depth(depth)

        # visit_node + específico (feito dentro do accept)
        node.accept(depth_v)
        node.accept(leaves_v)

    depth_v.finish()
    leaves_v.finish()