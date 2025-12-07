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
        return f"id: {self.id_destino} - nombre: {self.nombre} - descripcion: {self.descripcion} - actividades: {self.actividades} - costo: {self.costo}"


class DestinoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_destino(self, destino):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Destino (nombre, descripcion, actividades, costo) VALUES (:1,:2,:3,:4)",
                       (destino.nombre, destino.descripcion, destino.actividades, destino.costo))
        self.conexion.commit()
        cursor.close()

    def mostrar_destino(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Destino")
        datos = cursor.fetchall()
        cursor.close()
        lista = []
        for d in datos:
            lista.append(Destino(d[0], d[1], d[2], d[3], d[4]))
        return lista

    def eliminar_destino(self, id_destino):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM Destino WHERE id_destino = :1", (id_destino,))
        self.conexion.commit()
        cursor.close()

    def buscar_destino(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Destino WHERE LOWER(nombre) = :1", (nombre.lower(),))
        d = cursor.fetchone()
        cursor.close()
        if d:
            return Destino(d[0], d[1], d[2], d[3], d[4])
        return None


class PaqueteTuristico:
    def __init__(self, id, destino_id, fecha_inicio, fecha_fin, precio_total):
        self.id = id
        self.destino_id = destino_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total

    def __str__(self):
        return f"id: {self.id} - destino: {self.destino_id} - inicio: {self.fecha_inicio} - fin: {self.fecha_fin} - precio: {self.precio_total}"


class PaqueteTuristicoDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_paquete(self, paquete):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Paquetes (destino_id, fecha_inicio, fecha_fin, precio_paquete) VALUES (:1,:2,:3,:4)",
                       (paquete.destino_id, paquete.fecha_inicio, paquete.fecha_fin, paquete.precio_total))
        self.conexion.commit()
        cursor.close()

    def mostrar_paquetes(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Paquetes")
        datos = cursor.fetchall()
        cursor.close()
        lista = []
        for p in datos:
            lista.append(PaqueteTuristico(p[0], p[1], p[2], p[3], p[4]))
        return lista


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
        cursor.close()

    def iniciar_sesion(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre, clave, is_admin FROM Clientes WHERE nombre = :1", (nombre,))
        d = cursor.fetchone()
        cursor.close()
        if d:
            return Cliente(d[0], d[1], d[2], d[3])
        return None


class Reserva:
    def __init__(self, id, cliente_id, paquete_id, fecha_reserva):
        self.id = id
        self.cliente_id = cliente_id
        self.paquete_id = paquete_id
        self.fecha_reserva = fecha_reserva

    def __str__(self):
        return f"id: {self.id} - cliente: {self.cliente_id} - paquete: {self.paquete_id} - fecha: {self.fecha_reserva}"


class ReservaDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_reserva(self, reserva):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Reservas (id_cliente, id_paquete, fecha_reserva) VALUES (:1,:2,:3)",
                       (reserva.cliente_id, reserva.paquete_id, reserva.fecha_reserva))
        self.conexion.commit()
        cursor.close()

    def mostrar_reservas(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Reservas")
        datos = cursor.fetchall()
        cursor.close()
        lista = []
        for r in datos:
            lista.append(Reserva(r[0], r[1], r[2], r[3]))
        return lista


def hashear(p):
    b = p.encode("utf-8")
    salt = bcrypt.gensalt()
    h = bcrypt.hashpw(b, salt)
    return h.decode()

def verificarPassword(intento, real):
    return bcrypt.checkpw(intento.encode("utf-8"), real.encode("utf-8"))


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
        print("/"*35)
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Salir")
        op = input("Opcion: ")

        if op == "1":
            nombre = input("Nombre: ").strip().lower()
            if clienteDAO.iniciar_sesion(nombre):
                print("Ese nombre ya existe.")
            else:
                clave = input("Contraseña: ")
                clave_h = hashear(clave)
                try:
                    is_admin = int(input("¿Es admin? (1/0): "))
                except:
                    is_admin = 0
                user = Cliente(None, nombre, clave_h, is_admin)
                clienteDAO.Registrarse(user)
                print("Registrado.")

        elif op == "2":
            nombre = input("Nombre: ").strip().lower()
            cliente = clienteDAO.iniciar_sesion(nombre)

            if cliente:
                clave = input("Contraseña: ")
                if verificarPassword(clave, cliente.clave):

                    if cliente.is_admin:
                        while True:
                            print("---- ADMIN ----")
                            print("1. Agregar destino")
                            print("2. Mostrar destinos")
                            print("3. Eliminar destino")
                            print("4. Buscar destino")
                            print("5. Crear paquete")
                            print("6. Mostrar paquetes")
                            print("7. Ver reservas")
                            print("8. Cerrar")
                            op2 = input("Opcion: ")

                            if op2 == "1":
                                n = input("Nombre: ")
                                dsc = input("Descripcion: ")
                                act = input("Actividades: ")
                                while True:
                                    try:
                                        costo = float(input("Costo: "))
                                        break
                                    except:
                                        print("Ingrese numero.")
                                dest = Destino(None, n, dsc, act, costo)
                                destinoDAO.crear_destino(dest)
                                print("Destino agregado.")

                            elif op2 == "2":
                                lista = destinoDAO.mostrar_destino()
                                for d in lista:
                                    print(d)

                            elif op2 == "3":
                                lista = destinoDAO.mostrar_destino()
                                for d in lista:
                                    print(d)
                                try:
                                    eliminar = int(input("ID: "))
                                except:
                                    print("ID invalido.")
                                    continue
                                destinoDAO.eliminar_destino(eliminar)
                                print("Eliminado.")

                            elif op2 == "4":
                                n = input("Nombre: ")
                                print(destinoDAO.buscar_destino(n))

                            elif op2 == "5":
                                lista = destinoDAO.mostrar_destino()
                                if not lista:
                                    print("No hay destinos.")
                                    continue
                                for d in lista:
                                    print(d)
                                try:
                                    did = int(input("ID destino: "))
                                except:
                                    print("ID invalido.")
                                    continue
                                existe = False
                                costo = 0
                                for d in lista:
                                    if d.id_destino == did:
                                        existe = True
                                        costo = d.costo
                                if not existe:
                                    print("No existe.")
                                    continue
                                fi = input("Fecha inicio: ")
                                ff = input("Fecha fin: ")
                                p = PaqueteTuristico(None, did, fi, ff, costo)
                                try:
                                    paqueteDAO.crear_paquete(p)
                                except:
                                    print("Error al crear paquete.")
                                else:
                                    print("Paquete creado.")

                            elif op2 == "6":
                                lista = paqueteDAO.mostrar_paquetes()
                                for p in lista:
                                    print(p)

                            elif op2 == "7":
                                lista = reservaDAO.mostrar_reservas()
                                for r in lista:
                                    print(r)

                            elif op2 == "8":
                                break

                    else:
                        while True:
                            print("---- CLIENTE ----")
                            print("1. Ver destinos")
                            print("2. Reservar paquete")
                            print("3. Mis reservas")
                            print("4. Ver paquetes")
                            print("5. Cerrar")
                            op3 = input("Opcion: ")

                            if op3 == "1":
                                lista = destinoDAO.mostrar_destino()
                                for d in lista:
                                    print(d)

                            elif op3 == "2":
                                lista = paqueteDAO.mostrar_paquetes()
                                if not lista:
                                    print("No hay paquetes.")
                                    continue
                                for p in lista:
                                    print(p)
                                try:
                                    pid = int(input("ID paquete: "))
                                except:
                                    print("ID invalido.")
                                    continue
                                existe = False
                                for p in lista:
                                    if p.id == pid:
                                        existe = True
                                if not existe:
                                    print("No existe.")
                                    continue
                                fecha = input("Fecha reserva: ")
                                r = Reserva(None, cliente.id_cliente, pid, fecha)
                                try:
                                    reservaDAO.crear_reserva(r)
                                except:
                                    print("No se pudo reservar.")
                                else:
                                    print("Reservado.")

                            elif op3 == "3":
                                lista = reservaDAO.mostrar_reservas()
                                hay = False
                                for r in lista:
                                    if r.cliente_id == cliente.id_cliente:
                                        print(r)
                                        hay = True
                                if not hay:
                                    print("No tiene reservas.")

                            elif op3 == "4":
                                lista = paqueteDAO.mostrar_paquetes()
                                for p in lista:
                                    print(p)

                            elif op3 == "5":
                                break

                else:
                    print("Contraseña incorrecta.")
            else:
                print("Usuario no encontrado.")

        elif op == "3":
            break

except Exception as e:
    print("Error:", e)


# ----------------------------------------------
# Código creado por el grupo: Pa que try si igual Except :)
# ----------------------------------------------