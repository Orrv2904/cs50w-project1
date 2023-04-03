# Project 1 Books

Web Programming with Python and JavaScript
##
Este proyecto consta en una aplicación en donde los usuarios pueden registrar sus cuentas e iniciar sesión en el sitio, 
de igual forma podran buscar un libro ya sea por el número ISBN de el libro, el título de el libro, o el autor de un libro,
en donde cada libro tendra su apartado de envio y muestra de reseñas.

<details>
  <summary>Tabla de Contenido</summary>
  <ol>
    <li><a href="#tecnologias">Tecnologías que se usaron</a></li>
    <li><a href="#como_funciona">¿Comó Funciona?</a></li>
    <li><a href="#instalacion">Instalación</a></li>
    <li><a href="#ejecucion">Ejecución</a></li>
  </ol>
</details>

<input type="hidden" id="tecnologias" value="">

## Tecnologías que se usaron:
1. <b>Python</b>: Se utilizo para la creación de las tablas por medio de modelos haciendo uso de ORM, de igual forma para importar toda la información de los libros contenida en un csv.
2. <b>Flask</b>: Se utlizo para la creación de toda la aplicación, para ser más especificos en la creación de las rutas y funcionalidades de la aplicación.
3. <b>PostgreSQL</b>: Se utilizo para almacenar toda la información recibida de nuestra aplicación.
4. <b>HTML</b>: Se utlizo para la creación de nuestras plantillas (templates) que se muestran en la vista cliente.
5. <b>SASS</b>: Se utilizo para mejorar la eficiencia en la escritura de los estilos CSS.

## 

<input type="hidden" id="como_funciona" value="">

## ¿Comó Funciona?

Funciona de la siguiente manera:
<details><summary><b>Creación de cuenta e Inicio de Sesión</b></summary>
Para crear la cuenta el usuario solamente debera de ingresar los datos que se le solicitan, que son <b>Nombre de Usuario, Correo Electrónico Vigente y Contraseña</b>,
en donde una vez creada su cuenta este le devolvera a la misma vista para que el inicie sesión con la cuenta que acaba de crear.
</details>
<details><summary><b>Búsqueda</b></summary>
Una vez el usuario haya iniciado sesion en el sitio, la aplicacion le redigira a un buscador en donde el usuario podra buscar un libro por medio del <b>ISBN, Autor o Titulo</b>, en donde la aplicacion le devolvera una lista 
de todos los libros que se encuentran en nuestra base de datos y retornara una plantilla que contendra la informacion de los libros que coincidan con el parametro de busqueda ingresado por el usuario.
</details>
<details><summary><b>Reseña</b></summary>
Cuando el usuario haya hecho la busqueda del libro del cual desea saber la informacion, podra hacer click a cada libro por medio de un boton o ya sea por la imagen o el titulo, en donde este le redirigira a otra vista
en la cual el podra ver las reseñas de los usuarios antiguos y el mismo podra agregar su propia reseña del libro, <b style="background-color: yellow; padding: 5px;">NOTA</b>: El usuario solo podra agregar una reseña por cada libro ya que el registro se hara por el <b>ISBN</b>.
</details>
<details><summary><b>Acceso al API</b></summary>
Si el usuario desea conocer los detalles de un libro solo debera agregar la siguiente ruta a la <b>URL</b> del navegador:

```
/api/#ISBN
```
En donde esta le devolvera informacion del <b>ISBN</b> al cual esta haciendo la busqueda, mostrandole algo similar a esto:
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

