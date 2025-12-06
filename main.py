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

    def __str__(self):
        return f"{self.id_destino} - {self.nombre} - {self.descripcion} - {self.actividades} - {self.costo}"

class DestinoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_destino(self, destino):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Destino (nombre, descripcion, actividades, costo) VALUES (:1,:2,:3,:4)",
                       (destino.nombre, destino.descripcion, destino.actividades, destino.costo))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def mostrar_destino(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Destino")
        registros = cursor.fetchall()
        cursor.close()
        destinos = []
        for r in registros:
            destinos.append(Destino(r[0], r[1], r[2], r[3], r[4]))
        return destinos

    def eliminar_destino(self, id_destino):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM Destino WHERE id_destino = :1", (id_destino,))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def buscar_destino(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Destino WHERE nombre = :1", (nombre,))
        r = cursor.fetchone()
        cursor.close()
        if r:
            return Destino(r[0], r[1], r[2], r[3], r[4])
        return None

class PaqueteTuristico:
    def __init__(self, id, destino_id, fecha_inicio, fecha_fin, precio_total):
        self.id = id
        self.destino_id = destino_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total

class PaqueteTuristicoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_paquete(self, paquete):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Paquetes (destino_id, fecha_inicio, fecha_fin, precio_paquete) VALUES (:1,:2,:3,:4)",
                       (paquete.destino_id, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def mostrar_paquetes(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Paquetes")
        filas = cursor.fetchall()
        cursor.close()
        return filas

class Cliente:
    def __init__(self, id_cliente, nombre, clave, is_admin):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.clave = clave
        self.is_admin = bool(is_admin)

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
        cursor.execute("SELECT id_cliente, nombre, clave, is_admin FROM Clientes WHERE nombre = :1", (nombre,))
        r = cursor.fetchone()
        cursor.close()
        if r:
            return Cliente(r[0], r[1], r[2], r[3])
        return None

class Reserva:
    def __init__(self, id, cliente_id, paquete_id, fecha_reserva):
        self.id = id
        self.cliente_id = cliente_id
        self.paquete_id = paquete_id
        self.fecha_reserva = fecha_reserva

class ReservaDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_reserva(self, reserva):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Reservas (id_cliente, id_paquete, fecha_reserva) VALUES (:1,:2,:3)",
                       (reserva.cliente_id, reserva.paquete_id, reserva.fecha_reserva))
        self.conexion.commit()
        fila = cursor.rowcount
        cursor.close()
        return fila

    def mostrar_reservas(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Reservas")
        filas = cursor.fetchall()
        cursor.close()
        return filas

def hashear(password):
    b = password.encode("utf-8")
    salt = bcrypt.gensalt()
    h = bcrypt.hashpw(b, salt)
    return h.decode()

def verificarPassword(intento, hasheado):
    return bcrypt.checkpw(intento.encode("utf-8"), hasheado.encode("utf-8"))

try:
    conexion = oracledb.connect(
        user="system",
        password="12345",
        dsn="localhost:1521/XEPDB1"
    )

    destinoDAO = DestinoDAO(conexion)
    paqueteDAO = PaqueteTuristicoDAO(conexion)
    clienteDAO = ClienteDAO(conexion)
    reservaDAO = ReservaDAO(conexion)

    while True:
        print('/'*30)
        print("Menu de Registro")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Salir")
        select = input("Seleccione una opcion: ")

        if select == "1":
            nombre = input("Nombre: ")
            if clienteDAO.iniciar_sesion(nombre):
                print("Ese nombre ya existe.")
            else:
                clave = input("Contraseña: ")
                clave_h = hashear(clave)
                print("¿Es admin? (1 = Sí / 0 = No)")
                is_admin = int(input("-> "))
                user = Cliente(None, nombre, clave_h, is_admin)
                fila = clienteDAO.Registrarse(user)
                print("Registrado.")

        elif select == "2":
            nombre = input("Nombre de usuario: ")
            cliente = clienteDAO.iniciar_sesion(nombre)

            if cliente:
                clave = input("Contraseña: ")
                if verificarPassword(clave, cliente.clave):
                    print("Bienvenido", cliente.nombre)

                    if cliente.is_admin:
                        while True:
                            print("------ Menú Administrador ------")
                            print("1. Agregar Destino")
                            print("2. Mostrar Destinos")
                            print("3. Eliminar Destino")
                            print("4. Buscar Destino")
                            print("5. Crear Paquete")
                            print("6. Mostrar Paquetes")
                            print("7. Ver Reservas")
                            print("8. Cerrar Sesión")
                            op = input("Opción: ")

                            if op == "1":
                                n = input("Nombre destino: ")
                                dsc = input("Descripción: ")
                                act = input("Actividades: ")
                                costo = float(input("Costo: "))
                                dest = Destino(None, n, dsc, act, costo)
                                destinoDAO.crear_destino(dest)
                                print("Destino agregado.")

                            elif op == "2":
                                for d in destinoDAO.mostrar_destino():
                                    print(d)

                            elif op == "3":
                                for d in destinoDAO.mostrar_destino():
                                    print(d)
                                did = int(input("ID destino: "))
                                destinoDAO.eliminar_destino(did)
                                print("Destino eliminado.")

                            elif op == "4":
                                n = input("Nombre del destino: ")
                                print(destinoDAO.buscar_destino(n))

                            elif op == "5":
                                destinos = destinoDAO.mostrar_destino()
                                for d in destinos:
                                    print(d)
                                did = int(input("ID destino: "))
                                fi = input("Fecha inicio: ")
                                ff = input("Fecha fin: ")
                                precio = 0
                                for d in destinos:
                                    if d.id_destino == did:
                                        precio = d.costo
                                        break
                                paquete = PaqueteTuristico(None, did, fi, ff, precio)
                                paqueteDAO.crear_paquete(paquete)
                                print("Paquete creado.")

                            elif op == "6":
                                for p in paqueteDAO.mostrar_paquetes():
                                    print(p)

                            elif op == "7":
                                for r in reservaDAO.mostrar_reservas():
                                    print(r)

                            elif op == "8":
                                break

                    else:
                        while True:
                            print("----- Menú Cliente -----")
                            print("1. Ver destinos")
                            print("2. Reservar paquete")
                            print("3. Ver mis reservas")
                            print("4. Ver paquetes")
                            print("5. Cerrar sesión")
                            op = input("Opción: ")

                            if op == "1":
                                for d in destinoDAO.mostrar_destino():
                                    print(d)

                            elif op == "2":
                                paquetes = paqueteDAO.mostrar_paquetes()
                                for p in paquetes:
                                    print(p)
                                pid = int(input("ID del paquete: "))
                                fecha = input("Fecha reserva: ")
                                reserva = Reserva(None, cliente.id_cliente, pid, fecha)
                                reservaDAO.crear_reserva(reserva)
                                print("Reserva creada.")

                            elif op == "3":
                                for r in reservaDAO.mostrar_reservas():
                                    print(r)

                            elif op == "4":
                                for p in paqueteDAO.mostrar_paquetes():
                                    print(p)
                else:
                    print("Contraseña incorrecta.")
            else:
                print("Usuario no encontrado.")

        elif select == "3":
            break

except Exception as e:
    print("Error:", e)
