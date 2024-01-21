from fastapi import APIRouter

from routers.security import *

router = APIRouter(prefix="/token", tags=["token"])


@router.get("/")
def get_info(current_user: Annotated[User, Depends(get_current_user)]):
    """Get information of a login user"""
    info = current_user.model

    dialogues = []
    for d, h in zip(current_user.dialogues, (d.history for d in current_user.dialogues)):
        entry = d.model._asdict()
        entry.update(history=h)
        dialogues.append(entry)

    graphs = []
    for g, n, e in zip(current_user.graphs, (g.knowledge_nodes for g in current_user.graphs),
                       (g.knowledge_relationships for g in current_user.graphs)):
        entry = g.model._asdict()
        entry.update(nodes=n, edges=e)
        graphs.append(entry)

    response = {
        "info": info,
        "dialogues": dialogues,
        "graphs": graphs
    }
    return {"user_data": response}


@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Client logins system with username and password."""
    user = authenticate_application_form(form_data)
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/")
def register(user: Annotated[User, Depends(create_user)]):
    """Client register with a from."""
    return {"msg": f"{user.username} registered successfully"}


@router.delete("/")
def deregister(current_user: Annotated[User, Depends(get_current_user)]):
    """Client deregister a user. This will delete the user as well as all related data. Can not be reverted for now."""
    username = current_user.username
    current_user.detach()
    if current_user.exists():
        raise service_unavailable_exception
    return {"msg": f"{username} deregistered successfully"}
