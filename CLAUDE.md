# CLAUDE.md

Guia para Claude Code sobre el proyecto Nursing Final Test.

## Descripcion del Proyecto

Simulador de examen final de enfermeria con enfoque en semiologia psiquiatrica. Permite practicar con preguntas de opcion multiple (MCQ) y preguntas abiertas.

## Arquitectura

```
Nursing-Final-Test/
├── cards/                      # Datos fuente
│   └── cards_semiologia.csv    # Tarjetas en formato Anki (separador pipe)
├── quiz_app/                   # Aplicacion principal
│   ├── app.py                  # API FastAPI (rutas REST)
│   ├── database.py             # Conexion SQLite, esquema, migraciones
│   ├── quiz_engine.py          # Logica de quizzes, muestreo, sesiones
│   ├── load_cards.py           # Carga CSV a SQLite
│   ├── generate_explanations.py # Explicaciones hardcoded por tarjeta
│   ├── generate_distractors.py # Distractores hardcoded para MCQ
│   ├── text_normalizer.py      # Normalizacion de texto en espanol
│   ├── data/                   # Base de datos local (gitignore)
│   │   └── quiz.db
│   └── static/                 # Frontend vanilla
│       ├── index.html
│       ├── app.js
│       └── style.css
├── Dockerfile                  # Build para Hugging Face Spaces
├── pyproject.toml              # Dependencias (uv)
└── uv.lock                     # Lock file
```

## Base de Datos

SQLite con 4 tablas principales:

- `cards`: Tarjetas con pregunta (frente), respuesta (dorso), tema, subtema, explicacion
- `distractors`: Opciones incorrectas para MCQ (3 por tarjeta, referencia card_id)
- `quiz_sessions`: Sesiones de quiz con configuracion y resultados
- `responses`: Respuestas individuales por sesion

## Flujo de Datos

1. `load_cards.py` carga tarjetas desde CSV
2. `generate_explanations.py` inserta explicaciones educativas (hardcoded)
3. `generate_distractors.py` inserta distractores para MCQ (hardcoded)
4. `quiz_engine.py` genera quizzes combinando cards + distractors
5. Frontend consume API y renderiza la interfaz

## Comandos Frecuentes

```bash
# Ejecutar localmente
cd quiz_app && python3 app.py

# Regenerar base de datos
cd quiz_app
python3 load_cards.py
python3 generate_explanations.py
python3 generate_distractors.py

# Verificar estado de distractores
sqlite3 quiz_app/data/quiz.db "SELECT COUNT(*) FROM distractors"
```

## Deploy

Dos repositorios remotos:

- `origin`: GitHub (https://github.com/aspardog/Nursing-Final-Test)
- `space`: Hugging Face (https://huggingface.co/spaces/santiagopardo03/test-enfermeria)

Para Hugging Face, usar la rama `space-deploy` que no contiene archivos binarios:

```bash
git checkout space-deploy
git cherry-pick <commit>
git push space space-deploy:main
git checkout main
```

## Storage Persistente (Hugging Face)

En Hugging Face Spaces, la app detecta `SPACE_ID` y usa `/data/quiz.db` para persistir el historial entre reinicios. La primera ejecucion copia la DB inicial desde `/app/quiz_app/data/quiz.db`.

## Notas Importantes

- Los distractores y explicaciones estan hardcoded en archivos .py para evitar perdida de datos si la DB se recrea
- La DB local (`quiz_app/data/quiz.db`) esta en gitignore
- El frontend no requiere build step (vanilla JS/CSS/HTML)
- El puerto local es 8000, en Hugging Face es 7860
