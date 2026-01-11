from abc import ABC#importar ABCMeta
from abc import abstractmethod#importar abstractmethod
import json#importar json
import os#importar os

class Autenticable(ABC):#Interfaz Autenticable
    @abstractmethod#Método iniciar sesión
    def iniciar_sesion(self):
        pass
    @abstractmethod#Método cerrar sesión
    def cerrar_sesion(self):
        pass

class AsignarSede(ABC):#Interfaz AsignarSede
    @abstractmethod#Método asignar sede
    def asignar_sede(self, sede: str):
        pass

class Cargable(ABC):#Interfaz Cargable
    @abstractmethod#Método cargar datos
    def cargar_datos(self):
        pass

class SolicitudAsistencia(ABC):#Clase SolicitudAsistencia
    @abstractmethod#Método crear solicitud asistencia
    def crear_solicitud_asistencia(self, asunto: str):
        pass
    @abstractmethod#Método estado solicitud
    def estado_solicitud(self, estado: str):
        pass

class GestorSede(ABC):#Clase GestorSede
    @abstractmethod#Método notificar sede
    def notificar_sede(self, sede: str):
        pass
    @abstractmethod#Método imprimir documentación sede
    def imprimir_documentacion_sede(self, sede: str):
        pass

class GestionProceso(ABC):#Clase GestionProceso
    @abstractmethod#Método abrir inscripciones
    def abrir_inscripciones(self):
        pass
    @abstractmethod#Método cerrar inscripciones
    def cerrar_inscripciones(self):
        pass
    @abstractmethod#Método abrir postulaciones
    def abrir_postulaciones(self):
        pass
    @abstractmethod#Método cerrar postulaciones
    def cerrar_postulaciones(self):
        pass

class Usuario(Autenticable, ABC):#Clase abstracta Usuario
    def __init__(self, cedula_pasaporte: str, nombre: str, apellido: str, correo: str):
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    def iniciar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")
    def cerrar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")

class RepositorioAspirantes(ABC):#Interfaz Repositorio
    @abstractmethod#Método leer datos
    def leer_todos(self):
        pass
    @abstractmethod#Método guardar datos
    def guardar_todos(self, datos):
        pass

class RepositorioAspirantesJSON(RepositorioAspirantes):#Repositorio JSON
    def __init__(self, archivo="aspirantes.json"):#Modificar el nombre de la base de datos en futuro
        self.archivo = archivo
        if not os.path.exists(self.archivo):#Crear archivo si no existe
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
    def leer_todos(self):#Leer base de datos
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    def guardar_todos(self, datos):#Guardar base de datos
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

class ServicioAutenticacion:#Clase ServicioAutenticacion
    def __init__(self, repositorio: RepositorioAspirantes):
        self.repositorio = repositorio
    def crear_usuario(self, cedula, usuario: str, contrasena: str):#Método crear usuario
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["cedula_pasaporte"] == cedula:
                if "usuario" in a:
                    raise ValueError("El usuario ya existe")
                if usuario != cedula:# Validar que el usuario sea igual a la cédula o pasaporte
                    raise ValueError("El usuario debe ser igual a la cédula o pasaporte")
                a["usuario"] = usuario
                a["contrasena"] = contrasena
                self.repositorio.guardar_todos(aspirantes)
                print("Usuario creado correctamente")
                return
        raise ValueError("No existe aspirante con esa cédula")
    def iniciar_sesion(self, usuario: str, contrasena: str):#Método iniciar sesión
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar usuario y contraseña
            if a.get("usuario") == usuario and a.get("contrasena") == contrasena:
                print("Inicio de sesión exitoso")
                return True
        print("Credenciales incorrectas")
        return False

class ServicioRecuperacion:#Servicio recuperación contraseña
    def __init__(self, repositorio: RepositorioAspirantes):
        self.repositorio = repositorio
    def cambiar_contrasena_por_correo(self, correo, nueva_contrasena):#Método cambiar contraseña
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:
            if a["correo"] == correo:
                a["contrasena"] = nueva_contrasena
                self.repositorio.guardar_todos(aspirantes)
                print("Contraseña actualizada correctamente")
                return
        raise ValueError("Correo no registrado")
    
