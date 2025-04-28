import os
import sqlite3
import pandas as pd
import uuid

# Path to SQLite Database
db_path = os.getenv("DB_PATH", "sales.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Import magasins.csv
df_magasins = pd.read_csv("magasins.csv")
df_magasins = df_magasins[["ID Magasin", "Ville"]]
df_magasins.columns = ["magasin_id", "ville"]

for _, row in df_magasins.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO magasins (magasin_id, ville, région)
        VALUES (?, ?, ?)
    """, (row["magasin_id"], row["ville"], "Inconnue"))

# 2. Import produits.csv
df_produits = pd.read_csv("produits.csv")
df_produits = df_produits[["ID Référence produit", "Nom", "Prix"]]
df_produits.columns = ["produit_id", "nom", "prix"]

for _, row in df_produits.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO produits (produit_id, nom, catégorie, prix)
        VALUES (?, ?, ?, ?)
    """, (row["produit_id"], row["nom"], "Standard", row["prix"]))

# 3. Importer ventes.csv
df_ventes = pd.read_csv("ventes.csv")
df_ventes.columns = ["date_vente", "produit_id", "quantité", "magasin_id"]

# Add unique ID for each sale
for i, row in df_ventes.iterrows():
    vente_id = str(uuid.uuid4())  # Identifiant unique
    montant = None

    # Get product price
    cursor.execute("SELECT prix FROM produits WHERE produit_id = ?", (row["produit_id"],))
    result = cursor.fetchone()
    if result:
        montant = row["quantité"] * result[0]

        # Verify if the line exist (combination produit_id + date + magasin)
        cursor.execute("""
            SELECT 1 FROM ventes 
            WHERE produit_id=? AND date_vente=? AND magasin_id=?
        """, (row["produit_id"], row["date_vente"], row["magasin_id"]))
        if cursor.fetchone():
            continue  # skip, already added

        cursor.execute("""
            INSERT INTO ventes (vente_id, produit_id, magasin_id, date_vente, quantité, montant)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vente_id, row["produit_id"], row["magasin_id"], row["date_vente"], row["quantité"], montant))

# Save and close
conn.commit()
conn.close()
print("✅ Data imported with success.")
