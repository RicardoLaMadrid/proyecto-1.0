from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__,template_folder='templates')


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='proyecto'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/asignaturas_maestro')
def asignaturas_maestro():
    return render_template('asignaturas_maestro.html')

@app.route('/estudiantes_maestro')
def estudiantes_maestro():
    return render_template('estudiantes_maestro.html')

@app.route('/calificaciones_maestro')
def calificaciones_maestro():
    return render_template('calificaciones_maestro.html')

@app.route('/calificaciones_estudiante')
def calificaciones_estudiante():
    return render_template('calificaciones_estudiante.html')

@app.route('/estudiante')
def estudiante():
    return render_template('estudiante.html')

@app.route('/asignatura_estudiante')
def asignatura_estudiante():
    return render_template('asignatura_estudiante.html')


@app.route('/perfil_estudiante')
def perfil_estudiante():
    return render_template('perfil_estudiante.html')

@app.route('/inicio', methods=['POST'])
def inicio():
    return render_template('inicio.html')

@app.route('/acceso-login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':

        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']


        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s',(_correo,_password))
        account = cur.fetchone()

        if account:
            session['logueado']=True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']

            if session['id_rol']==1:
                return render_template("admin.html")
            elif session['id_rol']==2:
                return render_template("maestro.html")
            elif session['id_rol']==3:
                return render_template("estudiante.html")
       
        else: 
            return render_template('index.html', mensaje="usuario o contraseña incorrecto")

@app.route('/lista_maestros', methods=["GET","POST"])
def listar_maestros():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()

    return render_template("lista_maestros.html",usuarios=usuarios)

@app.route('/lista_estudiantes', methods=["GET","POST"])
def listar_estudiantes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()

    return render_template("lista_estudiantes.html",usuarios=usuarios)




if __name__ == '__main__' :
    app.secret_key="ricardo"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

