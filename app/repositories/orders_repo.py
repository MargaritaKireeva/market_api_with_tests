from app.core.db_connection import get_connection


class OrdersRepo:

    def create(self, user_id, conn=None):
        close = False
        if conn is None:
            conn = get_connection()
            close = True
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO orders (user_id,status) VALUES (%s,'created') RETURNING id,status",
                (user_id,)
            )
            o = cur.fetchone()
            if close:
                conn.commit()
            return {"id": o[0], "status": o[1]}
        finally:
            if close:
                conn.close()

    def get(self, order_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id,user_id,status FROM orders WHERE id=%s", (order_id,))
            row = cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "user_id": row[1], "status": row[2]}
        finally:
            conn.close()

    def update_status(self, order_id, status):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE orders SET status=%s WHERE id=%s RETURNING id, user_id, status",
                (status, order_id)
            )
            row = cur.fetchone()
            conn.commit()
            return {"id": row[0], "status": row[2]}
        finally:
            conn.close()
