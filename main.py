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


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")



@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    db_output = Ticket.query.all()
    if request.method == "POST":
        action = request.form['adm_action']
        if action == "1":
            Ticket.query.delete()
            db.session.commit()
            db_output = Ticket.query.all()
            return render_template("admin.html", tickets=db_output, count=len(db_output))
        if action == "2":
            db_output = Ticket.query.all()
            return render_template("admin.html", tickets=db_output, count=len(db_output))
        if action == "3":
            t_output = open('TicketList.txt', 'w')
            for N in range(0, len(db_output)):
                unt = db_output[N].type + '-' + str('{:03}'.format(db_output[N].id))
                t_output.write(', '.join((str(db_output[N].counter), unt, db_output[N].room, str(db_output[N].status), "\n")))
            return render_template("admin.html", tickets=db_output, count=len(db_output))
    else:
        return render_template("admin.html", tickets=db_output, count=len(db_output))


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
            return render_template("ticket.html", tickets=db_output)
        except:
            return "Generation error"
    else:
        return render_template("client.html", tickets=db_output)


@app.route('/ticket')
def queue():
    db_output = Ticket.query.all()
    return render_template("ticket.html", tickets=db_output)


@app.route('/volunteer')
def volonter():
    return render_template("volunteer.html")


@app.route('/oper', methods=['POST', 'GET'])

def oper():
    db_output = Ticket.query.all()
    tester = []
    if request.method == "POST":
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
        for elem in db_output:
            if elem.status == True:
                tester.append(elem)
        return render_template("oper.html", tickets=tester, count=len(tester))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=2554)
