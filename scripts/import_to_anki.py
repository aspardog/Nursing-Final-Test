#!/usr/bin/env python3
"""
Script para importar tarjetas a Anki usando AnkiConnect.

Requisitos:
1. Anki abierto
2. AnkiConnect instalado (codigo: 2055492159)

Uso:
    python scripts/import_to_anki.py [--clean]

Opciones:
    --clean    Borra todas las tarjetas existentes antes de importar
"""
import argparse
import json
import urllib.request
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / "cards"
ANKI_CONNECT_URL = "http://localhost:8765"

# Mapeo de tipos de nota (ingles -> espanol)
NOTE_TYPE_MAP = {
    "Basic": "Básico",
    "Cloze": "Respuesta anidada",
}

# Campos por tipo de nota en espanol
FIELD_MAP = {
    "Básico": {"front": "Anverso", "back": "Reverso"},
    "Respuesta anidada": {"front": "Texto", "back": "Reverso Extra"},
}

# Archivos CSV en orden de carga
CSV_FILES = [
    "cards_semiologia.csv",
    "cards_urgencias_basic.csv",
    "cards_salas_basic.csv",
    "cards_arritmias_basic.csv",
    "cards_mezclas_basic.csv",
    "cards_semiologia_cloze.csv",
    "cards_urgencias_cloze.csv",
    "cards_salas_cloze.csv",
    "cards_arritmias_cloze.csv",
    "cards_mezclas_cloze.csv",
]

# Mazos a crear
DECKS = [
    "Examen Final Enfermería::Semiología",
    "Examen Final Enfermería::Urgencias",
    "Examen Final Enfermería::Salas de Cirugía",
    "Examen Final Enfermería::Arritmias",
    "Examen Final Enfermería::Mezclas y Diluciones",
]


def anki_request(action: str, **params) -> dict:
    """Enviar request a AnkiConnect."""
    request_data = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode()

    try:
        response = urllib.request.urlopen(
            urllib.request.Request(ANKI_CONNECT_URL, request_data)
        ).read()
        return json.loads(response)
    except Exception as e:
        return {"error": str(e)}


def check_connection() -> bool:
    """Verificar conexion con AnkiConnect."""
    result = anki_request("version")
    if result.get("error"):
        print("❌ Error: No se puede conectar con AnkiConnect")
        print("   Asegurate de que:")
        print("   1. Anki este abierto")
        print("   2. AnkiConnect este instalado (Herramientas > Complementos > codigo: 2055492159)")
        return False
    print(f"✓ Conectado a AnkiConnect v{result['result']}")
    return True


def delete_existing_cards():
    """Borrar todas las tarjetas del mazo Examen Final Enfermeria."""
    print("\n🗑️  Borrando tarjetas anteriores...")
    card_ids = anki_request("findCards", query='deck:"Examen Final Enfermería"')

    if card_ids.get("result"):
        note_ids = anki_request("cardsToNotes", cards=card_ids["result"])
        if note_ids.get("result"):
            anki_request("deleteNotes", notes=note_ids["result"])
            print(f"   Eliminadas {len(card_ids['result'])} tarjetas")
    else:
        print("   No habia tarjetas anteriores")


def create_decks():
    """Crear los mazos necesarios."""
    print("\n📁 Creando mazos...")
    for deck in DECKS:
        anki_request("createDeck", deck=deck)
        print(f"   ✓ {deck}")


def parse_csv(filepath: Path) -> list[dict]:
    """Parsear archivo CSV en formato Anki."""
    cards = []
    note_type = "Básico"
    deck_name = "Examen Final Enfermería"

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("#notetype:"):
                nt = line.split(":")[1].strip()
                note_type = NOTE_TYPE_MAP.get(nt, "Básico")
            elif line.startswith("#deck:"):
                deck_name = line.split(":", 1)[1].strip()
            elif line.startswith("#"):
                continue
            else:
                parts = line.split("|")
                if len(parts) >= 3:
                    cards.append({
                        "front": parts[0].strip(),
                        "back": parts[1].strip(),
                        "tags": [parts[2].strip()] if parts[2].strip() else [],
                        "note_type": note_type,
                        "deck": deck_name
                    })

    return cards


def add_note(deck: str, model: str, front: str, back: str, tags: list) -> dict:
    """Agregar una nota a Anki."""
    fields = FIELD_MAP.get(model, FIELD_MAP["Básico"])

    note = {
        "deckName": deck,
        "modelName": model,
        "fields": {fields["front"]: front, fields["back"]: back},
        "tags": tags,
        "options": {"allowDuplicate": False}
    }

    return anki_request("addNote", note=note)


def import_cards():
    """Importar todas las tarjetas desde los CSV."""
    print("\n📥 Importando tarjetas...")
    total_added = 0

    for csv_file in CSV_FILES:
        filepath = CARDS_DIR / csv_file
        if not filepath.exists():
            print(f"   ⚠️  {csv_file} no encontrado")
            continue

        cards = parse_csv(filepath)
        added = 0

        for card in cards:
            result = add_note(
                card["deck"],
                card["note_type"],
                card["front"],
                card["back"],
                card["tags"]
            )
            if result.get("result"):
                added += 1

        print(f"   ✅ {csv_file}: {added} tarjetas")
        total_added += added

    return total_added


def main():
    parser = argparse.ArgumentParser(
        description="Importar tarjetas de enfermeria a Anki"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Borrar tarjetas existentes antes de importar"
    )
    args = parser.parse_args()

    print("🏥 Importador de Tarjetas a Anki\n")

    if not check_connection():
        return 1

    if args.clean:
        delete_existing_cards()

    create_decks()
    total = import_cards()

    print(f"\n🎉 ¡Listo! {total} tarjetas importadas")
    print("\n💡 Tip: Sincroniza con AnkiWeb para tener las tarjetas en tu celular")

    return 0


if __name__ == "__main__":
    exit(main())
