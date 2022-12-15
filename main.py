from flask import Flask,render_template

app = Flask(__name__)

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

@app.route('/client')
def client():
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
