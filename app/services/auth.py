from app.repositories.abstract.user import UserRepository


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository
    ):
        self.user_repo = user_repo

    def login(
        self,
        email: str,
        password: str
    ):
        from app.utils.security import (
            verify_password,
            create_access_token,
            create_refresh_token
        )

        from app.schemas.auth import TokenResponse

        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        if not user.password_hash:
            raise ValueError(
                "Password not set"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        refresh_token = create_refresh_token(
            {"sub": str(user.id)}
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        