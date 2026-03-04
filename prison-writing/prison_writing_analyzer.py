#!/opt/homebrew/bin/python3.10
# prison_writing_analyzer.py — OCR + analyse graphologique de documents visuels
# Goldberg Variations — outil générique, contexte configurable via --context-file
#
# Usage :
#   python prison_writing_analyzer.py /dossier/images/
#   python prison_writing_analyzer.py /dossier/ --context-file contexts/goldberg-prison.json
#   python prison_writing_analyzer.py /dossier/ --output-dir /chemin/sortie/
#   python prison_writing_analyzer.py /dossier/ --resume
#   python prison_writing_analyzer.py /dossier/ --recheck-only
#   python prison_writing_analyzer.py /dossier/ --consolidate
#   python prison_writing_analyzer.py /dossier/ --dry-run
#   python prison_writing_analyzer.py /dossier/ --sample 10

import argparse
import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ── Clé API ───────────────────────────────────────────────────────────────────
_secrets = Path.home() / ".claude" / "secrets" / "opc-skills.env"
if _secrets.exists():
    for line in _secrets.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

import google.genai as genai

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_MAIN     = "gemini-3-flash-preview"   # pass principal (rapide, bon)
MODEL_RECHECK  = "gemini-2.5-pro"           # recheck images difficiles
CONFIDENCE_THRESHOLD = 0.70                 # en dessous → recheck automatique

OUTPUT_BASE    = Path.home() / "Projects/Films/goldberg/sources/heic-prison-docs"  # défaut Joshua
JSON_DIR       = OUTPUT_BASE / "json"
CORPUS_DIR     = OUTPUT_BASE / "corpus"
TEMP_DIR       = OUTPUT_BASE / "_temp_jpeg"
PROGRESS_FILE  = OUTPUT_BASE / ".progress_writing.json"

# ── Contexte configurable ──────────────────────────────────────────────────────
# Charger un contexte custom : python script.py /dossier --context-file mon_contexte.json
# Format : {"project": "...", "subject_description": "...", "doc_types": [...], "prompt_suffix": "..."}
CONTEXT: dict = {}  # rempli depuis --context-file ou via load_context()

IMAGE_EXTENSIONS = {".heic", ".jpg", ".jpeg", ".png", ".dng", ".tiff", ".tif"}
MAX_RETRIES    = 3
RETRY_BACKOFF  = [15, 45, 120]

# ── Types de documents connus dans le dossier Joshua ──────────────────────────
DOC_TYPES = [
    "lettre_manuscrite",       # lettre écrite à la main sur papier
    "jpay_imprime",            # email prison JPay imprimé (header JPay.com visible)
    "corrlinks_imprime",       # email prison CorrLinks imprimé
    "document_admin_prison",   # formulaire ou document administratif prison
    "rapport_psychiatrique",   # évaluation psychologique/psychiatrique tapée
    "document_judiciaire",     # document de tribunal, sentencing, motion, etc.
    "note_personnelle",        # notes informelles, journaux intimes
    "dessin_croquis",          # dessin ou illustration
    "enveloppe",               # photo d'enveloppe
    "article_presse",          # article de journal/magazine
    "autre",
]

