CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_website INTEGER,
    sku TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    price INTEGER NOT NULL,
    available INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS electrokom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    price INTEGER NOT NULL,
    available TEXT NOT NULL,
    mnp TEXT NOT NULL,
    FOREIGN KEY (mnp)  REFERENCES suppliers (sku)
);
