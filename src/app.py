from pathlib import Path
from typing import Union

from fastapi import FastAPI, Request, Response, Form, Depends, HTTPException, responses
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette import status

from forms import UserCreateForm

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


fake_users_db = {
    "kobran": {
        "username": "kobran",
        "full_name": "Kobran",
        "email": "maile@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "jocke": {
        "username": "jocke",
        "full_name": "Jocke",
        "email": "mail2@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/threads/")
async def read_items(current_user: User = Depends(get_current_user)):
    return {"username": current_user.full_name}


@app.get("/login/", response_class=HTMLResponse)
async def login_page(request: Request) -> Response:
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/")
async def login_user(name: str = Form(), pwd: str = Form()):
    if True:
        return {"msg": "success"}
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register/", response_class=HTMLResponse)
async def register_page(request: Request) -> Response:
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register/")
async def register_user(request: Request):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        return responses.RedirectResponse("/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("register.html", form.__dict__)