# ── Prompt principal ───────────────────────────────────────────────────────────
PROMPT_MAIN = """Tu analyses un document issu des archives personnelles de Joshua Ryne Goldberg,
incarcéré au Federal Detention Center de Tallahassee (Floride) depuis 2015.
Ces documents sont des sources primaires pour un film documentaire.

TÂCHES (répondre en JSON strict, aucun commentaire autour) :

1. TRANSCRIPTION : Retranscrire mot pour mot tout le texte visible.
   - Préserver la mise en page (retours à la ligne, listes, etc.)
   - Signaler [illisible] pour les mots indéchiffrables
   - Signaler [raturé: probable_mot] pour les ratures
   - Si multi-pages visibles : séparer par --- PAGE ---

2. CLASSIFICATION du document :
   Types possibles : lettre_manuscrite | jpay_imprime | corrlinks_imprime |
   document_admin_prison | rapport_psychiatrique | document_judiciaire |
   note_personnelle | dessin_croquis | enveloppe | article_presse | autre

3. MÉTADONNÉES :
   - Date du document (si visible, format YYYY-MM-DD ou texte brut si ambigu)
   - Destinataire et expéditeur (si identifiables)
   - Medium d'écriture : stylo_bille | crayon | feutre | dactylo | impression_numerique | inconnu
   - Support : papier_ligne | papier_libre | formulaire_prison | papier_officiel | autre

4. GRAPHOLOGIE (uniquement si manuscrit) :
   - Pression : legere | moyenne | forte | variable
   - Inclinaison : gauche | verticale | droite | variable
   - Taille : petite | moyenne | grande | variable
   - Régularité : reguliere | irreguliere | chaotique
   - Espacement entre mots : serre | normal | large
   - Lisibilité : excellente | bonne | moyenne | difficile
   - Corrections/ratures : aucune | quelques | nombreuses
   - Observations libres : 1-2 phrases sur ce que l'écriture révèle

5. DATA MINING :
   - Personnes citées (noms propres, surnoms, initiales)
   - Lieux cités
   - Dates/événements mentionnés dans le texte
   - Thèmes principaux (max 5 mots-clés)
   - État émotionnel apparent : stable | anxieux | depressif | optimiste | agite |
     colere | ironie | paranoiaque | plat | autre

6. CONFIANCE : score 0.0-1.0 sur la qualité de ta transcription
   (1.0 = tout lisible, 0.0 = document illisible)

Répondre UNIQUEMENT avec ce JSON (sans markdown, sans texte avant/après) :
{
  "transcription": "...",
  "type_document": "...",
  "date_document": null,
  "destinataire": null,
  "expediteur": null,
  "medium": "...",
  "support": "...",
  "graphologie": {
    "pression": null,
    "inclinaison": null,
    "taille": null,
    "regularite": null,
    "espacement": null,
    "lisibilite": null,
    "corrections": null,
    "observations": null
  },
  "personnes_citees": [],
  "lieux_cites": [],
  "dates_mentionnees": [],
  "themes": [],
  "etat_emotionnel": "...",
  "contenu_notable": "phrase résumant l'intérêt documentaire de ce document",
  "confidence_transcription": 0.0,
  "flags": []
}"""

PROMPT_RECHECK = """Document de prison difficile à lire. Porte une attention maximale à la transcription.
Utilise les zones de contexte (lignes voisines, début de mots) pour déduire les mots incertains.
Note [incertain: ta_déduction] pour les mots déduits avec <70% certitude.

""" + PROMPT_MAIN

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_secrets():
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("ERREUR : GEMINI_API_KEY manquante. Source ~/.claude/secrets/opc-skills.env")
        sys.exit(1)
    return key


def collect_images(source: Path) -> list[Path]:
    """Collecte HEIC, DNG, JPEG depuis le dossier source."""
    files = [
        p for p in source.iterdir()
        if p.suffix.lower() in IMAGE_EXTENSIONS
        and not p.name.startswith("._")  # exclure resource forks macOS/exFAT
        and not p.name.startswith(".")
    ]
    return sorted(files, key=lambda p: p.name)


def convert_to_jpeg(src: Path, out_dir: Path) -> Path:
    """Convertit HEIC ou DNG en JPEG via sips (natif macOS). Retourne le path JPEG."""
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / (src.stem + ".jpg")
    if dst.exists():
        return dst
    result = subprocess.run(
        ["sips", "-s", "format", "jpeg", str(src), "--out", str(dst)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"sips failed on {src.name}: {result.stderr.strip()}")
    return dst


def encode_image(path: Path) -> tuple[str, str]:
    """Encode l'image en base64. Retourne (base64_data, mime_type)."""
    suffix = path.suffix.lower()
    mime = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".heic": "image/heic",
    }.get(suffix, "image/jpeg")
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return data, mime


def parse_json_response(text: str) -> dict:
    """Extrait le JSON de la réponse Gemini (peut contenir du texte parasite)."""
    text = text.strip()
    # Chercher le JSON entre { }
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"Aucun JSON trouvé dans la réponse : {text[:200]}")
    return json.loads(text[start:end])


