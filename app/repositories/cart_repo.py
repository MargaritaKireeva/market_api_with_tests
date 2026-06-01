from app.core.db_connection import get_connection


class CartRepo:

    def add(self, user_id, product_id, quantity):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s,%s,%s) "
                "ON CONFLICT (user_id, product_id) DO UPDATE SET quantity = cart.quantity + EXCLUDED.quantity",
                (user_id, product_id, quantity)
            )
            conn.commit()
        finally:
            conn.close()

    def get(self, user_id, conn=None):
        close = False
        if conn is None:
            conn = get_connection()
            close = True
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT product_id, quantity FROM cart WHERE user_id=%s",
                (user_id,)
            )
            rows = cur.fetchall()
            return [{"product_id": r[0], "quantity": r[1]} for r in rows]
        finally:
            if close:
                conn.close()

    def clear(self, user_id, conn=None):
        close = False
        if conn is None:
            conn = get_connection()
            close = True
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
            if close:
                conn.commit()
        finally:
            if close:
                conn.close()
