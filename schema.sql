-- magasins Table
CREATE TABLE IF NOT EXISTS magasins (
    magasin_id INTEGER PRIMARY KEY,
    ville TEXT NOT NULL,
    région TEXT
);

-- produits Table
CREATE TABLE IF NOT EXISTS produits (
    produit_id TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    catégorie TEXT,
    prix REAL NOT NULL
);

-- ventes Table
CREATE TABLE IF NOT EXISTS ventes (
    vente_id TEXT PRIMARY KEY,
    produit_id TEXT NOT NULL,
    magasin_id INTEGER NOT NULL,
    date_vente TEXT NOT NULL,
    quantité INTEGER NOT NULL,
    montant REAL,
    FOREIGN KEY (produit_id) REFERENCES produits(produit_id),
    FOREIGN KEY (magasin_id) REFERENCES magasins(magasin_id)
);