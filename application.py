import os
import re

from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify, get_flashed_messages, current_app
import requests
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from authlib.integrations.flask_client import OAuth
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
engine = create_engine(os.getenv("DATABASE_URL"), pool_size=20, max_overflow=30)
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
            user_id = session["user_id"]
            user_name_query = text("SELECT name FROM users WHERE id = :user_id")
            user_name = db.execute(user_name_query, {"user_id": user_id}).fetchone()[0]
            search_term = request.form["search_term"]
            search_term = search_term.title()
            print(search_term)
            if not search_term:
                flash("Por favor ingrese todos los campos", "info")
                return redirect('/books')
            book_query = text("SELECT * FROM books WHERE LOWER(isbn) LIKE LOWER(:search_term) OR LOWER(title) LIKE LOWER(:search_term) OR LOWER(author) LIKE LOWER(:search_term) OR year LIKE :search_term")
            books = db.execute(book_query, {"search_term": f"%{search_term.lower()}%"}).fetchall()
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
                        book_img = "https://via.placeholder.com/128x196?text=Image+Not+Available"
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
                db.commit()
                flash("Coincidencias encontradas correctamente", "success")
                messages = get_flashed_messages()
                print(messages)
                return render_template("index.html", books=libros, user_name=user_name)
            else:
                flash("No encontramos registros similares a su busqueda", "info")
                messages = get_flashed_messages()
                print(messages)
                return render_template("index.html")
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)


@app.route('/autocomplete')
@login_required
def autocomplete():
    search_term = request.args.get('search_term', '')
    search_term = search_term.title()
    books_query = text("SELECT * FROM books WHERE isbn = :search_term OR title LIKE :search_term OR author LIKE :search_term OR year = :search_term")
    books = db.execute(books_query, {'search_term': f'%{search_term}%'}).fetchall()
    results = [{'title': book[2]} for book in books]
    return jsonify(results)







@app.route('/review', methods=["GET", "POST"])
@login_required
def review():
    if request.method == "GET":
        return render_template("review.html")


@app.route('/book_details/<string:isbn>', methods=["GET", "POST"])
@login_required
def book_details(isbn):
    if request.method == "POST":
        try:
            review_data_query = text("SELECT r.score, r.comment, u.name, AVG(r.score) as avg_score, COUNT(r.score) as review_count FROM review r JOIN users u ON r.user_id = u.id WHERE r.isbn = :isbn GROUP BY r.score, r.comment, u.name")
            review_data = db.execute(review_data_query, {"isbn": isbn}).fetchall()
            review_data_query2 = text("""
            SELECT AVG(r.score) as avg_score, COUNT(r.score) as review_count
            FROM review r
            WHERE r.isbn = :isbn
            """)
            review_data2 = db.execute(review_data_query2, {"isbn": isbn}).fetchone()
            avg_score = review_data2.avg_score or 0
            review_count = review_data2.review_count or 0



            api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            api_response = requests.get(api_url)
            if api_response.status_code == 200:
                book_info = api_response.json()["items"][0]["volumeInfo"]
                book_description = book_info.get("description", "Descripción no disponible.")
                book_img = book_info.get("imageLinks", {}).get("thumbnail", "/static/images/128x196.png")
                book_title = book_info.get("title", "Título no disponible.")
                book_author = book_info.get("authors", ["Autor no disponible."])[0]
                book_year = book_info.get("publishedDate", "Año de publicación no disponible.")
                book_rating = book_info.get("averageRating", 0)
                book_rating_count = book_info.get("ratingsCount", 0)
                return render_template("review.html",
                       book_title=book_title,
                       book_author=book_author,
                       book_year=book_year,
                       book_description=book_description,
                       book_img=book_img,
                       book_rating=book_rating,
                       book_rating_count=book_rating_count,
                       isbn=isbn,
                       review_data=review_data,
                       review_data2=review_data2,
                       avg_score=avg_score,
                       review_count=review_count)
            else:
                flash("El libro no fue encontrado", "error")
                return redirect(url_for('index'))
        except Exception as e:
            print("Error: ", str(e))
            flash("Ocurrió un error al procesar su solicitud. Por favor inténtelo de nuevo más tarde.", "error")
            return redirect(url_for('index'))
    else:
        # return render_template("review.html")
        print("prueba")
        try:
            review_data_query = text("SELECT r.score, r.comment, u.name, AVG(r.score) as avg_score, COUNT(r.score) as review_count FROM review r JOIN users u ON r.user_id = u.id WHERE r.isbn = :isbn GROUP BY r.score, r.comment, u.name")
            review_data = db.execute(review_data_query, {"isbn": isbn}).fetchall()
            review_data_query2 = text("""
            SELECT AVG(r.score) as avg_score, COUNT(r.score) as review_count
            FROM review r
            WHERE r.isbn = :isbn
            """)
            review_data2 = db.execute(review_data_query2, {"isbn": isbn}).fetchone()
            avg_score = review_data2.avg_score or 0
            review_count = review_data2.review_count or 0

            api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            api_response = requests.get(api_url)
            if api_response.status_code == 200:
                book_info = api_response.json()["items"][0]["volumeInfo"]
                book_description = book_info.get("description", "Descripción no disponible.")
                book_img = book_info.get("imageLinks", {}).get("thumbnail", "/static/images/128x196.png")
                book_title = book_info.get("title", "Título no disponible.")
                book_author = book_info.get("authors", ["Autor no disponible."])[0]
                book_year = book_info.get("publishedDate", "Año de publicación no disponible.")
                book_rating = book_info.get("averageRating", 0)
                book_rating_count = book_info.get("ratingsCount", 0)
                return render_template("review.html",
                                       book_title=book_title,
                                       book_author=book_author,
                                       book_year=book_year,
                                       book_description=book_description,
                                       book_img=book_img,
                                       book_rating=book_rating,
                                       book_rating_count=book_rating_count,
                                       isbn=isbn,
                                       review_data=review_data,
                                       review_data2=review_data2,
                                       avg_score=avg_score,
                                       review_count=review_count)
            else:
                flash("El libro no fue encontrado", "error")
                return redirect(url_for('index'))
        except Exception as e:
            print("Error: ", str(e))
            flash("Ocurrió un error al procesar su solicitud. Por favor inténtelo de nuevo más tarde.", "error")
            return redirect(url_for('index'))
            # return redirect(url_for(f'book_details/{isbn}'))

        
