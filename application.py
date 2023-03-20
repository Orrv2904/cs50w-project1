import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
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
        search_term = request.form["search_term"]
        book_query = text("SELECT * FROM books WHERE isbn = :search_term OR title LIKE :search_term OR author LIKE :search_term OR year = :search_term")
        book = db.execute(book_query, {"search_term": search_term}).fetchone()
        if book:
            # Book found in database, use database information
            book_info = {
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "year": book.year,
                "published_date": book.published_date,
                "description": book.description,
                "thumbnail": book.thumbnail,
                "isbn": book.isbn,
                "buy_link": book.buy_link
            }
            return render_template("book.html", book=book_info)
        else:
            # Book not found in database, use Google Books API
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}&key={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    book_data = data["items"][0]["volumeInfo"]
                book_info = {
                    "title": book.title if book else book_data.get("title", ""),
                    "author": book.author if book else ", ".join(book_data.get("authors", [])),
                    "publisher": book.publisher_name if book else book_data.get("publisher", ""),
                    "published_date": book.published_date if book else book_data.get("publishedDate", ""),
                    "description": book.description if book else book_data.get("description", ""),
                    "thumbnail": book.thumbnail if book else book_data["imageLinks"].get("thumbnail", ""),
                    "isbn": book.isbn if book else book_data["industryIdentifiers"][0].get("identifier", ""),
                    "buy_link": book.buy_link if book else book_data.get("buyLink", "")
                }
                return render_template("book.html", book=book_info)
            else:
                flash(f"No books found for search term '{search_term}'")
                return redirect(url_for("books")) # Redirect to the search page if no books were found.






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
