import SASFU
aspirante1 = SASFU.Aspirante("1312685560", "Juan", "Pérez", "juan@gmail.com", "099000933", True, 8.02)
soport1 = SASFU.Soporte("0923456789", "María", "Gómez", "maria@soporte.com", "098765432")
profesor1=SASFU.Profesor("1002003004","Carlos","Lopez","carlez@hotmail.com", "arquitecto")
profesor1.crear_cuestionario("Matemáticas", 10)

soport1.recibir_asistencia(aspirante1)

hora = input("hora del examen:")
modalidad = input("presencial o virtual:")
sede = input("sede:")

evaluacion1 = SASFU.Evaluacion(SASFU.mixto(), hora, modalidad, sede)
evaluacion1.aplicar_examen(respuestas_correctas=45, total_preguntas=50)
print(evaluacion1.mostrar_resultado())

postulacion1 = SASFU.Postulacion("Ingeniería en Software", 850)
postulacion1.iniciar()
postulacion1.seleccionar_carrera()
postulacion1.finalizar()