class SistemaFacade:#Clase Fachada del sistema
    def __init__(self):
        self.repo = RepositorioAspirantesJSON()
        self.auth = ServicioAutenticacion(self.repo)
        self.recuperacion = ServicioRecuperacion(self.repo)
    def registrar_usuario(self, cedula, usuario, contrasena):#Registrar usuario
        self.auth.crear_usuario(cedula, usuario, contrasena)
    def login(self, usuario, contrasena):#Iniciar sesión
        return self.auth.iniciar_sesion(usuario, contrasena)
    def recuperar_contrasena(self, correo, nueva):#Recuperar contraseña
        self.recuperacion.cambiar_contrasena_por_correo(correo, nueva)

class Administrador(Usuario, AsignarSede, Cargable, GestionProceso):#Clase Hija Administrador de Usuario
    def __init__(self, cedula, nombre, apellido, correo, cargo):
        super().__init__(cedula, nombre, apellido, correo)
        self.cargo = cargo
    def iniciar_sesion(self):
        print(f"Bienvenido Administrador {self.nombre}")
    def cerrar_sesion(self):
        print(f"Hasta luego Administrador {self.nombre}")
    def asignar_sede(self, sede):
        print(f"Administrador {self.nombre} ha asignado la sede: {sede}")
    def cargar_datos(self):
        print("El administrador está cargando datos...")
    def abrir_inscripciones(self):
        print("El administrador ha abierto las inscripciones.")
    def cerrar_inscripciones(self):
        print("El administrador ha cerrado las inscripciones.")
    def abrir_postulaciones(self):
        print("El administrador ha abierto las postulaciones.")
    def cerrar_postulaciones(self):
        print("El administrador ha cerrado las postulaciones.")
    def gestionar_soporte(self, solicitud):#Gestionar soporte
        print(f"Administrador {self.nombre} está gestionando la solicitud: {solicitud}")

class Aspirante(Usuario, Cargable, SolicitudAsistencia, GestorSede):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono, titulo, nota_grado):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
        self.titulo = titulo
        self._nota_grado = None
        self.nota_grado = nota_grado
    @property#Propiedad nota grado
    def nota_grado(self):
        return self._nota_grado
    @nota_grado.setter#Setter nota grado con validación
    def nota_grado(self, valor):
        if not (0 <= valor <= 10):
            raise ValueError("La nota debe estar entre 0 y 10.")
        self._nota_grado = valor
    def iniciar_sesion(self):
        print(f"Aspirante {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Aspirante {self.nombre} cerró sesión.")
    def cargar_datos(self):
        print("El aspirante ha cargado sus datos.")
    def crear_solicitud_asistencia(self, asunto):
        print(f"Aspirante {self.nombre} creó una solicitud sobre: {asunto}")
    def estado_solicitud(self, estado):
        print(f"Estado de solicitud: {estado}")
    def notificar_sede(self, sede):
        print(f"Aspirante {self.nombre} ha notificado la sede: {sede}")
    def imprimir_documentacion_sede(self, sede):
        print(f"Aspirante {self.nombre} imprime documentación para la sede: {sede}")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def iniciar_sesion(self):
        print(f"Soporte {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Soporte {self.nombre} cerró sesión.")
    def recibir_asistencia(self, aspirante):
        print(f"Soporte atendiendo a {aspirante.nombre}")
    def derivar_asistencia(self, administrador):#Derivar asistencia
        print(f"Soporte deriva la asistencia al Administrador {administrador.nombre}")

class Profesor(Usuario):#Clase Hija Profesor de Usuario
    def __init__(self, cedula, nombre, apellido, correo, facultad):
        super().__init__(cedula, nombre, apellido, correo)
        self.facultad = facultad
    def iniciar_sesion(self):
        print(f"Profesor {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Profesor {self.nombre} cerró sesión.")
    def crear_cuestionario(self, tema, cantidad):
        print(f"Profesor {self.nombre} creó un cuestionario de '{tema}' con {cantidad} preguntas.")

class ManejadorAsistencia(ABC):#Clase abstracta ManejadorAsistencia
    def __init__(self, siguiente=None):
        self.siguiente = siguiente
    @abstractmethod#Método manejar solicitud
    def manejar(self, solicitud):
        pass

class SoporteHandler(ManejadorAsistencia):#Clase SoporteHandler
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud == "tecnico":#Si es técnico
            print("Soporte resolvió el problema técnico")
        elif self.siguiente:#Si hay siguiente en la cadena
            print("Soporte escala al Administrador")
            self.siguiente.manejar(solicitud)

class AdministradorHandler(ManejadorAsistencia):#Clase AdministradorHandler
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud in ["academico", "grave"]:#Si es académico o grave
            print("Administrador resolvió el problema")
        else:#Solicitud no válida
            print("Solicitud no válida")
