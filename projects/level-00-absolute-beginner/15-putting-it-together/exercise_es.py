"""Aprende a combinar variables, funciones, archivos y ciclos en un programa completo."""
# ============================================================
# Ejercicio 15: Juntando Todo
# ============================================================
#
# Este ejercicio combina todo de los Ejercicios 01-14:
# - Variables y strings
# - Entrada del usuario
# - Condiciones (if/else)
# - Listas y diccionarios
# - Ciclos
# - Funciones
# - Lectura de archivos
#
# Es un programa pequeño pero completo: un reporte de calificaciones.
#
# EJECUTA ESTO: python exercise_es.py
# ============================================================


def load_students(filename):
    """Lee datos de estudiantes de un archivo y devuelve una lista de diccionarios."""
    students = []

    for line in open(filename):
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        name = parts[0]
        score = int(parts[1])

        # Cada estudiante es un diccionario con nombre y puntuación
        student = {"name": name, "score": score}
        students.append(student)

    return students


def get_letter_grade(score):
    """Convierte una puntuación numérica a una calificación con letra."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_average(students):
    """Calcula el promedio de puntuaciones de una lista de diccionarios de estudiantes."""
    total = 0
    for student in students:
        total = total + student["score"]
    return total / len(students)


def print_report(students):
    """Imprime un reporte de calificaciones formateado para todos los estudiantes."""
    print("=" * 40)
    print("    REPORTE DE CALIFICACIONES")
    print("=" * 40)
    print()

    for student in students:
        name = student["name"]
        score = student["score"]
        grade = get_letter_grade(score)
        print(f"  {name:<10} {score:>3}  ({grade})")

    print()
    print("-" * 40)

    average = calculate_average(students)
    print(f"  Promedio de la clase: {average:.1f}")
    print(f"  Más alta: {max(s['score'] for s in students)}")
    print(f"  Más baja:  {min(s['score'] for s in students)}")
    print(f"  Estudiantes: {len(students)}")
    print("=" * 40)


# ---- El programa principal empieza aquí ----

# Cargar datos del archivo (reutilizando datos de muestra del Ejercicio 14)
students = load_students("../14-reading-files/data/sample.txt")

# Imprimir el reporte
print_report(students)

# Preguntar al usuario si quiere buscar un estudiante específico
print()
lookup = input("Buscar un estudiante por nombre (o presiona Enter para saltar): ")

if lookup:
    found = False
    for student in students:
        if student["name"].lower() == lookup.lower():
            grade = get_letter_grade(student["score"])
            print(f"\n{student['name']} obtuvo {student['score']} ({grade})")
            found = True

    if not found:
        print(f"\nNo se encontró ningún estudiante llamado '{lookup}'.")

print("\n¡Listo!")

# ============================================================
# LO QUE ACABAS DE CONSTRUIR:
#
# Un programa que lee datos de un archivo, los procesa, formatea
# un reporte, y responde a la entrada del usuario. Esta es la base
# de toda herramienta de procesamiento de datos que construirás
# de aquí en adelante.
#
# Si entendiste este ejercicio, estás listo para el Nivel 0.
# ============================================================
