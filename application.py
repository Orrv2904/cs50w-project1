import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from flask import abort
from psycopg2 import paramstyle

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def log():
    #return "Project 1: TODO"
    return render_template("auth.html")

@app.route("/books", methods=['GET','POST'])
def books():
    if request.methods == 'GET':
        return render_template("index.html")


@app.route('/Auth')
def Auth():  
    return render_template("auth.html")

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        rname = request.form.get("name")
        remail = request.form.get("email")
        rpassword = request.form.get("password")
        hashed_password = generate_password_hash(rpassword)

        if not rname or not remail or not rpassword:
            flash("Por favor ingrese todos los campos", "info")
            return render_template("/Auth")

        try:
            verificar_usuario = text("SELECT EXISTS(SELECT 1 FROM users WHERE name = :rname)")
            verificar_correo = text("SELECT EXISTS(SELECT 1 FROM users WHERE email = :remail)")
            res2 = db.execute(verificar_usuario, {"rname" :rname})
            res3 = db.execute(verificar_correo, {"remail" :remail})
            user_exists = res2.fetchone()[0]
            email_exists = res3.fetchone()[0]

            if user_exists or email_exists:
                flash("El usuario o el correo electrónico ya existe", "error")
                return render_template("/Auth")
            
            agregar_usuario = text("INSERT INTO users (name, email, password) VALUES (:rname, :remail, :hashed_password)")
            db.execute(agregar_usuario, {"rname" :rname, "remail" :remail, "hashed_password" :hashed_password})
            db.commit()
            db.close()
            flash("Usuario registrado exitosamente", "success")
            return redirect('/Auth')
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            #flash("Ha ocurrido un error", "error")
            abort(404)
