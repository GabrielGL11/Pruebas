import json

#cargamos datos de aspirantes desde el archivo JSON
def cargar_aspirantes():
    with open("aspirantes_universidad.json", "r", encoding="utf-8") as f:
        return json.load(f)

aspirantes = cargar_aspirantes()

#consultar datos

def buscar_por_cedula(cedula):
    for a in aspirantes:
        if a["cedula"] == cedula:
            return a
    return None

def aspirantes_con_vulnerabilidad():
    return [a for a in aspirantes if a["vulnerabilidad_socioeconomica"]]

def aspirantes_con_merito():
    return [a for a in aspirantes if a["merito_academico"]]

def aspirantes_rurales():
    return [a for a in aspirantes if a["ruralidad"]]

def aspirantes_con_discapacidad():
    return [a for a in aspirantes if a["discapacidad"]]

def aspirantes_cupo_activo():
    return [a for a in aspirantes if a["cupo_historico_activo"]]

def top_puntajes(n=10):
    return sorted(
        aspirantes,
        key=lambda a: a["puntaje_mayor_eval_4_ult_periodos"],
        reverse=True
    )[:n]

#muestra de datos
if __name__ == "__main__":
    print("Total aspirantes:", len(aspirantes))
    print("Vulnerables:", len(aspirantes_con_vulnerabilidad()))
    print("Rurales:", len(aspirantes_rurales()))
    print("Top 5 puntajes:")
    for a in top_puntajes(5):
        print(a["nombre"], a["puntaje_mayor_eval_4_ult_periodos"])
