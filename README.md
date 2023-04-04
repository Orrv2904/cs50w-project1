# Project 1 Books

Web Programming with Python and JavaScript
##
Este proyecto consiste en una aplicación en donde los usuarios pueden registrar sus cuentas e iniciar sesión en el sitio. De igual forma, podrán buscar un libro ya sea por el número ISBN del libro, el título del libro o el autor del libro. Cada libro tendrá su apartado de envío y muestra de reseñas.

Tabla de Contenido
     <ol>
    <li><a href="#tecnologias">Tecnologías que se usaron</a></li>
    <li><a href="#como_funciona">¿Como Funciona?</a></li>
    <li><a href="#instalacion">Instalacion</a></li>
    <li><a href="#ejecucion">Ejecucion</a></li>
  </ol>

<input type="hidden" id="tecnologias" value="">

## Tecnologías que se usaron:

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://badge.fury.io/py/flask"><img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-316192.svg?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://badge.fury.io/py/psycopg2"><img src="https://img.shields.io/badge/psycopg2-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="psycopg2"></a>
  <a href="https://badge.fury.io/py/HTML"><img src="https://img.shields.io/badge/HTML-239120?style=flat-square&logo=html5&logoColor=white" alt="HTML"></a>
  <a href="https://badge.fury.io/py/sass"><img src="https://img.shields.io/badge/Sass-CC6699?style=flat-square&logo=sass&logoColor=white" alt="Sass"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript"></a>
</p>

1. <b>Python</b>: Se utilizó para la creación de las tablas por medio de modelos haciendo uso de ORM, de igual forma para importar toda la información de los libros contenida en un CSV.

2. <b>Flask</b>: Se utilizó para la creación de toda la aplicación, para ser más específicos en la creación de las rutas y funcionalidades de la aplicación.

3. <b>PostgreSQL</b>: Se utilizó para almacenar toda la información recibida de nuestra aplicación.

4. <b>HTML</b>: Se utilizó para la creación de nuestras plantillas (templates) que se muestran en la vista del cliente.

5. <b>SASS</b>: Se utilizó para mejorar la eficiencia en la escritura de los estilos CSS.

6. <b>JavaScript</b>: Se utilizó para mejorar la apariencia de las vistas y darle algunas funcionalidades extras.

## 

<input type="hidden" id="como_funciona" value="">

## ¿Comó Funciona?

Funciona de la siguiente manera:

<details><summary><b>Creación de cuenta e Inicio de Sesión</b></summary>
Para crear la cuenta el usuario solamente deberá ingresar los datos que se le solicitan, que son <b>Nombre de Usuario, Correo Electrónico Vigente y Contraseña</b>,
en donde una vez creada su cuenta, se le redirigirá a la misma vista para que inicie sesión con la cuenta que acaba de crear.
</details>
<details><summary><b>Búsqueda</b></summary>
Una vez que el usuario haya iniciado sesión en el sitio, la aplicación lo redirigirá a un buscador en donde podrá buscar un libro por medio del <b>ISBN, Autor o Título</b>, en donde la aplicación le devolverá una lista 
de todos los libros que se encuentran en nuestra base de datos y retornará una plantilla que contendrá la información de los libros que coincidan con el parámetro de búsqueda ingresado por el usuario.
</details>
<details><summary><b>Reseña</b></summary>
Cuando el usuario haya hecho la búsqueda del libro del cual desea saber la información, podrá hacer clic en cada libro por medio de un botón o ya sea por la imagen o el título, en donde este lo redirigirá a otra vista
en la cual podrá ver las reseñas de los usuarios antiguos y el mismo podrá agregar su propia reseña del libro, <b style="background-color: yellow; padding: 5px;">NOTA</b>: El usuario solo podrá agregar una reseña por cada libro ya que el registro se hará por el <b>ISBN</b>.
</details>
<details><summary><b>Acceso al API</b></summary>
Si el usuario desea conocer los detalles de un libro solo deberá agregar la siguiente ruta a la <b>URL</b> del navegador:

```
/api/#ISBN
```
En donde esta le devolverá información del <b>ISBN</b> al cual está haciendo la búsqueda, mostrándole algo similar a esto:
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

