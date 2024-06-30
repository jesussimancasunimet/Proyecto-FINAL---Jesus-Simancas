import requests  # Importa la librería requests para hacer solicitudes HTTP
import json  # Importa la librería json para manejar datos en formato JSON
import urllib.request  # Importa urllib para hacer solicitudes HTTP
import random  # Importa la librería random para generar valores aleatorios
import string  # Importa la librería string para manejar cadenas de texto
import os  # Importa la librería os para interactuar con el sistema operativo
import matplotlib.pyplot as plt  # Importa pyplot de matplotlib para crear gráficos
from bokeh.plotting import figure, show  # Importa figure y show de bokeh para crear gráficos interactivos

# Define la clase Cliente para almacenar datos de los clientes
class Cliente:
    def __init__(self, nombre, cedula, edad, tipo_entrada, nombre_estadio):  # Constructor de la clase
        self.nombre = nombre  # Asigna el nombre
        self.cedula = cedula  # Asigna la cédula
        self.edad = edad  # Asigna la edad
        self.tipo_entrada = tipo_entrada  # Asigna el tipo de entrada
        self.nombre_estadio = nombre_estadio  # Asigna el nombre del estadio
        self.id_boleto = self.generar_id_boleto()  # Genera un ID de boleto

    def generar_id_boleto(self):  # Método para generar un ID de boleto
        caracteres = string.ascii_letters + string.digits  # Define los caracteres permitidos
        id_boleto = ''.join(random.choice(caracteres) for _ in range(8))  # Genera una cadena aleatoria de 8 caracteres
        return id_boleto  # Devuelve el ID del boleto

# Define la clase Equipo para almacenar datos de los equipos
class Equipo:
    def __init__(self, id, code, name, group):  # Constructor de la clase
        self.id = id  # Asigna el ID
        self.code = code  # Asigna el código
        self.name = name  # Asigna el nombre
        self.group = group  # Asigna el grupo

# Define la clase Stadium para almacenar datos de los estadios
class Stadium:
    def __init__(self, id, name, city, capacity_general, capacity_vip, restaurants):  # Constructor de la clase
        self.id = id  # Asigna el ID
        self.name = name  # Asigna el nombre
        self.city = city  # Asigna la ciudad
        self.capacity_general = capacity_general  # Asigna la capacidad general
        self.capacity_vip = capacity_vip  # Asigna la capacidad VIP
        self.restaurants = restaurants  # Asigna los restaurantes
        self.asientos = [["Disponible" for _ in range(self.capacity_vip)] for _ in range(self.capacity_general)]  # Inicializa los asientos como disponibles

# Define la clase Restaurant para almacenar datos de los restaurantes
class Restaurant:
    def __init__(self, name, products):  # Constructor de la clase
        self.name = name  # Asigna el nombre
        self.products = products  # Asigna los productos

# Define la clase Product para almacenar datos de los productos
class Product:
    def __init__(self, name, quantity, price, adicional, stock):  # Constructor de la clase
        self.name = name  # Asigna el nombre
        self.quantity = quantity  # Asigna la cantidad
        self.price = float(price) + float(price) * 0.16  # Calcula el precio con IVA
        self.adicional = adicional  # Asigna información adicional
        self.stock = stock  # Asigna el stock

# Define la clase Match para almacenar datos de los partidos
class Match:
    def __init__(self, match_data, equipos, estadios):  # Constructor de la clase
        self.id = match_data['id']  # Asigna el ID
        self.number = match_data['number']  # Asigna el número del partido
        self.home = self.get_equipo_by_id(match_data['home']['id'], equipos)  # Obtiene el equipo local
        self.away = self.get_equipo_by_id(match_data['away']['id'], equipos)  # Obtiene el equipo visitante
        self.date = match_data['date']  # Asigna la fecha
        self.group = match_data['group']  # Asigna el grupo
        self.estadio = self.get_estadio_by_id(match_data['stadium_id'], estadios)  # Obtiene el estadio

    def get_equipo_by_id(self, equipo_id, equipos):  # Método para obtener un equipo por ID
        for equipo in equipos:  # Recorre los equipos
            if equipo.id == equipo_id:  # Si encuentra el ID
                return equipo  # Devuelve el equipo
        return None  # Si no encuentra, devuelve None

    def get_estadio_by_id(self, estadio_id, estadios):  # Método para obtener un estadio por ID
        for estadio in estadios:  # Recorre los estadios
            if estadio.id == estadio_id:  # Si encuentra el ID
                return estadio  # Devuelve el estadio
        return None  # Si no encuentra, devuelve None

