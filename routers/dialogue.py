from fastapi import APIRouter

from routers.security import *

router = APIRouter(prefix="/dialogue", tags=["dialogue"])


@router.get("/all")
def get_dialogues(current_user: Annotated[User, Depends(get_current_user)]):
    return [get_dialogue(i, current_user) for i in range(len(current_user.dialogues))]


@router.get("/")
def get_dialogue(did: int, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        dialogue = current_user.dialogues[did]
    except Exception:
        raise forbidden_exception
    history = dialogue.history
    dialogue = dialogue.model._asdict()
    dialogue.update(history=[h.model._asdict() for h in history])
    return dialogue


@router.post("/")
def open_dialogue(current_user: Annotated[User, Depends(get_current_user)]):
    current_user.open_dialogue("")
    return get_dialogue(-1, current_user)


@router.put("/")
def continue_dialogue(did: int, question: str, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        dialogue = current_user.dialogues[did]
    except Exception:
        raise forbidden_exception
    if not dialogue.history:
        dialogue.title = question
    answer = ""
    query = dialogue.continue_dialogue(question, answer)
    return query.model._asdict()


@router.delete("/")
def detach_dialogue(did: int, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        current_user.detach_dialogue(did)
    except Exception:
        raise forbidden_exception
    return None