* Para poder ejecutar la aplicación deberá tener un IDE instalado, le recomiendo que use Visual Studio Code ya que en este se creó la aplicación. Puede descargarlo aquí: [VS Code](https://code.visualstudio.com/docs/?dv=win).
Posteriormente, deberá clonar o descargar nuestro repositorio. Puede hacerlo con este comando:
```
Git Clone https://github.com/Orrv2904/cs50w-project1.git
```
* Una vez descargado, podrás acceder a él por medio del CMD de Windows o si prefieres, puedes usar ```MINGW64``` de Git y luego ejecutar el comando ```Code .``` para abrirlo en VS Code.

* Ahora deberá instalar las <b>dependencias</b> de nuestro programa. Para ello, deberá abrir una terminal dentro de VS Code. Puede abrirla desde el menú superior seleccionando "Terminal" y luego "New Terminal", o presionando la combinación de teclas ```Ctrl + Shift + ``` si estás en Windows o Linux, o ```Cmd + Shift +``` si estás en Mac.
* Dentro de esta terminal, deberás instalar ```pip``` si aún no lo tienes instalado. Para hacerlo, ejecuta el siguiente comando: ```pip install pip```. Normalmente, pip viene instalado con Python. Si aún no tienes instalado Python, puedes aprender cómo hacerlo leyendo [aqui](https://tutorial.djangogirls.org/es/python_installation/).
* Luego, deberás crear un <b>Entorno Virtual</b> haciendo uso del siguiente comando: ```python -m venv env```. Para activarlo, ejecuta este otro comando: ```.\env\Scripts\activate```.
* Ahora deberás instalar nuestras dependencias que se encuentran en nuestro archivo <b>requirements.txt</b>. Para ello, ejecuta ```pip install -r .\requirements.txt``` y espera a que se termine de instalar todo.
* Posteriormente, deberás crear un archivo llamado <b>.env</b> donde contendrá todas las variables de entorno que usará nuestra aplicación. Puedes crearlo manualmente o también puedes ejecutar este comando: ```touch .env```. Dentro de este archivo, deberás escribir las variables que están en ```.env.templates```, que son las siguientes:
```
DATABASE_URL=
FLASK_DEBUG=
FLASK_APP= 
```
<b style="background-color: yellow; padding: 5px;">NOTA:</b> Antes de cada variable, deberás anteponer export. Esto es para indicar que la variable de entorno especificada será exportada a cualquier proceso secundario lanzado desde la terminal actual.
En la variable ```DATABASE_URL=``` deberás igresar la ```URL``` de tu base de datos <b>PostgreSQL</b> creada en [RailWay](https://railway.app/) o en [Render](https://render.com/). Si quieres saber más acerca de esto puedes leer más aquí [RailWay](https://ekomenyong.com/insights/how-to-setup-free-postgresql-database-on-railway-app) y [Render](https://medium.com/geekculture/how-to-create-and-connect-to-a-postgresql-database-with-render-and-pgadmin-577b326fd19d).

Ahora deberás obtener la cadena de conexión otorgada por Railway o Render. Para ello, deberás crear tu cuenta y crear la base de datos como se mencionó anteriormente.
* Railway tiene una sección llamada ```Connect``` en la cual deberás estar en la base de datos que deseas utilizar. Deberás seleccionar esta opción:  ![01](https://user-images.githubusercontent.com/82064182/229641462-89e7c60a-e30a-43f4-8287-9fa401e1f295.png)

* En Render, deberás seleccionar la cadena de conexión externa. ![02](https://user-images.githubusercontent.com/82064182/229641700-5d0ba55a-6f44-438f-a456-0fbb8e300b8e.png)

Una vez obtenida esta cadena de conexión, deberás pegarla en la variable <b>DATABASE_URL=</b>, obteniendo un resultado similar a este:```export DATABASE_URL=postgresql://postgres:PASSSWORD@HOST:PORT/USER```.

* Y en <b>FLASK_DEBUG= y FLASK_APP=</b> deberás de agregar esto: ```
    FLASK_DEBUG=1
    FLASK_APP=application.py```
    
* Para terminar en esta sección deberás de crear las tablas e ingresar los datos a la base de datos, para ello deberás ejecutar los siguientes comandos en la terminal: 
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

Para ejecutar la aplicación, deberás ejecutar el siguiente comando:
 * ```Flask Run``` el cual te abrirá la aplicación en un puerto de tu computadora, por lo general es el <b>5000</b>. Puedes acceder a él mediante tu navegador web escribiendo la siguiente dirección ```http://localhost:5000/```
##
