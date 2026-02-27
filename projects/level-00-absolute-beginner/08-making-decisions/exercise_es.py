"""Aprende a controlar el flujo del programa usando sentencias condicionales if, elif y else."""
# ============================================================
# Ejercicio 08: Tomando Decisiones (if / else)
# ============================================================
#
# Los programas necesitan tomar decisiones. "Si esto es verdad,
# haz eso. Si no, haz otra cosa."
#
# Python usa if, elif (else if), y else para esto.
#
# LA INDENTACIÓN IMPORTA. Las líneas indentadas después de
# if/elif/else son el código que se ejecuta cuando esa
# condición es verdadera. Usa 4 espacios para cada nivel
# de indentación.
# ============================================================

# if/else simple
temperature = 75

if temperature > 80:
    print("Hace calor afuera.")
else:
    print("No hace tanto calor.")

# if / elif / else — múltiples condiciones
score = 85

if score >= 90:
    print("Calificación: A")
elif score >= 80:
    print("Calificación: B")
elif score >= 70:
    print("Calificación: C")
elif score >= 60:
    print("Calificación: D")
else:
    print("Calificación: F")

# Operadores de comparación:
#   ==   igual a (¡DOS signos de igual, no uno!)
#   !=   diferente de
#   >    mayor que
#   <    menor que
#   >=   mayor o igual que
#   <=   menor o igual que

# Verificar igualdad
password = "secret123"

if password == "secret123":
    print("Acceso concedido.")
else:
    print("Acceso denegado.")

# Combinar condiciones con "and" / "or"
age = 25
has_license = True

if age >= 16 and has_license:
    print("Puedes conducir.")
else:
    print("No puedes conducir.")

# "not" invierte una condición
is_raining = False

if not is_raining:
    print("No necesitas paraguas.")

# ============================================================
# ERROR COMÚN:
#
# Usar = (asignación) en vez de == (comparación):
#   if x = 5:    # MAL — esto guarda 5 en x
#   if x == 5:   # BIEN — esto verifica si x es igual a 5
# ============================================================
