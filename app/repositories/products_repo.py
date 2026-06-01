from app.core.db_connection import get_connection


class ProductsRepo:

    def create(self, name, price):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id, name, price",
                (name, price)
            )
            p = cur.fetchone()
            conn.commit()
            return {"id": p[0], "name": p[1], "price": p[2]}
        finally:
            conn.close()

    def get(self, product_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, price FROM products WHERE id=%s",
                (product_id,)
            )
            p = cur.fetchone()
            return {"id": p[0], "name": p[1], "price": p[2]} if p else None
        finally:
            conn.close()

    def get_all(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, price FROM products")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]
        finally:
            conn.close()

    def update(self, product_id, name, price):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING id, name, price",
                (name, price, product_id)
            )
            row = cur.fetchone()
            conn.commit()
            if not row:
                return None
            return {"id": row[0], "name": row[1], "price": row[2]}
        finally:
            conn.close()

    def delete(self, product_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
            conn.commit()
        finally:
            conn.close()
