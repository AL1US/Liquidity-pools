from fastapi import APIRouter, Form, Request

from app.utils.frontend import templates

router = APIRouter()

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"request": request}
    )

# апи для пост
@router.post("/login")
def login():
    pass
# принять данные

# вызвать метод регистрации если аккаунт не зареган 

# запомнить его в куках или в сессии

# вернуть ошибку или успех