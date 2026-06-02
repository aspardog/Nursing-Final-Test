# CLAUDE.md

Guia para Claude Code sobre el proyecto Nursing Final Test.

## Descripcion del Proyecto

Simulador de examen final de enfermeria con 354 tarjetas en 4 temas: Salud Mental, Urgencias, Cirugia y Mezclas. Permite practicar con preguntas de opcion multiple (MCQ) y preguntas abiertas. Las tarjetas tambien pueden importarse a Anki.

## Arquitectura

```
Nursing-Final-Test/
├── cards/                      # Datos fuente (formato Anki, separador pipe)
│   ├── cards_semiologia.csv    # 209 tarjetas Basic
│   ├── cards_urgencias_basic.csv
│   ├── cards_salas_basic.csv
│   ├── cards_arritmias_basic.csv
│   ├── cards_mezclas_basic.csv
│   └── *_cloze.csv             # Tarjetas Cloze (28 total)
├── scripts/
│   └── import_to_anki.py       # Importador via AnkiConnect
├── quiz_app/                   # Aplicacion principal
│   ├── app.py                  # API FastAPI (rutas REST)
│   ├── database.py             # Conexion SQLite, esquema, migraciones, versionado
│   ├── quiz_engine.py          # Logica de quizzes, muestreo, sesiones
│   ├── load_cards.py           # Carga CSV a SQLite (orden determinista)
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
rm -f data/quiz.db
python3 load_cards.py
python3 generate_explanations.py
python3 generate_distractors.py

# Verificar estado
sqlite3 quiz_app/data/quiz.db "SELECT COUNT(*) FROM cards"        # 354
sqlite3 quiz_app/data/quiz.db "SELECT COUNT(*) FROM distractors"  # 942
sqlite3 quiz_app/data/quiz.db "SELECT DISTINCT tema FROM cards"   # 4 temas
```

## Integracion con Anki

Requiere Anki abierto con AnkiConnect instalado (codigo: 2055492159).

```bash
# Importar todas las tarjetas a Anki
python scripts/import_to_anki.py

# Borrar y reimportar (para actualizaciones)
python scripts/import_to_anki.py --clean
```

### Mapeo de tipos de nota

| CSV | Anki (espanol) | Campos |
|-----|----------------|--------|
| Basic | Básico | Anverso, Reverso |
| Cloze | Respuesta anidada | Texto, Reverso Extra |

### Mazos creados

- Examen Final Enfermería::Semiología (214)
- Examen Final Enfermería::Urgencias (67)
- Examen Final Enfermería::Salas de Cirugía (40)
- Examen Final Enfermería::Arritmias (18)
- Examen Final Enfermería::Mezclas y Diluciones (15)

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
- `database.py` tiene DB_VERSION para forzar actualizaciones en HF Spaces
- Los CSV tienen orden determinista en `load_cards.py` para IDs predecibles
- Las tarjetas Cloze no son elegibles para MCQ (se muestran como pregunta abierta)

## Temas y Mapeo

El archivo `load_cards.py` contiene TEMA_MAPPING que consolida los temas originales:

| Original | Tema Principal |
|----------|----------------|
| semiologia | salud_mental |
| urgencias | urgencias |
| arritmias | urgencias |
| salas | cirugia |
| mezclas | mezclas |
