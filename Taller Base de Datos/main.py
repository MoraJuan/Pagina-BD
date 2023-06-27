import mysql.connector
from flask import Flask,request,render_template
from sqlalchemy import create_engine

app = Flask(__name__)
def abrirC():
    conexion = mysql.connector.connect(
        user='root',
        password='Juancruzmora12345678',
        host='127.0.0.1',
        port='3306',
        auth_plugin='mysql_native_password',
        database='mydb') 
    cursor = conexion.cursor()
    return cursor,conexion

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
        
@app.route("/consultarCL", methods=["POST", "GET"])
def consultarCL():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        # Realizar la consulta SELECT a la tabla Producto
        query = "SELECT c.nombre FROM Clientes c INNER JOIN Ventas v ON c.id = v.cliente_id INNER JOIN Productos p ON v.producto_id = p.id WHERE p.tipo = 'Cerveza';"
        cursor.execute(query)
        productos = cursor.fetchall()
        valor = int(productos[0][0])

        conexion.commit()
        cursor.close()
        conexion.close()
        return render_template("consultarCL.html",cantidad=valor)
    else:
        return render_template("index.html")

@app.route("/consultarCC", methods=["POST", "GET"])
def consultarCC():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        query = "SELECT c.nombre FROM Cliente c INNER JOIN facturacion f ON c.idCliente = f.Cliente_idCliente INNER JOIN productos p ON f.productos_id = p.id WHERE p.tipo = 'Cerveza';"
        
        cursor.execute(query)
        productos = cursor.fetchall()
        
        nombres_clientes = [resultado[0] for resultado in productos]
        return render_template("consultarCC.html", listaN=nombres_clientes)
    else:
        return render_template("index.html")
'''

            <a class="BotonMenu" href="{{url_for('consultarQCP')}}" > Consulta quienes han comprado dos productos ejemplo cerveza y pañales</a><br><br>
            <a class="BotonMenu" href="{{url_for('consultarP')}}"  > Consulta que proveedores proveyeron chocolate </a><br><br>
            <a class="BotonMenu" href="{{url_for('consultarP3')}}"  > Listado de producto que tenga menos de 3 unidades</a><br><br>

def consultarP():
    if request.method == 'POST':
        
        return render_template("consultarP.html" )
    else:
        return render_template("index.html")

def consultarP3():
    if request.method == 'POST':
        
        return render_template("consultarP3.html")
    else:
        return render_template("index.html")

def consultarQCP():
    if request.method == 'POST':
        
        return render_template("consultarQCP.html")
    else:
        return render_template("index.html")
        '''


if __name__== "__main__":
    app.run(debug = True)