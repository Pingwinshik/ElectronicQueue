from quart import g, Quart, render_template, request
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response
from dataclasses import dataclass

app = Quart(__name__)
QuartDB(app, url="sqlite:///Tickets.db")
QuartSchema(app)


@dataclass
class Ticket:
    counter: int
    litera: str
    id: int
    room: str
    status: int

@dataclass
class Tickets:
    alltickets: list[Ticket]


async def get_tickets() -> Tickets:
    query = """SELECT counter, litera, id, room, status
                from tickets"""
    tickets =[
        Ticket(**row)
        async for row in g.connection.iterate(query)
    ]
    return Tickets(alltickets=tickets)



admin_login = "admin"
oper_login = "oper"
volunteer_login = "volunteer"
admin_password = "password"


@app.route("/")
@app.route("/index")
async def index():
    return await render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
async def login():
    return await render_template("oper.html")




@app.route('/client', methods=['POST', 'GET'])
async def client():
    return await render_template("client.html")


@app.route('/ticket')
async def queue():
    return await render_template("ticket.html")


if __name__ == '__main__':
    app.run(host='192.168.50.186', debug=True, port=1911)
