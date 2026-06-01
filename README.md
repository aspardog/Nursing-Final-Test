# Quiz Enfermeria

Simulador de examen final para estudiantes de enfermeria. Genera quizzes de practica con preguntas de opcion multiple y abiertas basadas en tarjetas Anki de semiologia psiquiatrica.

## Caracteristicas

- **Modo mixto**: 70% MCQ + 30% preguntas abiertas (configurable)
- **Modo solo MCQ** o **solo abierto**
- **Timer opcional** por pregunta (30s, 60s, 90s)
- **Filtros por tema**: selecciona subtemas especificos
- **Feedback inmediato**: siempre muestra la respuesta correcta
- **Autoevaluacion**: para preguntas abiertas (sabia/medias/no sabia)
- **Historial**: revisa sesiones anteriores y tu progreso
- **Resumen detallado**: desglose por tema y formato, lista de tarjetas falladas

## Requisitos

- Python 3.10+
- pip

## Instalacion local

```bash
# Clonar el repositorio
git clone <repo-url>
cd Nursing-Final-Test

# Instalar dependencias
pip install -r quiz_app/requirements.txt

# Cargar las tarjetas en la base de datos
cd quiz_app
python load_cards.py

# Iniciar el servidor
python -m uvicorn app:app --port 8000
```

Abrir http://localhost:8000 en el navegador.

## Estructura del proyecto

```
Nursing-Final-Test/
├── cards/
│   └── cards_semiologia.csv    # Tarjetas Anki (209 tarjetas)
├── material/                    # PDFs extraidos
├── quiz_app/
│   ├── app.py                  # FastAPI server
│   ├── database.py             # SQLite schema
│   ├── quiz_engine.py          # Logica de quizzes
│   ├── distractor_generator.py # Generador de distractoras
│   ├── load_cards.py           # Carga tarjetas a DB
│   ├── data/
│   │   └── quiz.db             # Base de datos SQLite
│   ├── static/
│   │   ├── index.html          # Frontend
│   │   ├── style.css
│   │   └── app.js
│   └── tests/
│       └── test_engine.py
├── Dockerfile
└── README.md
```

## API Endpoints

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/` | Sirve el frontend |
| GET | `/api/temas` | Lista temas/subtemas disponibles |
| POST | `/api/quiz/start` | Inicia una sesion de quiz |
| POST | `/api/quiz/answer` | Registra una respuesta |
| POST | `/api/quiz/end` | Termina la sesion |
| GET | `/api/quiz/{id}/summary` | Resumen de una sesion |
| GET | `/api/history` | Ultimas 20 sesiones |

## Deploy en Render.com

1. Crea una cuenta en [render.com](https://render.com)

2. Conecta tu repositorio de GitHub

3. Crea un nuevo **Web Service** con estos settings:
   - **Build Command**: `pip install -r quiz_app/requirements.txt && cd quiz_app && python load_cards.py`
   - **Start Command**: `cd quiz_app && python -m uvicorn app:app --host 0.0.0.0 --port $PORT`

4. Variables de entorno (opcional):
   - `PORT`: 10000 (default de Render)

5. Deploy!

### Usando Docker

```bash
# Build
docker build -t quiz-enfermeria .

# Run
docker run -p 8000:8000 quiz-enfermeria
```

## Agregar mas tarjetas

1. Crea un CSV con formato Anki en `cards/`:
   ```
   #separator:pipe
   #html:true
   #columns:Front|Back|Tags
   #tags column:3
   Pregunta|Respuesta con <b>HTML</b>|examen_final::tema::subtema
   ```

2. Ejecuta `python load_cards.py` para cargar las nuevas tarjetas

3. Las distractoras MCQ deben generarse manualmente o con Claude

## Tecnologias

- **Backend**: FastAPI, SQLite
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Sin frameworks JS**: todo es vanilla para simplicidad

## Licencia

Uso educativo personal.
