from pydantic import BaseModel
from utils.bases import DataFormBase, HookBase
from utils.enums import EdgeTrigger

"""
desc: Workflows are not strictly *models* : they are not stored in database but rather in-memory.
      However, to allow to be referenced via a "weak int pointer" by instances, nodes and workflows
      must define an ID considered as a primary key.
"""


class Workflow(BaseModel):
    """
    brief: A pattern of a workflow. Users should be able to create instances of this pattern.
    """

    id: int
    name: str
    description: str | None = None
    is_active: bool = True
    nodes: list["Node"]
    edges: list["Edge"]

    # Since workflows are built once per run and stored in memory,
    # build optimized accessors to win runtime compute.
    __prev_map: dict[int, list["Node"]] | None = None
    __next_map: dict[int, list["Node"]] | None = None
    __node_by_id_map: dict[int, "Node"] | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Link nodes to workflow
        for node in self.nodes:
            node.set_workflow(self)

        # Build optimized accessors
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

    def get_node(self, node_id: int) -> "Node":
        return (
            self.__node_by_id_map[node_id] if node_id in self.__node_by_id_map else None
        )

    def get_initial_nodes(self) -> list["Node"]:
        return [node for node in self.nodes if not self.__prev_map[node.id]]

    def get_next_nodes(self, node_id: int) -> list["Node"]:
        return self.__next_map[node_id]


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
    __workflow: Workflow = None

    def get_workflow(self) -> Workflow:
        return self.__workflow

    def set_workflow(self, workflow: Workflow):
        self.__workflow = workflow

    def get_next_auto_nodes(self):
        return self.__workflow.get_next_nodes(self.id)

    def get_next_on_choice_candidate_nodes(self):
        return [
            edge.next
            for edge in self.__workflow.edges
            if edge.prev == self and edge.trigger == EdgeTrigger.on_choice
        ]


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
