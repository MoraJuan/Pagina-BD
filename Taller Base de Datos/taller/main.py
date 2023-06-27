import mysql.connector
from flask import Flask,request,render_template
import datetime

app = Flask(__name__)
def abrirC():
    conexion = mysql.connector.connect(
        user='root',
        password='admin',
        host='127.0.0.1',
        port='3306',
        auth_plugin='mysql_native_password',
        database='mydb') 
    cursor = conexion.cursor()
    return cursor,conexion

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/consultas", methods=["POST", "GET"])
def consultas():
    return render_template("indexC.html")

@app.route("/funcionalidades", methods=["POST", "GET"])
def funcionalidades():
    return render_template("indexF.html")
        
@app.route("/consultarCL", methods=["POST", "GET"])
def consultarCL():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        # Realizar la consulta SELECT a la tabla Producto
        #Cantidad de leche que se vendio
        query = "SELECT cantidad FROM Facturacion WHERE Productos_id IN (SELECT id FROM Productos WHERE tipo = 'Leche');"
        cursor.execute(query)
        productos = cursor.fetchall()
        print(productos)
        valor = 0
        for producto in productos:
            valor = valor + producto[0]
        return render_template("consultarCL.html",cantidad=valor)
    else:
        return render_template("index.html")

@app.route("/consultarCC", methods=["POST", "GET"])
def consultarCC():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        query = "SELECT nombre FROM cliente WHERE idCliente IN (SELECT idCliente FROM facturacion WHERE idCliente IN (SELECT id FROM productos WHERE tipo = 'Cerveza'));"
        cursor.execute(query)
        productos = cursor.fetchall()
        if len(productos) == 0:
            raise Exception("No se encontraron clientes que hayan comprado cerveza")
        nombres_clientes = [resultado[0] for resultado in productos]
        return render_template("consultarCC.html", listaN=nombres_clientes)
    else:
        return render_template("index.html")

@app.route("/consultarQCP", methods=["POST", "GET"])    
def consultarQCP():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        # Realizar la consulta SQL para obtener los nombres de los clientes que compraron cerveza y pañales (intersección)
        query_interseccion = "SELECT nombre FROM Cliente WHERE idCliente IN (SELECT Cliente_idCliente FROM Facturacion WHERE Productos_id IN (SELECT id FROM Productos WHERE tipo = 'Cerveza')) AND idCliente IN (SELECT Cliente_idCliente FROM Facturacion WHERE Productos_id IN (SELECT id FROM Productos WHERE tipo = 'Pañales'))"
        cursor.execute(query_interseccion)
        resultados_interseccion = cursor.fetchall()
        nombres = [resultado[0] for resultado in resultados_interseccion]
        
        return render_template("consultarQCP.html", listaN=nombres)
    else:
        return render_template("index.html")

@app.route("/consultarP", methods=["POST", "GET"])   
def consultarP():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        # Consulta quein provee chocolate
        query = "SELECT p.nombre FROM proveedores p, provee pr, productos pd WHERE p.cuil = pr.proveedores_cuil AND pr.productos_id = pd.id AND pd.tipo = 'Chocolates';"

        cursor.execute(query)
        resultados = cursor.fetchall()
        nombres = [resultado[0] for resultado in resultados]
        return render_template("consultarP.html",nombres=nombres)
    else:
        return render_template("index.html")

@app.route("/consultarP3", methods=["POST", "GET"])   
def consultarP3():
    if request.method == 'GET':
        cursor,conexion=abrirC()
        query = "SELECT tipo FROM productos WHERE cantidad <= 100;"
        cursor.execute(query)
        resultados = cursor.fetchall()
        nombres = [resultado[0] for resultado in resultados]
        return render_template("consultarP3.html",tipos=nombres)
    else:
        return render_template("index.html")
        
'''
            <!--<a class="BotonMenu" href="{{url_for('agregarProveedor')}}"> Agregar Proveedor</a>
            <a class="BotonMenu" href="{{url_for('agregarFactura')}}"> Agregar Factura</a>
            <a class="BotonMenu" href="{{url_for('agregarProductos')}}"> Agregar Productos</a>
            <a class="BotonMenu" href="{{url_for('agregarFacturacion')}}"> Agregar Facturacion</a> -->
'''

@app.route("/agregarCliente",methods=["POST","GET"])
def agregarCliente():
    return render_template("agregarCliente.html")

