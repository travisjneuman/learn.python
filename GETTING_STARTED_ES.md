# Como Usar Este Curriculum

> **Orientacion del curriculum.** Como funcionan los niveles, modos de estudio y estimaciones de tiempo.
> Si todavia no instalaste Python, empieza con [START_HERE.md](./START_HERE.md) primero.

Esta guia te explica como esta organizado el curriculum, en que orden seguirlo y como manejar tu ritmo de estudio.

---

## Orden de Lectura

Empieza con estos cuatro documentos, en este orden:

1. **[START_HERE.md](./START_HERE.md)** -- Instala Python y ejecuta tu primer script en menos de 10 minutos.
2. **[00_COMPUTER_LITERACY_PRIMER.md](./00_COMPUTER_LITERACY_PRIMER.md)** -- Que es una terminal, un archivo y un programa. Saltate esto si ya lo sabes.
3. **[01_ROADMAP.md](./01_ROADMAP.md)** -- La vista general completa del programa: cada nivel, cada hito.
4. **[03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md)** -- Instrucciones detalladas de instalacion para Windows, Mac y Linux.

Despues de eso, sigue el enlace "Next" al final de cada documento. Todo el curriculum es una cadena de un solo clic -- nunca tienes que adivinar que viene despues.

## Documentos Solo de Referencia

Estos documentos no estan pensados para leerse de principio a fin. Usalos cuando necesites buscar algo:

- **[02_GLOSSARY.md](./02_GLOSSARY.md)** -- Definiciones de terminos clave. Vuelve aqui cuando encuentres palabras desconocidas.
- **[13_SAMPLE_DATABASE_SCHEMAS.md](./13_SAMPLE_DATABASE_SCHEMAS.md)** -- Esquemas de base de datos de ejemplo usados en proyectos relacionados con SQL. Relevante a partir del Nivel 6.
- **[concepts/](./concepts/)** -- Guias de conceptos sobre variables, loops, funciones, etc. Leelas cuando un proyecto las referencie o cuando necesites repasar.

---

## Estimaciones de Tiempo

Cuanto tiempo toma cada seccion depende de tu ritmo y experiencia previa. Estas son estimaciones aproximadas para alguien que trabaja el material con cuidado, incluyendo los ejercicios de "Modificalo / Rompelo / Arreglalo".

| Seccion | Horas Estimadas |
|---------|----------------|
| Level 00 (Principiante Absoluto) | ~5 horas |
| Level 0 (Terminal, Archivos, I/O Basico) | ~15 horas |
| Level 1 (Input, CSV, JSON, Rutas) | ~20 horas |
| Level 2 (Estructuras de Datos, Limpieza) | ~20 horas |
| Level 3 (Paquetes, Logging, TDD) | ~25 horas |
| Level 4 (Validacion de Schemas, Pipelines) | ~25 horas |
| Level 5 (Scheduling, Monitoreo) | ~25 horas |
| Level 6 (SQL, ETL, Idempotencia) | ~30 horas |
| Level 7 (APIs, Caching, Observabilidad) | ~30 horas |
| Level 8 (Dashboards, Concurrencia) | ~30 horas |
| Level 9 (Arquitectura, SLOs, Seguridad) | ~35 horas |
| Level 10 (Empresarial, Produccion) | ~35 horas |
| Elite Track (Algoritmos, Sistemas Distribuidos) | ~40 horas |
| Cada Modulo de Expansion (12 disponibles) | ~10-20 horas |
| **Total** | **~400-500 horas** |

---

## Sugerencias de Ritmo Semanal

| Horas por Semana | Duracion Aproximada |
|----------------|---------------------|
| 5 horas/semana | ~2 anos |
| 10 horas/semana | ~1 ano |
| 20 horas/semana | ~6 meses |
| Tiempo completo (40 horas/semana) | ~3 meses |

No hay prisa. La practica constante importa mas que la velocidad. Es mejor dedicar 5 horas por semana durante dos anos que estudiar intensivamente un mes y quemarte.

