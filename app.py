import _mysql_connector
from mysql.connector import ERROR
from flask import Flask, render_template, request

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
            cursor1.Execute(f"""SELECT * FROM empleados;""")
            resultado = cursor1.fetchall() #continuara
            
            print("Datos insertados con exito")
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connectes():
            cursor1.close()
            conexion.close()
    return render_template('empleados/index.html')

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
            cursor1.Execute(f"""insert into empleados (id_empleado, nombre_empleado, correo_empleado, foto_empleado, imagen_empleado')
                                values (null, '{nombre}', '{_correo}', '{_fotofilename}');""")
            conexion.commit()
            print("Datos insertados con exito")
    except Error as e:
        print('Error durante la conexion o ejecucion de la consola: ', e)
    finally:
        if conexion.is_connectes():
            cursor1.close()
            conexion.close()
    return render_template('empleados/index.html')
app.run(host='0.0.0.0', port=81, debug=True)