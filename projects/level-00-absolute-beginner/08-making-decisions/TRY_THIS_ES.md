# Prueba Esto — Ejercicio 08

1. Crea un verificador de edad que use `input()`:
   ```python
   age = int(input("Ingresa tu edad: "))
   if age >= 18:
       print("Eres mayor de edad.")
   else:
       print("Eres menor de edad.")
   ```

2. Crea un juego de adivinar números:
   ```python
   secret = 7
   guess = int(input("Adivina un número del 1 al 10: "))
   if guess == secret:
       print("¡Correcto!")
   elif guess < secret:
       print("¡Muy bajo!")
   else:
       print("¡Muy alto!")
   ```

3. Cambia los valores de `temperature` y `score` en el archivo del ejercicio. Ejecútalo de nuevo. Predice cuál será la salida ANTES de ejecutarlo. ¿Acertaste?

---

| [← Anterior](../07-user-input/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../09-lists/TRY_THIS_ES.md) |
|:---|:---:|---:|