# Función para cargar datos de equipos, estadios y partidos
def cargar_datos():
    equipos = cargar_equipos()  # Carga los equipos
    estadios = cargar_estadios()  # Carga los estadios
    partidos = cargar_partidos(equipos, estadios)  # Carga los partidos
    return equipos, estadios, partidos  # Devuelve los datos

# Función para cargar equipos desde una URL
def cargar_equipos():
    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"  # URL de equipos
    try:
        response = requests.get(url_equipos)  # Hace una solicitud GET
        response.raise_for_status()  # Verifica si hay errores
        equipos_data = response.json()  # Convierte la respuesta a JSON
        return [Equipo(e["id"], e["code"], e["name"], e["group"]) for e in equipos_data]  # Crea una lista de equipos
    except requests.exceptions.RequestException as e:  # Captura excepciones
        print(f"Error al cargar equipos: {e}")  # Imprime el error
        return []  # Devuelve una lista vacía

# Función para cargar estadios desde una URL
def cargar_estadios():
    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"  # URL de estadios
    try:
        response = urllib.request.urlopen(url_estadios)  # Hace una solicitud GET
        data = json.load(response)  # Convierte la respuesta a JSON
        estadios = []  # Inicializa la lista de estadios
        for item in data:  # Recorre los datos
            restaurants = [Restaurant(r["name"], [Product(p["name"], p["quantity"], p["price"], p["adicional"], p["stock"]) for p in r["products"]]) for r in item["restaurants"]]  # Crea una lista de restaurantes
            estadio = Stadium(item["id"], item["name"], item["city"], item["capacity"][0], item["capacity"][1], restaurants)  # Crea un estadio
            estadios.append(estadio)  # Añade el estadio a la lista
        return estadios  # Devuelve la lista de estadios
    except urllib.error.URLError as e:  # Captura excepciones
        print(f"Error al cargar estadios: {e}")  # Imprime el error
        return []  # Devuelve una lista vacía

# Función para cargar partidos desde una URL
def cargar_partidos(equipos, estadios):
    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"  # URL de partidos
    try:
        response = requests.get(url_partidos)  # Hace una solicitud GET
        response.raise_for_status()  # Verifica si hay errores
        partidos_data = response.json()  # Convierte la respuesta a JSON
        return [Match(m, equipos, estadios) for m in partidos_data]  # Crea una lista de partidos
    except requests.exceptions.RequestException as e:  # Captura excepciones
        print(f"Error al cargar partidos: {e}")  # Imprime el error
        return []  # Devuelve una lista vacía

