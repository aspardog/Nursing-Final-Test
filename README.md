---
title: Quiz Enfermeria
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
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

- Backend: Python 3.10 a 3.13, FastAPI, Uvicorn, Pydantic.
- Persistencia: SQLite.
- Frontend: HTML, CSS y JavaScript sin framework.
- Testing: pytest.
- Deploy: Docker o Render Blueprint.

## Estructura

```text
Nursing-Final-Test/
├── cards/
│   └── cards_semiologia.csv       # Tarjetas Anki fuente
├── material/                       # Material extraido de PDF/DOCX
│   ├── 01_semiologia/
│   ├── 02_salas_cirugia/
│   ├── 03_urgencias/
│   ├── 04_arritmias/
│   ├── 05_mezclas/
│   └── resumen.md
├── quiz_app/
│   ├── app.py                     # API FastAPI y rutas
│   ├── database.py                # Conexion, esquema y migraciones SQLite
│   ├── load_cards.py              # Carga de tarjetas CSV a la base
│   ├── quiz_engine.py             # Muestreo, sesiones, respuestas y resumen
│   ├── distractor_generator.py    # Utilidades para distractoras MCQ
│   ├── generate_explanations.py   # Carga explicaciones educativas por tarjeta
│   ├── requirements.txt
│   ├── static/
│   │   ├── index.html
│   │   ├── app.js
│   │   └── style.css
│   └── tests/
│       └── test_engine.py
├── extract.py                     # Extraccion mecanica de material fuente
├── Dockerfile
├── render.yaml
└── README.md
```

La base `quiz_app/data/quiz.db`, los uploads originales, entornos virtuales y caches Python estan ignorados por Git.

## Instalacion Local

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r quiz_app/requirements.txt
cd quiz_app
python load_cards.py
python generate_explanations.py
python -m uvicorn app:app --reload --port 8000
```

Abre `http://127.0.0.1:8000`.

Si no necesitas explicaciones educativas, puedes omitir `python generate_explanations.py`; la app seguira mostrando preguntas y respuestas.

Nota: las dependencias fijadas actualmente no instalan bien en Python 3.14. Usa Python 3.11 o 3.12 para desarrollo local.

## Pruebas

Desde la raiz del proyecto:

```bash
pytest quiz_app/tests
```

Los tests usan la base SQLite local. Si es una instalacion nueva, ejecuta primero:

```bash
cd quiz_app
python load_cards.py
python generate_explanations.py
```

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
cd quiz_app
python load_cards.py
```

Las tarjetas se cargan de forma idempotente por texto de pregunta (`frente`).

## Material Fuente

`extract.py` procesa archivos ubicados en `uploads/` y genera texto/JPG en `material/`. El resumen actual indica:

- Semiologia psiquiatrica: 34 paginas, texto extraido.
- Salas de cirugia: 17 paginas, texto y JPG.
- Urgencias: 25 paginas, texto y JPG.
- Arritmias: 11 paginas en JPG.
- Mezclas y diluciones: ejercicios extraidos desde DOCX.

`uploads/` esta ignorado para no publicar archivos temporales u originales pesados.

## Deploy

### Docker

```bash
docker build -t nursing-final-test .
docker run -p 8000:8000 nursing-final-test
```

### Render

El archivo `render.yaml` define un Web Service Python. Tambien puedes configurar Render manualmente:

- Build Command: `pip install -r quiz_app/requirements.txt && cd quiz_app && python load_cards.py && python generate_explanations.py`
- Start Command: `cd quiz_app && python -m uvicorn app:app --host 0.0.0.0 --port $PORT`
- Python: 3.11

El build command carga tarjetas y explicaciones en una base nueva antes de iniciar el servicio.

## Notas de Desarrollo

- La base SQLite es local y regenerable.
- `database.py` crea el esquema y migra la columna `explicacion` si falta.
- Las distractoras se leen desde la tabla `distractors`; las tarjetas sin distractoras pueden usarse como preguntas abiertas.
- El frontend no requiere build step.

## Licencia

Uso educativo personal.
