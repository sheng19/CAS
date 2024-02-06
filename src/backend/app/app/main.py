from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from api.api_v1.api import api_router
from core.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/', response_class=HTMLResponse)
def get_login_page():
    with open('login.html') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content)
