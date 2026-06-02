---
layout: default
title: Guía de Anki
---

# Importar Tarjetas a Anki

[← Volver al inicio](.)

---

## ¿Por qué usar Anki?

Anki usa **repetición espaciada**, un método científicamente probado para memorización a largo plazo. Las tarjetas que te cuestan más aparecen con mayor frecuencia.

**Ventajas:**
- Retención superior al estudio tradicional
- App móvil para estudiar en cualquier lugar
- Sincronización entre dispositivos
- Estadísticas de progreso

---

## Paso 1: Instalar Anki

### Desktop (requerido para importar)

Descarga Anki para tu sistema operativo:

[Descargar Anki](https://apps.ankiweb.net/){: .btn .btn-primary }

### Móvil (opcional, para estudiar)

- **iOS**: [AnkiMobile](https://apps.apple.com/app/ankimobile-flashcards/id373493387) (de pago)
- **Android**: [AnkiDroid](https://play.google.com/store/apps/details?id=com.ichi2.anki) (gratis)

---

## Paso 2: Instalar AnkiConnect

AnkiConnect es un complemento que permite importar tarjetas automáticamente.

1. Abre **Anki** en tu computadora
2. Ve a **Herramientas → Complementos**
3. Click en **Obtener complementos...**
4. Ingresa el código: `2055492159`
5. Click **OK**
6. **Reinicia Anki**

---

## Paso 3: Clonar el Repositorio

Si no tienes el repositorio:

```bash
git clone https://github.com/aspardog/Nursing-Final-Test.git
cd Nursing-Final-Test
```

---

## Paso 4: Importar las Tarjetas

Con Anki abierto, ejecuta:

```bash
python scripts/import_to_anki.py
```

Verás algo como:

```
🏥 Importador de Tarjetas a Anki

✓ Conectado a AnkiConnect v6

📁 Creando mazos...
   ✓ Examen Final Enfermería::Semiología
   ✓ Examen Final Enfermería::Urgencias
   ✓ Examen Final Enfermería::Salas de Cirugía
   ✓ Examen Final Enfermería::Arritmias
   ✓ Examen Final Enfermería::Mezclas y Diluciones

📥 Importando tarjetas...
   ✅ cards_semiologia.csv: 209 tarjetas
   ✅ cards_urgencias_basic.csv: 52 tarjetas
   ...

🎉 ¡Listo! 354 tarjetas importadas
```

### Actualizar tarjetas existentes

Si ya tienes tarjetas y quieres actualizar:

```bash
python scripts/import_to_anki.py --clean
```

Esto borra las tarjetas anteriores y reimporta todo.

---

## Paso 5: Sincronizar con AnkiWeb

Para tener las tarjetas en tu celular:

1. En Anki desktop, click en **Sincronizar**
2. Crea una cuenta de AnkiWeb si no tienes
3. Espera a que suba las tarjetas
4. En la app móvil, sincroniza con la misma cuenta

---

## Estructura de Mazos

Después de importar tendrás:

```
Examen Final Enfermería/
├── Semiología (214 tarjetas)
├── Urgencias (67 tarjetas)
├── Salas de Cirugía (40 tarjetas)
├── Arritmias (18 tarjetas)
└── Mezclas y Diluciones (15 tarjetas)
```

---

## Tipos de Tarjetas

### Basic (Básico)

Pregunta en el frente, respuesta en el reverso.

| Anverso | Reverso |
|---------|---------|
| ¿Qué hallazgo en el EKG corresponde a ISQUEMIA? | Onda T simétrica (invertida y simétrica) |

### Cloze (Respuesta anidada)

Texto con espacios en blanco para completar.

**Ejemplo:**
> El pensamiento se valora en 3 aspectos: [...], [...] y [...].

---

## Configuración Recomendada

### Opciones del Mazo

Click derecho en el mazo → **Opciones**:

| Parámetro | Valor Sugerido |
|-----------|----------------|
| Tarjetas nuevas/día | 20-30 |
| Revisiones máximas/día | 200 |
| Intervalo de graduación | 1 10 |
| Intervalo fácil | 4 días |

### Horario de Estudio

- **Mañana**: Tarjetas nuevas + revisiones
- **Noche**: Solo revisiones pendientes
- **Consistencia**: Mejor 20 min diarios que 2 horas esporádicas

---

## Solución de Problemas

### "AnkiConnect no disponible"

- Verifica que Anki esté abierto
- Verifica que AnkiConnect esté instalado (Herramientas → Complementos)
- Reinicia Anki

### "model was not found"

El script usa nombres en español. Verifica que tienes los tipos de nota:
- **Básico** (no "Basic")
- **Respuesta anidada** (no "Cloze")

Si no los tienes, crea una tarjeta manualmente primero para que Anki cree el tipo de nota.

### Las tarjetas no aparecen en el celular

1. En desktop: Click en **Sincronizar**
2. Espera a que termine (puede tomar unos minutos)
3. En la app móvil: Sincroniza también

---

[← Volver al inicio](.) | [Guía de la App Web](guia-app)
