import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Comparateur de prix", layout="wide")

st.title("Comparateur de prix — Decitre vs Eyrolles vs Mollat")

# Charger le tableau comparateur
with open("output/comparison_table.json", encoding="utf-8") as f:
    rows = json.load(f)

df = pd.DataFrame(rows)

# Colonnes à afficher (sans les urls)
cols = [
    "titre",
    "Decitre_prix", "Eyrolles_prix", "Mollat_prix",
    "meilleur_site", "meilleur_prix", "ecart"
]

# Tri + recherche
df = df.sort_values("meilleur_prix", ascending=True)

search = st.text_input("Rechercher un livre (mot-clé dans le titre) :")
if search:
    df_filtered = df[df["titre"].str.contains(search.lower(), na=False)]
else:
    df_filtered = df

st.dataframe(df_filtered[cols], use_container_width=True)

st.divider()
st.subheader("Choisir une offre")

# Choix produit
titre = st.selectbox("Livre", df_filtered["titre"].tolist() if len(df_filtered) else df["titre"].tolist())
row = df[df["titre"] == titre].iloc[0]

# Choix site
site = st.selectbox("Site", ["Decitre", "Eyrolles", "Mollat"])
prix = row.get(f"{site}_prix")
url = row.get(f"{site}_url")

if pd.isna(prix) or prix is None:
    st.warning(f"Pas d'offre sur {site} pour ce livre.")
else:
    st.success(f"{site} : {prix} €")
    if url:
        st.link_button("Ouvrir l'offre", url)
