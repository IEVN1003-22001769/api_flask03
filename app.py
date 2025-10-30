from flask import Flask, render_template, request
import forms
import math


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World :)"

@app.route('/Alumnos', methods=['GET','POST'])
def alumnos():
    mat=0
    nom=""
    ape=""
    en=""
    alumnos_clase=forms.UserForm(request.form)
    if request.method=='POST' and alumnos_clase.validate():
        mat=alumnos_clase.matricula.data
        nom=alumnos_clase.nombre.data
        ape=alumnos_clase.apellido.data
        en=alumnos_clase.correo.data
    return render_template('Alumnos.html', form=alumnos_clase,mat=mat, nom=nom, ape=ape, en=en)


@app.route('/figuras', methods=['GET','POST'])
def figuras():
    resultado = None
    figurillas = forms.FigurasA(request.form)
    if request.method == 'POST' and figurillas.validate():
        figuraSeleccionada = figurillas.figura.data
        n1 = figurillas.valor1.data
        n2 = figurillas.valor2.data 

        if figuraSeleccionada == 'triangulo':
            if n2 is None:
                figurillas.valor2.errors.append("La altura es requerido")
            else:
                resultado = 0.5 * n1 * n2
        
        elif figuraSeleccionada == 'rectangulo':
            if n2 is None:
                figurillas.valor2.errors.append("El ancho es requerido")
            else:
                resultado = n1 * n2

        elif figuraSeleccionada == 'circulo':
            resultado = math.pi * (n1 ** 2)

        elif figuraSeleccionada == 'pentagono':
            if n2 is None:
                figurillas.valor2.errors.append("El apotema es requerido")
            else:
                resultado = (5 / 2) * n1 * n2

    return render_template('figuras.html', form=figurillas, resultado=resultado)

@app.route('/index')
def index():
    titulo="IEVN1003 - PWA"
    listado=["Opera 1", "Opera 2", "Opera 3", "Opera 4"]
    return render_template('index.html', titulo=titulo, listado=listado)

@app.route('/operas', methods=['GET','Post'])
def operas():
    if request.method=='POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        resultado=int(n1)+int(n2)
        return render_template('operas.html', resultado=resultado)
    
    return render_template('operas.html')


@app.route('/distancia')
def distancia():
    return render_template('distancia.html')



@app.route('/about')
def about():
    return "<h1>This is the about page.<h1>"

@app.route("/user/<string:user>")
def user(user):
    return "Hola "+ user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def funt(n1,n2):
    return "La suma es: {}".format(n1+n2)

@app.route("/prueba")
def prueba():
    return """
    <h1>Prueba de HTML</h1>
    <p>Esto es un parrafo</p>
    <ul>
    <li>Elemento 1</li>
    <li>Elemento 2</li>
    <li>Elemento 3</li>
    </ul>
        """
if __name__ == '__main__':
    app.run(debug=True)