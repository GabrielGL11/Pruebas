import json

#cargar datos
def cargar_resultados():
    with open("resultados_examenes.json", "r", encoding="utf-8") as f:
        return json.load(f)

resultados = cargar_resultados()

#consultas
def mostrar_resumen(r):
    print("-" * 50)
    print(f"Cédula : {r['cedula']}")
    print(f"Nombre : {r['nombre']}")
    print(f"Edad   : {r['edad']}")
    print(f"Examen : {r['resultado_examen']['tipo_examen']}")
    print(f"Puntaje: {r['resultado_examen']['puntaje']}/1000")
    print(f"Sede   : {r['resultado_examen']['sede']}")
    print(f"Horario: {r['resultado_examen']['horario']}")
    print(f"Modalid: {r['resultado_examen']['modalidad']}")

def mostrar_todos():
    for r in resultados:
        mostrar_resumen(r)

def buscar_por_cedula():
    cedula = input("Ingrese la cédula: ")
    for r in resultados:
        if r["cedula"] == cedula:
            mostrar_resumen(r)
            return
    print(" Aspirante no encontrado")

def top_puntajes(n=5):
    top = sorted(
        resultados,
        key=lambda x: x["resultado_examen"]["puntaje"],
        reverse=True
    )[:n]

    for r in top:
        mostrar_resumen(r)

def filtrar_por_examen():
    tipo = input("Ingrese tipo de examen (mixto / área / general): ").lower()
    for r in resultados:
        if tipo in r["resultado_examen"]["tipo_examen"].lower():
            mostrar_resumen(r)

def filtrar_por_sede():
    sede = input("Ingrese sede (Quito / Guayaquil / Cuenca): ").lower()
    for r in resultados:
        if sede == r["resultado_examen"]["sede"].lower():
            mostrar_resumen(r)


#menu
def menu():
    while True:
        print("\n===== MENÚ DE RESULTADOS SASFU =====")
        print("1. Mostrar todos los resultados")
        print("2. Buscar por cédula")
        print("3. Top 5 puntajes")
        print("4. Filtrar por tipo de examen")
        print("5. Filtrar por sede")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_todos()
        elif opcion == "2":
            buscar_por_cedula()
        elif opcion == "3":
            top_puntajes()
        elif opcion == "4":
            filtrar_por_examen()
        elif opcion == "5":
            filtrar_por_sede()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida")
            
if __name__ == "__main__":
    menu()
