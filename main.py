import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, g, url_for
from os import urandom

cluster = MongoClient(
    "mongodb+srv://sundar:Password@cluster0.hid9c.mongodb.net/<student>?retryWrites=true&w=majority")

db = cluster["student"]
collection = db["test"]
letter = db["test"]
faculty = db["test"]

app = Flask(__name__)
app.secret_key = urandom(30)


@app.route("/")
def home():
    return render_template("land.html")


@app.route("/login")
def login():
    return render_template("loginpage.html")


@app.route("/signup", methods=['GET'])
def signup():
    return render_template("signup.html")


@app.route("/signform", methods=['POST'])
def sign():
    user = {
        'first_name': request.form.get('first-name'),
        'last_name': request.form.get('last-name'),
        'year': request.form.get('se11'),
        'branch': request.form.get('sel2'),
        'section': request.form.get('sel3'),
        'roll_no': request.form.get('roll-no'),
        'emai_id': request.form.get('exampleInputEmail1'),
        'phone_no': request.form.get('pno'),
        'password': request.form.get('exampleInputPassword1')
    }

    db.collection.insert_one(user)
    return render_template("loginpage.html")


@app.route("/log", methods=['POST'])
def log():
    if request.method == 'POST':
        session.pop('user', None)

        p_users = db.collection.find_one({'emai_id': request.form["email"]})
        if p_users:
            if request.form.get("pwd") == p_users["password"]:
                session['user'] = request.form['email']
                return redirect(url_for('stdpanel'))
        else:
            f_users = db.faculty.find_one({'email': request.form["email"]})
            if f_users:
                if request.form.get("pwd") == f_users["password"]:
                    session['user'] = request.form['email']
                    return redirect(url_for('adminpanel'))

    return "Invalid email or password"


@app.route('/stdpanel')
def stdpanel():
    if g.user:
        values = db.collection.find_one({'emai_id': session['user']})
        lett = db.letters.find_one({'roll_no': values['roll_no']})
        return render_template("student panel.html", user=session["user"], values=values, lett=lett)

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/subletter', methods=['POST'])
def subletter():
    if request.method == 'POST':
        let = {
            'name': request.form.get('name'),
            'sub': request.form.get('sub'),
            'body': request.form.get('input'),
            'roll_no': request.form.get('roll_no'),
            'std_email': request.form.get('std_email'),
            'fac_email': request.form.get('fac_email'),
            'fac_name': request.form.get('fac'),
            'isAccepted': False,
            'progress': 1
        }
        db.letter.insert_one(let)
        return "Letter submitted"

    return "Please check again"


@app.route('/adminpanel')
def adminpanel():
    if g.user:
        values = db.faculty.find_one({'email': session['user']})
        let = db.letter.find_one({'fac_name': values['fac_name']})

        return render_template("facultypanel.html", user=session["user"], values=values, let=let)

    return redirect(url_for('login'))


@app.route('/accept')
def accept():
    let = db.letter.find_one({'fac_email': g.user})
    existing = let['progress']
    db.letter.update({'fac_email': g.user}, {
                     '$set': {"isAccepted": True, "progress": existing+1}})
    return redirect(url_for('adminpanel'))


@ app.route('/lettertrack')
def lettertrack():
    values = db.collection.find_one({'emai_id': g.user})
    val = db.letter.find_one({'std_email': g.user})
    return render_template("lettertrack.html", val=val, values=values)


@ app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']
