"""
Utilities for improving Spanish orthography in user-facing text.
"""
from __future__ import annotations

import re


_REPLACEMENTS: list[tuple[str, str]] = [
    (r"\brespuesta multiple\b", "respuesta múltiple"),
    (r"\bcomo evaluas\b", "cómo evalúas"),
    (r"\bevaluacion\b", "evaluación"),
    (r"\bevaluaciones\b", "evaluaciones"),
    (r"\bpsiquiatrica\b", "psiquiátrica"),
    (r"\bpsiquiatricas\b", "psiquiátricas"),
    (r"\bpsiquiatrico\b", "psiquiátrico"),
    (r"\bpsiquiatricos\b", "psiquiátricos"),
    (r"\binformacion\b", "información"),
    (r"\balteracion\b", "alteración"),
    (r"\balteraciones\b", "alteraciones"),
    (r"\bcronologica\b", "cronológica"),
    (r"\bcronologico\b", "cronológico"),
    (r"\bclinicamente\b", "clínicamente"),
    (r"\bcronica\b", "crónica"),
    (r"\borganica\b", "orgánica"),
    (r"\borganico\b", "orgánico"),
    (r"\borganicas\b", "orgánicas"),
    (r"\borganicos\b", "orgánicos"),
    (r"\bmetabolica\b", "metabólica"),
    (r"\bmetabolicas\b", "metabólicas"),
    (r"\btoxica\b", "tóxica"),
    (r"\btoxicas\b", "tóxicas"),
    (r"\binfeccion\b", "infección"),
    (r"\bconexion\b", "conexión"),
    (r"\bsensopercepcion\b", "sensopercepción"),
    (r"\borientacion\b", "orientación"),
    (r"\batencion\b", "atención"),
    (r"\bfocalizacion\b", "focalización"),
    (r"\bconcentracion\b", "concentración"),
    (r"\bpercepcion\b", "percepción"),
    (r"\bfuncion\b", "función"),
    (r"\bfunciones\b", "funciones"),
    (r"\bdiagnostico\b", "diagnóstico"),
    (r"\bpatologico\b", "patológico"),
    (r"\bpatologica\b", "patológica"),
    (r"\bpatologia\b", "patología"),
    (r"\bneurologico\b", "neurológico"),
    (r"\bneurologica\b", "neurológica"),
    (r"\bneurologicos\b", "neurológicos"),
    (r"\bneurologicas\b", "neurológicas"),
    (r"\bpsicoticos\b", "psicóticos"),
    (r"\bpsicotico\b", "psicótico"),
    (r"\bpsicotica\b", "psicótica"),
    (r"\bpsicoticas\b", "psicóticas"),
    (r"\btaquipsiquia\b", "taquipsiquia"),
    (r"\bbradipsiquia\b", "bradipsiquia"),
    (r"\binteres\b", "interés"),
    (r"\binhibicion\b", "inhibición"),
    (r"\bdespersonalizacion\b", "despersonalización"),
    (r"\bdesrealizacion\b", "desrealización"),
    (r"\bdisgregacion\b", "disgregación"),
    (r"\blogica\b", "lógica"),
    (r"\blogico\b", "lógico"),
    (r"\blogicamente\b", "lógicamente"),
    (r"\bexplicacion\b", "explicación"),
    (r"\baqui\b", "aquí"),
    (r"\bsueno\b", "sueño"),
    (r"\bmas\b", "más"),
    (r"\bano\b", "año"),
    (r"\banos\b", "años"),
    (r"\bmania\b", "manía"),
    (r"\bdepresion\b", "depresión"),
    (r"\bansiedad\b", "ansiedad"),
    (r"\bintoxicacion\b", "intoxicación"),
    (r"\breaccion\b", "reacción"),
    (r"\bclinico\b", "clínico"),
    (r"\bclinica\b", "clínica"),
    (r"\bclasificacion\b", "clasificación"),
    (r"\bsistematicamente\b", "sistemáticamente"),
    (r"\bprerequisito\b", "prerrequisito"),
    (r"\bprivacion\b", "privación"),
    (r"\bfacilmente\b", "fácilmente"),
    (r"\butil\b", "útil"),
    (r"\bmedica\b", "médica"),
    (r"\bmedico\b", "médico"),
    (r"\bmedicas\b", "médicas"),
    (r"\bmedicos\b", "médicos"),
    (r"\brecien\b", "recién"),
    (r"\brelacion\b", "relación"),
    (r"\brelaciones\b", "relaciones"),
    (r"\bcomun\b", "común"),
    (r"\bcomunes\b", "comunes"),
    (r"\brapido\b", "rápido"),
    (r"\brapida\b", "rápida"),
    (r"\brapidamente\b", "rápidamente"),
    (r"\bmotricidad\b", "motricidad"),
    (r"\bmovimiento\b", "movimiento"),
    (r"\bmovimientos\b", "movimientos"),
    (r"\bmanifestacion\b", "manifestación"),
    (r"\bmanifestaciones\b", "manifestaciones"),
    (r"\bsintoma\b", "síntoma"),
    (r"\bsintomas\b", "síntomas"),
    (r"\bsigno\b", "signo"),
    (r"\bsignos\b", "signos"),
    (r"\bexpresion\b", "expresión"),
    (r"\bexpresiones\b", "expresiones"),
    (r"\bfisico\b", "físico"),
    (r"\bfisica\b", "física"),
    (r"\bfisicos\b", "físicos"),
    (r"\bfisicas\b", "físicas"),
    (r"\brespuestas\b", "respuestas"),
    (r"\brespuesta\b", "respuesta"),
    (r"\bmotivacion\b", "motivación"),
    (r"\bcomprension\b", "comprensión"),
    (r"\bestimulo\b", "estímulo"),
    (r"\bestimulos\b", "estímulos"),
    (r"\bespontanea\b", "espontánea"),
    (r"\bespontaneo\b", "espontáneo"),
    (r"\bespontaneas\b", "espontáneas"),
    (r"\bespontaneos\b", "espontáneos"),
    (r"\bnucleo\b", "núcleo"),
    (r"\bmultiples\b", "múltiples"),
    (r"\btemprano\b", "temprano"),
    (r"\bsevero\b", "severo"),
    (r"\bsevera\b", "severa"),
]

_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(pattern, flags=re.IGNORECASE), replacement) for pattern, replacement in _REPLACEMENTS
]


def _apply_case(replacement: str, original: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def normalize_spanish_text(text: str | None) -> str | None:
    if text is None:
        return None

    result = text
    for pattern, replacement in _PATTERNS:
        result = pattern.sub(lambda match: _apply_case(replacement, match.group(0)), result)

    return result
