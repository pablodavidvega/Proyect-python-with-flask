import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os 

app = Flask (__name__)

carpeta = os.path.join('uploads') #Creo la variable carpeta para manipular uploads
app.config['carpeta'] = carpeta  #Crear una referencia de la ruta

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
    now = datetime.now()
    tiempo = now.strftime('%Y%H_%M_%S_')
    if _foto.filename != '':
        nuevonombreFoto = tiempo + _foto.filename
        _foto.save('uploads/'+ nuevonombreFoto)
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
                                values (null, '{_nombre}', '{_correo}', '{nuevonombreFoto}');""")
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
            cursor1.execute(f"""select imagen_empleado from empleados where id_empleado = {id};""")
            fila = cursor1.fetchall()
            os.remove(os.path.join(app.config['carpeta'], fila[0][0]))
            cursor1.execute(f"""delete from empleados where id_empleado= {id};""")
            conexion.commit()
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()
    return redirect('/consulta')

@app.route('/editar/<int:id>')
def editar(id):
    
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
            cursor1.execute(f"""SELECT * FROM empleados where id_empleado = {id};""")
            resultado = cursor1.fetchall() #sacar la informacion del objeto cursor y la pasa auna variable
            conexion.commit()
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()
    
    return render_template('empleados/edit.html', datos=resultado)

@app.route('/update', methods = ['POST'])
def update():
    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    _id = request.form['txtID']
    now = datetime.now()
    tiempo = now.strftime('%Y%H_%M_%S_')
 
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
            #si me actualizaron la foto
            if _foto.filename != '':
                nuevonombreFoto = tiempo + _foto.filename
                _foto.save('uploads/'+ nuevonombreFoto)
                cursor1.execute(f"""select imagen_empleado from empleados where id_empleado = {id});""")
                fila= cursor1.fetchall()
                os.remove(os.path.join(app.config['carpeta'],fila [0][0]))
                cursor1.execute(f"""update empleados set imagen_empleados = {nuevonombreFoto})
                                where id_empleado ={_id};""")
            
                cursor1.commit
            cursor1.execute(f"""update empleados set nombre_empleado ={nombre}, correo_empleado = {_correo}
                            where id_empleado={_id};""")
            
            cursor1.commit()
            
        #Si no actualizaron la foto
        cursor1.execute(f"""update empleados set nombre_empleado ={nombre}, correo_empleado = {_correo}
                            where id_empleado={_id};""")
            
        conexion.commit()
        print("Datos insertados con exito")
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connected():
            cursor1.close()
            conexion.close()

app.run(host='0.0.0.0', port=81, debug=True)


