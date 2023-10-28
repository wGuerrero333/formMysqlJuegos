from flask import Flask , render_template, request, redirect

import pymysql

# formulario con plantilla wtf (instalar flask-wtf)
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, SubmitField, StringField, PasswordField, validators
from wtforms.validators import DataRequired , Length

app = Flask(__name__)
app.config.from_mapping( SECRET_KEY= '1234')

class formualarioRegistro(FlaskForm):
    nombre = StringField('Nombre' , validators= [  DataRequired() , Length( min = 1, max = 20)  ])
 
    submit = SubmitField('BUSCAR wtf')

    # La forma convencional de conectarse a mysql SIN mysqlalchemy


def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='juegos')

def insertar_juego(nombre, descripcion, precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO juegos(nombre, descripcion, precio) VALUES (%s, %s, %s)",
                       (nombre, descripcion, precio))
    conexion.commit()
    conexion.close()

@app.route('/juegos')
def juegos():
    return render_template('auth/agregarJuegos.html')

@app.route('/guardar_juego' ,methods = ['GET','POST'])
    
def guardar_juego():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    insertar_juego(nombre,descripcion,precio)
    # return f'Datos {nombre},{descripcion},{precio} insertados'
    return render_template('auth/agregarJuegos.html')
    
@app.route('/formulario_agregar_juego', methods = ['GET','POST'])
def formulario_agregar_juego():
    def obtener_juegos():
        conexion = obtener_conexion()
        juegos = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos")
            juegos = cursor.fetchall()
        conexion.close()
        return juegos
    juegos = obtener_juegos()
    return render_template('auth/listadojuegos.html', juegos= juegos)
# La id viene en la URL por default, si en esta route methods = ['POST'] no ejecutaria

@app.route("/editar_juego/<int:id>")
def editar_juego(id):
    def obtener_juego_por_id(id):
        conexion = obtener_conexion()
        juego = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id,))
            juego = cursor.fetchone()
        conexion.close()
        return juego

    juego = obtener_juego_por_id(id)
    return render_template("auth/editar_juego.html", juego=juego)


@app.route('/actualizar_juego', methods = ['GET','POST'])
def actualizar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    id = request.form["id"]
    def actualizar_juego(nombre, descripcion, precio, id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
                        (nombre, descripcion, precio, id))
        conexion.commit()
        conexion.close()
    actualizar_juego(nombre,descripcion,precio,id)
    return redirect("formulario_agregar_juego")
    
    
    

@app.route('/eliminar_juego', methods = ['GET','POST'])
def eliminar_juego():
    def eliminar(id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
        conexion.commit()
        conexion.close()
    eliminar(request.form["id"])


  
    return redirect("formulario_agregar_juego")
    


@app.route('/buscar_juego', methods = ['GET','POST'])
#IMPORTANTE sobre el funcionamiento de las rutas
# en la ruta buscar_juego primero se renderiza el form de busqueda que se pasa junto con el valor del nombre tomado del formulario.
# luego IF el metodo es POST se ejecuta la busqueda enla db y se renderiza la form de resultados que se pasa junto con el juego encontrado en la DB
def buscar_juego():
    formularioJuegos = formualarioRegistro()

    if request.method == 'POST':
        if request.method != 'UPDATE':
            nombre = formularioJuegos.nombre.data
            
            def obtenerDb(name):
               
                conexion = obtener_conexion()
                juego = None
                with conexion.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, nombre, precio ,descripcion FROM juegos WHERE nombre = %s", (name))
                    juego = cursor.fetchall()
                conexion.close()
                return juego
            juegoencontrado = obtenerDb(nombre)
            # si devulve una tupla vacia
            if juegoencontrado == ():
                return "No se encontro en la db"
        #IF methos POST renderiza
        return render_template('auth/juegoEncontrado.html', juegoencontrado = juegoencontrado)
    #Primer renderizado
    return render_template('auth/buscar.html', formularioJuegos = formularioJuegos)
    
    
    



