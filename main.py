from sanic import Sanic
from sanic.response import json, html, text
from sanic_ext import render
from sanic_jwt.decorators import protected
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
        database=Settings.S_database,
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
        database=Settings.S_database,
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute('DROP TABLE IF EXISTS "Operators";')
    await conn.close()


async def init_tables():
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database=Settings.S_database,
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute('''CREATE TABLE IF NOT EXISTS "Tickets" (id serial PRIMARY KEY,
                type varchar (2) NOT NULL,
                number smallint NOT NULL,
                wnd varchar(9) NOT NULL,
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
                    password varchar (100) NOT NULL,
                    serv_ticket_id smallint DEFAULT NULL);'''
                       )
    await conn.execute('''CREATE TABLE IF NOT EXISTS "Administrum" (id serial PRIMARY KEY,
                       logged_in boolean NOT NULL DEFAULT false,
                       login varchar (100) NOT NULL,
                       password varchar (100) NOT NULL);'''
                       )
    await conn.close()


async def create_ticket(T_type, T_number, T_window):
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database=Settings.S_database,
        user=Settings.S_user,
        password=Settings.S_password)
    await conn.execute(''' INSERT INTO "Tickets"(type, number, wnd, operator_id, status) VALUES($1, $2, $3, $4, $5)''', T_type, T_number, T_window, None, 0)
    await conn.close()


@app.route('/EditTicket', methods=["POST"])
async def edit_ticket(data: str):
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database=Settings.S_database,
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
    app.run(host=Settings.a_host, port=Settings.a_port, debug=Settings.a_debug)


@app.route('/')
async def index(request):
    return await render("index.html")


@app.route("/login")
async def login(request):
    return await render("login.html")


@app.route("/client")
async def client(request):
    return await render("client.html")


@app.route('/ticket')
async def ticket(request, T_id=1):
    conn = await asyncpg.connect(
        host=Settings.S_host,
        port=Settings.S_port,
        database=Settings.S_database,
        user=Settings.S_user,
        password=Settings.S_password)
    temp = dict(await conn.fetchrow(''' SELECT * FROM "Tickets" WHERE id = $1''', T_id))
    await conn.close()
    return await render("ticket.html", context={"tick": temp})


@app.route('/screen')
async def screen(request):
    return await render("screen.html")


@app.route('/statistic')
@protected()
async def statistic(request):
    return await render("statistic.html")


@app.route('/admin')
async def admin(request):
    return await render("admin.html")


@app.route('/oper')
async def oper(request):
    return await render("oper.html")


@app.route('/volunteer')
async def volunteer(request):
    return await render("volunteer.html")


if __name__ == '__main__':
    loop.run_until_complete(nigger())
    loop.run_until_complete(init_tables())
    init()
