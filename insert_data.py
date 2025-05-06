import os
import sqlite3
import pandas as pd
import uuid

# Path to SQLite Database
db_path = os.getenv("DB_PATH", "/data/sales.db")
print("✅ DB path used:", db_path)
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
df_produits = df_produits[["ID Référence produit", "Nom", "Prix", "Stock"]]
df_produits.columns = ["produit_id", "nom", "prix", "stock"]

print("✅ Produits :")
print(df_produits.head())

for _, row in df_produits.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO produits (produit_id, nom, prix, stock, categorie)
        VALUES (?, ?, ?, ?, ?)
    """, (row["produit_id"], row["nom"], row["prix"], row["stock"], "Général"))

# 3. Import ventes.csv
df_ventes = pd.read_csv("ventes.csv")
df_ventes.columns = ["date", "produit_id", "quantité", "magasin_id"]

print("✅ Ventes :")
print(df_ventes.head())

for _, row in df_ventes.iterrows():
    vente_id = str(uuid.uuid4())  # Unique ID
    
    # Get product price
    cursor.execute("SELECT prix FROM produits WHERE produit_id = ?", (row["produit_id"],))
    result = cursor.fetchone()
    montant = row["quantité"] * result[0] if result else 0

    # Check if sale already exists
    cursor.execute("""
        SELECT 1 FROM ventes 
        WHERE produit_id=? AND date=? AND magasin_id=?
    """, (row["produit_id"], row["date"], row["magasin_id"]))
    
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO ventes (vente_id, date, produit_id, magasin_id, quantité, montant)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vente_id, row["date"], row["produit_id"], row["magasin_id"], row["quantité"], montant))

# Save and close
conn.commit()
conn.close()
print("✅ Data imported with success.")