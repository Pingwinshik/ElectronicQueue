from sanic import Sanic
from sanic.response import json, html, text
import asyncpg
import asyncio
import os

app = Sanic(__name__)
app.static("/static", os.getcwd() + "/static")

loop = asyncio.get_event_loop()


async def nigger():
    sys_conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="Lilipu6!"
    )
    await sys_conn.execute(f'CREATE DATABASE "EQS" OWNER postgres')
    await sys_conn.close()


async def drop_table():
    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        database="EQS",
        user='postgres',
        password='Lilipu6!')
    await conn.execute('DROP TABLE IF EXISTS "Tickets";')
    await conn.close()


async def init_table():
    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        database="EQS",
        user='postgres',
        password='Lilipu6!')
    await conn.execute('''CREATE TABLE "Tickets" (id serial PRIMARY KEY,
                type varchar (2) NOT NULL,
                number smallint NOT NULL,
                operator_id smallint,
                status smallint  NOT NULL);'''
                       )
    await conn.close()


async def create_ticket():
    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        database="EQS",
        user='postgres',
        password='Lilipu6!')
    await conn.execute(''' INSERT INTO "Tickets"(type, number, operator_id, status) VALUES($1, $2, $3, $4)''', 'S', 99,
                       13, 1)
    await conn.close()


@app.route('/EditTicket', methods=["POST"])
async def edit_ticket(data: str):
    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        database="EQS",
        user='postgres',
        password='Lilipu6!')
    cur = conn.cursor()
    await cur.execute('CREATE TABLE Tickets (id serial PRIMARY KEY,'
                      'type varchar (2) NOT NULL,'
                      'number smallint NOT NULL,'
                      'operator_id smallint,'
                      'status smallint  NOT NULL);'
                      )
    await conn.commit()
    await cur.close()
    await conn.close()


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
    loop.run_until_complete(nigger())
    loop.run_until_complete(init_table())
    loop.run_until_complete(create_ticket())
    init()
