CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price FLOAT NOT NULL
);

CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    UNIQUE (user_id, product_id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('created', 'confirmed', 'shipped', 'delivered', 'cancelled'))
);