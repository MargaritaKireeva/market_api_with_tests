class AuthService:

    def __init__(self, repo):
        self.repo = repo

    def register(self, email: str, password: str):
        existing = self.repo.get_by_email(email)

        if existing:
            return {"error": "User already exists"}

        return self.repo.create(email, password)

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user:
            return None

        if user[2] != password:
            return None

        return {"token": f"token-{user[0]}"}
