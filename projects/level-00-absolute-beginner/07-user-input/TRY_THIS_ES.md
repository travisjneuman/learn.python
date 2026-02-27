# Prueba Esto — Ejercicio 07

1. Crea un programa de saludo simple que pida el nombre y el apellido por separado, y luego imprima el nombre completo:
   ```python
   first = input("¿Tu nombre? ")
   last = input("¿Tu apellido? ")
   print(f"¡Hola, {first} {last}!")
   ```

2. Crea una calculadora de propinas: pide el precio de la comida y el porcentaje de propina, calcula la propina y el total:
   ```python
   price = float(input("Precio de la comida: $"))
   tip_pct = float(input("Porcentaje de propina (como 20): "))
   tip = price * (tip_pct / 100)
   print(f"Propina: ${round(tip, 2)}")
   print(f"Total: ${round(price + tip, 2)}")
   ```
   Nota: `float()` convierte a un número decimal (en vez de `int()` que solo acepta números enteros).

3. ¿Qué pasa si escribes una palabra cuando el programa espera un número? Inténtalo y lee el error.

---

| [← Anterior](../06-strings-and-text/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../08-making-decisions/TRY_THIS_ES.md) |
|:---|:---:|---:|
