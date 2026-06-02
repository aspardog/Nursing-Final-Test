---
layout: default
title: NurseRecall
---

# Estudiar enfermería con recuperación activa

Esta herramienta combina dos formas de práctica que se complementan: **Anki** para sostener la memoria a largo plazo y **quizzes** para entrenar la recuperación bajo presión, detectar vacíos y convertirlos en repaso dirigido.

[Iniciar Quiz](https://huggingface.co/spaces/santiagopardo03/test-enfermeria){: .btn .btn-primary }
[Importar a Anki](guia-anki){: .btn }
[Guía de la App](guia-app){: .btn }

<style>
  .study-flow {
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
    align-items: stretch;
    gap: 0.75rem;
    margin: 2rem 0 1.5rem;
  }

  .study-flow-step {
    border: 1px solid #dce6f0;
    border-radius: 8px;
    padding: 0.9rem;
    background: #f8fbfd;
    text-align: center;
  }

  .study-flow-step strong {
    display: block;
    color: #155f7a;
    margin-bottom: 0.3rem;
  }

  .study-flow-step span {
    display: block;
    color: #5b6770;
    font-size: 0.92rem;
    line-height: 1.35;
  }

  .study-flow-arrow {
    align-self: center;
    color: #159957;
    font-weight: 700;
    font-size: 1.25rem;
  }

  @media (max-width: 720px) {
    .study-flow {
      grid-template-columns: 1fr;
    }

    .study-flow-arrow {
      text-align: center;
      transform: rotate(90deg);
    }
  }
</style>

<div class="study-flow" aria-label="Flujo de estudio con Anki y quizzes">
  <div class="study-flow-step">
    <strong>Anki diario</strong>
    <span>recuperar conceptos</span>
  </div>
  <div class="study-flow-arrow">→</div>
  <div class="study-flow-step">
    <strong>Quiz corto</strong>
    <span>probar transferencia</span>
  </div>
  <div class="study-flow-arrow">→</div>
  <div class="study-flow-step">
    <strong>Revisión</strong>
    <span>corregir errores</span>
  </div>
  <div class="study-flow-arrow">→</div>
  <div class="study-flow-step">
    <strong>Repaso dirigido</strong>
    <span>volver a lo débil</span>
  </div>
</div>

---

## La lógica de estudio

El objetivo no es leer más veces el mismo material. El objetivo es **recordar sin mirar**, equivocarse temprano, corregir con feedback y volver a encontrarse con el contenido antes de olvidarlo por completo.

| Momento | Herramienta | Qué haces | Para qué sirve |
|---------|-------------|-----------|----------------|
| Todos los días | **Anki** | Respondes tarjetas pendientes sin mirar la respuesta. | Mantener conceptos, definiciones, clasificaciones y fórmulas con repetición espaciada. |
| 2-4 veces por semana | **Quiz** | Haces bloques cortos de preguntas por tema o mixtas. | Simular recuperación activa, integrar temas y descubrir debilidades. |
| Después del quiz | **Revisión** | Lees explicaciones, marcas errores y vuelves a estudiar lo fallado. | Convertir errores en decisiones concretas de repaso. |
| Antes del examen | **Quiz mixto + Anki** | Alternas preguntas abiertas, opción múltiple y tarjetas vencidas. | Practicar memoria, rapidez y discriminación entre respuestas parecidas. |

---

## Flujo recomendado

### 1. Construye base con Anki

Usa Anki como el sistema diario. No lo trates como lectura pasiva: cada tarjeta debe obligarte a producir una respuesta, aunque sea corta, antes de revelar el dorso.

- Haz primero las tarjetas vencidas.
- Si fallas una tarjeta, no la marques como sabida.
- Prioriza sesiones breves y constantes sobre maratones antes del examen.

### 2. Evalúa transferencia con quizzes

El quiz muestra si puedes recuperar la información fuera del formato exacto de la tarjeta. Empieza con 10-20 preguntas y sube la dificultad cuando el resultado sea estable.

- Usa **modo mixto** para alternar opción múltiple y preguntas abiertas.
- Practica por tema cuando estés construyendo base.
- Practica todos los temas mezclados cuando estés cerca del examen.

### 3. Cierra el ciclo con revisión

El resultado del quiz no es solo una nota. Es una lista de decisiones: qué subtema repasar, qué conceptos confundes y qué respuestas reconoces pero no puedes explicar.

- Revisa cada error el mismo día.
- Vuelve a Anki para reforzar lo fallado.
- Repite el quiz del tema cuando los errores cambien de patrón, no solo cuando baje el porcentaje.

---

## Por qué funciona

### Recuperación activa

Recordar una respuesta desde la memoria fortalece más el aprendizaje que solo releer. En el estudio clásico de Roediger y Karpicke, los estudiantes que practicaron con pruebas tuvieron mejor retención a largo plazo que quienes dedicaron más tiempo a releer el material. Esta idea se conoce como **test-enhanced learning** o **retrieval practice**.

### Repetición espaciada

La memoria mejora cuando el repaso se distribuye en el tiempo. La revisión de Cepeda y colaboradores sobre práctica distribuida muestra que espaciar las sesiones suele mejorar la retención frente a concentrar el estudio en una sola sesión. Anki automatiza esta parte: adelanta lo difícil y retrasa lo que ya recuerdas.

### Evidencia en educación en salud

En educación de profesiones de la salud, una revisión sistemática encontró beneficios significativos de la práctica distribuida y la recuperación activa en la mayoría de los estudios incluidos. Una revisión y metaanálisis reciente en educación médica también reportó un efecto favorable de la repetición espaciada frente a técnicas estándar de estudio.

---

## Cómo usar las dos herramientas juntas

| Si estás... | Haz esto |
|-------------|----------|
| Empezando un tema | Anki diario + quiz corto solo de ese tema. |
| Fallando muchas preguntas | Revisa explicaciones, vuelve a tarjetas básicas y repite en 24-48 horas. |
| Reconociendo respuestas pero sin poder explicarlas | Usa preguntas abiertas y obliga una respuesta en voz alta antes de mirar. |
| Cerca del examen | Mezcla todos los temas, limita el tiempo y revisa errores el mismo día. |

---

## Contenido disponible

La base actual contiene **354 tarjetas** organizadas en cuatro áreas:

| Tema | Tarjetas | Enfoque |
|------|----------|---------|
| **Salud Mental** | 214 | Semiología psiquiátrica, funciones mentales, síntomas y trastornos. |
| **Urgencias** | 85 | IAM, ACV, arritmias, bloqueos, taquiarritmias y emergencias metabólicas. |
| **Cirugía** | 40 | Salas de cirugía, heridas, clasificación ASA, anestesia y cálculos. |
| **Mezclas** | 15 | Concentraciones, diluciones, infusiones y cálculos prácticos. |

---

## Referencias

- Roediger, H. L., & Karpicke, J. D. (2006). [Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention](https://doi.org/10.1111/j.1467-9280.2006.01693.x). *Psychological Science*.
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). [Distributed practice in verbal recall tasks: A review and quantitative synthesis](https://doi.org/10.1037/0033-2909.132.3.354). *Psychological Bulletin*.
- Trumble, E., Lodge, J., Mandrusiak, A., & Forbes, R. (2024). [Systematic review of distributed practice and retrieval practice in health professions education](https://pubmed.ncbi.nlm.nih.gov/37615780/). *Advances in Health Sciences Education*.
- Maye, J. A., & Hurley, F. (2026). [The Effectiveness of Spaced Repetition in Medical Education: A Systematic Review and Meta-Analysis](https://pubmed.ncbi.nlm.nih.gov/41601436/). *The Clinical Teacher*.

---

<small>Uso educativo. Esta herramienta ayuda a estudiar, pero no reemplaza clase, práctica clínica ni revisión de fuentes institucionales.</small>
