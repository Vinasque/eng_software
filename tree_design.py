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
    
# VISITOR

class Visitor:
    """Interface para visitantes."""
    def visit_node(self, node: Node):
        print(f"[Visitor] visit_node: {node}.")

    def visit_decision(self, node: DecisionNode):
        print(f"[Visitor] visit_decision: {node}.")

    def visit_leaf(self, node: LeafNode):
        print(f"[Visitor] visit_leaf: {node}.")


class DepthVisitor(Visitor):
    """Visitante que 'calcula' profundidade."""
    def __init__(self, expected_depth: int = 3):
        self.expected_depth = expected_depth

    def finish(self):
        print(f"[DepthVisitor] profundidade: {self.expected_depth}")
        return self.expected_depth


class CountLeavesVisitor(Visitor):
    """Visitante que 'conta' folhas."""
    def __init__(self, expected_count: int = 2):
        self.expected_count = expected_count

    def finish(self):
        print(f"[CountLeavesVisitor] folhas: {self.expected_count}")
        return self.expected_count
    
# STATE

class BuilderState:
    """Interface para estados do construtor da árvore."""
    @abstractmethod
    def handle(self, builder: "TreeBuilder"): pass

class SplittingState(BuilderState):
    def handle(self, builder: "TreeBuilder"):
        print("[State] SplittingState: dividindo nós.")
        print("         ...criando DecisionNodes/LeafNodes")
        builder.set_state(StoppingState())

class StoppingState(BuilderState):
    def handle(self, builder: "TreeBuilder"):
        print("[State] StoppingState: condição de parada atingida.")
        builder.set_state(PruningState())

class PruningState(BuilderState):
    def handle(self, builder: "TreeBuilder"):
        print("[State] PruningState: realizando poda.")
        builder.set_state(None)  # fim do fluxo

class TreeBuilder:
    """Simula a construção em etapas."""
    def __init__(self, root: Node | None = None):
        self.state: BuilderState | None = SplittingState()
        self.root = root

    def set_state(self, state: BuilderState | None):
        self.state = state
        print(f"[State] transição: {type(state).__name__ if state else 'Fim'}.")

    def next(self):
        if self.state is None:
            print("[State] não há mais estados.")
            return

        if self.root is not None:
            print(f"[State] trabalhando sobre root '{self.root.name}'.")
        self.state.handle(self)

def print_tree(root: Node, indent: str = ""):
    """Imprime a estrutura hierárquica."""
    print(f"{indent}- {root}")
    if hasattr(root, "get_children"):
        for ch in root.get_children():
            print_tree(ch, indent + "  ")