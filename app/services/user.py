from app.utils.security import hash_password
from app.repositories.abstract.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:

    def __init__(
        self,
        user_repo: UserRepository
    ):
        self.user_repo = user_repo


    def create_user(
        self,
        user_data: UserCreate
    ) -> User:

        if not user_data.email.endswith(
            "@inspheresolutions.com"
        ):
            raise ValueError(
                "Only inspheresolutions.com email addresses are allowed"
            )

        existing_email = self.user_repo.get_by_email(
            user_data.email
        )

        if existing_email:
            raise ValueError(
                "Email already exists"
            )

        existing_employee = (
            self.user_repo.get_by_employee_id(
                user_data.employee_id
            )
        )

        if existing_employee:
            raise ValueError(
                "Employee ID already exists"
            )
        hashed_password = hash_password(
        user_data.password
        )


        return self.user_repo.create_user(
            employee_id=user_data.employee_id,
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role,
            designation=user_data.designation
        )