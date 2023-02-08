from sanic import Sanic
from sanic.response import json, html, text
import asyncpg
import asyncio
import os
import Settings

app = Sanic(__name__)
app.static("/static", os.getcwd() + "/static")

loop = asyncio.get_event_loop()


async def nigger():
    sys_conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        user=Settings.S_user,
        password=Settings.S_password
    )
    try:
        await sys_conn.execute(f'CREATE DATABASE "EQS" OWNER postgres')
    except:
        pass
    await sys_conn.close()


async def drop_tick_table():
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database="EQS",
        user=Settings.S_user,
        password=Settings.S_password)
    try:
        await conn.execute('DROP TABLE IF EXISTS "Tickets";')
    except:
        pass
    await conn.close()


async def drop_op_table():
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database="EQS",
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute('DROP TABLE IF EXISTS "Operators";')
    await conn.close()


async def init_tables():
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database="EQS",
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute('''CREATE TABLE IF NOT EXISTS "Tickets" (id serial PRIMARY KEY,
                type varchar (2) NOT NULL,
                number smallint NOT NULL,
                operator_id smallint,
                status smallint  NOT NULL);'''
                       )
    await conn.execute('''CREATE TABLE IF NOT EXISTS "Operators" (id serial PRIMARY KEY,
                    room varchar (5) NOT NULL,
                    wnd smallint NOT NULL,
                    logged_in boolean NOT NULL DEFAULT false,
                    is_working boolean NOT NULL DEFAULT false,
                    is_serving boolean NOT NULL DEFAULT false,
                    login varchar (100) NOT NULL,
                    password varchar (100) NOT NULL);'''
                       )
    await conn.close()


async def create_ticket(T_type, T_number, ):
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database="EQS",
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute(''' INSERT INTO "Tickets"(type, number, operator_id, status) VALUES($1, $2, $3, $4)''', T_type, T_number, None, 0)
    await conn.close()


@app.route('/EditTicket', methods=["POST"])
async def edit_ticket(data: str):
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database="EQS",
        user=Settings.S_user,
        password=Settings.S_password)
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
    loop.run_until_complete(init_tables())
    loop.run_until_complete(create_ticket("Р", 77))
    init()
