"""Aprende a abrir, leer y procesar datos de archivos de texto línea por línea."""
# ============================================================
# Ejercicio 14: Leyendo Archivos
# ============================================================
#
# Los programas necesitan leer datos de archivos — hojas de cálculo,
# registros, configuración, reportes. Leer un archivo es una de las
# cosas más comunes que vas a hacer.
#
# La función open() de Python abre un archivo.
# .read() obtiene todo el texto de una vez.
# .readlines() obtiene cada línea como un elemento separado en una lista.
#
# EJECUTA ESTO: python exercise_es.py
# (Asegúrate de estar en la carpeta 14-reading-files)
# ============================================================

# Leer el archivo completo como un string grande
contents = open("data/sample.txt").read()
print("--- Contenido crudo del archivo ---")
print(contents)

# Leer el archivo línea por línea
print("--- Línea por línea ---")
lines = open("data/sample.txt").readlines()

for line in lines:
    # .strip() elimina el carácter de nueva línea al final de cada línea
    clean_line = line.strip()
    if clean_line:  # Saltar líneas vacías
        print(clean_line)

# Procesar los datos — cada línea tiene "nombre,puntuación"
print()
print("--- Datos procesados ---")

names = []
scores = []

for line in open("data/sample.txt"):
    line = line.strip()
    if not line:
        continue  # Saltar líneas vacías

    # .split(",") divide la línea en cada coma
    parts = line.split(",")
    name = parts[0]
    score = int(parts[1])

    names.append(name)
    scores.append(score)

    print(f"  {name}: {score}")

# Calcular estadísticas de los datos del archivo
print()
print(f"Estudiantes: {len(names)}")
print(f"Puntuación más alta: {max(scores)}")
print(f"Puntuación más baja: {min(scores)}")
print(f"Promedio: {sum(scores) / len(scores)}")

# ============================================================
# LA MEJOR FORMA (la vas a aprender en el Nivel 0):
#
# Usar "with open()" es más seguro porque cierra automáticamente
# el archivo cuando terminas:
#
#   with open("data/sample.txt") as f:
#       for line in f:
#           print(line.strip())
#
# Por ahora, la forma más simple con open() funciona bien para aprender.
# ============================================================
