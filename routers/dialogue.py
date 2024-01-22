from fastapi import APIRouter

from routers.security import *

router = APIRouter(prefix="/dialogue", tags=["dialogue"])


@router.get("/all")
def get_dialogues(current_user: Annotated[User, Depends(get_current_user)]):
    return [get_dialogue(d) for d in current_user.dialogues]


@router.get("/")
def get_dialogue(dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    history = dialogue.history
    dialogue = dialogue.model._asdict()
    dialogue.update(history=[h.model._asdict() for h in history])
    return dialogue


@router.post("/")
def open_dialogue(current_user: Annotated[User, Depends(get_current_user)]):
    current_user.open_dialogue("")
    return get_dialogue(current_user.dialogues[-1])


@router.put("/")
def continue_dialogue(question: str, dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    if not dialogue.history:
        dialogue.title = question
    answer = ""
    query = dialogue.continue_dialogue(question, answer)
    return query.model._asdict()


@router.delete("/")
def detach_dialogue(dialogue: Annotated[Dialogue, Depends(get_current_dialogue)]):
    try:
        dialogue.detach()
    except Exception:
        raise service_unavailable_exception