@app.route('/create_review', methods=["POST", "GET"])
@login_required
def create_review():
    if request.method == "POST":
        user_id = session["user_id"]
        risbn = request.form.get("isbn")
        rraiting = request.form.get("rating")
        rcomment = request.form.get("comment")

        review_query = text("SELECT * FROM review WHERE user_id = :user_id AND isbn = :risbn")
        review = db.execute(review_query, {"user_id": user_id, "risbn": risbn}).fetchone()

        if review:
            error = "Ya has creado una review para este libro"
            flash("Ya has creado una review para este libro", "info")
            messages = get_flashed_messages()
            print(messages)
            print(error)
            return redirect(f'/book_details/{risbn}')

        if not risbn or not rraiting or not rcomment:
            error = "Complete los campos faltantes"
            flash("Complete los campos faltantes", "error")
            messages = get_flashed_messages()
            print(messages)
            return render_template('/book_details/<string:isbn>', error=error)

        try:
            
            createreview = text("INSERT INTO review (user_id, isbn, score, comment) VALUES (:user_id, :risbn, :rraiting, :rcomment)")
            db.execute(createreview, {"user_id" :user_id, "risbn" :risbn, "rraiting" :rraiting, "rcomment" :rcomment})
            db.commit()
            db.close()
            flash("Review creada correctamente", "success")
            messages = get_flashed_messages()
            print(messages)
            return redirect(f'/book_details/{risbn}')
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            flash("Ocurrió un error al procesar su solicitud", "error")
            return render_template('/book_details/<string:isbn>')

    else:
        return redirect('/book_details/<string:isbn>')


@app.route('/api/<isbn>')
def get_book_info(isbn):
    book_query = text("""
        SELECT b.author, b.title, b.year, b.isbn, AVG(r.score) AS average_score, COUNT(r.id) AS review_count
        FROM books AS b
        LEFT JOIN review AS r ON b.isbn = r.isbn
        WHERE b.isbn = :isbn
        GROUP BY b.author, b.title, b.year, b.isbn
    """)
    book_result = db.execute(book_query, {"isbn": isbn}).fetchone()

    if book_result is not None:
        author = book_result[0]
        title = book_result[1]
        year = book_result[2]
        isbn_10 = book_result[3]
        review_count = book_result[5]

        if book_result[4] is not None:
            average_score = round(book_result[4], 2)
        else:
            average_score = None

        response_data = {
            'title': title,
            'author': author,
            'year': year,
            'isbn': isbn_10,
            'review_count': review_count,
            'average_score': average_score
        }

        return jsonify(response_data)
    else:
        response_data = {
            'mensaje': f'El libro con ISBN {isbn} no se encuentra en nuestra base de datos.'
        }

        return jsonify(response_data), 404






    

