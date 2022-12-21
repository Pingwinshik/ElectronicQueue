import qrcode
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tickets.db'
db = SQLAlchemy(app)


class Ticket(db.Model):
    type = db.Column(db.String(1), primary_key=False, nullable=False)
    id = db.Column(db.Integer, primary_key=False, nullable=False)
    room = db.Column(db.String(5), primary_key=False, nullable=False)
    status = db.Column(db.Boolean, primary_key=False, nullable=False)
    counter = db.Column(db.Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return '<Ticket %r>' % self.counter


operator_existance = False

admin_login = "admin"
oper_login = "oper"
volunteer_login = "volunteer"
admin_password = "password"
room_id = {
    '1-102': 1,
    '1-105': 2,
    '1-106': 3,
    '1-109': 4,
    '1-110': 5,
    '1-113': 6,
    '1-123': 7,
    '1-127': 8,
    '1-130': 9,
    '1-140': 10,
    '1-143': 11,
    '1-143а': 12,
    '1-149': 13,
    '1-161': 17,
    '1-165': 18,
    '1-177': 19,
    '1-186Б': 20,
    '1-193Б': 21,
    '1-193А': 22,
    '1-193': 23,
}


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        db_output = Ticket.query.all()
        if (request.form.get('username')):
            if (request.form['username'] == admin_login and request.form['password'] == admin_password):
                return render_template("admin.html", tickets=db_output, count=len(db_output))
            elif (request.form['username'] == oper_login and request.form['password'] == admin_password):
                tester = []
                global operator_existance
                operator_existance = True
                for elem in db_output:
                    if elem.status == True:
                        tester.append(elem)
                return render_template("oper.html", tickets=tester, count=len(tester))
            elif (request.form['username'] == volunteer_login and request.form['password'] == admin_password):
                return render_template("volunteer.html")
            else:
                return render_template("login.html")
        if (request.form.get('adm_action')):
            if request.form['adm_action'] == "1":
                Ticket.query.delete()
                db.session.commit()
                db_output = Ticket.query.all()
                return render_template("admin.html", tickets=db_output, count=len(db_output))
            if request.form['adm_action'] == "2":
                db_output = Ticket.query.all()
                return render_template("admin.html", tickets=db_output, count=len(db_output))
            if request.form['adm_action'] == "3":
                t_output = open('TicketList.txt', 'w')
                for N in range(0, len(db_output)):
                    unt = db_output[N].type + '-' + str('{:03}'.format(db_output[N].id))
                    t_output.write(
                        ', '.join((str(db_output[N].counter), unt, db_output[N].room, str(db_output[N].status), "\n")))
                return render_template("admin.html", tickets=db_output, count=len(db_output))
        else:
            tester = []
            for elem in db_output:
                if elem.status == True:
                    tester.append(elem)
            if not tester:
                return render_template("oper.html", tickets=tester, count=len(tester))
            else:
                t_disable = tester[0].counter
                change = Ticket.query.get(t_disable)
                change.status = False
                db.session.commit()
                db_output = Ticket.query.all()
                tester = []
                for elem in db_output:
                    if elem.status == True:
                        tester.append(elem)
                return render_template("oper.html", tickets=tester, count=len(tester))
    else:
        return render_template("login.html")


@app.route('/client', methods=['POST', 'GET'])
def client():
    db_output = Ticket.query.all()
    tester = []
    if request.method == "POST":
        t_type = request.form['type']
        t_room = request.form['room']
        if not db_output:
            t_id = 1
        else:
            for elem in db_output:
                if elem.type == t_type:
                    tester.append(elem)
            if not tester:
                t_id = 1
            else:
                t_id = (tester[-1].id + 1)
        Temp = Ticket(type=t_type, id=t_id, room=t_room, status=True)
        try:
            db.session.add(Temp)
            db.session.commit()
            db_output = Ticket.query.all()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=25,
                border=4,
            )
            code = "" + request.base_url[:-7] + "/ticket?val=" + str(db_output[-1].counter - 1)
            qr.add_data(code)
            qr.make(fit=True)

            img = qr.make_image(fill_color=(90,135,233), back_color=(255,255,255))
            img.save("static/ticketQR.png", "PNG")
            return render_template("ticket.html", tickets=db_output[-1], val=db_output[-1].counter, nav=room_id[db_output[-1].room])
        except:
            return "Generation error"
    else:
        return render_template("client.html", tickets=db_output)


@app.route('/ticket')
def queue():
    val = int(request.args.get('val'))
    db_output = Ticket.query.all()
    return render_template("ticket.html", tickets=db_output[val], nav=room_id[db_output[val].room])

@app.route('/screen')
def screen():
    if operator_existance == False:
        start = 0
    else:
        start = 1
    db_output = Ticket.query.all()
    tester = []
    for elem in db_output:
        if elem.status == True:
            tester.append(elem)
    return render_template("screen.html", tickets=tester, temp=len(tester), OP=operator_existance, start=start)


@app.route('/volunteer')
def volonter():
    return render_template("volunteer.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=2554)
