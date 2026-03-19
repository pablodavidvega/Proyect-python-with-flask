from flask import Flask, render_template

app = Flask (__name__)

@app.route('/prueba')
def index():
    return render_template('empleados/index.html')

app.run(host='0.0.0.0', port=81, debug=True)