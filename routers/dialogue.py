from fastapi import APIRouter

from routers.security import *
from searching import search

router = APIRouter(prefix="/dialogue", tags=["dialogue"])


@router.get("/all")
def get_dialogues(current_user: Annotated[User, Depends(get_current_user)]):
    return [get_dialogue(d) for d in current_user.dialogues]


@router.get("/")
def get_dialogue(dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    history = dialogue.history
    nodes = dialogue.graph.knowledge_nodes
    edges = dialogue.graph.knowledge_relationships
    dialogue = dialogue.model._asdict()
    dialogue.update(history=[h.model._asdict() for h in history], nodes=[n._asdict() for n in nodes],
                    edges=[e._asdict() for e in edges])
    return dialogue


@router.post("/")
def open_dialogue(current_user: Annotated[User, Depends(get_current_user)]):
    current_user.open_dialogue("")
    return get_dialogue(current_user.dialogues[-1])


@router.put("/")
def continue_dialogue(question: str, dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    if not dialogue.history:
        dialogue.title = question
    answer, nodes, edges = search(question)
    query = dialogue.continue_dialogue(question, answer, nodes, edges)
    for node in nodes:
        if dialogue.graph.get_node_by_kid(node.properties["kid"]) is None:
            dialogue.graph.draw_node(node)
    for edge in edges:
        if dialogue.graph.get_relationship_by_type(edge.type, edge.start_node, edge.end_node) is not None:
            dialogue.graph.draw_relationship(edge)
    return query.model._asdict()


@router.delete("/")
def detach_dialogue(dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    try:
        dialogue.detach()
    except Exception:
        raise service_unavailable_exception
