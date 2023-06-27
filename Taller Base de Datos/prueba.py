import mysql.connector
from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)

conexion = mysql.connector.connect(
    user='root',
    password='Juancruzmora12345678',
    host='127.0.0.1',
    port='3306',
    auth_plugin='mysql_native_password',
    database='mydb') 
cursor = conexion.cursor()

consulta = "SELECT c.nombre FROM Cliente c INNER JOIN facturacion f ON c.idCliente = f.Cliente_idCliente INNER JOIN productos p ON f.productos_id = p.id WHERE p.tipo = 'Cerveza';"

cursor.execute(consulta)
productos = cursor.fetchall()

print(type(productos))
print(productos)

conexion.commit()
cursor.close()
conexion.close()
