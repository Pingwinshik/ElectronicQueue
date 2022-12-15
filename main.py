from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tickets.db'
db = SQLAlchemy(app)


class Ticket(db.Model):
    type = db.Column(db.String(1), primary_key=False, nullable=False)
    id = db.Column(db.Integer, primary_key=False, nullable=False)
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


@app.route('/admin')
def admin():
    return render_template("admin_ui.html")


@app.route('/client', methods=['POST', 'GET'])
def client():
    if request.method == "POST":
        t_type = request.form['type']
        t_id = request.form['id']
        Temp = Ticket(type=t_type, id=t_id)

        try:
            db.session.add(Temp)
            db.session.commit()
            return null
        except:
            return "Generation error"
    else:
        return render_template("client_ui.html")


@app.route('/queue')
def queue():
    return render_template("queue.html")


@app.route('/volonter')
def volonter():
    return render_template("volonter_ui.html")


@app.route('/oper')
def oper():
    return render_template("oper_ui.html")


if __name__ == '__main__':
    app.run(debug=True)