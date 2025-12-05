import requests
import oracledb
import bcrypt

class Destino:
    def __init__(self, id_destino, nombre, descripcion, actividades, costo):
        self.id_destino = id_destino
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo
        self.paquetesTuristicos = []

    def agregarpaquete(self, paquete):
        self.paquetesTuristicos.append(paquete)

    def __str__(self):
        return f"ID: {self.id_destino} - {self.nombre} - {self.descripcion} - {self.actividades} - {self.costo}"


class DestinoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_destino(self, destino):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO DESTINO (nombre, descripcion, actividades, costo) VALUES (:1,:2,:3,:4)",(destino.nombre, destino.descripcion, destino.actividades, destino.costo))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def mostrar_destino(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM DESTINO")
        registros = cursor.fetchall()
        cursor.close()
        destinos = []
        for r in registros:
            d = Destino(r[0], r[1], r[2], r[3], r[4])
            destinos.append(d)
        return destinos

    def eliminar_destino(self, id_destino):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM DESTINO WHERE id_destino = :1", (id_destino,))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def buscar_destino(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM DESTINO WHERE nombre = :1", (nombre,))
        r = cursor.fetchone()
        cursor.close()
        if r:
            return Destino(r[0], r[1], r[2], r[3], r[4])
        return None


class PaqueteTuristico:
    def __init__(self, id, destinos, fecha_inicio, fecha_fin, precio_total):
        self.id = id
        self.destinos = destinos
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total


class PaqueteTuristicoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def agregar_destino(self):
        pass

    def calcular_precio(self):
        pass
    
    def mostrar_paquete(self):
        pass
    
    def disponible_en_fecha(self):
        pass


class Cliente:
    def __init__(self, id_cliente, nombre, clave, is_admin):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.clave = clave
        self.is_admin = bool(is_admin)

    def __str__(self):
        tipo = "Administrador" if self.is_admin else "Cliente"
        return f"{self.nombre} ({tipo})"


class ClienteDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def Registrarse(self, user):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Clientes (nombre, clave, is_admin) VALUES (:1,:2,:3)",
                       (user.nombre, user.clave, int(user.is_admin)))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def iniciar_sesion(self, nombre):
        cursor = self.conexion.cursor()
        ##esto de aca lo hice mas para evitar error porque me lo daba deberia solo ser select from * clientes pero iwl xd
        cursor.execute("SELECT id_cliente, nombre, clave, is_admin FROM Clientes WHERE nombre = :1", (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        return None

    def mostrar_cliente(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE nombre = :1", (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        return None


def hashear(password):
    passwordB = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hasheado = bcrypt.hashpw(passwordB, salt)
    return hasheado.decode()

def verificarPassword(intento_pw, hasheado):
    intento_pw = intento_pw.encode("utf-8")
    hasheado = hasheado.encode("utf-8")
    return bcrypt.checkpw(intento_pw, hasheado)


class Reserva:
    def __init__(self, id, cliente_id, paquete_id, fecha_reserva):
        self.id = id
        self.cliente_id = cliente_id
        self.paquete_id = paquete_id
        self.fecha_reserva = fecha_reserva


class ReservaDAO:
    def __init__(self, conexion):
        self.conexion = conexion


try:
    conexion = oracledb.connect(
        user="system",
        password="123456",
        dsn="localhost:1521/XEPDB1"
    )

    destinoDAO = DestinoDAO(conexion)
    paqueteDAO = PaqueteTuristicoDAO(conexion)
    clienteDAO = ClienteDAO(conexion)
    reservaDAO = ReservaDAO(conexion)

    while True:
        print('/'*30)
        print("      Menu de Registro")
        print("(1.) Registrar usuario")
        print("(2.) Iniciar sesion")
        print("(3.) Salir")
        select = input("Seleccione una opcion : ")

        if select == "1":
            nombre = input("Nombre: ")
            if clienteDAO.iniciar_sesion(nombre):
                print("Ese nombre ya existe. Elige otro -_-")
            else:
                clave = input("Contraseña: ")
                password_hasheado = hashear(clave)

                ##esto de aca es mas para asignar el admin desde consola pero lo sacamos despues xd
                print("¿Es admin? (1 = Sí / 0 = No)")
                is_admin = int(input("-> "))

                user = Cliente(None, nombre, password_hasheado, is_admin)
                fila = clienteDAO.Registrarse(user)
                print(f"{fila} Registrado con exito")

        elif select == "2":
            nombre = input("Ingrese nombre de usuario: ")
            cliente = clienteDAO.iniciar_sesion(nombre)

            if cliente:
                clave = input("Ingrese su contraseña: ")

                if verificarPassword(clave, cliente.clave):
                    print(f"Bienvenido {cliente.nombre}!")

                    if cliente.is_admin:
                        print("Eres Dios")

                        while True:
                            print("------ Menú Administrador ------")
                            print("1. Agregar Destino")
                            print("2. Mostrar Destinos")
                            print("3. Eliminar Destino")
                            print("4. Buscar Destino por Nombre")
                            print("5. Cerrar Sesión")
                            op = input("Opción: ")

                            if op == "1":
                                nombre = input("Nombre destino: ")
                                descripcion = input("Descripción: ")
                                actividades = input("Actividades: ")
                                costo = float(input("Costo: "))

                                dest = Destino(None, nombre, descripcion, actividades, costo)
                                fila = destinoDAO.crear_destino(dest)
                                print("Destino agregado.",fila)

                                ## funciona la opcion pero por una razon no llama el str de la clase destino y se imprime todo junto -_-
                            elif op == "2":
                                for d in destinoDAO.mostrar_destino():
                                    print(d)

                            elif op == "3":
                                ##esto lo coloque mas que nada para saber que ids hay xd
                                for d in destinoDAO.mostrar_destino():
                                    print(d)
                                id_destino = int(input("Ingrese el ID del destino a eliminar: "))
                                filas = destinoDAO.eliminar_destino(id_destino)
                                print("Se ha eliminado con exito!")

                            elif op =="4":
                                nombre = input("Ingresa el nombre del destino a buscar: ")
                                filas = destinoDAO.buscar_destino(nombre)
                                print(filas)

                            elif op == "5":
                                break

                            else:
                                print("Opción inválida")

                    else:
                        print("Eres Cliente. Acceso limitado.")
                        while True:
                            print("----- Menú Cliente -----")
                            print("1. Ver destinos")
                            print("2. Cerrar sesión")
                            op = input("Opción: ")

                            if op == "1":
                                destinos = destinoDAO.mostrar_destino()
                                for d in destinos:
                                    print(d)

                            elif op == "2":
                                break

                            else:
                                print("Opción inválida")

                else:
                    print("Contraseña incorrecta")

            else:
                print("Usuario no encontrado")

        elif select == "3":
            break

        else:
            print("Opción inválida")

except Exception as e:
    print("Error:", e)

