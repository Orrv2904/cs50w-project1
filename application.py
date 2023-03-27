import os

from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify, get_flashed_messages
import requests
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from flask import abort
from psycopg2 import paramstyle
from helpers import login_required
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
    if session.get("user_id") is None:
        return render_template("auth.html")
    else:
        return redirect("/books")
    #return render_template("auth.html")

@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    if request.method == "GET":
        try:
            user_id = session["user_id"]
            user_name_query = text("SELECT name FROM users WHERE id = :user_id")
            user_name = db.execute(user_name_query, {"user_id": user_id}).fetchone()[0]
            db.commit()
            return render_template("index.html", user_name=user_name)
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)
    elif request.method == "POST":
        libros = []
        try:
            search_term = request.form["search_term"]
            search_term = "%" + search_term+ "%"
            print(search_term)
            if not search_term:
                flash("Por favor ingrese todos los campos", "info")
                return redirect('/books')
            book_query = text("SELECT * FROM books WHERE isbn = :search_term OR title LIKE :search_term OR author LIKE :search_term OR year = :search_term")
            books = db.execute(book_query, {"search_term": f"%{search_term}%"}).fetchall()
            if books:
                for book in books:
                    api = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + book[1]).json()
                    if "items" in api:
                        for item in api["items"]:
                            book_info = item.get("volumeInfo")
                            if book_info:
                                book_description = book_info.get("description")
                                if book_description:
                                    break
                        book_img = book_info.get("imageLinks", {}).get("thumbnail")
                    else:
                        book_img = None
                        book_description = None
                    book = {
                        "image_link": book_img,
                        "description": book_description,
                        "title": book[2],
                        "author": book[3],
                        "isbn": book[1],
                        "year": book[4]
                    }
                    libros.append(book)
                user_id = session["user_id"]
                user_name_query = text("SELECT name FROM users WHERE id = :user_id")
                user_name2 = db.execute(user_name_query, {"user_id": user_id}).fetchone()[0]
                db.commit()
                return render_template("index.html", books=libros, user_name2=user_name2)
            else:
                flash("El libro no fue encontrado", "error")
                return render_template("index.html", user_name2=user_name2)
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)


@app.route('/review', methods=["GET", "POST"])
def review():
    if request.method == "GET":
        return render_template("review.html")


@app.route('/book_details/<string:isbn>', methods=["GET", "POST"])
@login_required
def book_details(isbn):
    if request.method == "POST":
        try:
            print(isbn)
            # isbn = request.form["isbn"]
            # isbn = "%" + isbn "%"
            return render_template("review.html")
           
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)

        

    


@app.route('/flasherror')
def flasherror():
    return render_template("index.html")





@app.route('/Auth')
def Auth():  
    return render_template("auth.html")

def validar_contraseña(password):
    if len(password) < 10:
        return "La contraseña debe tener al menos 10 caracteres"
    if not any(char.isdigit() for char in password):
        return "La contraseña debe contener al menos un número"
    if not any(char.isalpha() for char in password):
        return "La contraseña debe contener al menos una letra"
    common_passwords = ["123456", "password", "123456789", "12345678", "12345"]
    if password.lower() in common_passwords:
        return "La contraseña es demasiado común"
    return None

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
            #print("Error: ", str(e))
            #flash("Ha ocurrido un error", "error")
            #abort(404)
            return redirect('/Auth')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        lemail = request.form.get("email")
        lpassword = request.form.get("password")
    if not request.form.get("email") or not request.form.get("password"):
        return redirect(url_for("auth"))
    try:
        seleccionar_usuario = text("SELECT * FROM users WHERE email=:email")
        res = db.execute(seleccionar_usuario, {'email': lemail})
        print(res)
        user = res.fetchone()
        print(user)
        db.commit()
        db.close()
        if user and check_password_hash(user[3], lpassword):
            session["user_id"] = user[0]
            return redirect("/books")
        else:
            error = "Correo electrónico o contraseña incorrecta, favor verifique sus datos"
            return render_template("auth.html", error=error)
    except Exception as e:
        db.rollback()
        print("Error: ", str(e))
        abort(404)


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
