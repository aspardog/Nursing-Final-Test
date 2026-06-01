---
title: Quiz Enfermeria
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Quiz interactivo de examen final de enfermería.
---

# Nursing Final Test

Simulador de examen final para estudiantes de enfermeria. El proyecto combina tarjetas tipo Anki, una API FastAPI, una base SQLite local y un frontend vanilla para practicar semiologia psiquiatrica con preguntas de opcion multiple y preguntas abiertas.

## Funcionalidades

- Quizzes configurables de 10, 20, 30 o 50 preguntas.
- Modos de practica: mixto, solo opcion multiple o solo preguntas abiertas.
- Proporcion MCQ ajustable en modo mixto.
- Timer opcional por pregunta: sin timer, 30s, 60s o 90s.
- Filtro por subtemas disponibles en la base.
- Feedback inmediato con respuesta correcta y, cuando existe, explicacion educativa.
- Autoevaluacion para preguntas abiertas: sabia, medias o no sabia.
- Historial de sesiones y resumen por formato/subtema.
- Lista final de tarjetas falladas para repasar.

## Stack

- Backend: Python 3.11, FastAPI, Uvicorn, Pydantic.
- Paquetes: uv con `pyproject.toml` y `uv.lock`.
- Persistencia: SQLite.
- Frontend: HTML, CSS y JavaScript sin framework.
- Deploy: Hugging Face Spaces con Docker.

## Estructura

```text
Nursing-Final-Test/
├── cards/
│   └── cards_semiologia.csv       # Tarjetas Anki fuente
├── quiz_app/
│   ├── app.py                     # API FastAPI y rutas
│   ├── database.py                # Conexion, esquema y migraciones SQLite
│   ├── load_cards.py              # Carga de tarjetas CSV a la base
│   ├── quiz_engine.py             # Muestreo, sesiones, respuestas y resumen
│   ├── distractor_generator.py    # Utilidades para distractoras MCQ
│   ├── generate_explanations.py   # Carga explicaciones educativas por tarjeta
│   ├── static/
│   │   ├── index.html
│   │   ├── app.js
│   │   └── style.css
├── Dockerfile
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

La base `quiz_app/data/quiz.db` es local y regenerable. El dato fuente que se sube al deploy vive en `cards/cards_semiologia.csv`.

## Instalacion Local

Requiere `uv` instalado.

```bash
uv sync --frozen
uv run --directory quiz_app python load_cards.py
uv run --directory quiz_app python generate_explanations.py
uv run --directory quiz_app python -m uvicorn app:app --reload --port 8000
```

Abre `http://127.0.0.1:8000`.

Si no necesitas explicaciones educativas, puedes omitir `uv run --directory quiz_app python generate_explanations.py`; la app seguira mostrando preguntas y respuestas.

Nota: el proyecto declara `requires-python = ">=3.11,<3.14"`. Usa Python 3.11, 3.12 o 3.13.

## API

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| `GET` | `/` | Sirve el frontend |
| `GET` | `/api/temas` | Lista temas/subtemas disponibles |
| `POST` | `/api/quiz/start` | Crea una sesion y devuelve preguntas |
| `POST` | `/api/quiz/answer` | Registra una respuesta |
| `POST` | `/api/quiz/end` | Cierra la sesion y devuelve resumen |
| `GET` | `/api/quiz/{session_id}/summary` | Consulta el resumen de una sesion |
| `GET` | `/api/history?limit=20` | Lista sesiones recientes |

Ejemplo para iniciar un quiz:

```bash
curl -X POST http://127.0.0.1:8000/api/quiz/start \
  -H "Content-Type: application/json" \
  -d '{"n_questions":10,"modo":"mixto","ratio_mcq":0.7}'
```

## Flujo de Datos

1. Las tarjetas fuente viven en `cards/cards_semiologia.csv` con formato Anki separado por `|`.
2. `quiz_app/load_cards.py` crea `quiz_app/data/quiz.db` y carga tarjetas, temas, subtemas y elegibilidad MCQ.
3. `quiz_app/generate_explanations.py` agrega explicaciones educativas a la tabla `cards`.
4. `quiz_app/quiz_engine.py` toma muestras aleatorias, arma MCQ con distractoras y registra respuestas.
5. El frontend consume la API y muestra configuracion, preguntas, feedback, resumen e historial.

## Agregar Tarjetas

Agrega archivos `.csv` en `cards/` con este formato:

```text
#separator:pipe
#html:true
#columns:Front|Back|Tags
#tags column:3
Pregunta|Respuesta con <b>HTML</b>|examen_final::tema::subtema
```

Luego ejecuta:

```bash
uv run --directory quiz_app python load_cards.py
```

Las tarjetas se cargan de forma idempotente por texto de pregunta (`frente`).

## Deploy

### Hugging Face Spaces

Este repo esta configurado para desplegarse como **Docker Space**. La configuracion que Hugging Face lee esta en el bloque YAML superior de este `README.md`:

```yaml
sdk: docker
app_port: 7860
```

Pasos:

1. Crea un Space nuevo en Hugging Face con SDK **Docker**.
2. Sube este repo al Space o conectalo como repositorio Git remoto.
3. Hugging Face construira el `Dockerfile`, cargara las tarjetas en SQLite durante el build y levantara FastAPI en el puerto `7860`.

Comandos utiles si quieres subirlo por Git:

```bash
git remote add space https://huggingface.co/spaces/TU_USUARIO/quiz-enfermeria
git push space main
```

La base `quiz_app/data/quiz.db` se genera dentro del contenedor a partir de `cards/cards_semiologia.csv`; no hace falta subirla. El historial de sesiones vive en SQLite dentro del contenedor, asi que puede reiniciarse cuando Hugging Face reconstruya o reinicie el Space.

### Docker

```bash
docker build -t nursing-final-test .
docker run -p 7860:7860 nursing-final-test
```

## Notas de Desarrollo

- La base SQLite es local y regenerable.
- `database.py` crea el esquema y migra la columna `explicacion` si falta.
- Las distractoras se leen desde la tabla `distractors`; las tarjetas sin distractoras pueden usarse como preguntas abiertas.
- El frontend no requiere build step.

## Licencia

Uso educativo personal.
