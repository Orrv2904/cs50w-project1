# Project 1 Books

Web Programming with Python and JavaScript
##
Este proyecto consta en una aplicación en donde los usuarios pueden registrar sus cuentas e iniciar sesión en el sitio, 
de igual forma podran buscar un libro ya sea por el número ISBN de el libro, el título de el libro, o el autor de un libro,
en donde cada libro tendra su apartado de envio y muestra de reseñas.

## Tecnologías que se usaron:
1. <b>Python</b>: Se utilizo para la creación de las tablas por medio de modelos haciendo uso de ORM, de igual forma para importar toda la información de los libros contenida en un csv.
2. <b>Flask</b>: Se utlizo para la creación de toda la aplicación, para ser más especificos en la creación de las rutas y funcionalidades de la aplicación.
3. <b>PostgreSQL</b>: Se utilizo para almacenar toda la información recibida de nuestra aplicación.
4. <b>HTML</b>: Se utlizo para la creación de nuestras plantillas (templates) que se muestran en la vista cliente.
5. <b>SASS</b>: Se utilizo para mejorar la eficiencia en la escritura de los estilos CSS.

## 

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


## Instalación:

Para poder ejecutar la aplicación debera de tener un IDE instalado, le recomiendo que use Visual Studio Code ya que en este se creo la aplicación, puede descargarlo aqui [VS Code](https://code.visualstudio.com/docs/?dv=win).
Posterior a ello debera clonar o descargar nuestro repositorio, puede hacerlo con este comando:
```
Git Clone https://github.com/Orrv2904/cs50w-project1.git
```
Una vez descargado, podra acceder a el por medio del CMD de Windows o si prefiere puede usar: ```MINGW64``` de Git y luego ejecutar el comando ```Code .``` para abrirlo en VS Code.

Ahora debera de instalar las <b>dependencias</b> de nuestro programa, para ello debera abrir una terminal dentro de VS Code, puede abrirla en el menú superior, selecciona "Terminal" y luego "New Terminal" (o presiona la combinación de teclas ```Ctrl + Shift + ``` si estás en Windows o Linux, o ```Cmd + Shift +``` si estas en Mac.

