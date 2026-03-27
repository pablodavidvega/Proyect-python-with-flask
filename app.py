import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for

app = Flask (__name__)

@app.route('/consulta')
def index():
    try:
        #conexion
       
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'sistem'
        )
        if conexion.is_connected():
            cursor1 = conexion.cursor()
            cursor1.execute(f"""SELECT * FROM empleados;""")
            resultado = cursor1.fetchall()  
            
            if resultado:
                print(resultado)
            else: 
                print('No existen Registros')
            conexion.commit()
            
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()
    return render_template('empleados/index.html', informacion=resultado)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def almacenamiento():
    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    try:
        #conexion
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'sistem'
        )
        if conexion.is_connected():
            cursor1 = conexion.cursor()
            cursor1.execute(f"""insert into empleados (id_empleado, nombre_empleado, correo_empleado, imagen_empleado)
                                values (null, '{_nombre}', '{_correo}', '{_foto.filename}');""")
            conexion.commit()
            print("Datos insertados con exito")
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()
    return redirect(url_for('index'))

#Crear el metodo de borrar
@app.route('/eliminar/<int:id>') #Recibir un parametro en la ruta , que tipo de dato es y como llamo ese parametro
def eliminar(id): #Paso el parametro de la ruta al metodo
    try:
        #conexion
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'sistem'
        )
        if conexion.is_connected():
            cursor1 = conexion.cursor()
            cursor1.execute(f"""delete from empleados where id_empleado= {id};""")
            conexion.commit()
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()
    return redirect('/consulta')

app.run(host='0.0.0.0', port=81, debug=True)


