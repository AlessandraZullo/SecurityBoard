#!/usr/bin/env python3
"""
base64_to_pdf.py

Decodifica un campo base64 (contenuto in un file JSON, oppure passato come
stringa grezza) e lo salva come PDF.

USO:
    # Da un file JSON, specificando la chiave che contiene il base64
    python3 base64_to_pdf.py --json risposta.json --key document -o output.pdf

    # Da un file JSON, provando a trovare automaticamente il campo base64
    python3 base64_to_pdf.py --json risposta.json -o output.pdf

    # Da un file di testo contenente solo la stringa base64 (anche con
    # eventuale prefisso "data:application/pdf;base64,")
    python3 base64_to_pdf.py --raw base64.txt -o output.pdf

    # Leggendo da stdin
    cat base64.txt | python3 base64_to_pdf.py -o output.pdf
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path


def pulisci_base64(s: str) -> str:
    """Rimuove virgolette, prefisso data URI, whitespace/newline e
    aggiunge il padding mancante."""
    s = s.strip()
    # toglie eventuali virgolette che racchiudono l'intera stringa
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    # rimuove un eventuale prefisso tipo "data:application/pdf;base64,"
    s = re.sub(r'^data:[^,]*,', '', s)
    # rimuove whitespace/newline reali e sequenze letterali \n \r (capita
    # quando il base64 è stato copiato da un JSON con escape non interpretati)
    s = s.replace('\\n', '').replace('\\r', '')
    s = re.sub(r'\s+', '', s)
    # ripristina il padding '=' se mancante
    s += '=' * (-len(s) % 4)
    return s


def trova_base64_in_json(dato, chiave_preferita=None):
    """Cerca ricorsivamente nel JSON una stringa che sembri un base64 di PDF.
    Se chiave_preferita è indicata, la usa con priorità."""

    candidati = []

    def ricorsione(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                nuovo_path = f"{path}.{k}" if path else k
                if isinstance(v, str):
                    if chiave_preferita and k == chiave_preferita:
                        candidati.insert(0, (nuovo_path, v))  # priorità massima
                    elif len(v) > 200:  # stringhe brevi non sono PDF
                        candidati.append((nuovo_path, v))
                else:
                    ricorsione(v, nuovo_path)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                ricorsione(v, f"{path}[{i}]")

    ricorsione(dato)
    return candidati


def decodifica_e_verifica(base64_str: str) -> bytes:
    pulito = pulisci_base64(base64_str)
    try:
        dati = base64.b64decode(pulito, validate=False)
    except Exception as e:
        raise ValueError(f"Decodifica base64 fallita: {e}")

    if not dati.startswith(b"%PDF"):
        raise ValueError(
            "Il contenuto decodificato non inizia con l'header '%PDF': "
            "non sembra un PDF valido (primi byte: "
            f"{dati[:20]!r})"
        )
    return dati


def main():
    parser = argparse.ArgumentParser(
        description="Decodifica un base64 (anche dentro un JSON) in un file PDF."
    )
    sorgente = parser.add_mutually_exclusive_group(required=False)
    sorgente.add_argument("--json", type=str, help="Percorso di un file JSON contenente il base64.")
    sorgente.add_argument("--raw", type=str, help="Percorso di un file di testo contenente solo la stringa base64.")
    parser.add_argument("--key", type=str, default=None,
                         help="Nome della chiave JSON che contiene il base64 (es: 'document', 'content', 'file').")
    parser.add_argument("-o", "--output", type=str, default="output.pdf",
                         help="Percorso del PDF da generare (default: output.pdf).")

    args = parser.parse_args()

    if args.json:
        testo = Path(args.json).read_text(encoding="utf-8")
        try:
            dato = json.loads(testo)
        except json.JSONDecodeError as e:
            print(f"[ERRORE] Il file non è un JSON valido: {e}", file=sys.stderr)
            sys.exit(1)

        candidati = trova_base64_in_json(dato, chiave_preferita=args.key)
        if not candidati:
            print("[ERRORE] Nessun campo stringa sufficientemente lungo trovato nel JSON.", file=sys.stderr)
            sys.exit(1)

        path_usato, base64_str = candidati[0]
        if len(candidati) > 1 and not args.key:
            print(f"[INFO] Trovati più campi candidati, uso '{path_usato}'. "
                  f"Se non è quello giusto, specifica --key.", file=sys.stderr)

    elif args.raw:
        base64_str = Path(args.raw).read_text(encoding="utf-8")

    else:
        # legge da stdin se non è stato passato né --json né --raw
        if sys.stdin.isatty():
            parser.error("Specifica --json oppure --raw, oppure passa il base64 su stdin.")
        base64_str = sys.stdin.read()

    try:
        dati_pdf = decodifica_e_verifica(base64_str)
    except ValueError as e:
        print(f"[ERRORE] {e}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.write_bytes(dati_pdf)
    print(f"[OK] PDF salvato in '{output_path}' ({len(dati_pdf)} byte).")


if __name__ == "__main__":
    main()