from app.core.db_connection import get_connection


class UsersRepo:

    def create(self, email, password):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id, email",
                (email, password)
            )
            user = cur.fetchone()
            conn.commit()
            return {"id": user[0], "email": user[1]}
        finally:
            conn.close()

    def get_by_email(self, email):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, email, password FROM users WHERE email=%s",
                (email,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "email": row[1], "password": row[2]}
        finally:
            conn.close()

    def get_by_id(self, user_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, email, password FROM users WHERE id=%s",
                (user_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "email": row[1], "password": row[2]}
        finally:
            conn.close()

    def delete_by_id(self, user_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
        finally:
            conn.close()

    def delete_all(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("TRUNCATE orders, cart, users RESTART IDENTITY CASCADE")
            conn.commit()
        finally:
            conn.close()