@app.route("/guardarCliente", methods=["POST", "GET"])
def guardarCliente():
    if request.method == 'POST':
        cursor,conexion=abrirC()
        query = "INSERT INTO Cliente (cuil, nombre, puntos) VALUES (%s, %s, 0);"
        cuil = request.form.get("cuil")
        nombre = request.form.get("nombre")
        cursor.execute(query, (cuil, nombre))
        conexion.commit()
        return render_template("agregarCliente.html")
    else:
        return render_template("indexF.html")

@app.route("/agregarEmpleado",methods=["POST","GET"])
def agregarEmpleado():
    return render_template("agregarEmpleado.html")

@app.route("/guardarEmpleado", methods=["POST", "GET"])
def guardarEmpleado():
    if request.method == 'POST':
        cursor,conexion=abrirC()
        query = "INSERT INTO Empleados (cuil, nombre, apellido) VALUES (%s, %s, %s);"
        cuil = request.form.get("cuil")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        cursor.execute(query, (cuil, nombre, apellido))
        conexion.commit()
        return render_template("agregarEmpleado.html")
    else:
        return render_template("indexF.html")

@app.route("/agregarProducto",methods=["POST","GET"])
def agregarProducto():
    return render_template("agregarProducto.html")

@app.route("/guardarProducto", methods=["POST", "GET"])
def guardarProducto():
    if request.method == 'POST':
        cursor,conexion=abrirC()
        query1 = "SELECT * FROM Productos WHERE tipo = %s AND marca = %s;"
        tipo = request.form.get("tipo")
        marca = request.form.get("marca")
        cursor.execute(query1, (tipo, marca))
        producto = cursor.fetchone()
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        proveedor = request.form.get("proveedor")
        precioP = (100*int(precio))/120 

        if producto is None:
            query = "INSERT INTO productos (tipo,marca, precio, cantidad) VALUES (%s, %s,%s,%s);"
            cursor.execute(query, (tipo, marca, precio, cantidad))
            conexion.commit()
            query2 = "INSERT INTO provee (proveedores_cuil, productos_id, precioP, fecha,cantidadP) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query2, (proveedor, cursor.lastrowid, precioP, datetime.datetime.now(),cantidad))
            conexion.commit()
        else:
            query = "UPDATE productos SET precio = %s WHERE id = %s;"
            cursor.execute(query, precio, producto[0])
            conexion.commit()
            query = "UPDATE productos SET cantidad = cantidad + %s WHERE id = %s;"
            cursor.execute(query, cantidad, producto[0])
            conexion.commit()
            
            query2 = "INSERT INTO provee (proveedores_cuil, productos_id, precioP, fecha,cantidadP) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query2, (proveedor, producto[0], precioP, datetime.datetime.now(),cantidad))
            conexion.commit()
        return render_template("agregarProducto.html")
    else:
        return render_template("indexF.html")
        
@app.route("/agregarF", methods=["POST", "GET"])
def agregarF():
    return render_template("agregarF.html")

@app.route("/guardarF", methods=["POST", "GET"])
def guardarF():
    if request.method == 'POST':
        cursor,conexion=abrirC()

        #Buscar producto por tipo y marca
        query1 = "SELECT * FROM Productos WHERE tipo = %s AND marca = %s;"
        tipo = request.form.get("tipo")
        marca = request.form.get("marca")
        cursor.execute(query1, (tipo, marca))
        producto = cursor.fetchone()
        
        if producto is None:
            return render_template("agregarF.html",aviso="No existe el producto")
        else:
            #Preguntar si la cantidad de productos en stock es menor a la cantidad ingresada
            if producto[3] < cantidad:
                return render_template("agregarF.html",aviso="No hay suficientes productos en stock")
            else:
                productos_id = producto[0]
                precio = producto[2]
                fecha = request.form.get("fecha")
                cantidad = request.form.get("cantidad")
                importe = precio * cantidad

                query3= "INSERT INTO Factura(tipo) VALUES(%s)"
                tipoF = request.form.get("tipoF")
                cursor.execute(query3,(tipoF))

                query3B = "SELECT * FROM Factura WHERE tipo = %s"
                cursor.execute(query3B,(tipoF))
                factura = cursor.fetchone()
                facturas_numero = factura[0]

                cuilE = request.form.get("cuilE")
                idCliente = request.form.get("idCliente")

                query4 = "INSERT INTO Facturacion (fecha, importe, cantidad, facturas_numero, productos_id, empleados_cuil,cliente_idCliente) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query4,(fecha, importe, cantidad, facturas_numero, productos_id, cuilE, idCliente))
                return render_template("agregarF.html",aviso="Factura agregada con exito")
    else:
        return render_template("indexF.html")

if __name__== "__main__":
    app.run(debug = True)