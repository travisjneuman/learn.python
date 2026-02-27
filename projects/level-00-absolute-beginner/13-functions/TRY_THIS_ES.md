# Prueba Esto — Ejercicio 13

1. Escribe una función que tome una temperatura en Fahrenheit y devuelva Celsius:
   ```python
   def to_celsius(fahrenheit):
       return (fahrenheit - 32) * 5 / 9

   print(to_celsius(212))  # 100.0
   print(to_celsius(32))   # 0.0
   print(to_celsius(72))   # 22.2...
   ```

2. Escribe una función que tome una lista de números y devuelva el promedio:
   ```python
   def average(numbers):
       return sum(numbers) / len(numbers)

   print(average([90, 85, 92, 78]))
   ```

3. Escribe una función llamada `is_even` que tome un número y devuelva `True` si es par, `False` si es impar:
   ```python
   def is_even(number):
       return number % 2 == 0

   print(is_even(4))   # True
   print(is_even(7))   # False
   ```

---

| [← Anterior](../12-dictionaries/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../14-reading-files/TRY_THIS_ES.md) |
|:---|:---:|---:|
