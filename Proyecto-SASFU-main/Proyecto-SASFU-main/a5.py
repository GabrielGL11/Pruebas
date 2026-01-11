import random
from consultas import (
    aspirantes,
    buscar_por_cedula,
    top_puntajes,
    aspirantes_con_vulnerabilidad
)

def mostrar_aspirante(a):
    print("\n----------------------------")
    print(f"Cédula: {a['cedula']}")
    print(f"Nombre: {a['nombre']}")
    print(f"Edad: {a['edad']}")
    print(f"Puntaje: {a['puntaje_mayor_eval_4_ult_periodos']}")
    print(f"Vulnerabilidad: {a['vulnerabilidad_socioeconomica']}")
    print(f"Mérito académico: {a['merito_academico']}")
    print("----------------------------")

def mostrar_aleatorio():
    aspirante = random.choice(aspirantes)
    mostrar_aspirante(aspirante)

def buscar_manual():
    cedula = input("Ingrese la cédula: ")
    aspirante = buscar_por_cedula(cedula)
    if aspirante:
        mostrar_aspirante(aspirante)
    else:
        print("❌ Aspirante no encontrado")

def menu():
    while True:
        print("\n===== SISTEMA DE ASPIRANTES =====")
        print("1. Mostrar aspirante al azar")
        print("2. Buscar aspirante por cédula")
        print("3. Mostrar top 5 puntajes")
        print("4. Mostrar aspirantes vulnerables")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_aleatorio()
        elif opcion == "2":
            buscar_manual()
        elif opcion == "3":
            for a in top_puntajes(5):
                mostrar_aspirante(a)
        elif opcion == "4":
            for a in aspirantes_con_vulnerabilidad()[:5]:
                mostrar_aspirante(a)
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
