from app.core.db_connection import get_connection


class CartRepo:

    def add(self, user_id, product_id, quantity):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s,%s,%s) "
            "ON CONFLICT (user_id, product_id) DO UPDATE SET quantity = cart.quantity + EXCLUDED.quantity",
            (user_id, product_id, quantity)
        )

        conn.commit()
        conn.close()

    def get(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT product_id, quantity FROM cart WHERE user_id=%s",
            (user_id,)
        )

        rows = cur.fetchall()
        conn.close()

        return rows

    def clear(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        conn.commit()
        conn.close()