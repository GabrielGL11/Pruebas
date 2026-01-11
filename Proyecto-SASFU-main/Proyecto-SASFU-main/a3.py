#Clases: Universidad, Oferta_Academica, Periodo
from abc import ABC #Importar ABCMeta
from abc import abstractmethod #Importar abstractmethod
import json #Importar json

class Iniciar_fase(ABC):#Interfaz Iniciar_fase/Patrón de diseño Strategy
    @abstractmethod
    def iniciar(self):
        pass

class Finalizar_fase(ABC):#Interfaz Finalizar_fase/Patrón de diseño Strategy 
    @abstractmethod
    def finalizar(self):
        pass

class Universidad:
    PAIS = "Ecuador"
    def __init__(self, nombre:str, provincia:str, canton:str, direccion:str, enlace:str,universidad:str,tipo:str):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace
        self.universidad = universidad.upper()
        self.tipo = tipo.upper()
        
    @property
    def universidad(self):#Getter universidad
        return self._universidad
        
    @universidad.setter
    def universidad(self, valor:str):#Setter universidad con validación
        valor=valor.upper()
        valores_permitidos = ["PUBLICA", "PRIVADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._universidad = valor
        
    @property
    def tipo(self):#Getter tipo
        return self._tipo
        
    @tipo.setter
    def tipo(self, valor:str):#Setter tipo con validación
        valor=valor.upper()
        valores_permitidos = ["NORMAL", "TECNICA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._tipo = valor
        
class Modalidad(ABC): #Principio SOLID/OCP 
    @abstractmethod
    def validar(self):
        pass

class Presencial(Modalidad):
    def validar(self):
        return "Modalidad Presencial válida"
        
class Virtual(Modalidad):
    def validar(self):
        return "Modalidad Virtual válida"

class Hibrida(Modalidad):
    def validar(self):
        return "Modalidad Híbrida válida"

class Oferta_Academica:
    def __init__(self, universidad:str, carrera:str, cantidad:int, codigo:int, modalidad:Modalidad):
        self.universidad = universidad
        self.carrera = carrera
        self.cantidad = cantidad 
        self.codigo = codigo
        self.modalidad = modalidad 
        self.postulantes = []
     
    @property
    def cantidad(self):#Getter cantidad
        return self._cantidad
        
    @cantidad.setter
    def cantidad(self, valor:int):#Setter cantidad con validación
        if valor < 0:
            raise ValueError("La cantidad de cupos no puede ser negativa.")
        self._cantidad = valor  
   
    def esta_disponible(self): #Método esta_disponible
        return len(self.postulantes) < self.cantidad

    @property
    def codigo(self): #Getter codigo
        return self._codigo
        
    @codigo.setter
    def codigo(self, valor:int): #Setter código con validación
        if valor <= 0:
            raise ValueError("El código debe ser positivo")
        self._codigo = valor

    def verificar_cupos(self): #Método verificar_cupos
        disponibles = self.cantidad - len(self.postulantes)
        print(f"Cupos restantes para {self.carrera}: {disponibles}.")

    def exportar(self): #Método exportar
        return{
            "Universidad": self.universidad,
            "Carrera": self.carrera,
            "Codigo": self.codigo,
            "Modalidad": self.modalidad.__class__.__name__,
            "Cupos": self.cantidad,
            "Postulantes": len(self.postulantes)
        }
        
class OfertaFactory: #Patrón de diseño Factory Method 
    @staticmethod
    def crear_desde_json(data): #Método crear_desde_json
        modalidades = {
            "Presencial": Presencial(),
            "Virtual": Virtual(),
            "Hibrida": Hibrida()
        }

        return Oferta_Academica(
            universidad=data["Universidad"],
            carrera=data["Carrera"],
            cantidad=data["Cupos"],
            codigo=data["Codigo"],
            modalidad=modalidades[data["Modalidad"]]
        )
        
class OfertaRepositorio: #Repositorio json
    def __init__(self, archivo="ofertas.json"):
        self.archivo = archivo
    
    def guardar(self, ofertas: list[Oferta_Academica]): #Método guardar
        data = [o.exportar() for o in ofertas]
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    def cargar(self) -> list[Oferta_Academica]: #Método cargar
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [OfertaFactory.crear_desde_json(d) for d in data]
        except FileNotFoundError:
            return []

class ControladorOfertas: #Patrón de diseño Controller
    def __init__(self, repo: OfertaRepositorio):  
        self.repo = repo
        self.ofertas = []

    def cargar(self): #Método cargar
        self.ofertas = self.repo.cargar()  
        return self.ofertas

    def guardar(self): #Método guardar
        self.repo.guardar(self.ofertas)  

    def agregar_oferta(self, oferta: Oferta_Academica): #Método agregar_oferta
        self.ofertas.append(oferta)
        self.guardar()
        
    def buscar_por_carrera(self, carrera:str): #Método buscar_por_carrera
        return [o for o in self.ofertas if o.carrera == carrera]
    
    def listar(self): #Método listar
        return self.ofertas
    
class Periodo(Iniciar_fase,Finalizar_fase):#Clase Periodo que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, ano_lectivo:str, semestre:str):
        self.ano_lectivo = ano_lectivo
        self.semestre = semestre
        self._activo = False
  
    def iniciar(self):#Método iniciar el peridodo
        self._activo = True
        print(f"El periodo {self.ano_lectivo} - {self.semestre} ha iniciado.")
    
    def finalizar(self):#Metodo finalizar el periodo
        self._activo = False
        print(f"El periodo {self.ano_lectivo} - {self.semestre} ha finalizado.")
    
    def esta_activo(self): #Método esta_activo
        return self._activo
