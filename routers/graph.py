from fastapi import APIRouter

from routers.security import *

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/all")
def get_graphs(current_user: Annotated[User, Depends(get_current_user)]):
    return [get_graph(g) for g in current_user.graphs]


@router.get("/")
def get_graph(graph: Annotated[Graph, Depends(get_current_graph)]):
    nodes = graph.knowledge_nodes
    edges = graph.knowledge_relationships
    graph = graph.model._asdict()
    graph.update(nodes=[n._asdict() for n in nodes], edges=[e._asdict() for e in edges])
    return graph


@router.post("/")
def draw_graph(current_user: Annotated[User, Depends(get_current_user)]):
    current_user.draw_graph("", datetime.now(), datetime.now())
    return get_graph(current_user.graphs[-1])


@router.delete("/")
def detach_graph(gid: int, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        current_user.detach_graph(gid)
    except Exception:
        raise forbidden_exception


@router.post("/node")
def draw_k_node(node: Annotated[models.KNode, Depends(create_node)],
                graph: Annotated[Graph, Depends(get_current_graph)]):
    try:
        graph.draw_node(node)
    except Exception:
        raise forbidden_exception


@router.post("/edge")
def draw_k_edge(edge: Annotated[models.KRelationship, Depends(create_edge)],
               graph: Annotated[Graph, Depends(get_current_graph)]):
    try:
        graph.draw_relationship(edge)
    except Exception:
        raise forbidden_exception


@router.put("/node")
def update_k_node(node: Annotated[models.KNode, Depends(create_node)],
                  graph: Annotated[Graph, Depends(get_current_graph)]):
    try:
        graph.set_node(node)
    except Exception:
        raise forbidden_exception


@router.put("/edge")
def update_k_edge(edge: Annotated[models.KRelationship, Depends(create_edge)],
                  graph: Annotated[Graph, Depends(get_current_graph)]):
    try:
        graph.set_relationship(edge)
    except Exception:
        raise forbidden_exception


@router.delete("/node")
def detach_k_node(kid: int, graph: Annotated[Graph, Depends(get_current_graph)]):
    graph.detach_node(kid)
    if graph.get_node_by_kid(kid) is not None:
        raise service_unavailable_exception


@router.delete("/edge")
def detach_k_edge(k_type: str, start_node: int, end_node: int, graph: Annotated[Graph, Depends(get_current_graph)]):
    graph.detach_relationship(k_type, start_node, end_node)
    if graph.get_relationship_by_type(k_type, start_node, end_node) is not None:
        raise service_unavailable_exception
