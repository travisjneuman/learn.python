"""Aprende a realizar operaciones aritméticas y entender la división entera vs. decimal."""
# ============================================================
# Ejercicio 05: Números y Matemáticas
# ============================================================
#
# Python tiene dos tipos de números:
#   - int (entero): números sin decimales como 5, -3, 1000
#   - float (punto flotante): números con decimales como 3.14, -0.5
#
# Python puede hacer todas las operaciones matemáticas básicas.
# ============================================================

# Suma
print("5 + 3 =", 5 + 3)

# Resta
print("10 - 4 =", 10 - 4)

# Multiplicación (usa * no x)
print("6 * 7 =", 6 * 7)

# División (siempre da un resultado decimal)
print("15 / 4 =", 15 / 4)

# División entera (descarta la parte decimal)
print("15 // 4 =", 15 // 4)

# Residuo (se llama "módulo" — lo que sobra después de dividir)
print("15 % 4 =", 15 % 4)

# Exponente (potencia)
print("2 ** 8 =", 2 ** 8)

# El orden de operaciones funciona como en clase de matemáticas: paréntesis primero
print("(2 + 3) * 4 =", (2 + 3) * 4)
print("2 + 3 * 4 =", 2 + 3 * 4)

# Guarda resultados en variables
price = 29.99
tax_rate = 0.08
tax_amount = price * tax_rate
total = price + tax_amount

print()
print("Precio:", price)
print("Impuesto:", tax_amount)
print("Total:", total)

# Redondea un número a 2 decimales
print("Total (redondeado):", round(total, 2))

# ============================================================
# ERROR COMÚN:
#
# La división con / siempre da un float (decimal), incluso si
# la respuesta es un número entero:
#   10 / 2 da 5.0 (no 5)
#
# Usa // si quieres un resultado entero:
#   10 // 2 da 5
# ============================================================
