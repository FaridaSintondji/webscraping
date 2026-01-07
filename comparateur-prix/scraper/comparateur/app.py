import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Comparateur de prix", layout="wide")
st.title("📚 Comparateur de prix — Decitre vs Eyrolles vs Mollat")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "output" / "comparison_table.json"

if not DATA_PATH.exists():
    st.error("Fichier output/comparison_table.json introuvable. Lance d'abord : python compare.py")
    st.stop()

with open(DATA_PATH, encoding="utf-8") as f:
    rows = json.load(f)

df = pd.DataFrame(rows)

if df.empty:
    st.warning("Aucune donnée à afficher. Vérifie output/products.jl puis relance compare.py.")
    st.stop()

# ---- Sidebar filtres
st.sidebar.header("Filtres")

mode = st.sidebar.radio(
    "Afficher",
    ["Tous les livres", "Livres comparables (≥ 2 sites)", "Uniquement présents sur 3 sites"],
    index=1,
)

search = st.sidebar.text_input("Rechercher (dans le titre)")

df_view = df.copy()

if mode == "Livres comparables (≥ 2 sites)":
    df_view = df_view[df_view["nb_sites"] >= 2]
elif mode == "Uniquement présents sur 3 sites":
    df_view = df_view[df_view["nb_sites"] == 3]

if search:
    df_view = df_view[df_view["titre"].fillna("").str.contains(search, case=False, na=False)]

# ✅ IMPORTANT : stop si aucun résultat
if df_view.empty:
    st.warning("Aucun livre ne correspond à ces filtres (ex: aucun livre présent sur 3 sites).")
    st.stop()

# Tri
df_view = df_view.sort_values(["meilleur_prix", "nb_sites", "titre"], ascending=[True, False, True])

# ---- Affichage tableau
cols = [
    "ean", "titre",
    "Decitre_prix", "Eyrolles_prix", "Mollat_prix",
    "meilleur_prix", "meilleurs_sites", "nb_sites",
]
st.dataframe(df_view[cols], use_container_width=True)

st.divider()
st.subheader("🧾 Détails & liens cliquables")

# Choix produit
titres = df_view["titre"].fillna("(sans titre)").tolist()
titre_choisi = st.selectbox("Livre", titres)

row = df_view[df_view["titre"] == titre_choisi].iloc[0]

best_price = row.get("meilleur_prix")
best_sites = row.get("meilleurs_sites") or []

st.markdown(f"**EAN :** `{row.get('ean')}`")
st.markdown(f"**Prix le moins cher :** **{best_price:.2f} €**")

if isinstance(best_sites, list) and len(best_sites) > 1:
    st.info("Égalité : plusieurs sites proposent le même prix minimal.")
st.markdown(f"**Site(s) au prix minimal :** {', '.join(best_sites) if best_sites else '—'}")

st.write("### Offres")
sites = ["Decitre", "Eyrolles", "Mollat"]

for site in sites:
    prix = row.get(f"{site}_prix")
    url = row.get(f"{site}_url")

    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        st.write(f"**{site}**")

    with col2:
        if pd.isna(prix) or prix is None:
            st.write("—")
        else:
            tag = " ✅" if site in best_sites else ""
            st.write(f"{float(prix):.2f} €{tag}")

    with col3:
        if url and not (pd.isna(prix) or prix is None):
            st.link_button("Ouvrir la page", url)
        else:
            st.write("")
