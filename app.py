from flask import Flask, render_template, request, make_response, redirect, url_for, flash,jsonify
import forms
import json
import os
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
    estudiantes=[]
    tem=[]
    datos={}

    alumnos_clase=forms.UserForm(request.form)
    if request.method=='POST' and alumnos_clase.validate():
        mat=alumnos_clase.matricula.data
        nom=alumnos_clase.nombre.data
        ape=alumnos_clase.apellido.data
        en=alumnos_clase.correo.data
        datos={"matricula":mat, "nombre":nom, "apellido":ape, "correo":en}

        datos_str=request.cookies.get("estudiante")
        if not datos_str:
            return "No hay cookies"
        tem=json.loads(datos_str)
        estudiantes=tem
        print(type(estudiantes))
        estudiantes.append(datos)  

    response=make_response(render_template('Alumnos.html', form=alumnos_clase,mat=mat, nom=nom, ape=ape, en=en))
    response.set_cookie("estudiante", json.dumps(estudiantes))
    return response


@app.route("/get_cookie")
def get_cookie():
    datos_str=request.cookies.get("estudiante")
    if not datos_str:
        return "No hay cookies"
    datos=json.loads(datos_str)

    return jsonify(datos)


@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    form = forms.PizzaForm(request.form)
    precioT = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
    precioI = 10
    accion = request.args.get('accion')

    if accion == 'quitar':
        item_id = request.args.get('id', 0, type=int)
        pedido_actual = []
        pedido_cookie = request.cookies.get('pedido_actual')
        if pedido_cookie:
            try:
                pedido_actual = json.loads(pedido_cookie)
            except json.JSONDecodeError:
                pedido_actual = []
        
        pedido_nuevo = [item for item in pedido_actual if item['id'] != item_id]
        for i, item in enumerate(pedido_nuevo):
            item['id'] = i
            
        response = make_response(redirect(url_for('pizzeria')))
        response.set_cookie('pedido_actual', json.dumps(pedido_nuevo))
        return response

    if accion == 'confirmar':
        nombre = request.args.get('nombre', 'Cliente')
        total = request.args.get('total', 0, type=float)
        return render_template('confirmacion.html', nombre=nombre, total=total)

    
    pedido_actual = []
    pedido_cookie = request.cookies.get('pedido_actual')
    if pedido_cookie:
        try:
            pedido_actual = json.loads(pedido_cookie)
        except json.JSONDecodeError:
            pedido_actual = []

    # siseqprieta agregaroterminar
    if request.method == 'POST':
        # vtoomn agtrgear
        if request.form.get('submit_button') == 'Agregar':
            if form.tamano.validate(form) and form.cantidad.validate(form):
                ingredientes = []
                precioING = 0
                
                if form.jamon.data:
                    ingredientes.append('Jamón'); precioING += precioI
                if form.pina.data:
                    ingredientes.append('Piña'); precioING += precioI
                if form.champinones.data:
                    ingredientes.append('Champiñones'); precioING += precioI
                
                precio_tamano = precioT.get(form.tamano.data, 0)
                cantidad = form.cantidad.data
                subtotal = (precio_tamano + precioING) * cantidad
                
                pizza_item = {
                    "id": len(pedido_actual), 
                    "tamano": form.tamano.data,
                    "ingredientes": ", ".join(ingredientes) if ingredientes else "Sencilla",
                    "cantidad": cantidad,
                    "subtotal": subtotal
                }
                pedido_actual.append(pizza_item)
                
                ventas_lista = []
                ventas_cookie = request.cookies.get('cookie_ventas')
                if ventas_cookie:
                    try:
                        ventas_lista = json.loads(ventas_cookie)
                    except json.JSONDecodeError:
                        ventas_lista = []
                ventas_por_cliente = {}
                gran_total = 0
                for venta in ventas_lista:
                    nombre = venta.get('nombre', 'Desconocido')
                    total = venta.get('total', 0)
                    gran_total += total
                    ventas_por_cliente[nombre] = ventas_por_cliente.get(nombre, 0) + total
                
                total_pedido_actual = sum(item['subtotal'] for item in pedido_actual)
                
                response = make_response(render_template('pizza.html', 
                                                         form=form, 
                                                         pedido=pedido_actual, 
                                                         total=total_pedido_actual,
                                                         ventas_clientes=ventas_por_cliente,
                                                         gran_total=gran_total))
                response.set_cookie('pedido_actual', json.dumps(pedido_actual))
                return response
        
        # botm terminar
        elif request.form.get('submit_button') == 'Terminar':
            if not pedido_actual:
                return redirect(url_for('pizzeria'))

            total_pedido = sum(item['subtotal'] for item in pedido_actual)
            ventas_totales = []
            ventas_cookie = request.cookies.get('cookie_ventas')
            if ventas_cookie:
                try:
                    ventas_totales = json.loads(ventas_cookie)
                except json.JSONDecodeError:
                    ventas_totales = []
            
            nombre_cliente = form.nombre.data or "Cliente Mostrador"
            direccion_cliente = form.direccion.data or "N/A"
            telefono_cliente = form.telefono.data or "N/A"

            venta = {
                "nombre": nombre_cliente,
                "direccion": direccion_cliente,
                "telefono": telefono_cliente,
                "total": total_pedido
            }
            ventas_totales.append(venta)
            
            response = make_response(redirect(url_for('pizzeria', 
                                                      accion='confirmar', 
                                                      nombre=nombre_cliente, 
                                                      total=total_pedido)))
            response.set_cookie('cookie_ventas', json.dumps(ventas_totales))
            response.set_cookie('pedido_actual', json.dumps([]))
            return response

    # caragdela pagina
    ventas_lista = []
    ventas_cookie = request.cookies.get('cookie_ventas')
    if ventas_cookie:
        try:
            ventas_lista = json.loads(ventas_cookie)
        except json.JSONDecodeError:
            ventas_lista = []
    ventas_por_cliente = {}
    gran_total = 0
    for venta in ventas_lista:
        nombre = venta.get('nombre', 'Desconocido')
        total = venta.get('total', 0)
        gran_total += total
        ventas_por_cliente[nombre] = ventas_por_cliente.get(nombre, 0) + total
    
    total_pedido_actual = sum(item['subtotal'] for item in pedido_actual)
    
    return render_template('pizza.html', 
                           form=form, 
                           pedido=pedido_actual, 
                           total=total_pedido_actual,
                           ventas_clientes=ventas_por_cliente,
                           gran_total=gran_total)

# cookies
@app.route('/get_cookies')
def get_cookies():
    pedido_str = request.cookies.get('pedido_actual')
    ventas_str = request.cookies.get('cookie_ventas')
    pedido_json = []
    ventas_json = []
    
    if pedido_str:
        try:
            pedido_json = json.loads(pedido_str)
        except json.JSONDecodeError:
            pass 
            
    if ventas_str:
        try:
            ventas_json = json.loads(ventas_str)
        except json.JSONDecodeError:
            pass 
            
    # Regresa un JSON con ambas cookies
    return jsonify(
        pedido_actual=pedido_json,
        ventas_totales=ventas_json
    )

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