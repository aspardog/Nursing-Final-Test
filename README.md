---
title: Quiz Enfermeria
emoji: "\U0001FA7A"
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Simulador de examen final de enfermeria.
---

# Nursing Final Test

Simulador de examen final para estudiantes de enfermeria. El proyecto combina tarjetas tipo Anki, una API FastAPI, una base SQLite y un frontend vanilla para practicar semiologia psiquiatrica con preguntas de opcion multiple y preguntas abiertas.

## Funcionalidades

- Quizzes configurables: 10, 20, 30 o 50 preguntas
- Tres modos de practica: mixto, solo opcion multiple, solo preguntas abiertas
- Proporcion MCQ ajustable en modo mixto
- Temporizador opcional por pregunta: sin limite, 30s, 60s o 90s
- Filtro por subtemas
- Feedback inmediato con respuesta correcta y explicacion educativa
- Autoevaluacion para preguntas abiertas: sabia, medias, no sabia
- Historial de sesiones persistente
- Resumen por formato y subtema
- Lista de tarjetas falladas para repaso

## Stack Tecnico

| Componente | Tecnologia |
|------------|------------|
| Backend | Python 3.11, FastAPI, Uvicorn, Pydantic |
| Base de datos | SQLite |
| Frontend | HTML, CSS, JavaScript (sin framework) |
| Dependencias | uv con pyproject.toml |
| Deploy | Hugging Face Spaces (Docker) |

## Estructura del Proyecto

```
Nursing-Final-Test/
├── cards/
│   └── cards_semiologia.csv       # Tarjetas fuente (formato Anki)
├── quiz_app/
│   ├── app.py                     # API FastAPI
│   ├── database.py                # Conexion y esquema SQLite
│   ├── quiz_engine.py             # Logica de quizzes y sesiones
│   ├── load_cards.py              # Carga de tarjetas CSV
│   ├── generate_explanations.py   # Explicaciones educativas (hardcoded)
│   ├── generate_distractors.py    # Distractores MCQ (hardcoded)
│   ├── text_normalizer.py         # Normalizacion de texto espanol
│   ├── data/
│   │   └── quiz.db                # Base de datos (generada, no versionada)
│   └── static/
│       ├── index.html
│       ├── app.js
│       └── style.css
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── CLAUDE.md                      # Guia para Claude Code
└── README.md
```

## Instalacion Local

Requisito: tener `uv` instalado.

```bash
# Instalar dependencias
uv sync --frozen

# Inicializar base de datos
cd quiz_app
python load_cards.py
python generate_explanations.py
python generate_distractors.py

# Ejecutar servidor
python -m uvicorn app:app --reload --port 8000
```

Abrir http://127.0.0.1:8000 en el navegador.

Nota: el proyecto requiere Python 3.11, 3.12 o 3.13.

## API REST

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/` | Frontend principal |
| GET | `/api/temas` | Lista temas y subtemas disponibles |
| POST | `/api/quiz/start` | Inicia sesion y devuelve preguntas |
| POST | `/api/quiz/answer` | Registra una respuesta |
| POST | `/api/quiz/end` | Finaliza sesion y devuelve resumen |
| GET | `/api/quiz/{id}/summary` | Consulta resumen de una sesion |
| GET | `/api/history` | Lista sesiones recientes |

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/quiz/start \
  -H "Content-Type: application/json" \
  -d '{"n_questions":10,"modo":"mcq"}'
```

## Base de Datos

Cuatro tablas principales:

- **cards**: Tarjetas con pregunta, respuesta, tema, subtema, explicacion
- **distractors**: Opciones incorrectas para MCQ (3 por tarjeta)
- **quiz_sessions**: Configuracion y resultados de cada sesion
- **responses**: Respuestas individuales

Los distractores y explicaciones estan hardcoded en archivos Python para evitar perdida de datos si la base se regenera.

## Agregar Tarjetas

Crear archivo CSV en `cards/` con formato Anki:

```
#separator:pipe
#html:true
#columns:Front|Back|Tags
#tags column:3
Pregunta|Respuesta con <b>HTML</b>|examen_final::tema::subtema
```

Ejecutar:

```bash
cd quiz_app && python load_cards.py
```

Las tarjetas se cargan de forma idempotente por texto de pregunta.

## Deploy en Hugging Face Spaces

El proyecto usa Docker SDK. Configuracion en el header YAML de este README:

```yaml
sdk: docker
app_port: 7860
```

### Storage Persistente

En Hugging Face Spaces, la aplicacion detecta la variable `SPACE_ID` y usa `/data/quiz.db` como base de datos. Esto permite que el historial de sesiones persista entre reinicios del Space.

Primera ejecucion: copia la DB inicial con tarjetas, explicaciones y distractores a `/data/`.
Ejecuciones posteriores: usa la DB existente en `/data/`.

### Comandos de Deploy

```bash
# Agregar remote de Hugging Face
git remote add space https://huggingface.co/spaces/TU_USUARIO/quiz-enfermeria

# Push usando rama space-deploy (sin archivos binarios)
git checkout space-deploy
git cherry-pick <commits>
git push space space-deploy:main
git checkout main
```

### Docker Local

```bash
docker build -t nursing-final-test .
docker run -p 7860:7860 nursing-final-test
```

## Notas de Desarrollo

- La base SQLite local esta en gitignore y es regenerable
- `database.py` crea el esquema y migra columnas automaticamente
- Las tarjetas sin distractores funcionan como preguntas abiertas
- El frontend no requiere build step
- Puerto local: 8000, puerto Hugging Face: 7860

## Licencia

MIT - Uso educativo.