def analyze_image(client, image_path: Path, model: str, prompt: str) -> dict:
    """Appelle Gemini sur une image. Retourne le dict analysé."""
    # Convertir si nécessaire
    if image_path.suffix.lower() in {".dng", ".tiff", ".tif"}:
        jpeg_path = convert_to_jpeg(image_path, TEMP_DIR)
    elif image_path.suffix.lower() == ".heic":
        jpeg_path = convert_to_jpeg(image_path, TEMP_DIR)
    else:
        jpeg_path = image_path

    b64data, mime = encode_image(jpeg_path)

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {
                        "parts": [
                            {"inline_data": {"mime_type": mime, "data": b64data}},
                            {"text": prompt},
                        ]
                    }
                ]
            )
            result = parse_json_response(response.text)
            result["_meta"] = {
                "fichier": image_path.name,
                "model_utilise": model,
                "traite_le": datetime.now().isoformat(),
                "needs_recheck": False,
            }
            return result
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF[attempt]
                print(f"    Erreur ({e.__class__.__name__}), retry dans {wait}s...")
                time.sleep(wait)
            else:
                raise


def load_progress(progress_file: Path) -> dict:
    if progress_file.exists():
        return json.loads(progress_file.read_text())
    return {"done": [], "failed": [], "recheck_pending": []}


def save_progress(progress_file: Path, state: dict):
    progress_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ── Consolidation ─────────────────────────────────────────────────────────────

