import json
from collections import defaultdict

SITES = ["Decitre", "Eyrolles", "Mollat"]

# Lire le JSON Lines
products = []
with open("output/products.jl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            products.append(json.loads(line))

# grouped[titre][site] = offer
grouped = defaultdict(dict)

for p in products:
    titre = str(p.get("titre", "")).strip().lower()
    site = str(p.get("site", p.get("source", ""))).strip()

    # Normaliser le nom des sites (au cas où)
    mapping = {"eyrolles": "Eyrolles", "decitre": "Decitre", "mollat": "Mollat"}
    site_norm = mapping.get(site.lower(), site)

    grouped[titre][site_norm] = {
        "prix": p.get("prix"),
        "url": p.get("url")
    }

rows = []
for titre, offers in grouped.items():
    if not titre:
        continue

    available = [(s, offers[s]["prix"]) for s in offers if offers[s].get("prix") is not None]
    if not available:
        continue

    available_sorted = sorted(available, key=lambda x: x[1])
    best_site, best_price = available_sorted[0]
    worst_price = available_sorted[-1][1]

    row = {
        "titre": titre,
        "meilleur_site": best_site,
        "meilleur_prix": best_price,
        "ecart": round(worst_price - best_price, 2),
    }

    # Colonnes par site
    for s in SITES:
        row[f"{s}_prix"] = offers.get(s, {}).get("prix")
        row[f"{s}_url"] = offers.get(s, {}).get("url")

    rows.append(row)

# Trier par meilleur prix
rows.sort(key=lambda r: (r["meilleur_prix"] is None, r["meilleur_prix"]))

with open("output/comparison_table.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

print(" OK: output/comparison_table.json généré")
print(f"Produits comparés: {len(rows)}")
