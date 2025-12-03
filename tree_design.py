from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple, Optional

# Print mais bonito
def log(tag: str, msg: str) -> None:
    print(f"[{tag}] {msg}")

# COMPOSITE

class Node(ABC):
    """Componente base do Composite."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def add(self, child: "Node") -> None: ...

    @abstractmethod
    def remove(self, child: "Node") -> None: ...

    @abstractmethod
    def get_children(self) -> list["Node"]: ...

    @abstractmethod
    def accept(self, visitor: "Visitor") -> None: ...

    # Novamente, só para deixar o print mais bonito
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self.name}>"


class DecisionNode(Node):
    """Nó interno que pode ter filhos."""
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Node] = []

    def add(self, child: Node) -> None:
        if not isinstance(child, Node):
            raise TypeError("child deve ser um Node.")
        self._children.append(child)
        log("Composite", f"Adicionado filho {child} em DecisionNode('{self.name}').")

    def remove(self, child: Node) -> None:
        if child in self._children:
            self._children.remove(child)
            log("Composite", f"Removido filho {child} de DecisionNode('{self.name}').")
        else:
            log("Composite", f"Filho {child} não encontrado em '{self.name}'.")

    def get_children(self) -> list[Node]:
        return list(self._children)  # cópia defensiva

    def accept(self, visitor: "Visitor") -> None:
        log("Visitor", f"visit_decision em '{self.name}'.")
        visitor.visit_node(self)      # gancho genérico
        visitor.visit_decision(self)  # específico


class LeafNode(Node):
    """Folha."""
    def add(self, child: Node) -> None:
        raise NotImplementedError("LeafNode não pode receber filhos.")

    def remove(self, child: Node) -> None:
        raise NotImplementedError("LeafNode não tem filhos para remover.")

    def get_children(self) -> list[Node]:
        return []

    def accept(self, visitor: "Visitor") -> None:
        log("Visitor", f"visit_leaf em '{self.name}'.")
        visitor.visit_node(self)
        visitor.visit_leaf(self)

# ITERATORS

class PreOrderIterator:
    """Iterator em pré-ordem que também fornece a profundidade."""
    def __init__(self, root: Node):
        # pilha de tuplas (node, depth)
        self._stack: List[Tuple[Node, int]] = [(root, 0)]

    def __iter__(self) -> Iterator[Tuple[Node, int]]:
        return self

    def __next__(self) -> Tuple[Node, int]:
        if not self._stack:
            raise StopIteration
        current, d = self._stack.pop()
        if hasattr(current, "get_children"):
            for ch in reversed(current.get_children()):
                self._stack.append((ch, d + 1))
        log("Iterator", f"visitando (pré-ordem): {current} (depth={d})")
        return current, d


class BFSIterator:
    """Iterator em largura (BFS)."""
    def __init__(self, root: Node):
        self._queue: List[Tuple[Node, int]] = [(root, 0)]

    def __iter__(self) -> Iterator[Tuple[Node, int]]:
        return self

    def __next__(self) -> Tuple[Node, int]:
        if not self._queue:
            raise StopIteration
        current, d = self._queue.pop(0)
        if hasattr(current, "get_children"):
            for ch in current.get_children():
                self._queue.append((ch, d + 1))
        log("Iterator", f"visitando (largura): {current} (depth={d})")
        return current, d

# VISITOR

class Visitor(ABC):
    """Interface para visitors."""

    def visit_node(self, node: Node) -> None:
        log("Visitor", f"visit_node: {node}.")

    def visit_decision(self, node: DecisionNode) -> None:
        log("Visitor", f"visit_decision: {node}.")

    def visit_leaf(self, node: LeafNode) -> None:
        log("Visitor", f"visit_leaf: {node}.")


class DepthVisitor(Visitor):
    """Visitante que 'calcula' profundidade."""
    def __init__(self) -> None:
        self.max_depth_vista: int = -1  # começa em -1 para root = 0

    # Gancho auxiliar usado pelo demo quando o iterator fornece profundidade
    def note_depth(self, depth: int) -> None:
        self.max_depth_vista = max(self.max_depth_vista, depth)
        log("DepthVisitor", f" registrando depth = {depth}: max = {self.max_depth_vista}")

    def finish(self) -> int:
        log("DepthVisitor", f"profundidade: {self.max_depth_vista}")
        return self.max_depth_vista


class CountLeavesVisitor(Visitor):
    """Visitante que 'conta' folhas."""
    def __init__(self) -> None:
        self.count: int = 0

    def visit_leaf(self, node: LeafNode) -> None:
        super().visit_leaf(node)
        self.count += 1
        log("CountLeavesVisitor", f"contando folha: agora = {self.count}")

    def finish(self) -> int:
        log("CountLeavesVisitor", f"folhas: {self.count}")
        return self.count


# ==========
# STATE
# ==========

class BuilderState(ABC):
    """Interface para estados do construtor da árvore."""
    @abstractmethod
    def handle(self, builder: "TreeBuilder") -> None:
        ...


class SplittingState(BuilderState):
    def handle(self, builder: "TreeBuilder") -> None:
        log("State", "SplittingState: dividindo nós.")
        log("State", "         ...criando DecisionNodes/LeafNodes.")
        builder.set_state(StoppingState())

class StoppingState(BuilderState):
    def handle(self, builder: "TreeBuilder") -> None:
        log("State", "StoppingState: condição de parada atingida.")
        builder.set_state(PruningState())

class PruningState(BuilderState):
    def handle(self, builder: "TreeBuilder") -> None:
        log("State", "PruningState: realizando poda.")
        # Se o root for DecisionNode, remove o último filho
        if isinstance(builder.root, DecisionNode):
            children = builder.root.get_children()
            if children:
                to_remove = children[-1]
                builder.root.remove(to_remove)
                log("State", f"Poda: removido '{to_remove}' do root.")
        builder.set_state(None)  # fim do fluxo

class TreeBuilder:
    """Simula a construção em etapas."""
    def __init__(self, root: Optional[Node] = None):
        self.state: Optional[BuilderState] = SplittingState()
        self.root: Optional[Node] = root

    def set_state(self, state: Optional[BuilderState]) -> None:
        self.state = state
        log("State", f"transição: {type(state).__name__ if state else 'Fim'}.")

    def next(self) -> None:
        if self.state is None:
            log("State", "não há mais estados.")
            return

        if self.root is None:
            log("State", "aviso: root = None (nada a fazer).")
        else:
            log("State", f"trabalhando sobre root '{self.root.name}'.")
        self.state.handle(self)

    def run(self) -> None:
        while self.state is not None:
            self.next()

def print_tree(root: Node, indent: str = "") -> None:
    """Imprime a estrutura hierárquica."""
    print(f"{indent}- {root}")
    for ch in root.get_children():
        print_tree(ch, indent + "  ")