def consolidate(json_dir: Path, corpus_dir: Path):
    """Génère les fichiers corpus depuis tous les JSON existants."""
    corpus_dir.mkdir(parents=True, exist_ok=True)
    jsons = sorted(json_dir.glob("*.json"))
    if not jsons:
        print("Aucun JSON trouvé pour la consolidation.")
        return

    records = []
    for jf in jsons:
        try:
            records.append(json.loads(jf.read_text()))
        except Exception as e:
            print(f"  Skip {jf.name}: {e}")

    print(f"  {len(records)} documents chargés...")

    # ── 1. Transcription complète ──────────────────────────────────────────────
    lines_full = ["# Transcription complète — Écrits de prison de Joshua Ryne Goldberg",
                  f"_Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')} — {len(records)} documents_\n"]
    for r in records:
        fichier = r.get("_meta", {}).get("fichier", "?")
        doc_type = r.get("type_document", "?")
        date_doc = r.get("date_document") or "date inconnue"
        confidence = r.get("confidence_transcription", 0)
        lines_full += [
            f"---",
            f"## {fichier}",
            f"**Type** : {doc_type} | **Date** : {date_doc} | **Confiance** : {confidence:.0%}",
            "",
            r.get("transcription", "_Transcription manquante_"),
            "",
        ]
    (corpus_dir / "transcription_complete.md").write_text("\n".join(lines_full), encoding="utf-8")

    # ── 2. Catégorisation ──────────────────────────────────────────────────────
    from collections import Counter
    type_counts = Counter(r.get("type_document", "?") for r in records)
    medium_counts = Counter(r.get("medium", "?") for r in records)
    emotion_counts = Counter(r.get("etat_emotionnel", "?") for r in records)

    lines_cat = [
        "# Catégorisation — Écrits de prison Joshua Ryne Goldberg",
        f"_Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        "## Types de documents",
        *[f"- **{t}** : {c}" for t, c in type_counts.most_common()],
        "\n## Mediums d'écriture",
        *[f"- **{m}** : {c}" for m, c in medium_counts.most_common()],
        "\n## États émotionnels observés",
        *[f"- **{e}** : {c}" for e, c in emotion_counts.most_common()],
        "\n## Tableau détaillé",
        "| Fichier | Type | Date | État émotionnel | Confiance |",
        "|---------|------|------|-----------------|-----------|",
    ]
    for r in records:
        f = r.get("_meta", {}).get("fichier", "?")
        lines_cat.append(
            f"| {f} | {r.get('type_document','?')} | {r.get('date_document') or '—'} "
            f"| {r.get('etat_emotionnel','?')} | {r.get('confidence_transcription',0):.0%} |"
        )
    (corpus_dir / "categorisation.md").write_text("\n".join(lines_cat), encoding="utf-8")

    # ── 3. Analyse graphologique ───────────────────────────────────────────────
    manuscrits = [r for r in records if r.get("graphologie", {}).get("observations")]
    glines = [
        "# Analyse graphologique — Écriture manuscrite de Joshua Ryne Goldberg",
        f"_{len(manuscrits)} documents manuscrits analysés_\n",
        "## Observations par document",
    ]
    pression_counts = Counter()
    inclinaison_counts = Counter()
    lisibilite_counts = Counter()
    for r in manuscrits:
        g = r.get("graphologie", {})
        fichier = r.get("_meta", {}).get("fichier", "?")
        date_doc = r.get("date_document") or "date inconnue"
        glines += [
            f"### {fichier} — {date_doc}",
            f"**Pression** : {g.get('pression','?')} | "
            f"**Inclinaison** : {g.get('inclinaison','?')} | "
            f"**Taille** : {g.get('taille','?')} | "
            f"**Régularité** : {g.get('regularite','?')} | "
            f"**Lisibilité** : {g.get('lisibilite','?')}",
            "",
            g.get("observations") or "",
            "",
        ]
        if g.get("pression"): pression_counts[g["pression"]] += 1
        if g.get("inclinaison"): inclinaison_counts[g["inclinaison"]] += 1
        if g.get("lisibilite"): lisibilite_counts[g["lisibilite"]] += 1

    glines += [
        "## Synthèse graphologique",
        f"**Pressions** : {dict(pression_counts.most_common())}",
        f"**Inclinaisons** : {dict(inclinaison_counts.most_common())}",
        f"**Lisibilité** : {dict(lisibilite_counts.most_common())}",
    ]
    (corpus_dir / "graphologie.md").write_text("\n".join(glines), encoding="utf-8")

    # ── 4. Data mining ─────────────────────────────────────────────────────────
    all_persons = Counter()
    all_themes = Counter()
    all_lieux = Counter()
    timeline = []

    for r in records:
        for p in r.get("personnes_citees", []):
            if p: all_persons[p.strip()] += 1
        for t in r.get("themes", []):
            if t: all_themes[t.strip()] += 1
        for l in r.get("lieux_cites", []):
            if l: all_lieux[l.strip()] += 1
        if r.get("date_document") and r.get("contenu_notable"):
            timeline.append((
                r["date_document"],
                r.get("_meta", {}).get("fichier", "?"),
                r["contenu_notable"]
            ))

    timeline.sort(key=lambda x: x[0])

    mlines = [
        "# Data Mining — Écrits de prison Joshua Ryne Goldberg",
        f"_Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')} — {len(records)} documents_\n",
        "## Personnes citées (top 30)",
        *[f"- **{p}** : {c} occurrences" for p, c in all_persons.most_common(30)],
        "\n## Thèmes récurrents",
        *[f"- **{t}** : {c}" for t, c in all_themes.most_common(20)],
        "\n## Lieux mentionnés",
        *[f"- **{l}** : {c}" for l, c in all_lieux.most_common(15)],
        "\n## Timeline documentaire (documents datés)",
        *[f"- **{d}** [{f}] : {n}" for d, f, n in timeline],
        "\n## Documents sans date identifiée",
        *[
            f"- {r.get('_meta',{}).get('fichier','?')} : {r.get('contenu_notable','')}"
            for r in records if not r.get("date_document")
        ],
    ]
    (corpus_dir / "data_mining.md").write_text("\n".join(mlines), encoding="utf-8")

    print(f"\n  Corpus généré dans {corpus_dir}/")
    print(f"  - transcription_complete.md ({len(records)} docs)")
    print(f"  - categorisation.md")
    print(f"  - graphologie.md ({len(manuscrits)} manuscrits)")
    print(f"  - data_mining.md ({len(all_persons)} personnes, {len(all_themes)} thèmes)")


# ── Main ──────────────────────────────────────────────────────────────────────

