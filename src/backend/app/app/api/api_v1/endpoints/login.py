import secrets
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()
db = {}


@router.post('/login')
def login(
    request: Request,
    redirect_url: str,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if form_data.username != '123' and form_data.password != '123':
        return {'message': 'Incorrect username or password'}

    request.session['login'] = True
    request.session['user_info'] = {}
    ticket = secrets.token_hex(10)
    db[ticket] = redirect_url
    request.session['user_info'][redirect_url] = ticket
    redirect_url_with_ticket = f'{redirect_url}?ticket={ticket}'

    return RedirectResponse(
        url=redirect_url_with_ticket, status_code=status.HTTP_303_SEE_OTHER
    )


class TicketInfo(BaseModel):
    ticket: str
    url: str


@router.post('/verify')
def verify(ticket_info: TicketInfo = Body(...)):
    if ticket_info.ticket not in db:
        return {'message': 'Invalid ticket'}

    stored_service_url = db.get(ticket_info.ticket)
    if stored_service_url != ticket_info.url:
        return {'message': 'Invalid url'}

    return RedirectResponse(
        url=stored_service_url, status_code=status.HTTP_303_SEE_OTHER
    )
