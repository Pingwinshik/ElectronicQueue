from sanic import Sanic
from sanic.response import json, html, text
from databases import Database
from dataclasses import dataclass
import asyncio
import os


@dataclass
class TData:
    type: str
    number: int
    operator_id: int
    status: int


app = Sanic(__name__)
app.static("/static", os.getcwd() + "/static")


async def create_db_connection():
    Tickets = Database("postgresql://postgres:localhost:5432/Tickets")
    await Tickets.connect()
    return Tickets


def init_db() -> None:
    async def _inner() -> None:
        db = await create_db_connection()
        db.execute("""CREATE TABLE Ticket {
	id SERIAL PRIMARY KEY,
	type INTEGER NOT NULL,
	number INTEGER NOT NULL,
	operator_id INTEGER,
	status SMALLINT NOT NULL
};""")


@app.route('/CreateTicket', methods=["POST"])
async def create_ticket(data: TData) -> None:
    return()


def init():
    app.run(host='127.0.0.1', port=9001, debug=True)


@app.route('/')
async def index(request):
  template = open(os.getcwd() + "/templates/index.html", encoding='utf-8')
  return html(template.read())


@app.route("/login")
async def login(request):
  template = open(os.getcwd() + "/templates/login.html", encoding='utf-8')
  return html(template.read())


@app.route("/client")
async def client(request):
  template = open(os.getcwd() + "/templates/client.html", encoding='utf-8')
  return html(template.read())


@app.route('/ticket')
async def ticket(request):
  template = open(os.getcwd() + "/templates/ticket.html", encoding='utf-8')
  return html(template.read())


@app.route('/volunteer')
async def volunteer(request):
  template = open(os.getcwd() + "/templates/volunteer.html", encoding='utf-8')
  return html(template.read())


@app.route('/screen')
async def screen(request):
  template = open(os.getcwd() + "/templates/screen.html", encoding='utf-8')
  return html(template.read())


@app.route('/statistic')
async def statistic(request):
  template = open(os.getcwd() + "/templates/statistic.html", encoding='utf-8')
  return html(template.read())


if __name__ == '__main__':
    init_db()
    init()