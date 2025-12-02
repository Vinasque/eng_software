from abc import abstractmethod

# COMPOSITE

class Node:
    """Componente base do Composite."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def add(self, child: "Node"): pass

    @abstractmethod
    def remove(self, child: "Node"): pass

    @abstractmethod
    def get_children(self): pass

    def accept(self, visitor):
        # as subclasses vão subescrever
        print(f"[Visitor] visit_node em '{self.name}'.")

class DecisionNode(Node):
    """Nó interno que pode ter filhos."""
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, child: Node):
        self.children.append(child)
        print(f"[Composite] Adicionado filho {child} em DecisionNode('{self.name}').")

    def remove(self, child: Node):
        if child in self.children:
            self.children.remove(child)
            print(f"[Composite] Removido filho {child} de DecisionNode('{self.name}').")
        else:
            print(f"[Composite] Filho {child} não encontrado em '{self.name}'.")

    def get_children(self):
        return list(self.children)

    def accept(self, visitor):
        print(f"[Visitor] visit_decision em '{self.name}'.")
        visitor.visit_decision(self)

class LeafNode(Node):
    """Folha"""
    def accept(self, visitor):
        print(f"[Visitor] visit_leaf em '{self.name}'.")
        visitor.visit_leaf(self)

# ITERATOR

class PreOrderIterator:
    """Iterator em pré-ordem."""
    def __init__(self, root: Node):
        self.stack = [root]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        current = self.stack.pop()
        # Empilha filhos em ordem reversa para visitar na ordem natural
        if hasattr(current, "get_children"):
            children = current.get_children()
            for ch in reversed(children):
                self.stack.append(ch)
        print(f"[Iterator] visitando (pré-ordem): {current}")

        return current