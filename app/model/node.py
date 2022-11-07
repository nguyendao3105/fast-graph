from typing import Optional, List
from pydantic import BaseModel

class NodeBase(BaseModel):
    node_id: int
    labels: list


class Node(NodeBase):
    properties: Optional[dict] = None

class Nodes(BaseModel):
    nodes: List[Node]

class Relationship(BaseModel):
    relationship_id: int
    relationship_type: str
    source_node: Node
    target_node: Node
    properties: Optional[dict] = None