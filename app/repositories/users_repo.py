from app.core.db_connection import get_connection


class UsersRepo:

    def create(self, email, password):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            RETURNING id, email
            """,
            (email, password)
        )

        user = cur.fetchone()
        conn.commit()
        conn.close()

        return {"id": user[0], "email": user[1]}

    def get_by_email(self, email):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, email, password FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()
        conn.close()

        return user