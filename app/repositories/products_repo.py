from app.core.db_connection import get_connection


class ProductsRepo:

    def create(self, name, price):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO products (name, price)
            VALUES (%s, %s)
            RETURNING id, name, price
            """,
            (name, price)
        )

        p = cur.fetchone()
        conn.commit()
        conn.close()

        return {"id": p[0], "name": p[1], "price": p[2]}

    def get(self, product_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, price FROM products WHERE id=%s",
            (product_id,)
        )

        p = cur.fetchone()
        conn.close()

        return {"id": p[0], "name": p[1], "price": p[2]} if p else None

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, price FROM products")
        rows = cur.fetchall()

        conn.close()

        return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]

    def update(self, product_id, name, price):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE products
            SET name = %s,
                price = %s
            WHERE id = %s
            RETURNING id, name, price
            """,
            (name, price, product_id)
        )

        row = cur.fetchone()
        conn.commit()
        conn.close()

        if not row:
            return None

        return {"id": row[0], "name": row[1], "price": row[2]}

    def delete(self, product_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        conn.close()