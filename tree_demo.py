from tree_design import DecisionNode, LeafNode

if __name__ == "__main__":
    print("=-= Demo: Composite =-=")

    root = DecisionNode("root")
    a = DecisionNode("A")
    b = LeafNode("B")
    c = LeafNode("C")

    root.add(a)
    root.add(b)
    a.add(c)

    print("Estrutura montada!")