@app.route('/review_data', methods=["GET"])
def review_data():
    if request.method == "GET":
        try:
            review_data = text("SELECT r.score, r.comment, u.name FROM review r JOIN users u ON r.user_id = u.id WHERE r.isbn = :isbn")
            review_data = db.execute(review_data, {"isbn": j}).fetchall()
            print(review_data)
            db.commit()
            return render_template("/book_details/<string:isbn>", review_data=review_data)
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
    common_passwords = ["123456", "password", "123456789", "12345678", "12345", "contraseña"]
    if password.lower() in common_passwords:
        return "La contraseña es demasiado común"
    return None


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        rname = request.form.get("name").lower()
        remail = request.form.get("email").lower()
        rpassword = request.form.get("password")
        hashed_password = generate_password_hash(rpassword)

        email_regex = r"^[a-zA-Z0-9._%+-]+@(gmail|outlook|yahoo|Gmail|Outlook|Yahoo)\.(com|edu|net)$"
        if not re.match(email_regex, remail):
            flash("Ingrese un correo electrónico válido (Gmail, Outlook, Yahoo)", "info")
            return render_template("auth.html")

        error_msg = validar_contraseña(rpassword)
        if error_msg:
            flash(error_msg, "info")
            return render_template("auth.html")

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

# oAuth Setup
# This only works on deploy
oauth = OAuth(app)


google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params={
        "scope": "openid email profile",
        "prompt": "select_account",
        "hd": "your_domain.com",  # optional: restrict login to a specific domain
        "redirect_uri": "https://books-ffiv.onrender.com/"  # your redirect URL
    },
    api_base_url="https://openidconnect.googleapis.com/",
    client_kwargs={"scope": "openid email profile"}
)


@app.route('/google_login')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/google_authorize')
def google_authorize():
    token = google.authorize_access_token()
    user = google.parse_id_token(token)
    email = user['email']
    try:
        verificar_correo = text("SELECT EXISTS(SELECT 1 FROM users WHERE email = :email)")
        res = db.execute(verificar_correo, {"email" :email})
        email_exists = res.fetchone()[0]

        if email_exists:
            flash("El correo electrónico ya existe", "error")
            return redirect(url_for('Auth'))

        agregar_usuario = text("INSERT INTO users (name, email) VALUES (:name, :email)")
        db.execute(agregar_usuario, {"name" :user['name'], "email" :user['email']})
        db.commit()

        session['profile'] = user
        session.permanent = True
        return redirect('/')
    except Exception as e:
        db.rollback()
        print("Error: ", str(e))
        flash("Ha ocurrido un error", "error")
        abort(404)

@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session['user_id']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        try:
            user_query = text("SELECT * FROM users WHERE id = :user_id")
            user = db.execute(user_query, {'user_id': user_id}).fetchone()

            if not check_password_hash(user.password, old_password):
                flash('La contraseña anterior es incorrecta.', 'error')
                return redirect('/change_password')

            if new_password != confirm_password:
                flash('La nueva contraseña y la confirmación no coinciden.', 'error')
                return redirect('/change_password')

            password_error = validar_contraseña(new_password)
            if password_error:
                flash(password_error, 'error')
                return redirect('/change_password')

            new_password_hash = generate_password_hash(new_password)
            update_query = text("UPDATE users SET password = :password WHERE id = :user_id")
            db.execute(update_query, {'password': new_password_hash, 'user_id': user_id})
            db.commit()

            flash('La contraseña ha sido actualizada correctamente.', 'success')
            return redirect('/change_password')

        except Exception as e:
            db.rollback()
            print('Error:', str(e))
            abort(500)

    elif request.method == "GET":
        try:
            user_id = session["user_id"]
            user_query = text("SELECT name, email, password FROM users WHERE id = :user_id")
            user = db.execute(user_query, {'user_id': user_id}).fetchone()
            user_name = user[0]
            user_email = user[1]
            user_password_hash = user[2]
            db.commit()
            return render_template("change_password.html", user_name=user_name, user_email=user_email)
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)

@app.route('/record', methods=['GET'])
@login_required
def record():
    if request.method == "GET":
        try:
            user_id = session["user_id"]
            user_name_query = text("SELECT name FROM users WHERE id = :user_id")
            user_name = db.execute(user_name_query, {"user_id": user_id}).fetchone()[0]
            reviews_query = text("SELECT users.name, books.isbn, review.score, review.comment FROM review JOIN users ON review.user_id = users.id JOIN books ON review.isbn = books.isbn WHERE user_id = :user_id")
            reviews = db.execute(reviews_query, {'user_id': user_id}).fetchall()
            db.commit()
            return render_template("record.html", reviews=reviews, user_name=user_name)
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            abort(404)