Para poder ejecutar la aplicación debera de tener un IDE instalado, le recomiendo que use Visual Studio Code ya que en este se creo la aplicación, puede descargarlo aqui [VS Code](https://code.visualstudio.com/docs/?dv=win).
Posterior a ello debera clonar o descargar nuestro repositorio, puede hacerlo con este comando:
```
Git Clone https://github.com/Orrv2904/cs50w-project1.git
```
Una vez descargado, podra acceder a el por medio del CMD de Windows o si prefiere puede usar: ```MINGW64``` de Git y luego ejecutar el comando ```Code .``` para abrirlo en VS Code.

Ahora debera de instalar las <b>dependencias</b> de nuestro programa, para ello debera abrir una terminal dentro de VS Code, puede abrirla en el menú superior, selecciona "Terminal" y luego "New Terminal" (o presiona la combinación de teclas ```Ctrl + Shift + ``` si estás en Windows o Linux, o ```Cmd + Shift +``` si estas en Mac.
Dentro de esta terminal deberas de instalar ```pip``` si aun no lo tienes instaldo, para hacerlo ejecuta el siguiente comando ```pip install pip```, normalmente viene instaldo con Python si aun no tienes instalado Python puedes ver como hacerlo leyendo [aqui](https://tutorial.djangogirls.org/es/python_installation/).
Luego deberas de crear un <b>Ambiente Virtual</b> haciendo uso del siguiente comando ```python -m venv env``` y para activarlo ejecuta este otro comando ```.\env\Scripts\activate```.
Ahora deberas de instalar nuestras dependecias que se encuentran en nuestro archivo <b>requirements.txt</b>, para ello ejecuta ```pip install -r .\requirements.txt``` y espera que se termine de instalar todo.
Posterior deberas crear un archivo llamado <b>.env</b> en donde contendra todas las variables de entorno que usara nuestra aplicacion, puedes crearlo manual o tambien puedes ejecutar este comando: ```touch .env``` y dentro de este deberas de pasar las variables que estan en ```.env.templates``` que son estas:
```
DATABASE_URL=
FLASK_DEBUG=
FLASK_APP= 
```
<b style="background-color: yellow; padding: 5px;">NOTA</b>: Antes de cada variable deberas de anteponer ```export``` esto es para indicar que la variable de entorno especificada será exportada a cualquier proceso secundario lanzado desde la terminal actual.
En la variable ```DATABASE_URL=``` deberas igresar la ```URL``` de tu base de datos <b>PostgreSQL</b> creada en [RailWay](https://railway.app/) o en [Render](https://render.com/), si quieres saber más acerca de esto puedes leer más aquí [RailWay](https://ekomenyong.com/insights/how-to-setup-free-postgresql-database-on-railway-app) y [Render](https://medium.com/geekculture/how-to-create-and-connect-to-a-postgresql-database-with-render-and-pgadmin-577b326fd19d).

Ahora deberas obtener la cadena de conexión otorgada por Railway o Render, para ello deberas de crear tu cuenta y crear la base de datos a como te deje arriba:
* RailWay tiene un apartado llamado ```Connect``` en la cual deberas estar en la base de datos a usar, y deberas seleccionar esta parte: ![01](https://user-images.githubusercontent.com/82064182/229641462-89e7c60a-e30a-43f4-8287-9fa401e1f295.png)

* En Render deberas de seleccionar la cadena externa: ![02](https://user-images.githubusercontent.com/82064182/229641700-5d0ba55a-6f44-438f-a456-0fbb8e300b8e.png)

Una vez obteniedo esta cadena de conexión la deberas de pegar en <b>DATABASE_URL=</b> obteniendo un resultado como este ```export DATABASE_URL=postgresql://postgres:PASSSWORD@HOST:PORT/USER```.

* Y en <b>FLASK_DEBUG= y FLASK_APP=</b> deberas de agregar esto: ```
    FLASK_DEBUG=1
    FLASK_APP=application.py```

##

<input type="hidden" id="ejecucion" value="">

## Ejecución:

Para ejecutar la aplicación deberas de ejecutar el siguiente comando:
 * ```Flask Run``` el cual te abrira la aplicación en un puerto de tu compuradora, por lo general es el <b>5000</b> puedes acceder a el por medio de la terminal o escribiendo el siguiente comando ```http://localhost:5000/```
##
