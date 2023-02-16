from sanic import Sanic, redirect, Websocket
from sanic.response import json as jsr, html, text
from sanic_ext import render
from sanic_jwt.decorators import protected
import asyncpg
import asyncio
import websockets
import os
import Settings
import json

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
                room varchar(6) NOT NULL,
                operator_id smallint,
                status smallint  NOT NULL);'''
                       )
    await conn.execute('''CREATE TABLE IF NOT EXISTS "Operators" (id serial PRIMARY KEY,
                    room varchar (6) NOT NULL,
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



def init():
    app.run(host=Settings.a_host, port=Settings.a_port, debug=Settings.a_debug)


@app.websocket("/Tick_WS")
async def Serve_tick(request, ws: Websocket):
    while True:
        t_id = await ws.recv()
        conn = await asyncpg.connect(
            host=Settings.S_host,
            port=Settings.S_port,
            database=Settings.S_database,
            user=Settings.S_user,
            password=Settings.S_password)
        temp = dict(await conn.fetchrow(''' SELECT * FROM "Tickets" WHERE id = $1''', int(t_id)))
        await conn.close()
        data = json.dumps(temp)
        await ws.send(data)


@app.route('/ticket-listener/ticket/<num:int>')
async def ticket_listener(request, num: int):
    async with websockets.connect("ws://" + Settings.a_host + ":" + str(Settings.a_port) + "/Tick_WS") as ws:
        await ws.send(str(num))
        response = json.loads(await ws.recv())
        return jsr(response)


@app.websocket("/Op_WS")
async def Serve_op(request, ws: Websocket):
    while True:
        op_data = await ws.recv()
        conn = await asyncpg.connect(
            host=Settings.S_host,
            port=Settings.S_port,
            database=Settings.S_database,
            user=Settings.S_user,
            password=Settings.S_password)
        temp = await conn.fetchrow(''' SELECT room FROM "Operators" WHERE id = $1 ORDER BY id''', int(op_data))
        tickets = await conn.fetch('''SELECT type, number FROM "Tickets" WHERE room = $1 AND status !=3 ORDER BY id LIMIT 2;''', temp["room"])
        if len(tickets) == 2:
            resp = dict(one=dict(tickets[0]), two=dict(tickets[1]))
        elif len(tickets) == 1:
            resp = dict(one=dict(tickets[0]), two=None)
        else:
            resp = dict(one=None, two=None)
        await conn.close()
        data = json.dumps(resp)
        await ws.send(data)


@app.route('/op-listener/oper/<num:int>')
async def operator_listener(request, num: int):
    async with websockets.connect("ws://" + Settings.a_host + ":" + str(Settings.a_port) + "/Op_WS") as ws:
        await ws.send(str(num))
        response = json.loads(await ws.recv())
        return jsr(response)


@app.route('/')
async def index(request):
    return await render("index.html")


@app.route("/login")
async def login(request):
    return await render("login.html")


@app.route("/client", methods=['GET', 'POST'])
async def client(request):
    if request.method == 'GET':
        return await render("client.html")
    if request.method == 'POST':
        T_type = request.form.get("type")
        T_room = request.form.get("room")
        conn = await asyncpg.connect(
            host=Settings.S_host,
            port=Settings.S_port,
            database=Settings.S_database,
            user=Settings.S_user,
            password=Settings.S_password)
        temp = await conn.fetchrow(''' SELECT * FROM "Tickets" WHERE type = $1 ORDER BY id DESC''', T_type)
        if temp != None:
            T_number = (temp['number'])+1
        else:
            T_number = 1
        await conn.execute(''' INSERT INTO "Tickets"(type, number, room, operator_id, status) VALUES($1, $2, $3, $4, $5)''', T_type, T_number, T_room, None, 0)
        redr = await conn.fetchrow(''' SELECT id FROM "Tickets" WHERE type = $1 ORDER BY id DESC''', T_type)
        await conn.close()
        return redirect(app.url_for('ticket', num=redr['id']))


@app.route('/ticket/<num:int>')
async def ticket(request, num: int):
    async with websockets.connect("ws://" + Settings.a_host + ":" + str(Settings.a_port) + "/Tick_WS") as ws:
        await ws.send(str(num))
        response = json.loads(await ws.recv())
    return await render("ticket.html", context={"tick": response})


@app.route('/screen')
async def screen(request):
    return await render("screen.html")


@app.route('/stat')
async def statistic(request):
    return await render("stat.html")


@app.route('/admin')
async def admin(request):
    return await render("admin.html")


@app.route('/mine')
async def mine(request):
    return await render("mine.html")


@app.route('/oper/<num:int>', methods=['GET', 'POST'])
async def oper(request, num: int):
    if request.method == 'GET':
        conn = await asyncpg.connect(
            host=Settings.S_host,
            port=Settings.S_port,
            database=Settings.S_database,
            user=Settings.S_user,
            password=Settings.S_password)
        temp = await conn.fetchrow(''' SELECT room FROM "Operators" WHERE id = $1 ORDER BY id''', num)
        tickets = await conn.fetch('''SELECT * FROM "Tickets" WHERE room = $1 AND status !=3  ORDER BY id LIMIT 2;''', temp["room"])
        await conn.close()
        return await render("oper.html", context={"tickets": tickets})
    if request.method == 'POST':
        action = request.form.get("oper_action")
        if action == "1":
            conn = await asyncpg.connect(
                host=Settings.S_host,
                port=Settings.S_port,
                database=Settings.S_database,
                user=Settings.S_user,
                password=Settings.S_password)
            temp = await conn.fetchrow(''' SELECT room FROM "Operators" WHERE id = $1 ORDER BY id''', num)
            change = await conn.fetchrow('''SELECT id FROM "Tickets" WHERE room = $1 AND status !=3  ORDER BY id''', temp["room"])
            await conn.execute('''UPDATE "Tickets" SET status=3 WHERE id = $1 AND status !=3''', change["id"])
            await conn.close()
            return redirect(app.url_for('oper', num=num))

@app.route('/volunteer', methods=['GET', 'POST'])
async def volunteer(request):
    if request.method == 'GET':
        return await render("volunteer.html")
    if request.method == 'POST':
        T_type = request.form.get("type")
        T_room = request.form.get("room")
        conn = await asyncpg.connect(
            host=Settings.S_host,
            port=Settings.S_port,
            database=Settings.S_database,
            user=Settings.S_user,
            password=Settings.S_password)
        temp = await conn.fetchrow(''' SELECT * FROM "Tickets" WHERE type = $1 ORDER BY id DESC''', T_type)
        if temp != None:
            T_number = (temp['number'])+1
        else:
            T_number = 1
        await conn.execute(
            ''' INSERT INTO "Tickets"(type, number, room, operator_id, status) VALUES($1, $2, $3, $4, $5)''', T_type, T_number, T_room, None, 0)
        redr = await conn.fetchrow(''' SELECT id FROM "Tickets" WHERE type = $1 ORDER BY id DESC''', T_type)
        await conn.close()
        return redirect(app.url_for('ticket', num=redr['id']))


if __name__ == '__main__':
    loop.run_until_complete(nigger())
    loop.run_until_complete(init_tables())
    init()
    answer = input()
    if answer:
        os.system('pause')