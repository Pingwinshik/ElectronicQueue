from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tickets.db'
db = SQLAlchemy(app)


class Ticket(db.Model):
    type = db.Column(db.String(1), primary_key=False, nullable=False)
    id = db.Column(db.Integer, primary_key=False, nullable=False)
    room = db.Column(db.String(5), primary_key=False, nullable=False)
    counter = db.Column(db.Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return '<Ticket %r>' % self.counter


@app.route('/')
@app.route('/index')
def index():
    Otype = "Enzu"
    Oid = 911
    Oroom = "N/A"
    Oticket = Ticket(type=Otype, id=Oid, room=Oroom)
    try:
        db.session.add(Oticket)
        db.session.commit()
        return render_template("index.html")
    except:
        return "Zero-ticket error"


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/client', methods=['POST', 'GET'])
def client():
    db_output=Ticket.query.all()
    if request.method == "POST":
        t_type = request.form['type']
        t_room = request.form['room']
        t_id = (db_output[-1].counter)
        Temp = Ticket(type=t_type, id=t_id, room=t_room)

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


@app.route('/oper')
def oper():
    return render_template("oper.html")


if __name__ == '__main__':
    app.run(debug=True)