# Función para verificar si un número es vampiro
def es_numero_vampiro(cedula):
    cedula_str = str(cedula)  # Convierte la cédula a cadena
    cedula_length = len(cedula_str)  # Obtiene la longitud de la cédula
    if cedula_length % 2 != 0:  # Verifica si la longitud es impar
        return False  # No es vampiro si es impar
    for i in range(1, 10**(cedula_length // 2)):  # Itera posibles factores
        if (cedula % i == 0):  # Verifica si i es un factor
            factor1 = i  # Asigna el primer factor
            factor2 = cedula // i  # Asigna el segundo factor
            if len(str(factor1)) == cedula_length // 2 and len(str(factor2)) == cedula_length // 2:  # Verifica la longitud de los factores
                digits = list(cedula_str)  # Convierte la cédula a lista de dígitos
                factors_digits = list(str(factor1) + str(factor2))  # Convierte los factores a lista de dígitos
                factors_digits.sort()  # Ordena los dígitos de los factores
                digits.sort()  # Ordena los dígitos de la cédula
                if factors_digits == digits:  # Compara los dígitos
                    return True  # Es vampiro si coinciden
    return False  # No es vampiro si no coincide

# Función para verificar si un número es perfecto
def es_numero_perfecto(cedula):
    suma_divisores = sum(divisor for divisor in range(1, cedula) if cedula % divisor == 0)  # Suma los divisores de la cédula
    return suma_divisores == cedula  # Verifica si la suma es igual a la cédula

# Función para buscar partidos por país
def buscar_partidos_por_pais(pais, partidos):
    return [partido for partido in partidos if partido.home.name == pais or partido.away.name == pais]  # Devuelve los partidos del país

# Función para buscar partidos por estadio
def buscar_partidos_por_estadio(estadio, partidos):
    return [partido for partido in partidos if partido.estadio.name == estadio]  # Devuelve los partidos en el estadio

# Función para buscar partidos por fecha
def buscar_partidos_por_fecha(fecha, partidos):
    return [partido for partido in partidos if partido.date == fecha]  # Devuelve los partidos en la fecha

# Función para solicitar datos del cliente
def solicitar_datos_cliente(partidos):
    print("Bienvenido al sistema de venta de entradas")  # Mensaje de bienvenida
    nombre = input("Nombre del cliente: ")  # Solicita el nombre
    cedula = input("Cédula del cliente: ")  # Solicita la cédula
    edad = int(input("Edad del cliente: "))  # Solicita la edad
    mostrar_partidos(partidos)  # Muestra los partidos disponibles
    partido_id = input("ID del partido al que desea comprar: ")  # Solicita el ID del partido
    tipo_entrada = input("Tipo de entrada que desea comprar (General/VIP): ")  # Solicita el tipo de entrada
    return nombre, cedula, edad, partido_id, tipo_entrada  # Devuelve los datos del cliente

# Función para mostrar partidos disponibles
def mostrar_partidos(partidos):
    print("----- Partidos Disponibles -----")  # Encabezado
    for partido in partidos:  # Recorre los partidos
        print(f"ID: {partido.id}, Fecha: {partido.date}, Local: {partido.home.name}, Visitante: {partido.away.name}, Estadio: {partido.estadio.name}")  # Muestra los detalles del partido
        print("---------------------------")  # Separador

# Función para calcular el costo de una entrada
def calcular_costo_entrada(tipo_entrada, cedula):
    descuento = 0.5 if cedula.isdigit() and es_numero_vampiro(int(cedula)) else 0  # Calcula el descuento si la cédula es un número vampiro
    precio_base = 35 if tipo_entrada == "General" else 75 if tipo_entrada == "VIP" else None  # Asigna el precio base según el tipo de entrada
    if precio_base is None:  # Verifica si el tipo de entrada es válido
        print("Tipo de entrada inválido.")  # Mensaje de error
        return None  # Devuelve None si es inválido
    iva = precio_base * 0.16  # Calcula el IVA
    total = precio_base - (precio_base * descuento) + iva  # Calcula el total con descuento e IVA
    return precio_base, descuento, iva, total  # Devuelve el precio base, descuento, IVA y total

# Función para seleccionar un asiento
def seleccionar_asiento(estadio):
    print("----- Mapa del Estadio -----")  # Encabezado
    for i in range(estadio.capacity_general):  # Recorre las filas del estadio
        print(" ".join(["O" for _ in range(estadio.capacity_vip)]))  # Muestra los asientos disponibles
    while True:  # Ciclo para seleccionar asiento
        fila = int(input("Número de fila: "))  # Solicita la fila
        columna = int(input("Número de columna: "))  # Solicita la columna
        if 1 <= fila <= estadio.capacity_general and 1 <= columna <= estadio.capacity_vip:  # Verifica si la fila y columna son válidas
            if estadio.asientos[fila - 1][columna - 1] == "Disponible":  # Verifica si el asiento está disponible
                estadio.asientos[fila - 1][columna - 1] = "Ocupado"  # Marca el asiento como ocupado
                return f"Fila {fila}, Columna {columna}"  # Devuelve la fila y columna seleccionada
            else:
                print("El asiento seleccionado está ocupado. Por favor, elija otro.")  # Mensaje de error si el asiento está ocupado
        else:
            print("Asiento inválido. Intente nuevamente.")  # Mensaje de error si la fila o columna son inválidas

# Función para vender una entrada
def vender_entrada(partidos, estadios, clientes):
    nombre, cedula, edad, partido_id, tipo_entrada = solicitar_datos_cliente(partidos)  # Solicita los datos del cliente
    partido = next((p for p in partidos if p.id == partido_id), None)  # Busca el partido por ID
    if partido is None:  # Verifica si el partido existe
        print("Partido no encontrado.")  # Mensaje de error si no encuentra el partido
        return  # Termina la función si no encuentra el partido
    estadio = partido.estadio  # Asigna el estadio del partido
    asiento = seleccionar_asiento(estadio)  # Selecciona un asiento
    costo_entrada = calcular_costo_entrada(tipo_entrada, cedula)  # Calcula el costo de la entrada
    if costo_entrada is None:  # Verifica si el tipo de entrada es válido
        return  # Termina la función si el tipo de entrada es inválido
    subtotal, descuento, iva, total = costo_entrada  # Desempaqueta el costo de la entrada
    print(f"----- Detalle del Boleto -----\nNombre del cliente: {nombre}\nCédula: {cedula}\nEdad: {edad}\nPartido: {partido.home.name} vs {partido.away.name}\nEstadio: {estadio.name}\nAsiento: {asiento}\nCosto:\nSubtotal: ${subtotal}\nDescuento: ${subtotal * descuento}\nIVA (16%): ${iva}\nTotal: ${total}")  # Muestra el detalle del boleto
    if input("¿Quiere pagar la entrada? (Si/No): ").lower() == "si":  # Pregunta si quiere pagar la entrada
        cliente = Cliente(nombre, cedula, edad, tipo_entrada, estadio.name)  # Crea un cliente
        clientes.append(cliente)  # Añade el cliente a la lista
        print(f"Pago exitoso. Su entrada ha sido reservada. Su ID de entrada es: {cliente.id_boleto}")  # Mensaje de éxito
    else:
        print("Venta de entrada cancelada.")  # Mensaje de cancelación

# Función para imprimir los productos
def imprimir_producto(producto):
    print(f"Nombre: {producto.name}\nCantidad: {producto.quantity}\nPrecio (con IVA): {producto.price}\nAdicional: {producto.adicional}\nStock: {producto.stock}\n-------------------------")

# Función para realizar una compra en el restaurante
def realizar_compra_restaurante(cedula, estadios, clientes):
    cliente = next((c for c in clientes if c.cedula == cedula), None)  # Busca el cliente por cédula
    if cliente is None or cliente.tipo_entrada != "VIP":  # Verifica si el cliente existe y es VIP
        print("Cliente no encontrado o no es VIP.")  # Mensaje de error
        return  # Termina la función si no es VIP
    nombre_estadio = cliente.nombre_estadio  # Asigna el nombre del estadio
    productos_seleccionados = []  # Inicializa la lista de productos seleccionados
    monto_total = 0.0  # Inicializa el monto total
    estadio = next((e for e in estadios if e.name == nombre_estadio), None)  # Busca el estadio por nombre
    if estadio:  # Verifica si el estadio existe
        for restaurant in estadio.restaurants:  # Recorre los restaurantes
            for product in restaurant.products:  # Recorre los productos
                imprimir_producto(product)  # Muestra los productos
    while True:  # Ciclo para seleccionar productos
        nombre_producto = input("Nombre del producto que desea comprar ('fin' para finalizar): ").lower()  # Solicita el nombre del producto
        if nombre_producto == "fin":  # Verifica si el usuario quiere finalizar
            break  # Termina
        producto = next((p for r in estadio.restaurants for p in r.products if p.name.lower() == nombre_producto), None)  # Busca el producto por nombre
        if producto:  # Verifica si el producto existe
            if cliente.edad < 18 and producto.adicional.lower() == "alcoholic":  # Verifica si el cliente es menor de edad y el producto es alcohólico
                print("No puedes comprar bebidas alcohólicas.")  # Mensaje de error
            else:
                productos_seleccionados.append(producto)  # Añade el producto a la lista
                monto_total += producto.price  # Suma el precio del producto al monto total
        else:
            print("Producto no encontrado.")  # Mensaje de error si no encuentra el producto
    subtotal = monto_total  # Asigna el subtotal
    descuento = 0.15 * monto_total if es_numero_perfecto(int(cliente.cedula)) else 0  # Calcula el descuento si la cédula es un número perfecto
    monto_total -= descuento  # Resta el descuento al monto total
    print(f"Productos seleccionados:")  # Encabezado
    for producto in productos_seleccionados:  # Recorre los productos seleccionados
        imprimir_producto(producto)  # Muestra los productos seleccionados
    if input(f"Monto total: {monto_total}\n¿Desea proceder con la compra? (Si/No): ").lower() == "si":  # Pregunta si desea proceder con la compra
        print(f"Pago exitoso:\nSubtotal: ${subtotal}\nDescuento: ${descuento}\nTotal: ${monto_total}")  # Mensaje de éxito
        for producto in productos_seleccionados:  # Recorre los productos seleccionados
            producto.stock -= 1  # Reduce el stock del producto
    else:
        print("Venta de productos cancelada.")  # Mensaje de cancelación

# Función para validar un boleto
def validar_boleto(clientes, id_boleto):
    cliente_asistido = next((c for c in clientes if c.id_boleto == id_boleto), None)  # Busca el cliente por ID de boleto
    if cliente_asistido:  # Verifica si el cliente existe
        print(f"El boleto es válido. Cliente: {cliente_asistido.nombre}")  # Mensaje de éxito
    else:
        print("El ID del boleto no es válido. El boleto es falso.")  # Mensaje de error

# Función para buscar productos
def buscar_productos(estadios, criterio, valor_busqueda=None, precio_minimo=None, precio_maximo=None):
    for estadio in estadios:  # Recorre los estadios
        for restaurant in estadio.restaurants:  # Recorre los restaurantes
            for product in restaurant.products:  # Recorre los productos
                if criterio == "nombre" and valor_busqueda in product.name:  # Busca por nombre
                    imprimir_producto(product)  # Muestra el producto
                elif criterio == "tipo" and valor_busqueda.lower() in product.adicional.lower():  # Busca por tipo
                    imprimir_producto(product)  # Muestra el producto
                elif criterio == "rango" and precio_minimo <= product.price <= precio_maximo:  # Busca por rango de precio
                    imprimir_producto(product)  # Muestra el producto

# Función para guardar los datos actuales en un archivo
def guardar_datos_actuales(clientes, equipos, estadios, partidos):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual
    ruta = os.path.join(directorio_actual, "datos_actuales.txt")  # Define la ruta del archivo
    with open(ruta, "w") as archivo:  # Abre el archivo en modo escritura
        archivo.write("Equipos:\n")  # Encabezado de equipos
        for equipo in equipos:  # Recorre los equipos
            archivo.write(f"ID: {equipo.id}\nCodigo: {equipo.code}\nNombre: {equipo.name}\nGrupo: {equipo.group}\n-------------------------\n")  # Escribe los datos del equipo
        archivo.write("Clientes:\n")  # Encabezado de clientes
        for cliente in clientes:  # Recorre los clientes
            archivo.write(f"Nombre: {cliente.nombre}\nCédula: {cliente.cedula}\nEdad: {cliente.edad}\nTipo de entrada: {cliente.tipo_entrada}\nID del boleto: {cliente.id_boleto}\n-------------------------\n")  # Escribe los datos del cliente
        archivo.write("Estadios:\n")  # Encabezado de estadios
        for estadio in estadios:  # Recorre los estadios
            archivo.write(f"Estadio: {estadio.name}\nCiudad: {estadio.city}\nCapacidad general: {estadio.capacity_general}\nCapacidad vip: {estadio.capacity_vip}\nRestaurantes:\n")  # Escribe los datos del estadio
            for restaurant in estadio.restaurants:  # Recorre los restaurantes
                archivo.write(f"- Nombre: {restaurant.name}\n  Productos:\n")  # Escribe los datos del restaurante
                for product in restaurant.products:  # Recorre los productos
                    archivo.write(f"  - Nombre: {product.name}\n    Cantidad: {product.quantity}\n    Precio: {product.price}\n    Adicional: {product.adicional}\n    Stock: {product.stock}\n")  # Escribe los datos del producto
                archivo.write("\n")  # Línea en blanco
            archivo.write("\n")  # Línea en blanco
        archivo.write("Partidos:\n")  # Encabezado de partidos
        for partido in partidos:  # Recorre los partidos
            archivo.write(f"ID: {partido.id}\nNúmero: {partido.number}\nEquipo local: {partido.home.name}\nEquipo visitante: {partido.away.name}\nFecha: {partido.date}\nGrupo: {partido.group}\nEstadio: {partido.estadio.name}\n-------------------------\n")  # Escribe los datos del partido

# Función para calcular el promedio de gasto de clientes VIP
def promedio_gasto_clientes_vip(partidos, estadios, clientes):
    total_gastos = 0  # Inicializa el total de gastos
    cantidad_clientes_vip = 0  # Inicializa la cantidad de clientes VIP
    for cliente in clientes:  # Recorre los clientes
        if cliente.tipo_entrada == "VIP":  # Verifica si el cliente es VIP
            gasto_total = 0  # Inicializa el gasto total
            costo_ticket = calcular_costo_entrada(cliente.tipo_entrada, cliente.cedula)  # Calcula el costo del ticket
            if costo_ticket is not None:  # Verifica si el costo del ticket es válido
                subtotal, descuento, iva, _ = costo_ticket  # Desempaqueta el costo del ticket
                gasto_total += subtotal - (subtotal * descuento) + iva  # Calcula el gasto total
            nombre_estadio = cliente.nombre_estadio  # Asigna el nombre del estadio
            estadio = next((e for e in estadios if e.name == nombre_estadio), None)  # Busca el estadio por nombre
            if estadio:  # Verifica si el estadio existe
                for restaurant in estadio.restaurants:  # Recorre los restaurantes
                    for product in restaurant.products:  # Recorre los productos
                        gasto_total += product.price  # Suma el precio del producto al gasto total
            total_gastos += gasto_total  # Suma el gasto total al total de gastos
            cantidad_clientes_vip += 1  # Incrementa la cantidad de clientes VIP
    if cantidad_clientes_vip > 0:  # Verifica si hay clientes VIP
        promedio = total_gastos / cantidad_clientes_vip  # Calcula el promedio de gasto
        print(f"El promedio de gasto de un cliente VIP en un partido es de: ${promedio}")  # Muestra el promedio de gasto
    else:
        print("No hay clientes VIP registrados.")  # Mensaje si no hay clientes VIP

# Función para mostrar la asistencia a los partidos
def mostrar_asistencia_partidos(partidos, clientes):
    asistencia_partidos = []  # Inicializa la lista de asistencia
    for partido in partidos:  # Recorre los partidos
        boletos_vendidos = sum(1 for c in clientes if c.nombre_estadio == partido.estadio.name and c.tipo_entrada != "")  # Cuenta los boletos vendidos
        personas_asistieron = boletos_vendidos  # Asigna las personas que asistieron
        relacion_asistencia_venta = personas_asistieron / boletos_vendidos if boletos_vendidos > 0 else 0  # Calcula la relación asistencia/venta
        asistencia_partidos.append((partido, boletos_vendidos, personas_asistieron, relacion_asistencia_venta))  # Añade la asistencia a la lista
    asistencia_partidos.sort(key=lambda x: x[3], reverse=True)  # Ordena la lista por relación asistencia/venta
    print("----- Tabla de Asistencia a los Partidos -----")  # Encabezado
    print("{:<30} {:<20} {:<15} {:<15} {:<25}".format("Partido", "Estadio", "Boletos Vendidos", "Personas Asistieron", "Relación Asistencia/Venta"))  # Encabezados de columna
    for partido, boletos_vendidos, personas_asistieron, relacion_asistencia_venta in asistencia_partidos:  # Recorre la lista de asistencia
        print("{:<30} {:<20} {:<15} {:<15} {:<25}".format(f"{partido.home.name} vs {partido.away.name}", partido.estadio.name, boletos_vendidos, personas_asistieron, relacion_asistencia_venta))  # Muestra los datos de asistencia

# Función para encontrar el partido con mayor asistencia
def encontrar_partido_mayor_asistencia(partidos, clientes):
    partido_mayor_asistencia = None  # Inicializa el partido con mayor asistencia
    mayor_asistencia = 0  # Inicializa la mayor asistencia
    for partido in partidos:  # Recorre los partidos
        personas_asistieron = sum(1 for c in clientes if c.nombre_estadio == partido.estadio.name and c.tipo_entrada != "")  # Cuenta las personas que asistieron
        if personas_asistieron > mayor_asistencia:  # Verifica si la asistencia es mayor
            mayor_asistencia = personas_asistieron  # Asigna la mayor asistencia
            partido_mayor_asistencia = partido  # Asigna el partido con mayor asistencia
    if partido_mayor_asistencia:  # Verifica si hay un partido con mayor asistencia
        print(f"El partido con mayor asistencia fue: {partido_mayor_asistencia.home.name} vs {partido_mayor_asistencia.away.name}")  # Muestra el partido con mayor asistencia
    else:
        print("No hay partidos registrados.")  # Mensaje si no hay partidos registrados

# Función para encontrar el partido con mayor boletos vendidos
def encontrar_partido_mayor_boletos_vendidos(partidos, clientes):
    partido_mayor_boletos = None  # Inicializa el partido con mayor boletos vendidos
    mayor_boletos_vendidos = 0  # Inicializa el mayor boletos vendidos
    for partido in partidos:  # Recorre los partidos
        boletos_vendidos = sum(1 for c in clientes if c.nombre_estadio == partido.estadio.name and c.tipo_entrada != "")  # Cuenta los boletos vendidos
        if boletos_vendidos > mayor_boletos_vendidos:  # Verifica si los boletos vendidos son mayores
            mayor_boletos_vendidos = boletos_vendidos  # Asigna el mayor boletos vendidos
            partido_mayor_boletos = partido  # Asigna el partido con mayor boletos vendidos
    if partido_mayor_boletos:  # Verifica si hay un partido con mayor boletos vendidos
        print(f"El partido con mayor número de boletos vendidos fue: {partido_mayor_boletos.home.name} vs {partido_mayor_boletos.away.name}")  # Muestra el partido con mayor boletos vendidos
    else:
        print("No hay partidos registrados.")  # Mensaje si no hay partidos registrados

# Función para obtener el top 3 de productos más vendidos
def obtener_top_productos_vendidos(estadios, clientes):
    productos_vendidos = {}  # Inicializa el diccionario de productos vendidos
    for estadio in estadios:  # Recorre los estadios
        for restaurant in estadio.restaurants:  # Recorre los restaurantes
            for product in restaurant.products:  # Recorre los productos
                total_vendidos = sum(1 for cliente in clientes if cliente.tipo_entrada == "VIP" and cliente.nombre_estadio == estadio.name)  # Cuenta los productos vendidos
                if product.name in productos_vendidos:  # Verifica si el producto ya está en el diccionario
                    productos_vendidos[product.name] += total_vendidos  # Suma los productos vendidos
                else:
                    productos_vendidos[product.name] = total_vendidos  # Añade el producto al diccionario
    top_productos = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)[:3]  # Ordena los productos por cantidad vendida y obtiene el top 3
    if top_productos:  # Verifica si hay productos vendidos
        print("Los tres productos más vendidos en el restaurante son:")  # Encabezado
        for producto, cantidad_vendida in top_productos:  # Recorre los productos más vendidos
            print(f"- Producto: {producto}\n  Cantidad vendida: {cantidad_vendida}")  # Muestra el producto y la cantidad vendida
    else:
        print("No hay productos registrados.")  # Mensaje si no hay productos registrados
    return top_productos  # Devuelve el top 3 de productos más vendidos

# Función para obtener el top 3 de clientes que más compraron boletos
def obtener_top_clientes_compradores(clientes):
    clientes_boletos = {}  # Inicializa el diccionario de clientes y boletos comprados
    for cliente in clientes:  # Recorre los clientes
        boletos_comprados = sum(1 for item in cliente.tipo_entrada if item != "")  # Cuenta los boletos comprados
        clientes_boletos[cliente] = boletos_comprados  # Añade el cliente y los boletos comprados al diccionario
    top_clientes = sorted(clientes_boletos.items(), key=lambda x: x[1], reverse=True)[:3]  # Ordena los clientes por boletos comprados y obtiene el top 3
    if top_clientes:  # Verifica si hay clientes que compraron boletos
        print("Los tres clientes que más compraron boletos son:")  # Encabezado
        for cliente, boletos_comprados in top_clientes:  # Recorre los clientes que más compraron boletos
            print(f"- Cliente: {cliente.nombre}\n  Boletos comprados: {boletos_comprados}")  # Muestra el cliente y los boletos comprados
    else:
        print("No hay clientes registrados.")  # Mensaje si no hay clientes registrados
    return top_clientes  # Devuelve el top 3 de clientes que más compraron boletos

# Función para graficar el top 3 de productos más vendidos
def graficar_top_productos_vendidos(top_productos):
    if top_productos:  # Verifica si hay productos vendidos
        productos = [producto[0] for producto in top_productos]  # Obtiene los nombres de los productos
        cantidades = [producto[1] for producto in top_productos]  # Obtiene las cantidades vendidas
        plt.bar(productos, cantidades)  # Crea un gráfico de barras
        plt.xlabel('Productos')  # Etiqueta del eje x
        plt.ylabel('Cantidad vendida')  # Etiqueta del eje y
        plt.title('Top 3 productos más vendidos')  # Título del gráfico
        plt.show()  # Muestra el gráfico
    else:
        print("No hay productos registrados.")  # Mensaje si no hay productos registrados

# Función para graficar el top 3 de clientes que más compraron boletos
def graficar_top_clientes_compradores(top_clientes):
    if top_clientes:  # Verifica si hay clientes que compraron boletos
        clientes = [cliente[0].nombre for cliente in top_clientes]  # Obtiene los nombres de los clientes
        boletos = [cliente[1] for cliente in top_clientes]  # Obtiene la cantidad de boletos comprados
        p = figure(x_range=clientes, plot_height=350, title='Top 3 clientes que más compraron boletos')  # Crea un gráfico de barras
        p.vbar(x=clientes, top=boletos, width=0.9)  # Añade las barras al gráfico
        p.xaxis.axis_label = 'Clientes'  # Etiqueta del eje x
        p.yaxis.axis_label = 'Boletos comprados'  # Etiqueta del eje y
        show(p)  # Muestra el gráfico
    else:
        print("No hay clientes registrados.")  # Mensaje si no hay clientes registrados

# Función principal
def main():
    equipos, estadios, partidos = cargar_datos()  # Carga los datos
    clientes = []  # Inicializa la lista de clientes
    while True:  # Ciclo principal
        print("-- Eurocopa 2024 --\nMenu Principal del Sistema:\n1. Busqueda de partidos.\n2. Venta de entradas.\n3. Validar boleto.\n4. Buscar productos.\n5. Comprar productos.\n6. Mostrar estadísticas.\n7. Salir.")  # Muestra el menú
        opcion = input("Elija una opcion: ")  # Solicita una opción
        if opcion == "1":  # Si la opción es 1
            op = input("Elija el filtro (pais, estadio, fecha): ").lower()  # Solicita el filtro
            if op == "pais":  # Si el filtro es país
                pais = input("Nombre del pais: ")  # Solicita el nombre del país
                partidos_pais = buscar_partidos_por_pais(pais, partidos)  # Busca los partidos por país
                if partidos_pais:  # Verifica si hay partidos
                    print(f"Partidos de {pais}:")  # Encabezado
                    for partido in partidos_pais:  # Recorre los partidos
                        print(f"Equipo local: {partido.home.name} vs Equipo visitante: {partido.away.name}")  # Muestra los partidos
                else:
                    print(f"No se encontraron partidos de {pais}.")  # Mensaje si no hay partidos
            elif op == "estadio":  # Si el filtro es estadio
                estadio = input("Nombre del estadio: ")  # Solicita el nombre del estadio
                partidos_estadio = buscar_partidos_por_estadio(estadio, partidos)  # Busca los partidos por estadio
                if partidos_estadio:  # Verifica si hay partidos
                    print(f"Partidos en {estadio}")  # Encabezado
                    for partido in partidos_estadio:  # Recorre los partidos
                        print(f"Equipo local: {partido.home.name} vs Equipo visitante: {partido.away.name}")  # Muestra los partidos
                else:
                    print(f"No se encontraron partidos en el estadio {estadio}.")  # Mensaje si no hay partidos
            elif op == "fecha":  # Si el filtro es fecha
                fecha = input("Fecha del partido (aaaa-mm-dd): ")  # Solicita la fecha
                partidos_fecha = buscar_partidos_por_fecha(fecha, partidos)  # Busca los partidos por fecha
                if partidos_fecha:  # Verifica si hay partidos
                    print(f"Partidos en la fecha {fecha}:")  # Encabezado
                    for partido in partidos_fecha:  # Recorre los partidos
                        print(f"ID: {partido.id}, Equipo local: {partido.home.name}, Equipo visitante: {partido.away.name}, Estadio: {partido.estadio.name}\n-----")  # Muestra los partidos
                else:
                    print(f"No se encontraron partidos en la fecha {fecha}.")  # Mensaje si no hay partidos
            else:
                print("Opción incorrecta.")  # Mensaje si la opción es incorrecta
        elif opcion == "2":  # Si la opción es 2
            vender_entrada(partidos, estadios, clientes)  # Vende una entrada
        elif opcion == "3":  # Si la opción es 3
            id_boleto = input("Ingrese ID del Boleto: ")  # Solicita el ID del boleto
            validar_boleto(clientes, id_boleto)  # Valida el boleto
        elif opcion == "4":  # Si la opción es 4
            op = input("Elija el filtro (nombre, tipo, rango): ").lower()  # Solicita el filtro
            if op == "nombre":  # Si el filtro es nombre
                name = input("Nombre del producto: ")  # Solicita el nombre del producto
                buscar_productos(estadios, "nombre", name)  # Busca productos por nombre
            elif op == "tipo":  # Si el filtro es tipo
                tipo = input("Tipo: (alcoholic, non-alcoholic, package, plate): ")  # Solicita el tipo de producto
                buscar_productos(estadios, "tipo", tipo)  # Busca productos por tipo
            elif op == "rango":  # Si el filtro es rango
                inf = float(input("Rango inferior: "))  # Solicita el rango inferior
                sup = float(input("Rango superior: "))  # Solicita el rango superior
                buscar_productos(estadios, "rango", precio_minimo=inf, precio_maximo=sup)  # Busca productos por rango de precio
            else:
                print("Opción incorrecta.")  # Mensaje si la opción es incorrecta
        elif opcion == "5":  # Si la opción es 5
            cedula = input("Ingrese cedula del cliente: ")  # Solicita la cédula del cliente
            realizar_compra_restaurante(cedula, estadios, clientes)  # Realiza una compra en el restaurante
        elif opcion == "6":  # Si la opción es 6
            promedio_gasto_clientes_vip(partidos, estadios, clientes)  # Muestra el promedio de gasto de clientes VIP
            mostrar_asistencia_partidos(partidos, clientes)  # Muestra la asistencia a los partidos
            encontrar_partido_mayor_asistencia(partidos, clientes)  # Encuentra el partido con mayor asistencia
            encontrar_partido_mayor_boletos_vendidos(partidos, clientes)  # Encuentra el partido con mayor boletos vendidos
            top_productos = obtener_top_productos_vendidos(estadios, clientes)  # Obtiene el top 3 de productos más vendidos
            top_clientes = obtener_top_clientes_compradores(clientes)  # Obtiene el top 3 de clientes que más compraron boletos
            graficar_top_productos_vendidos(top_productos)  # Grafica el top 3 de productos más vendidos
            graficar_top_clientes_compradores(top_clientes)  # Grafica el top 3 de clientes que más compraron boletos
        elif opcion == "7":  # Si la opción es 7
            guardar_datos_actuales(clientes, equipos, estadios, partidos)  # Guarda los datos actuales
            print("Saliendo del sistema. Presione ENTER para salir.")  # Mensaje de salida
            input()  # Espera una entrada
            break  # Termina el ciclo
        else:
            print("Opción incorrecta.")  # Mensaje si la opción es incorrecta

if __name__ == "__main__":  # Punto de entrada
    main()  # Ejecuta la función principal
