import json
import re
from collections import defaultdict
from pathlib import Path
from difflib import SequenceMatcher

SITES = ["Decitre", "Eyrolles", "Momox"]

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_PATH = BASE_DIR / "output" / "products.jl"
OUT_PATH = BASE_DIR / "output" / "comparison_table.json"


def safe_float(x):
    """Convertit différents formats en float (ou None)."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.replace("€", "").replace("\xa0", " ").strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None


def clean_ean(ean):
    """Garde uniquement 13 chiffres, sinon None."""
    if not ean:
        return None
    s = re.sub(r"\D", "", str(ean))
    return s if len(s) == 13 else None


def norm_title(t):
    """Normalisation simple pour regrouper les titres quand EAN absent."""
    if not t:
        return None
    s = t.lower().strip()

    # enlève ponctuation / symboles
    s = re.sub(r"[\[\]\(\)\{\}\.,;:!\?\"'’`~\-_/\\|]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    # enlève quelques mots fréquents qui perturbent (optionnel)
    stop = {"tome", "vol", "volume", "édition", "ed", "broché", "poche"}
    tokens = [w for w in s.split() if w not in stop]

    return " ".join(tokens) if tokens else s


def title_similarity(a, b):
    """Score 0..1 avec difflib (stdlib)."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def main():
    if not PRODUCTS_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable: {PRODUCTS_PATH}")

    # Lire products.jl (JSON lines)
    products = []
    with open(PRODUCTS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                products.append(json.loads(line))

    # grouped[key][site] = offer
    # key = "EAN:<ean13>" sinon "TIT:<titre_normalise>"
    grouped = defaultdict(dict)

    # stats utiles pour debug
    stats = {s: {"total": 0, "with_ean": 0} for s in SITES}

    # 1) premier passage: groupby EAN si présent sinon par titre normalisé
    for p in products:
        site = (p.get("site") or "").strip().capitalize()
        if site not in SITES:
            continue

        stats[site]["total"] += 1

        ean = clean_ean(p.get("ean"))
        if ean:
            stats[site]["with_ean"] += 1
            key = f"EAN:{ean}"
        else:
            tnorm = norm_title(p.get("titre"))
            if not tnorm:
                continue
            key = f"TIT:{tnorm}"

        grouped[key][site] = {
            "titre": (p.get("titre") or "").strip() if p.get("titre") else None,
            "prix": safe_float(p.get("prix")),
            "url": p.get("url"),
            "ean": ean,
        }

    # 2) rattrapage: rattacher les groupes TIT:* aux groupes EAN:* si titres très proches
    # (utile quand 1 site a EAN et l'autre non)
    ean_groups = [(k, v) for k, v in grouped.items() if k.startswith("EAN:")]
    tit_groups = [k for k in list(grouped.keys()) if k.startswith("TIT:")]

    SIM_THRESHOLD = 0.92  # ajuste si besoin (0.90-0.95)

    for tk in tit_groups:
        offers = grouped.get(tk, {})
        # titre de référence = premier titre non vide
        ref_title = None
        for s in SITES:
            t = offers.get(s, {}).get("titre")
            if t:
                ref_title = norm_title(t)
                break
        if not ref_title:
            continue

        best_match = None
        best_score = 0.0

        for ek, eoffers in ean_groups:
            # titre de référence côté EAN group
            et = None
            for s in SITES:
                t = eoffers.get(s, {}).get("titre")
                if t:
                    et = norm_title(t)
                    break
            if not et:
                continue

            score = title_similarity(ref_title, et)
            if score > best_score:
                best_score = score
                best_match = ek

        if best_match and best_score >= SIM_THRESHOLD:
            # fusion: on copie les sites manquants dans le groupe EAN
            for s, off in offers.items():
                if s not in grouped[best_match]:
                    grouped[best_match][s] = off
            # on supprime l'ancien groupe TIT
            grouped.pop(tk, None)

    # Construire les lignes
    rows = []
    for key, offers in grouped.items():
        # clé ean si groupe EAN:
        ean = key[4:] if key.startswith("EAN:") else None

        # Titre : prendre le premier non vide selon l'ordre SITES
        titre = None
        for s in SITES:
            t = offers.get(s, {}).get("titre")
            if t:
                titre = t
                break

        # Récupérer les prix disponibles
        prices = {}
        for s in SITES:
            pr = offers.get(s, {}).get("prix")
            if pr is not None:
                prices[s] = pr
        if not prices:
            continue

        best_price = min(prices.values())
        best_sites = [s for s, p in prices.items() if p == best_price]

        row = {
            "ean": ean,
            "titre": titre,
            "nb_sites": len(prices),
            "meilleur_prix": round(best_price, 2),
            "meilleurs_sites": best_sites,
        }

        for s in SITES:
            row[f"{s}_prix"] = offers.get(s, {}).get("prix")
            row[f"{s}_url"] = offers.get(s, {}).get("url")

        rows.append(row)

    # Tri : meilleur prix, puis nb_sites desc, puis titre
    rows.sort(key=lambda r: (r["meilleur_prix"], -r["nb_sites"], r.get("titre") or ""))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print("comparison_table.json généré")
    print(f"Total lignes: {len(rows)}")
    print(f"Comparables (>=2 sites): {sum(1 for r in rows if r['nb_sites'] >= 2)}")
    print(f"Présents sur 3 sites: {sum(1 for r in rows if r['nb_sites'] == 3)}")
    print("Stats EAN par site:")
    for s in SITES:
        print(f"  - {s}: {stats[s]['with_ean']}/{stats[s]['total']} items avec EAN")


if __name__ == "__main__":
    main()