def load_context(context_file: Path) -> dict:
    """Charge un fichier de contexte JSON pour personnaliser le prompt et les métadonnées."""
    if not context_file.exists():
        print(f"ERREUR : fichier de contexte introuvable : {context_file}")
        sys.exit(1)
    return json.loads(context_file.read_text())


def build_prompt(ctx: dict, recheck: bool = False) -> str:
    """Construit le prompt en injectant le contexte projet si fourni."""
    base = PROMPT_RECHECK if recheck else PROMPT_MAIN
    if not ctx:
        return base

    # Remplacer l'intro générique par une intro contextualisée
    subject_desc = ctx.get("subject_description", "")
    prompt_extra = ctx.get("prompt_context", "")
    extra_types = ctx.get("doc_types", [])

    preamble = f"Tu analyses un document du projet '{ctx.get('project', 'documentaire')}'. Sujet : {subject_desc}"
    if prompt_extra:
        preamble += f"\n\n{prompt_extra}"
    if extra_types:
        types_str = " | ".join(extra_types)
        # Injecter les types dans le prompt
        base = base.replace(
            "Types possibles : lettre_manuscrite | jpay_imprime | corrlinks_imprime |",
            f"Types possibles : {types_str}"
        ).replace(
            "   document_admin_prison | rapport_psychiatrique | document_judiciaire |\n   note_personnelle | dessin_croquis | enveloppe | article_presse | autre",
            ""
        )

    return preamble + "\n\n" + base


