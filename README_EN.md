# Project 1 Books

Web Programming with Python and JavaScript
##
This project consists of an application where users can register their accounts and log in to the site. They will also be able to search for a book either by the ISBN number of the book, the title of the book or the author of the book. Each book will have its own section to send and display reviews.

[You can see the Deploy here](https://books-ffiv.onrender.com)

Table of Contents
     <ol>
    <li><a href="#tecnologias">Technologies used</a></li>
    <li><a href="#como_funciona">How does it work?</a></li>
    <li><a href="#instalacion">Installation</a></li>
    <li><a href="#ejecucion">Execution</a></li>
  </ol>

<input type="hidden" id="tecnologias" value="">

## Tecnologías que se usaron:

<p align="center">
  <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://badge.fury.io/py/flask"><img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-316192.svg?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://badge.fury.io/py/psycopg2"><img src="https://img.shields.io/badge/psycopg2-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="psycopg2"></a>
  <a href="https://badge.fury.io/py/HTML"><img src="https://img.shields.io/badge/HTML-239120?style=flat-square&logo=html5&logoColor=white" alt="HTML"></a>
  <a href="https://badge.fury.io/py/sass"><img src="https://img.shields.io/badge/Sass-CC6699?style=flat-square&logo=sass&logoColor=white" alt="Sass"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript"></a>
</p>

1. <b>Python</b>: It was used to create the tables by means of models using ORM, as well as to import all the information of the books contained in a CSV.

2. <b>Flask</b>: It was used for the creation of the whole application, to be more specific in the creation of the routes and functionalities of the application.

3. <b>PostgreSQL</b>: It was used to store all the information received from our application.

4. <b>HTML</b>: It was used for the creation of our templates that are displayed in the client view.

5. <b>SASS</b>: It was used to improve efficiency in writing CSS styles.

6. <b>JavaScript</b>: It was used to improve the appearance of the views and to give some extra functionalities.

## 

<input type="hidden" id="como_funciona" value="">

## ¿Comó Funciona?

It works as follows:

<details><summary><b>Account Creation and Login</b></summary>
To create the account the user will only have to enter the requested data, which are <b>User Name, Current Email Address and Password</b>,
Once your account is created, you will be redirected to the same view to log in with the account you have just created.
</details>
<details><summary><b>Search</b></summary>
Once the user has logged into the site, the application will redirect him/her to a search engine where he/she can search for a book by <b>ISBN, Author or Title</b>, where the application will return a list of all the books in our database and will return a template containing the information of the books that match the search parameter entered by the user. 
of all the books in our database and will return a template containing the information of the books that match the search parameter entered by the user.
</details>
<details><summary><b>Review</b></summary>
When the user has searched for the book he/she wants to know the information about, the user can click on each book by means of a button or either by the image or the title, where he/she will be redirected to another view.
in which you will be able to see the reviews of former users and you can add your own review of the book, <b style="background-color: yellow; padding: 5px;">NOTE</b>: The user will only be able to add one review per book since the registration will be done by <b>ISBN</b>.
</details>
<details><summary><b>API Access</b></summary>
If the user wants to know the details of a book, just add the following path to the <b>URL</b> of the browser:

```
/api/#ISBN
```
Where it will return information of the <b>ISBN</b> you are searching for, showing you something similar to this:
```
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
 }
```

</details>


##

<input type="hidden" id="instalacion" value="">

## Instalación:

* In order to run the application you will need to have an IDE installed, I recommend you to use Visual Studio Code since this is the IDE in which the application was created. You can download it here: [VS Code](https://code.visualstudio.com/docs/?dv=win).
Afterwards, you will have to clone or download our repository. You can do it with this command:
```
Git Clone https://github.com/Orrv2904/cs50w-project1.git
```
* Once downloaded, you can access it through the Windows CMD or, if you prefer, you can use ```MINGW64``` and then run the command ```Code .``` to open it in VS Code.

* Now you must install the <b>dependencies</b> of our program. To do this, you will need to open a terminal inside VS Code. You can open it from the top menu by selecting "Terminal" and then "New Terminal", or by pressing the key combination ```Ctrl + Shift + ``` if you are on Windows or Linux, or ```Cmd + Shift +``` if you are on Mac.
* Inside this terminal, you must install ```pip``` if you do not already have it installed. To do this, run the following command: ```pip install pip```. Normally, pip comes installed with Python. If you don't already have Python installed, you can learn how to do it by reading [here](https://tutorial.djangogirls.org/es/python_installation/).
* Then, you must create a <b>Virtual Environment</b> using the following command: ```python -m venv env```. To activate it, run this other command: ```.\env\Scripts\activate```.
* If you get an error and it won't let you install, you should put this command: ```Set-ExecutionPolicy RemoteSigned -Scope CurrentUser``` and then try again.
* Now you will need to install our dependencies found in our <b>requirements.txt</b> file. To do this, run ```pip install -r .\requirements.txt``` and wait for the installation to finish.
* Afterwards, you must create a file called <b>.env</b> where it will contain all the environment variables that our application will use. You can create it manually or you can also execute this command: ```touch .env```. Inside this file, you will have to write the variables that are in ```.env.templates```, which are as follows:
```
DATABASE_URL=
FLASK_DEBUG=
FLASK_APP= 
```
<b style="background-color: yellow; padding: 5px;">NOTE:</b> Before each variable, you should prepend export. This is to indicate that the specified environment variable will be exported to any secondary process launched from the current terminal.
In the variable ```DATABASE_URL=``` you must enter the ```URL``` of your database <b>PostgreSQL</b> created in [RailWay](https://railway.app/) or in [Render](https://render.com/). If you want to know more about this you can read more here [RailWay](https://ekomenyong.com/insights/how-to-setup-free-postgresql-database-on-railway-app) and [Render](https://medium.com/geekculture/how-to-create-and-connect-to-a-postgresql-database-with-render-and-pgadmin-577b326fd19d).

Now you will need to obtain the connection string from Railway or Render. To do this, you will need to create your account and create the database as mentioned above.
* Railway has a section called ```Connect``` in which you must be in the database you want to use. You must select this option:  ![01](https://user-images.githubusercontent.com/82064182/229641462-89e7c60a-e30a-43f4-8287-9fa401e1f295.png)

* In Render, you must select the external connection string. ![02](https://user-images.githubusercontent.com/82064182/229641700-5d0ba55a-6f44-438f-a456-0fbb8e300b8e.png)

Once this connection string is obtained, you must paste it in the <b>DATABASE_URL=</b> variable, obtaining a result similar to this one:```export DATABASE_URL=postgresql://postgres:PASSSWORD@HOST:PORT/USER```.

* And in <b>FLASK_DEBUG= and FLASK_APP=</b> you must add this: ```
    FLASK_DEBUG=1
    FLASK_APP=application.py```
    
* To finish in this section you must create the tables and enter the data to the database, to do this you must execute the following commands in the terminal: 
  ```
     python -m create_tables
  ```
  Y 
  ```
     python -m import
  ```

##

<input type="hidden" id="ejecucion" value="">

## Ejecución:

To run the application, you must execute the following command:
 * ```Flask Run``` which will open the application on a port on your computer, usually <b>5000</b>. You can access it through your web browser by typing the following address ```http://localhost:5000/```
##
