#inyeccion en proceso
#Clase_base
from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod
class tipo_de_examen(ABC):
    @abstractmethod
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

#Tipos de examen
class mixto(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        # ponderación 50% general + 50% area
        return int((respuestas_correctas / total_preguntas) * 1000)

    def descripcion(self):
        return "Examen mixto (conocimiento general y area conocimiento)"

class por_area(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int ((respuestas_correctas / total_preguntas) * 1000)

    def descripcion(self):
        return "Examen por área de conocimiento"
    
class general(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int((respuestas_correctas / total_preguntas) * 1000)
    
    def descripcion(self):
        return "Conocimiento general"

#inyección de dependencia
class Evaluacion:
    def __init__(self, tipo_examen: tipo_de_examen, horario: str, modalidad: str, sede: str):
        self.tipo_examen = tipo_examen  #dependencia
        self.horario = horario
        self.modalidad = modalidad
        self.sede = sede
        self._puntaje = 0

    def aplicar_examen(self, respuestas_correctas: int, total_preguntas: int):
        self._puntaje = self.tipo_examen.calcular_resultado(respuestas_correctas, total_preguntas)

    def mostrar_resultado(self):
        return (f"{self.tipo_examen.descripcion()} — "
                f"Puntaje obtenido: {self._puntaje}/1000 — "
                f"Modalidad: {self.modalidad}, Sede: {self.sede}")