def main():
    parser = argparse.ArgumentParser(
        description="OCR + analyse graphologique de documents visuels — outil générique"
    )
    parser.add_argument("source", nargs="?", help="Dossier source contenant les images")
    parser.add_argument("--context-file", type=Path, help="Fichier JSON de contexte projet (voir contexts/)")
    parser.add_argument("--output-dir", type=Path, help="Dossier de sortie (défaut : heic-prison-docs/)")
    parser.add_argument("--resume", action="store_true", help="Reprendre depuis la dernière progression")
    parser.add_argument("--recheck-only", action="store_true", help="Recheck uniquement les fichiers à basse confiance")
    parser.add_argument("--consolidate", action="store_true", help="Générer corpus depuis JSON existants sans retraiter")
    parser.add_argument("--dry-run", action="store_true", help="Lister les fichiers sans appeler l'API")
    parser.add_argument("--sample", type=int, default=0, help="Traiter seulement N images (test)")
    args = parser.parse_args()

    # Contexte projet (optionnel)
    ctx = load_context(args.context_file) if args.context_file else {}

    # Output dynamique selon contexte ou --output-dir
    global JSON_DIR, CORPUS_DIR, TEMP_DIR, PROGRESS_FILE, OUTPUT_BASE
    if args.output_dir:
        OUTPUT_BASE = args.output_dir
        JSON_DIR = OUTPUT_BASE / "json"
        CORPUS_DIR = OUTPUT_BASE / "corpus"
        TEMP_DIR = OUTPUT_BASE / "_temp_jpeg"
        PROGRESS_FILE = OUTPUT_BASE / ".progress_writing.json"

    # Consolidation seule
    if args.consolidate:
        print("Consolidation corpus...")
        consolidate(JSON_DIR, CORPUS_DIR)
        return

    if not args.source:
        parser.print_help()
        sys.exit(1)

    source = Path(args.source)
    if not source.exists():
        print(f"ERREUR : dossier source introuvable : {source}")
        sys.exit(1)

    # Setup
    api_key = load_secrets()
    client = genai.Client(api_key=api_key)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    images = collect_images(source)
    print(f"\nSource : {source}")
    print(f"Images trouvées : {len(images)} ({sum(1 for i in images if i.suffix.lower()=='.dng')} DNG, "
          f"{sum(1 for i in images if i.suffix.lower()=='.heic')} HEIC, "
          f"{sum(1 for i in images if i.suffix.lower() in {'.jpg','.jpeg'})} JPEG)")

    if args.dry_run:
        for img in images[:20]:
            print(f"  {img.name}")
        print(f"  ... {len(images)} total")
        return

    if args.sample:
        images = images[:args.sample]
        print(f"Mode sample : {len(images)} images")

    progress = load_progress(PROGRESS_FILE)

    # Filtrer selon mode
    if args.recheck_only:
        to_process = [
            img for img in images
            if img.name in progress.get("recheck_pending", [])
        ]
        print(f"Recheck : {len(to_process)} images (confidence < {CONFIDENCE_THRESHOLD:.0%})")
    elif args.resume:
        done_set = set(progress.get("done", []))
        to_process = [img for img in images if img.name not in done_set]
        print(f"Reprise : {len(to_process)} restantes ({len(done_set)} déjà traitées)")
    else:
        # Exclure celles qui ont déjà un JSON valide
        done_set = {jf.stem for jf in JSON_DIR.glob("*.json")}
        to_process = [img for img in images if img.stem not in done_set]
        if len(to_process) < len(images):
            print(f"Skipping {len(images)-len(to_process)} déjà traités — utilise --resume pour forcer")

    total = len(to_process)
    if total == 0:
        print("Rien à traiter. Utilise --consolidate pour générer le corpus.")
        return

    print(f"\nDébut traitement : {total} images")
    print(f"Modèle principal : {MODEL_MAIN}")
    print(f"Modèle recheck   : {MODEL_RECHECK} (confidence < {CONFIDENCE_THRESHOLD:.0%})")
    print()

    success = 0
    errors = 0
    rechecked = 0

    for i, img in enumerate(to_process, 1):
        json_out = JSON_DIR / (img.stem + ".json")
        is_recheck = args.recheck_only

        model = MODEL_RECHECK if is_recheck else MODEL_MAIN
        prompt = build_prompt(ctx, recheck=is_recheck)

        print(f"[{i}/{total}] {img.name} ({img.suffix.upper()}) {'[RECHECK]' if is_recheck else ''}", end=" ", flush=True)

        try:
            result = analyze_image(client, img, model, prompt)
            confidence = result.get("confidence_transcription", 0)

            # Marquer pour recheck si confiance trop basse (et pas déjà en recheck)
            if confidence < CONFIDENCE_THRESHOLD and not is_recheck:
                result["_meta"]["needs_recheck"] = True
                if img.name not in progress["recheck_pending"]:
                    progress["recheck_pending"].append(img.name)

            json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            progress["done"].append(img.name)

            doc_type = result.get("type_document", "?")
            emotion = result.get("etat_emotionnel", "?")
            flag = "⚠ recheck" if result["_meta"]["needs_recheck"] else "✓"
            print(f"{flag} [{doc_type}] [{emotion}] conf={confidence:.0%}")

            success += 1
            if is_recheck:
                rechecked += 1

        except Exception as e:
            print(f"✗ ERREUR : {e}")
            progress["failed"].append(img.name)
            errors += 1

        # Sauvegarder la progression toutes les 10 images
        if i % 10 == 0:
            save_progress(PROGRESS_FILE, progress)

    save_progress(PROGRESS_FILE, progress)

    # Résumé
    print(f"\n{'='*60}")
    print(f"Traitement terminé")
    print(f"  Succès  : {success}")
    print(f"  Erreurs : {errors}")
    if rechecked:
        print(f"  Rechecks: {rechecked}")
    pending = len(progress.get("recheck_pending", []))
    if pending and not is_recheck:
        print(f"  Recheck en attente : {pending} images (confidence < {CONFIDENCE_THRESHOLD:.0%})")
        print(f"  → Lancer : python prison_writing_analyzer.py {source} --recheck-only")

    # Consolidation automatique si tout est terminé
    total_done = len(list(JSON_DIR.glob("*.json")))
    print(f"\n{total_done} JSON disponibles dans {JSON_DIR}")
    print("Génération du corpus...")
    consolidate(JSON_DIR, CORPUS_DIR)

    # Notification
    notify = Path.home() / ".claude/scripts/notify.sh"
    if notify.exists():
        subprocess.run([str(notify), f"Prison writing analyzer : {success} docs traités, corpus généré"])


if __name__ == "__main__":
    main()
