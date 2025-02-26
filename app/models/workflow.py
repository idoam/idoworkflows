from enum import Enum

from models.bases import DataFormBase, HookBase
from pydantic import BaseModel


class Node(BaseModel):
    """
    brief: Node of a workflow.
    """

    id: int
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    hooks: list[type[HookBase]] | None = None
    dataform_model: type[DataFormBase] | None = None
    __workflow: BaseModel | None = None

    def get_workflow(self):
        return self.__workflow

    def set_workflow(self, workflow: BaseModel):
        self.__workflow = workflow


class EdgeTrigger(str, Enum):
    auto = "auto"  # Unlocks `next` on prev validation status.
    on_choice = (
        "on_choice"  # Like `auto`, if user chose this path from all possible edges.
    )


class Edge(BaseModel):
    """
    brief: Links Nodes to create a graph.
    """

    prev: Node
    next: Node
    weight: int = 100
    trigger: EdgeTrigger = EdgeTrigger.auto
    name: str | None = None
    description: str | None = None


class Workflow(BaseModel):
    """
    brief: A pattern of a workflow. Users should be able to create instances of this pattern.
    """

    id: int
    name: str
    description: str | None = None
    is_active: bool = True
    nodes: list[Node]
    edges: list[Edge]

    # Static cache
    __prev_map: dict[int, list[Node]] | None = None
    __next_map: dict[int, list[Node]] | None = None
    __node_by_id_map: dict[int, Node] | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Link nodes to workflow
        for node in self.nodes:
            node.set_workflow(self)

        # Build static cache
        self.__prev_map = {
            node.id: [
                edge.prev
                for edge in self.edges
                if edge.next is node and edge.trigger == EdgeTrigger.auto
            ]
            for node in self.nodes
        }
        self.__next_map = {
            node.id: [
                edge.next
                for edge in self.edges
                if edge.prev is node and edge.trigger == EdgeTrigger.auto
            ]
            for node in self.nodes
        }
        self.__node_by_id_map = {node.id: node for node in self.nodes}

    def get_node(self, node_id: int) -> Node | None:
        return (
            self.__node_by_id_map[node_id] if node_id in self.__node_by_id_map else None
        )

    def get_initial_nodes(self) -> list[Node]:
        return [node for node in self.nodes if not self.__prev_map[node.id]]

    def get_next_nodes(self, node_id: int) -> list[Node]:
        return self.__next_map[node_id]
