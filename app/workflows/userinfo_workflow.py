from models import Edge, HookBase, Node, Workflow
from schemas import UserInfoCreate
from utils.enums import EdgeTrigger


class PrintHook(HookBase):
    def on_validated(self):
        print(f"{self.element} was validated.")


def build_example_workflow():
    a = Node(
        id=1,
        name="a",
        category="Category 1",
        dataform_model=UserInfoCreate,
        hooks=[
            PrintHook,
        ],
    )
    b = Node(id=2, name="b", category="Category 1")
    c = Node(id=3, name="c", category="Category 2")
    d = Node(id=4, name="d", category="Category 2")
    e = Node(id=5, name="e", category="Category 3")

    return Workflow(
        id=0,
        name="Workflow 1",
        nodes=[a, b, c, d, e],
        edges=[
            Edge(prev=a, next=b),
            Edge(prev=b, next=c),
            Edge(prev=b, next=d),
            Edge(
                prev=c,
                next=b,
                trigger=EdgeTrigger.on_choice,
                name="Back to b",
                description="Choosing this path will archive every element that was instantiated after b",
            ),
            Edge(
                prev=c,
                next=e,
                trigger=EdgeTrigger.on_choice,
                name="Continue through e",
            ),
            Edge(prev=d, next=e),
        ],
    )


workflow = build_example_workflow()