---

## Cuando Te Atoras

Atorarte no es fracasar -- es aprender. Todo programador profesional se atora a diario. La diferencia entre un principiante y un experto no es que los expertos nunca se atoran. Es que los expertos se han atorado miles de veces y construyeron un kit de herramientas para salir adelante.

Cuando te topas con un muro, esa sensacion incomoda es tu cerebro formando nuevas conexiones. La investigacion sobre aprendizaje muestra consistentemente que luchar con un problema -- incluso sin exito -- produce una comprension mas profunda que recibir la respuesta servida. Si todo se siente facil, no estas aprendiendo nada nuevo.

Asi que cuando te sientas atorado, frustrado, o como que "esto no es para ti," reconoce esa sensacion como evidencia de crecimiento. Respira hondo e intenta el proceso de abajo.

Para mas informacion sobre como aprender de manera efectiva, consulta [LEARNING_HOW_TO_LEARN.md](./LEARNING_HOW_TO_LEARN.md).

### Un proceso que funciona

1. **Lee el mensaje de error.** Los mensajes de error de Python te dicen exactamente que salio mal y en que linea. Leelo de abajo hacia arriba.
2. **Vuelve a leer el documento del concepto.** Cada proyecto enlaza a guias de conceptos relacionados. Regresa y relee la seccion relevante.
3. **Agrega sentencias `print()`.** Imprime el valor de las variables antes de la linea que falla. Ve como se ven los datos realmente.
4. **Toma un descanso.** Si llevas 20 minutos atorado, alejate 10 minutos. La respuesta a menudo llega cuando dejas de mirar la pantalla.
5. **Revisa las [Preguntas Frecuentes](./FAQ.md).** Problemas comunes y sus soluciones estan recopilados ahi.
6. **Busca el mensaje de error.** Copia la ultima linea del traceback y buscala en internet. Alguien ya se topo con el mismo error antes.
7. **Abre un issue.** Si crees que el curriculum tiene un bug (test roto, archivo faltante, instrucciones confusas), [abre un issue](https://github.com/travisjneuman/learn.python/issues) en GitHub.

---

## Como Rastrear Tu Progreso

Ejecuta el rastreador de progreso desde la raiz del repositorio:

```bash
python tools/progress.py
```

Tambien puedes actualizar manualmente [PROGRESS.md](./PROGRESS.md) conforme completes proyectos.

---

## Eligiendo un Modo de Aprendizaje

El curriculum soporta tres modos. Escoge el que se ajuste a como aprendes:

- **Play-First** -- Abre un proyecto, experimenta, rompe cosas, descubrelo por tu cuenta. Lee el documento del concepto cuando te atores.
- **Estructurado** -- Lee el documento del concepto, toma el quiz, luego haz los proyectos en orden. Usa checklists y puertas de dominio.
- **Hibrido (Recomendado)** -- Sigue el camino estructurado entre semana. Explora modulos de expansion y challenges los fines de semana. Repasa flashcards a diario.

---

---

## Herramientas de Practica

El curriculum incluye varias herramientas para reforzar tu aprendizaje mas alla de los proyectos principales:

- **Quizzes** — Pon a prueba tu comprension de cada concepto: [`concepts/quizzes/`](./concepts/quizzes/)
- **Flashcards** — Mazos de repaso rapido para terminos y patrones clave: [`practice/flashcards/`](./practice/flashcards/)
- **Challenges** — Problemas independientes ordenados por dificultad: [`practice/challenges/`](./practice/challenges/)
- **Ejercicios en el Navegador** — Ejecuta Python en tu navegador sin instalar nada: [`browser/`](./browser/index.html)
- **Repeticion Espaciada** — Algoritmo SM-2 para programar tus repasos: [`tools/spaced_repetition.py`](./tools/spaced_repetition.py)

---

| [← Anterior](README.md) | [Inicio](README.md) | [Siguiente →](START_HERE.md) |
|:---|:---:|---:|
