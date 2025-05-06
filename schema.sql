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
    prix REAL NOT NULL,
    stock INTEGER NOT NULL,
    categorie TEXT
);

-- ventes Table
CREATE TABLE IF NOT EXISTS ventes (
    vente_id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    produit_id TEXT NOT NULL,
    quantité INTEGER NOT NULL,
    magasin_id INTEGER NOT NULL,
    montant REAL,
    FOREIGN KEY (produit_id) REFERENCES produits (produit_id),
    FOREIGN KEY (magasin_id) REFERENCES magasins (magasin_id)
);