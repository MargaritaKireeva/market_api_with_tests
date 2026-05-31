from app.core.db_connection import get_connection


class OrdersRepo:

    def create(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO orders (user_id,status) VALUES (%s,'created') RETURNING id,status",
            (user_id,)
        )

        o = cur.fetchone()
        conn.commit()
        conn.close()

        return {"id": o[0], "status": o[1]}

    def get(self, order_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id,user_id,status FROM orders WHERE id=%s", (order_id,))

        row = cur.fetchone()
        conn.close()

        return row

    def update_status(self, order_id, status):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE orders SET status=%s WHERE id=%s RETURNING id, user_id, status",
            (status, order_id)
        )

        row = cur.fetchone()
        conn.commit()
        conn.close()

        return {"id": row[0], "status": row[2]}